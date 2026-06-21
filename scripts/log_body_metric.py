#!/usr/bin/env python3
"""Append a body metric row to data/body_metrics.csv."""
from __future__ import annotations

import argparse
from pathlib import Path
from _common import append_csv_row, today_iso

FIELDS = ["date", "weight_kg", "waist_navel_cm", "sleep_hours", "sleep_quality_0_10", "steps", "resting_hr", "notes"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--date", default=today_iso())
    p.add_argument("--weight-kg")
    p.add_argument("--waist-cm")
    p.add_argument("--sleep-hours")
    p.add_argument("--sleep-quality")
    p.add_argument("--steps")
    p.add_argument("--resting-hr")
    p.add_argument("--notes", default="")
    args = p.parse_args()
    row = {
        "date": args.date,
        "weight_kg": args.weight_kg or "",
        "waist_navel_cm": args.waist_cm or "",
        "sleep_hours": args.sleep_hours or "",
        "sleep_quality_0_10": args.sleep_quality or "",
        "steps": args.steps or "",
        "resting_hr": args.resting_hr or "",
        "notes": args.notes,
    }
    path = Path(args.root).expanduser().resolve() / "data" / "body_metrics.csv"
    append_csv_row(path, FIELDS, row)
    print(f"Logged body metrics for {args.date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
