#!/usr/bin/env python3
"""Create a timestamped zip backup of the data directory."""
from __future__ import annotations

import argparse
import zipfile
from datetime import datetime
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".")
    p.add_argument("--output-dir", default="backups")
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    out_dir = root / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = out_dir / f"fitness_data_backup_{stamp}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in (root / "data").rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(root))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
