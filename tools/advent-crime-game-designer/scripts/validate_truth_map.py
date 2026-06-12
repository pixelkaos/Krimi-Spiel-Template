#!/usr/bin/env python3
"""Validate a deduction truth map for uniqueness and clue consistency."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any


MAX_ASSIGNMENTS = 200_000


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Advent crime truth map JSON file.")
    parser.add_argument("path", help="Path to truth-map JSON")
    args = parser.parse_args()

    payload = load_json(Path(args.path))
    errors = validate(payload)
    if errors:
        print("Truth map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Truth map validation passed.")
    return 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit("Truth map root must be a JSON object.")
    return data


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    categories = payload.get("categories")
    if not isinstance(categories, dict) or not categories:
        return ["`categories` must be a non-empty object."]

    normalized_categories: dict[str, list[str]] = {}
    for name, values in categories.items():
        if not isinstance(name, str) or not name.strip():
            errors.append("Category names must be non-empty strings.")
            continue
        if not isinstance(values, list) or not values:
            errors.append(f"Category `{name}` must be a non-empty array.")
            continue
        if not all(isinstance(value, str) and value.strip() for value in values):
            errors.append(f"Category `{name}` values must be non-empty strings.")
            continue
        if len(set(values)) != len(values):
            errors.append(f"Category `{name}` contains duplicate values.")
            continue
        normalized_categories[name] = values

    if errors:
        return errors

    primary = payload.get("primary_category", "suspect")
    if primary not in normalized_categories:
        errors.append(f"`primary_category` `{primary}` is not present in categories.")
        return errors

    primary_values = normalized_categories[primary]
    target_categories = [name for name in normalized_categories if name != primary]
    for category in target_categories:
        if len(normalized_categories[category]) != len(primary_values):
            errors.append(
                f"Category `{category}` must have {len(primary_values)} values for exclusive solving."
            )

    solutions = payload.get("solutions")
    if not isinstance(solutions, dict):
        errors.append("`solutions` must be an object keyed by primary values.")
        return errors

    for primary_value in primary_values:
        row = solutions.get(primary_value)
        if not isinstance(row, dict):
            errors.append(f"Missing solution row for `{primary_value}`.")
            continue
        for category in target_categories:
            value = row.get(category)
            if value not in normalized_categories[category]:
                errors.append(
                    f"Solution `{primary_value}.{category}` must be one of {normalized_categories[category]}."
                )

    for category in target_categories:
        used = [solutions.get(primary_value, {}).get(category) for primary_value in primary_values]
        if len(set(used)) != len(primary_values):
            errors.append(f"Solution category `{category}` is not one-to-one.")

    clue_errors, constraints, clue_ids = parse_clues(payload.get("clues"), normalized_categories, primary)
    errors.extend(clue_errors)
    errors.extend(validate_decisive_clues(payload, clue_ids))
    if errors:
        return errors

    estimated = math.prod(math.factorial(len(primary_values)) for _ in target_categories)
    if estimated > MAX_ASSIGNMENTS:
        errors.append(
            f"Search space has {estimated} assignments; limit is {MAX_ASSIGNMENTS}. Add more fixed clues or test a smaller grid."
        )
        return errors

    matching = find_matching_assignments(primary_values, target_categories, normalized_categories, constraints)
    if len(matching) != 1:
        errors.append(f"Clues determine {len(matching)} possible solutions; expected exactly 1.")
        return errors

    expected = {
        primary_value: {category: solutions[primary_value][category] for category in target_categories}
        for primary_value in primary_values
    }
    if matching[0] != expected:
        errors.append("Unique clue-derived solution does not match `solutions`.")

    return errors


def parse_clues(
    clues: Any,
    categories: dict[str, list[str]],
    primary: str,
) -> tuple[list[str], list[dict[str, str]], set[str]]:
    errors: list[str] = []
    constraints: list[dict[str, str]] = []
    clue_ids: set[str] = set()

    if not isinstance(clues, list) or not clues:
        return ["`clues` must be a non-empty array."], constraints, clue_ids

    for index, clue in enumerate(clues):
        if not isinstance(clue, dict):
            errors.append(f"Clue at index {index} must be an object.")
            continue
        clue_id = clue.get("id")
        if not isinstance(clue_id, str) or not clue_id.strip():
            errors.append(f"Clue at index {index} needs a non-empty `id`.")
            continue
        if clue_id in clue_ids:
            errors.append(f"Duplicate clue id `{clue_id}`.")
        clue_ids.add(clue_id)

        clue_type = clue.get("type")
        if clue_type not in {"positive", "negative"}:
            errors.append(f"Clue `{clue_id}` type must be `positive` or `negative`.")
            continue

        subject_category = clue.get("subject_category")
        target_category = clue.get("target_category")
        subject = clue.get("subject")
        target = clue.get("target")
        for field, value in (
            ("subject_category", subject_category),
            ("target_category", target_category),
            ("subject", subject),
            ("target", target),
        ):
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Clue `{clue_id}` needs non-empty `{field}`.")
                continue

        if subject_category not in categories:
            errors.append(f"Clue `{clue_id}` unknown subject category `{subject_category}`.")
            continue
        if target_category not in categories:
            errors.append(f"Clue `{clue_id}` unknown target category `{target_category}`.")
            continue
        if subject not in categories[subject_category]:
            errors.append(f"Clue `{clue_id}` subject `{subject}` not in `{subject_category}`.")
            continue
        if target not in categories[target_category]:
            errors.append(f"Clue `{clue_id}` target `{target}` not in `{target_category}`.")
            continue

        normalized = normalize_constraint(
            clue_id,
            clue_type,
            subject_category,
            subject,
            target_category,
            target,
            primary,
        )
        if normalized is None:
            errors.append(
                f"Clue `{clue_id}` must connect the primary category `{primary}` to one other category."
            )
            continue
        constraints.append(normalized)

    return errors, constraints, clue_ids


def normalize_constraint(
    clue_id: str,
    clue_type: str,
    subject_category: str,
    subject: str,
    target_category: str,
    target: str,
    primary: str,
) -> dict[str, str] | None:
    if subject_category == primary and target_category != primary:
        return {
            "id": clue_id,
            "type": clue_type,
            "primary_value": subject,
            "category": target_category,
            "value": target,
        }
    if target_category == primary and subject_category != primary:
        return {
            "id": clue_id,
            "type": clue_type,
            "primary_value": target,
            "category": subject_category,
            "value": subject,
        }
    return None


def validate_decisive_clues(payload: dict[str, Any], clue_ids: set[str]) -> list[str]:
    errors: list[str] = []
    critical = payload.get("critical_solution", {})
    if not isinstance(critical, dict):
        errors.append("`critical_solution` must be an object when present.")
        return errors
    decisive = critical.get("decisive_clues", [])
    if decisive and not isinstance(decisive, list):
        errors.append("`critical_solution.decisive_clues` must be an array.")
        return errors
    for clue_id in decisive:
        if clue_id not in clue_ids:
            errors.append(f"Decisive clue `{clue_id}` is not present in `clues`.")
    return errors


def find_matching_assignments(
    primary_values: list[str],
    target_categories: list[str],
    categories: dict[str, list[str]],
    constraints: list[dict[str, str]],
) -> list[dict[str, dict[str, str]]]:
    matches: list[dict[str, dict[str, str]]] = []
    category_permutations = [
        list(itertools.permutations(categories[category])) for category in target_categories
    ]

    for combined in itertools.product(*category_permutations):
        assignment: dict[str, dict[str, str]] = {primary_value: {} for primary_value in primary_values}
        for category, values in zip(target_categories, combined):
            for primary_value, value in zip(primary_values, values):
                assignment[primary_value][category] = value
        if satisfies_constraints(assignment, constraints):
            matches.append(assignment)
            if len(matches) > 1:
                break
    return matches


def satisfies_constraints(
    assignment: dict[str, dict[str, str]],
    constraints: list[dict[str, str]],
) -> bool:
    for constraint in constraints:
        actual = assignment[constraint["primary_value"]][constraint["category"]]
        expected = constraint["value"]
        if constraint["type"] == "positive" and actual != expected:
            return False
        if constraint["type"] == "negative" and actual == expected:
            return False
    return True


if __name__ == "__main__":
    sys.exit(main())
