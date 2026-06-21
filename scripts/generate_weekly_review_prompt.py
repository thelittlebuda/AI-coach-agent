#!/usr/bin/env python3
"""Generate a self-contained Hermes prompt for a weekly review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import read_json, read_jsonl, read_csv_dicts, filter_by_date


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--days", type=int, default=14)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    prompt = f"""Run Álvaro's weekly fitness review.

Respond in Spanish. Be direct, numeric, and decision-oriented.

Tasks:
1. Compare 7-day average bodyweight trend if enough data exists.
2. Compare waist trend.
3. Review adherence: training, protein, calories, steps.
4. Review performance and recovery.
5. Decide whether to keep or adjust calories, protein, steps, training volume, conditioning.
6. Draft next-week changes if needed.
7. Create a decision_log entry.

Rules:
- Do not call a plateau with less than 14 days of usable trend data.
- If adherence is low, fix adherence before changing calorie targets.
- Make small changes: calories +/-150-200 kcal, steps +1000/day, volume +/-1 set.
- Handle pain conservatively; refer to doctor/physio for significant or persistent symptoms.

Active targets:
{json.dumps(read_json(root / 'data' / 'nutrition_targets.json', {}), indent=2, ensure_ascii=False)}

Active plan:
{json.dumps(read_json(root / 'data' / 'active_plan.json', {}), indent=2, ensure_ascii=False)}

Body metrics, last {args.days} days:
{json.dumps(filter_by_date(read_csv_dicts(root / 'data' / 'body_metrics.csv'), args.days), indent=2, ensure_ascii=False)}

Training log, last {args.days} days:
{json.dumps(filter_by_date(read_jsonl(root / 'data' / 'training_log.jsonl'), args.days), indent=2, ensure_ascii=False)}

Nutrition log, last {args.days} days:
{json.dumps(filter_by_date(read_jsonl(root / 'data' / 'nutrition_log.jsonl'), args.days), indent=2, ensure_ascii=False)}

External events, last {args.days} days:
{json.dumps(filter_by_date(read_jsonl(root / 'data' / 'external_events.jsonl'), args.days), indent=2, ensure_ascii=False)}
"""
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
