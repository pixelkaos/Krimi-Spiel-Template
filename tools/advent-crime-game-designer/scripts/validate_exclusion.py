#!/usr/bin/env python3
"""Validate single-culprit exclusion logic.

For an "exclude everyone but one" deduction (the typical Advent-calendar case),
this checks that exactly one suspect — the culprit — remains un-excluded, that every
other suspect is ruled out by a clue, and (optionally) that every exclusion clue is
reachable. Input is JSON (e.g. produced by /deduction-consistency-auditor); see
assets/templates/exclusion.example.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a single-culprit exclusion map JSON file.")
    parser.add_argument("path", help="Path to exclusion JSON")
    args = parser.parse_args()

    payload = load_json(Path(args.path))
    errors = validate(payload)
    if errors:
        print("Exclusion validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Exclusion validation passed.")
    return 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit("Exclusion map root must be a JSON object.")
    return data


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    suspects = payload.get("suspects")
    if (not isinstance(suspects, list) or not suspects
            or not all(isinstance(s, str) and s.strip() for s in suspects)):
        return ["`suspects` must be a non-empty array of strings."]
    if len(set(suspects)) != len(suspects):
        errors.append("`suspects` contains duplicate names.")

    culprit = payload.get("culprit")
    if not isinstance(culprit, str) or culprit not in suspects:
        errors.append("`culprit` must name one of `suspects`.")

    exclusions = payload.get("exclusions")
    if not isinstance(exclusions, list):
        errors.append("`exclusions` must be an array.")
    if errors:
        return errors

    excluded: set[str] = set()
    clues_used: list[tuple[str, str]] = []
    for index, exclusion in enumerate(exclusions):
        if not isinstance(exclusion, dict):
            errors.append(f"Exclusion at index {index} must be an object.")
            continue
        suspect = exclusion.get("suspect")
        clue = exclusion.get("clue")
        if not isinstance(suspect, str) or suspect not in suspects:
            errors.append(f"Exclusion at index {index}: `suspect` must name one of `suspects`.")
            continue
        if not isinstance(clue, str) or not clue.strip():
            errors.append(f"Exclusion for `{suspect}` needs a non-empty `clue`.")
            continue
        excluded.add(suspect)
        clues_used.append((suspect, clue))

    if errors:
        return errors

    if culprit in excluded:
        errors.append(f"Culprit `{culprit}` must not be excluded — that leaves no solution.")

    remaining = [s for s in suspects if s not in excluded]
    if remaining != [culprit]:
        if len(remaining) > 1:
            errors.append(f"Underdetermined: still in play: {remaining}; expected only `{culprit}`.")
        elif not remaining:
            errors.append("Over-excluded: no suspect remains; expected exactly the culprit.")
        else:
            errors.append(f"Wrong suspect remains: {remaining}; expected `{culprit}`.")

    reachable = payload.get("reachable_clues")
    if reachable is not None:
        if not isinstance(reachable, list) or not all(isinstance(c, str) for c in reachable):
            errors.append("`reachable_clues` must be an array of strings when present.")
        else:
            reachable_set = set(reachable)
            for suspect, clue in clues_used:
                if clue not in reachable_set:
                    errors.append(f"Exclusion clue `{clue}` for `{suspect}` is not reachable (unfair).")

    return errors


if __name__ == "__main__":
    sys.exit(main())
