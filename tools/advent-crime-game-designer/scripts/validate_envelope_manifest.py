#!/usr/bin/env python3
"""Validate envelope reachability, clue placement, and pacing metadata."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Advent envelope manifest JSON file.")
    parser.add_argument("path", help="Path to envelope manifest JSON")
    args = parser.parse_args()

    payload = load_json(Path(args.path))
    errors = validate(payload)
    if errors:
        print("Envelope manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Envelope manifest validation passed.")
    return 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit("Envelope manifest root must be a JSON object.")
    return data


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    budget = payload.get("daily_time_budget")
    if not isinstance(budget, int) or budget <= 0:
        errors.append("`daily_time_budget` must be a positive integer.")

    envelopes = payload.get("envelopes")
    if not isinstance(envelopes, list) or not envelopes:
        return errors + ["`envelopes` must be a non-empty array."]

    by_id: dict[str, dict[str, Any]] = {}
    clue_locations: dict[str, list[str]] = {}
    entry_points: list[str] = []

    for index, envelope in enumerate(envelopes):
        if not isinstance(envelope, dict):
            errors.append(f"Envelope at index {index} must be an object.")
            continue

        envelope_id = envelope.get("id")
        if not isinstance(envelope_id, str) or not envelope_id.strip():
            errors.append(f"Envelope at index {index} needs a non-empty `id`.")
            continue
        if envelope_id in by_id:
            errors.append(f"Duplicate envelope id `{envelope_id}`.")
        by_id[envelope_id] = envelope

        label = envelope.get("label")
        if not isinstance(label, str) or not label.strip():
            errors.append(f"Envelope `{envelope_id}` needs a non-empty `label`.")

        unlock_day = envelope.get("unlock_day")
        if not isinstance(unlock_day, int) or not 1 <= unlock_day <= 24:
            errors.append(f"Envelope `{envelope_id}` unlock_day must be an integer from 1 to 24.")

        time_cost = envelope.get("time_cost")
        if not isinstance(time_cost, int) or time_cost < 0:
            errors.append(f"Envelope `{envelope_id}` time_cost must be a non-negative integer.")

        clues = envelope.get("clues", [])
        if not isinstance(clues, list) or not all(isinstance(clue, str) and clue.strip() for clue in clues):
            errors.append(f"Envelope `{envelope_id}` clues must be an array of strings.")
        else:
            for clue in clues:
                clue_locations.setdefault(clue, []).append(envelope_id)

        leads_to = envelope.get("leads_to", [])
        if not isinstance(leads_to, list) or not all(
            isinstance(target, str) and target.strip() for target in leads_to
        ):
            errors.append(f"Envelope `{envelope_id}` leads_to must be an array of strings.")

        if envelope.get("entry_point") is True:
            entry_points.append(envelope_id)

    if errors:
        return errors

    final_envelope = payload.get("final_envelope")
    if not isinstance(final_envelope, str) or final_envelope not in by_id:
        errors.append("`final_envelope` must name an existing envelope.")

    if not entry_points:
        errors.append("At least one envelope must have `entry_point: true`.")
    elif not any(by_id[entry]["unlock_day"] == 1 for entry in entry_points):
        errors.append("At least one entry point must unlock on day 1.")

    for envelope_id, envelope in by_id.items():
        for target in envelope.get("leads_to", []):
            if target not in by_id:
                errors.append(f"Envelope `{envelope_id}` leads to unknown envelope `{target}`.")

    critical_clues = payload.get("critical_clues", [])
    if not isinstance(critical_clues, list) or not all(
        isinstance(clue, str) and clue.strip() for clue in critical_clues
    ):
        errors.append("`critical_clues` must be an array of strings.")
    else:
        for clue in critical_clues:
            if clue not in clue_locations:
                errors.append(f"Critical clue `{clue}` is not placed in any envelope.")

    if errors:
        return errors

    reachable = reachable_envelopes(by_id, entry_points)
    for envelope_id, envelope in by_id.items():
        if envelope.get("critical") is True and envelope_id not in reachable:
            errors.append(f"Critical envelope `{envelope_id}` is not reachable from an entry point.")
    for clue in critical_clues:
        if not any(location in reachable for location in clue_locations[clue]):
            errors.append(f"Critical clue `{clue}` is only placed in unreachable envelopes.")

    return errors


def reachable_envelopes(by_id: dict[str, dict[str, Any]], entry_points: list[str]) -> set[str]:
    seen: set[str] = set(entry_points)
    queue: deque[str] = deque(entry_points)
    while queue:
        current = queue.popleft()
        for target in by_id[current].get("leads_to", []):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


if __name__ == "__main__":
    sys.exit(main())
