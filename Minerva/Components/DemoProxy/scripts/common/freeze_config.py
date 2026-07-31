#!/usr/bin/env python3
"""Freeze an explicitly approved DemoProxy configuration into a drift lock."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from proxy.config import ConfigError, load_config  # noqa: E402
from proxy.hardening import create_lock  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        print(f"refusing to overwrite existing lock: {args.output}", file=sys.stderr)
        return 2
    try:
        lock = create_lock(load_config(args.config))
    except ConfigError as exc:
        print(f"configuration invalid: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(f".{args.output.name}.tmp")
    temporary.write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(args.output)
    print(json.dumps({"output": str(args.output), "rulesSha256": lock["rulesSha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
