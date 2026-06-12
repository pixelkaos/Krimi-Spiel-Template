#!/usr/bin/env python3
"""Validate event ordering and actor-location overlap in a case timeline."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Advent crime timeline JSON file.")
    parser.add_argument("path", help="Path to timeline JSON")
    args = parser.parse_args()

    payload = load_json(Path(args.path))
    errors = validate(payload)
    if errors:
        print("Timeline validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Timeline validation passed.")
    return 0


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None
    if not isinstance(data, dict):
        raise SystemExit("Timeline root must be a JSON object.")
    return data


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    raw_events = payload.get("events")
    if not isinstance(raw_events, list) or not raw_events:
        return ["`events` must be a non-empty array."]

    ids: set[str] = set()
    events: list[dict[str, Any]] = []
    for index, event in enumerate(raw_events):
        if not isinstance(event, dict):
            errors.append(f"Event at index {index} must be an object.")
            continue

        event_id = event.get("id")
        if not isinstance(event_id, str) or not event_id.strip():
            errors.append(f"Event at index {index} needs a non-empty `id`.")
            continue
        if event_id in ids:
            errors.append(f"Duplicate event id `{event_id}`.")
        ids.add(event_id)

        location = event.get("location")
        if not isinstance(location, str) or not location.strip():
            errors.append(f"Event `{event_id}` needs a non-empty `location`.")

        actors = event.get("actors")
        if not isinstance(actors, list) or not actors:
            errors.append(f"Event `{event_id}` needs a non-empty `actors` array.")
        elif not all(isinstance(actor, str) and actor.strip() for actor in actors):
            errors.append(f"Event `{event_id}` actors must be non-empty strings.")

        start = parse_time(event.get("time"), event_id, "time", errors)
        end = parse_time(event.get("end_time", event.get("time")), event_id, "end_time", errors)
        if start and end and end < start:
            errors.append(f"Event `{event_id}` ends before it starts.")

        truth_status = event.get("truth_status", "objective")
        if truth_status not in {"objective", "claim", "witnessed", "rumor", "lie"}:
            errors.append(
                f"Event `{event_id}` truth_status must be objective, claim, witnessed, rumor, or lie."
            )

        revealed_in = event.get("revealed_in", [])
        if revealed_in and (
            not isinstance(revealed_in, list)
            or not all(isinstance(item, str) and item.strip() for item in revealed_in)
        ):
            errors.append(f"Event `{event_id}` revealed_in must be an array of strings.")

        if start and end and isinstance(actors, list) and isinstance(location, str):
            events.append(
                {
                    "id": event_id,
                    "start": start,
                    "end": end,
                    "actors": actors,
                    "location": location,
                    "allows_overlap": bool(event.get("allows_overlap", False)),
                }
            )

    errors.extend(find_actor_overlaps(events))
    return errors


def parse_time(value: Any, event_id: str, field: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"Event `{event_id}` needs a non-empty `{field}`.")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"Event `{event_id}` has invalid ISO timestamp in `{field}`: {value}")
        return None


def find_actor_overlaps(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    by_actor: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        for actor in event["actors"]:
            by_actor.setdefault(actor, []).append(event)

    for actor, actor_events in by_actor.items():
        actor_events.sort(key=lambda item: item["start"])
        for left, right in zip(actor_events, actor_events[1:]):
            if left["allows_overlap"] or right["allows_overlap"]:
                continue
            overlaps = left["end"] > right["start"]
            different_locations = left["location"] != right["location"]
            if overlaps and different_locations:
                errors.append(
                    f"Actor `{actor}` overlaps between `{left['id']}` at `{left['location']}` "
                    f"and `{right['id']}` at `{right['location']}`."
                )
    return errors


if __name__ == "__main__":
    sys.exit(main())
