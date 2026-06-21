#!/usr/bin/env python3
"""Validate fitness coach local data for missing, malformed, or implausible values."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import read_jsonl, read_csv_dicts, to_float


def issue(file: str, severity: str, message: str, row: int | None = None) -> dict:
    return {"file": file, "severity": severity, "row": row, "message": message}


def validate_training(root: Path) -> list[dict]:
    path = root / "data" / "training_log.jsonl"
    issues = []
    try:
        rows = read_jsonl(path)
    except Exception as exc:
        return [issue(str(path), "error", str(exc))]
    for i, r in enumerate(rows, start=1):
        if not r.get("date"):
            issues.append(issue(str(path), "error", "Missing date", i))
        if r.get("completed") not in {"completed", "partial", "skipped", "planned"}:
            issues.append(issue(str(path), "error", "completed must be completed/partial/skipped/planned", i))
        duration = to_float(r.get("duration_min"))
        if duration is not None and duration > 180:
            issues.append(issue(str(path), "warning", "Session duration above 180 min", i))
        pain = r.get("pain") or {}
        severity = to_float(pain.get("severity_0_10")) if isinstance(pain, dict) else None
        if severity is not None and not (0 <= severity <= 10):
            issues.append(issue(str(path), "error", "Pain severity outside 0-10", i))
        for ex in r.get("exercises", []) or []:
            for s in ex.get("sets", []) or []:
                rpe = to_float(s.get("rpe"))
                if rpe is not None and not (1 <= rpe <= 10):
                    issues.append(issue(str(path), "error", f"RPE outside 1-10 in exercise {ex.get('name')}", i))
    return issues


def validate_nutrition(root: Path) -> list[dict]:
    path = root / "data" / "nutrition_log.jsonl"
    issues = []
    try:
        rows = read_jsonl(path)
    except Exception as exc:
        return [issue(str(path), "error", str(exc))]
    for i, r in enumerate(rows, start=1):
        if not r.get("date"):
            issues.append(issue(str(path), "error", "Missing date", i))
        kcal = to_float(r.get("kcal"))
        protein = to_float(r.get("protein_g"))
        if kcal is not None and (kcal < 1200 or kcal > 5000):
            issues.append(issue(str(path), "warning", "Calories outside normal plausibility range", i))
        if protein is not None and protein > 300:
            issues.append(issue(str(path), "warning", "Protein above 300 g/day", i))
        if r.get("confidence") not in {None, "", "high", "medium", "low", "unknown"}:
            issues.append(issue(str(path), "warning", "Unknown confidence label", i))
    return issues


def validate_body(root: Path) -> list[dict]:
    path = root / "data" / "body_metrics.csv"
    issues = []
    rows = read_csv_dicts(path)
    prev_weight = None
    prev_waist = None
    for i, r in enumerate(rows, start=2):
        if not r.get("date"):
            issues.append(issue(str(path), "error", "Missing date", i))
        weight = to_float(r.get("weight_kg"))
        waist = to_float(r.get("waist_navel_cm"))
        steps = to_float(r.get("steps"))
        if prev_weight is not None and weight is not None and abs(weight - prev_weight) > 2:
            issues.append(issue(str(path), "warning", "Weight changed by more than 2 kg since prior entry", i))
        if prev_waist is not None and waist is not None and abs(waist - prev_waist) > 3:
            issues.append(issue(str(path), "warning", "Waist changed by more than 3 cm since prior entry", i))
        if steps is not None and steps > 40000:
            issues.append(issue(str(path), "warning", "Steps above 40,000", i))
        prev_weight = weight if weight is not None else prev_weight
        prev_waist = waist if waist is not None else prev_waist
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    issues = validate_training(root) + validate_nutrition(root) + validate_body(root)
    if args.json:
        print(json.dumps({"issues": issues, "issue_count": len(issues)}, indent=2, ensure_ascii=False))
    else:
        if not issues:
            print("OK: no validation issues found.")
        else:
            for item in issues:
                loc = f":{item['row']}" if item.get("row") else ""
                print(f"{item['severity'].upper()} {item['file']}{loc} - {item['message']}")
    return 1 if any(i["severity"] == "error" for i in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
