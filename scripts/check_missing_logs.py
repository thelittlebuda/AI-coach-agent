#!/usr/bin/env python3
"""No-agent cron helper: print a reminder only if a required log is missing today.

Empty stdout means silent tick.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from _common import read_csv_dicts, read_jsonl


def today() -> str:
    return date.today().isoformat()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--check", choices=["bodyweight", "training", "nutrition"], required=True)
    p.add_argument("--after", help="Only warn after local HH:MM. Useful for cron.")
    args = p.parse_args()

    if args.after:
        now = datetime.now().time()
        threshold = datetime.strptime(args.after, "%H:%M").time()
        if now < threshold:
            return 0

    root = Path(args.root).expanduser().resolve()
    today_str = today()
    if args.check == "bodyweight":
        rows = read_csv_dicts(root / "data" / "body_metrics.csv")
        has = any(r.get("date") == today_str and r.get("weight_kg") for r in rows)
        if not has:
            print("Missing today's weigh-in. Log bodyweight when convenient.")
    elif args.check == "training":
        rows = read_jsonl(root / "data" / "training_log.jsonl")
        has = any(r.get("date") == today_str for r in rows)
        if not has:
            print("No training check-in logged today. Send completed/partial/skipped, top sets, pain, energy.")
    elif args.check == "nutrition":
        rows = read_jsonl(root / "data" / "nutrition_log.jsonl")
        has = any(r.get("date") == today_str for r in rows)
        if not has:
            print("No nutrition summary logged today. Send kcal/protein estimate and confidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
