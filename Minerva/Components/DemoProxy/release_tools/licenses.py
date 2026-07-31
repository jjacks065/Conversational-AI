"""Generate deterministic third-party notices from installed distributions."""

from __future__ import annotations

import argparse
import importlib.metadata
import re
from pathlib import Path


_LICENSE_NAME = re.compile(
    r"^(?:licen[cs]e|copying|notice|authors?)(?:[._-].*)?$", re.IGNORECASE
)


def generate_third_party_notices(output_path: Path) -> Path:
    distributions = sorted(
        importlib.metadata.distributions(),
        key=lambda distribution: (distribution.metadata.get("Name") or "").lower(),
    )
    sections = [
        "DemoResponseProxy Third-Party Notices",
        "=====================================",
        "",
        "This file is generated from the Python environment used to build the native runtime.",
        "",
    ]
    seen: set[tuple[str, str]] = set()
    for distribution in distributions:
        name = distribution.metadata.get("Name") or "Unknown distribution"
        version = distribution.version or "Unknown version"
        identity = (name.lower(), version)
        if identity in seen:
            continue
        seen.add(identity)
        license_expression = (
            distribution.metadata.get("License-Expression")
            or distribution.metadata.get("License")
            or "Not declared in package metadata"
        ).strip()
        sections.extend(
            [
                "-" * 78,
                f"Name: {name}",
                f"Version: {version}",
                f"License: {license_expression}",
            ]
        )
        project_url = distribution.metadata.get("Home-page")
        if project_url:
            sections.append(f"Project: {project_url.strip()}")
        license_files = _license_files(distribution)
        if not license_files:
            sections.append("License text: no license file was exposed by the installed wheel.")
        for relative, content in license_files:
            sections.extend(["", f"[{relative}]", content.rstrip()])
        sections.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8", newline="\n")
    return output_path


def _license_files(
    distribution: importlib.metadata.Distribution,
) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for relative in distribution.files or ():
        path = Path(str(relative))
        if not any(_LICENSE_NAME.fullmatch(part) for part in path.parts):
            continue
        located = Path(distribution.locate_file(relative))
        if not located.is_file():
            continue
        try:
            content = located.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        result.append((path.as_posix(), content))
    result.sort(key=lambda item: item[0].lower())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(generate_third_party_notices(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
