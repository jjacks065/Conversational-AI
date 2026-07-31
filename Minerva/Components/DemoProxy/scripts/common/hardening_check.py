#!/usr/bin/env python3
"""Run the DemoProxy frozen-rule, source, package, and live preflight audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from proxy.hardening import HardeningError, audit_hardening  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    try:
        result = audit_hardening(
            project_root=project_root,
            config_path=args.config or project_root / "config" / "proxy.yaml",
            lock_path=args.lock or project_root / "config" / "demo-lock.json",
            artifact_path=args.artifact,
            live=args.live,
        )
    except HardeningError as exc:
        print(json.dumps({"error": str(exc), "status": "failed"}, sort_keys=True))
        return 1
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
