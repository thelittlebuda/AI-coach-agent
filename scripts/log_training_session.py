#!/usr/bin/env python3
"""Append a training session JSON object to data/training_log.jsonl."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import append_jsonl, today_iso


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--date", default=today_iso())
    p.add_argument("--planned-session-id")
    p.add_argument("--completed", choices=["completed", "partial", "skipped", "planned"], required=True)
    p.add_argument("--duration-min", type=float)
    p.add_argument("--difficulty", choices=["too_easy", "right", "too_hard", "unknown"], default="unknown")
    p.add_argument("--energy", type=float)
    p.add_argument("--pain-present", action="store_true")
    p.add_argument("--pain-area")
    p.add_argument("--pain-severity", type=float, default=0)
    p.add_argument("--notes", default="")
    p.add_argument("--exercises-json", help="JSON array of exercise objects with set data")
    args = p.parse_args()

    exercises = []
    if args.exercises_json:
        exercises = json.loads(args.exercises_json)
        if not isinstance(exercises, list):
            raise SystemExit("--exercises-json must be a JSON array")

    entry = {
        "date": args.date,
        "planned_session_id": args.planned_session_id,
        "completed": args.completed,
        "duration_min": args.duration_min,
        "exercises": exercises,
        "conditioning": None,
        "energy_1_5": args.energy,
        "difficulty": args.difficulty,
        "pain": {
            "present": bool(args.pain_present),
            "area": args.pain_area,
            "severity_0_10": args.pain_severity,
        },
        "notes": args.notes,
    }
    append_jsonl(Path(args.root).expanduser().resolve() / "data" / "training_log.jsonl", entry)
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
