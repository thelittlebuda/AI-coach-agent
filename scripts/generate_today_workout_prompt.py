#!/usr/bin/env python3
"""Generate a self-contained Hermes prompt for today's workout delivery."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from _common import read_json, read_jsonl, filter_by_date


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--date", default=date.today().isoformat())
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    active_plan = read_json(root / "data" / "active_plan.json", {})
    recent_training = filter_by_date(read_jsonl(root / "data" / "training_log.jsonl"), 7)
    targets = read_json(root / "data" / "nutrition_targets.json", {})
    prompt = f"""You are Álvaro's Hermes fitness coach.

Task: Send today's workout or rest-day action for {args.date}.

Rules:
- Respond in Spanish.
- Keep it concise and executable.
- Do not redesign the week.
- Include warm-up, main exercises, sets, reps, RPE/RIR, rest, conditioning/cooldown, and low-energy modification.
- Respect 45-60 minutes total.
- Monitor right shoulder and avoid reckless overhead fatigue.

Active plan JSON:
{json.dumps(active_plan, indent=2, ensure_ascii=False)}

Recent training logs, last 7 days:
{json.dumps(recent_training, indent=2, ensure_ascii=False)}

Nutrition/movement targets:
{json.dumps(targets, indent=2, ensure_ascii=False)}
"""
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
