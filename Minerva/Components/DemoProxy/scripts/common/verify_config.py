#!/usr/bin/env python3
"""Validate DemoProxy YAML without printing secrets or header patterns."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from proxy.config import ConfigError, load_config  # noqa: E402


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else PROJECT_ROOT / "config" / "proxy.yaml"
    try:
        config = load_config(path)
    except ConfigError as exc:
        print(f"configuration invalid: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "valid",
                "listenHost": config.proxy.listen_host,
                "listenPort": config.proxy.listen_port,
                "healthPort": config.platform.health_port,
                "pacPort": config.platform.pac_port,
                "targetHost": config.target.host,
                "transformerVersion": config.transformation.transformer_version,
                "failOpen": config.proxy.fail_open,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
