"""Entry point for the self-contained DemoProxy mitmdump runtime."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _verify_config(path: str) -> int:
    from proxy.config import ConfigError, load_config

    try:
        config = load_config(Path(path))
    except ConfigError as exc:
        print(f"configuration invalid: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "failOpen": config.proxy.fail_open,
                "healthPort": config.platform.health_port,
                "listenHost": config.proxy.listen_host,
                "listenPort": config.proxy.listen_port,
                "pacPort": config.platform.pac_port,
                "status": "valid",
                "targetHost": config.target.host,
                "transformerVersion": config.transformation.transformer_version,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


def main(argv: list[str]) -> int:
    if argv[1:2] == ["--demo-verify-config"]:
        if len(argv) != 3:
            print("usage: mitmdump --demo-verify-config CONFIG_PATH", file=sys.stderr)
            return 2
        return _verify_config(argv[2])
    if argv[1:2] == ["--demo-hardening-check"]:
        if len(argv) not in {5, 6} or (len(argv) == 6 and argv[5] != "--live"):
            print(
                "usage: mitmdump --demo-hardening-check PROJECT_ROOT CONFIG LOCK [--live]",
                file=sys.stderr,
            )
            return 2
        from proxy.hardening import HardeningError, audit_hardening

        try:
            result = audit_hardening(
                project_root=Path(argv[2]),
                config_path=Path(argv[3]),
                lock_path=Path(argv[4]),
                live=len(argv) == 6,
            )
        except HardeningError as exc:
            print(f"hardening check failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, separators=(",", ":"), sort_keys=True))
        return 0
    from mitmproxy.tools.main import mitmdump

    mitmdump()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
