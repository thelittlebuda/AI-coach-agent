#!/usr/bin/env python3
"""Append a daily nutrition summary to data/nutrition_log.jsonl."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import append_jsonl, today_iso


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--date", default=today_iso())
    p.add_argument("--kcal", type=float)
    p.add_argument("--protein-g", type=float)
    p.add_argument("--fiber-g", type=float)
    p.add_argument("--alcohol-units", type=float)
    p.add_argument("--confidence", choices=["high", "medium", "low", "unknown"], default="unknown")
    p.add_argument("--notes", default="")
    args = p.parse_args()
    entry = {
        "date": args.date,
        "kcal": args.kcal,
        "protein_g": args.protein_g,
        "fiber_g": args.fiber_g,
        "alcohol_units": args.alcohol_units,
        "confidence": args.confidence,
        "notes": args.notes,
    }
    append_jsonl(Path(args.root).expanduser().resolve() / "data" / "nutrition_log.jsonl", entry)
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
