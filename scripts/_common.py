#!/usr/bin/env python3
"""Shared helpers for the Hermes fitness coach scripts. Standard library only."""
from __future__ import annotations

import csv
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def project_root(path: str | Path | None = None) -> Path:
    return Path(path or ".").expanduser().resolve()


def data_path(root: Path, name: str) -> Path:
    return root / "data" / name


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {path} line {line_no}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"JSONL row in {path} line {line_no} is not an object")
            rows.append(item)
    return rows


def append_jsonl(path: Path, item: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def append_csv_row(path: Path, fieldnames: List[str], row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fieldnames})


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def today_iso() -> str:
    return date.today().isoformat()


def window_start(days: int, end: Optional[date] = None) -> date:
    end = end or date.today()
    return end - timedelta(days=days - 1)


def to_float(value: Any) -> Optional[float]:
    if value in (None, "", "null"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean(values: Iterable[Optional[float]]) -> Optional[float]:
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)


def percent(numerator: float, denominator: float) -> Optional[float]:
    if denominator == 0:
        return None
    return 100.0 * numerator / denominator


def filter_by_date(rows: List[Dict[str, Any]], days: int, date_key: str = "date") -> List[Dict[str, Any]]:
    start = window_start(days)
    out = []
    for row in rows:
        raw = row.get(date_key)
        if not raw:
            continue
        try:
            d = parse_date(str(raw))
        except ValueError:
            continue
        if d >= start:
            out.append(row)
    return out
