#!/usr/bin/env python3
"""Compute simple estimated PRs from training_log.jsonl."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from _common import read_jsonl, to_float


def epley_1rm(kg: float, reps: float) -> float:
    return kg * (1 + reps / 30.0)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--top", type=int, default=10)
    args = p.parse_args()
    rows = read_jsonl(Path(args.root).expanduser().resolve() / "data" / "training_log.jsonl")
    best = {}
    for row in rows:
        for ex in row.get("exercises", []) or []:
            name = ex.get("name") or "unknown"
            for s in ex.get("sets", []) or []:
                kg = to_float(s.get("kg"))
                reps = to_float(s.get("reps"))
                if kg is None or reps is None or reps <= 0:
                    continue
                est = epley_1rm(kg, reps)
                current = best.get(name)
                if current is None or est > current["estimated_1rm"]:
                    best[name] = {"exercise": name, "estimated_1rm": est, "kg": kg, "reps": reps, "date": row.get("date")}
    prs = sorted(best.values(), key=lambda x: x["estimated_1rm"], reverse=True)[:args.top]
    print(json.dumps(prs, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
