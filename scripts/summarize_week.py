#!/usr/bin/env python3
"""Summarize recent body, training, and nutrition data for Hermes weekly review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import read_csv_dicts, read_jsonl, filter_by_date, to_float, mean, percent


def build_summary(root: Path, days: int) -> dict:
    body_rows = filter_by_date(read_csv_dicts(root / "data" / "body_metrics.csv"), days)
    training_rows = filter_by_date(read_jsonl(root / "data" / "training_log.jsonl"), days)
    nutrition_rows = filter_by_date(read_jsonl(root / "data" / "nutrition_log.jsonl"), days)

    weights = [to_float(r.get("weight_kg")) for r in body_rows]
    waists = [to_float(r.get("waist_navel_cm")) for r in body_rows]
    steps = [to_float(r.get("steps")) for r in body_rows]
    sleep = [to_float(r.get("sleep_hours")) for r in body_rows]

    completed = [r for r in training_rows if r.get("completed") == "completed"]
    partial = [r for r in training_rows if r.get("completed") == "partial"]
    skipped = [r for r in training_rows if r.get("completed") == "skipped"]

    kcal = [to_float(r.get("kcal")) for r in nutrition_rows]
    protein = [to_float(r.get("protein_g")) for r in nutrition_rows]

    return {
        "window_days": days,
        "body": {
            "weigh_ins": len([w for w in weights if w is not None]),
            "avg_weight_kg": mean(weights),
            "latest_weight_kg": next((w for w in reversed(weights) if w is not None), None),
            "avg_waist_cm": mean(waists),
            "latest_waist_cm": next((w for w in reversed(waists) if w is not None), None),
            "avg_steps": mean(steps),
            "avg_sleep_hours": mean(sleep),
        },
        "training": {
            "logged_sessions": len(training_rows),
            "completed": len(completed),
            "partial": len(partial),
            "skipped": len(skipped),
            "completion_rate_pct": percent(len(completed) + 0.5 * len(partial), max(len(training_rows), 1)),
        },
        "nutrition": {
            "logged_days": len(nutrition_rows),
            "avg_kcal": mean(kcal),
            "avg_protein_g": mean(protein),
            "protein_days_ge_160": len([p for p in protein if p is not None and p >= 160]),
        },
    }


def as_markdown(summary: dict) -> str:
    b = summary["body"]
    t = summary["training"]
    n = summary["nutrition"]
    return f"""# Fitness Summary - Last {summary['window_days']} Days

## Body
- Weigh-ins: {b['weigh_ins']}
- Average weight: {fmt(b['avg_weight_kg'])} kg
- Latest weight: {fmt(b['latest_weight_kg'])} kg
- Average waist: {fmt(b['avg_waist_cm'])} cm
- Latest waist: {fmt(b['latest_waist_cm'])} cm
- Average steps: {fmt(b['avg_steps'], 0)}
- Average sleep: {fmt(b['avg_sleep_hours'])} h

## Training
- Logged sessions: {t['logged_sessions']}
- Completed: {t['completed']}
- Partial: {t['partial']}
- Skipped: {t['skipped']}
- Completion rate: {fmt(t['completion_rate_pct'])}%

## Nutrition
- Logged days: {n['logged_days']}
- Average kcal: {fmt(n['avg_kcal'], 0)}
- Average protein: {fmt(n['avg_protein_g'])} g
- Days protein >=160 g: {n['protein_days_ge_160']}
"""


def fmt(value, decimals=1):
    if value is None:
        return "unknown"
    return f"{value:.{decimals}f}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    summary = build_summary(Path(args.root).expanduser().resolve(), args.days)
    print(as_markdown(summary) if args.format == "markdown" else json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
