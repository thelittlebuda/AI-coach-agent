#!/usr/bin/env python3
"""Export active plan sessions and exercises to CSV for a tracker UI."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from _common import read_json

FIELDS = ["session_id", "session_name", "priority", "exercise_order", "exercise", "sets", "reps", "intensity", "rest_sec", "conditioning"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--output", default="exports/active_plan_tracker.csv")
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    plan = read_json(root / "data" / "active_plan.json", {})
    out_path = root / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for session in plan.get("sessions", []):
        conditioning = session.get("conditioning")
        conditioning_text = ""
        if isinstance(conditioning, dict):
            conditioning_text = f"{conditioning.get('type')} {conditioning.get('duration_min')}min {conditioning.get('intensity')}"
        for idx, ex in enumerate(session.get("exercises", []) or [], start=1):
            rows.append({
                "session_id": session.get("session_id"),
                "session_name": session.get("name"),
                "priority": session.get("priority"),
                "exercise_order": idx,
                "exercise": ex.get("name"),
                "sets": ex.get("sets"),
                "reps": ex.get("reps"),
                "intensity": ex.get("intensity"),
                "rest_sec": ex.get("rest_sec"),
                "conditioning": conditioning_text,
            })
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
