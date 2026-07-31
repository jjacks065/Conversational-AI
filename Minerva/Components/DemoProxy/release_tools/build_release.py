"""Build the native runtime, deterministic release archive, and checksums."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from release_tools.assemble import assemble_release, write_checksums
from release_tools.build_runtime import build_native_runtime, detect_native_target


def main() -> int:
    source_root_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=source_root_default)
    parser.add_argument("--build-dir", type=Path, default=source_root_default / "build" / "native")
    parser.add_argument("--output-dir", type=Path, default=source_root_default / "dist")
    parser.add_argument("--version", default=(source_root_default / "VERSION").read_text().strip())
    args = parser.parse_args()

    target = detect_native_target()
    runtime, licenses = build_native_runtime(
        source_root=args.source_root,
        output_dir=args.build_dir,
        target=target,
    )
    artifact = assemble_release(
        source_root=args.source_root,
        target=target,
        runtime_path=runtime,
        licenses_dir=licenses,
        output_dir=args.output_dir,
        version=args.version,
    )
    checksums = write_checksums(args.output_dir)
    print(
        json.dumps(
            {
                "artifact": str(artifact),
                "checksums": str(checksums),
                "target": target.name,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
