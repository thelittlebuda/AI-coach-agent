#!/usr/bin/env python3
"""Render data/active_plan.json as readable Markdown."""
from __future__ import annotations

import argparse
from pathlib import Path
from _common import read_json


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    args = p.parse_args()
    plan = read_json(Path(args.root).expanduser().resolve() / "data" / "active_plan.json", {})
    print(f"# Active Plan: {plan.get('plan_id', 'unknown')}\n")
    print(f"Phase: {plan.get('phase', 'unknown')}\n")
    for s in plan.get("sessions", []):
        optional = " Optional" if s.get("optional") else ""
        print(f"## {s.get('session_id')} — {s.get('name')}{optional}\n")
        print(f"Goal: {s.get('goal', '')}\n")
        for ex in s.get("exercises", []) or []:
            print(f"- {ex.get('name')}: {ex.get('sets')} x {ex.get('reps')} @ {ex.get('intensity')}, rest {ex.get('rest_sec')}s")
        if s.get("conditioning"):
            c = s["conditioning"]
            print(f"- Conditioning: {c.get('type')}, {c.get('duration_min')} min, {c.get('intensity')}")
        for opt in s.get("options", []) or []:
            print(f"- Option: {opt}")
        print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
