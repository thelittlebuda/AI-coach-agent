#!/usr/bin/env python3
"""Append a traceable coaching decision to data/decision_log.jsonl."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import append_jsonl, today_iso


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--date", default=today_iso())
    p.add_argument("--decision-type", required=True)
    p.add_argument("--input-summary", required=True)
    p.add_argument("--change", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--confidence", choices=["high", "medium", "low"], required=True)
    p.add_argument("--next-review-date")
    p.add_argument("--rollback-condition")
    args = p.parse_args()
    entry = {
        "date": args.date,
        "decision_type": args.decision_type,
        "input_summary": args.input_summary,
        "change": args.change,
        "reason": args.reason,
        "confidence": args.confidence,
        "next_review_date": args.next_review_date,
        "rollback_condition": args.rollback_condition,
    }
    append_jsonl(Path(args.root).expanduser().resolve() / "data" / "decision_log.jsonl", entry)
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
