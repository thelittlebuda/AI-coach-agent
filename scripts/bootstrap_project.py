#!/usr/bin/env python3
"""Create the local Hermes fitness coach project folders and seed files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SEED_PROFILE = """user:
  name: Álvaro
  sex: male
  age: 32
  height_cm: 190
  current_weight_kg: 100
  recent_usual_weight_kg: 105
  estimated_body_fat_pct: 27
  waist_navel_cm: 102
primary_goal: reduce_body_fat_percentage
preferred_fat_loss_style: moderate
"""


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()

    for sub in ["data", "schemas", "skills", "scripts", "config", "exports", "backups"]:
        (root / sub).mkdir(parents=True, exist_ok=True)

    write_if_missing(root / "data" / "profile.yaml", SEED_PROFILE)
    write_if_missing(root / "data" / "body_metrics.csv", "date,weight_kg,waist_navel_cm,sleep_hours,sleep_quality_0_10,steps,resting_hr,notes\n")
    for name in ["training_log.jsonl", "nutrition_log.jsonl", "external_events.jsonl", "decision_log.jsonl", "weekly_reviews.jsonl"]:
        write_if_missing(root / "data" / name, "")
    write_if_missing(root / "data" / "nutrition_targets.json", json.dumps({
        "calories_kcal_per_day_min": 2400,
        "calories_kcal_per_day_max": 2600,
        "protein_g_per_day_min": 180,
        "protein_g_per_day_max": 210,
        "fiber_g_per_day_min": 25,
        "fiber_g_per_day_max": 40,
        "steps_initial_target": 7000
    }, indent=2) + "\n")

    print(f"Bootstrapped fitness coach project at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
