"""Build and smoke-test a native self-contained mitmdump executable."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from release_tools.assemble import ReleaseTarget, validate_runtime_binary
from release_tools.licenses import generate_third_party_notices
from release_tools.smoke import smoke_proxy_runtime


def detect_native_target(
    system_name: str | None = None, machine: str | None = None
) -> ReleaseTarget:
    system_name = (system_name or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    if system_name == "windows" and machine in {"amd64", "x86_64"}:
        return ReleaseTarget.from_name("windows-x64")
    if system_name == "darwin" and machine in {"arm64", "aarch64"}:
        return ReleaseTarget.from_name("macos-arm64")
    if system_name == "darwin" and machine in {"x86_64", "amd64"}:
        return ReleaseTarget.from_name("macos-x64")
    raise ValueError(f"unsupported native build platform: {system_name}/{machine}")


def build_native_runtime(
    *,
    source_root: Path,
    output_dir: Path,
    target: ReleaseTarget | None = None,
    python_executable: Path = Path(sys.executable),
) -> tuple[Path, Path]:
    native_target = detect_native_target()
    target = target or native_target
    if target != native_target:
        raise ValueError(
            f"PyInstaller does not cross-compile: requested {target.name}, native host is {native_target.name}"
        )
    if importlib.util.find_spec("PyInstaller") is None:
        raise RuntimeError(
            "PyInstaller is not installed; install requirements-build.txt in the build environment"
        )
    source_root = source_root.resolve()
    output_dir = output_dir.resolve()
    if output_dir == source_root or source_root not in output_dir.parents:
        raise ValueError("native build output must be a child of the DemoProxy source directory")
    target_root = output_dir / target.name
    dist_path = target_root / "bin"
    work_path = target_root / "work"
    spec_path = target_root / "spec"
    for path in (dist_path, work_path, spec_path):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    command = [
        str(python_executable),
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--log-level",
        "WARN",
        "--onefile",
        "--console",
        "--name",
        "mitmdump",
        "--distpath",
        str(dist_path),
        "--workpath",
        str(work_path),
        "--specpath",
        str(spec_path),
        "--paths",
        str(source_root),
        "--collect-all",
        "mitmproxy",
        "--collect-all",
        "proxy",
        "--copy-metadata",
        "mitmproxy",
        str(source_root / "release_tools" / "runtime_entry.py"),
    ]
    environment = os.environ.copy()
    environment["PYINSTALLER_CONFIG_DIR"] = str(target_root / "pyinstaller-cache")
    environment.setdefault("PYTHONHASHSEED", "1")
    environment.setdefault("SOURCE_DATE_EPOCH", "0")
    subprocess.run(command, cwd=source_root, env=environment, check=True)
    runtime_name = "mitmdump.exe" if target.platform == "windows" else "mitmdump"
    runtime_path = dist_path / runtime_name
    validate_runtime_binary(runtime_path, target)
    smoke = subprocess.run(
        [
            str(runtime_path),
            "--demo-verify-config",
            str(source_root / "config" / "proxy.example.yaml"),
        ],
        cwd=source_root,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if smoke.returncode != 0:
        raise RuntimeError(f"packaged runtime smoke test failed: {smoke.stderr.strip()}")
    payload = json.loads(smoke.stdout)
    if payload.get("status") != "valid" or payload.get("listenHost") != "127.0.0.1":
        raise RuntimeError("packaged runtime returned an unsafe validation result")
    hardening = subprocess.run(
        [
            str(runtime_path),
            "--demo-hardening-check",
            str(source_root),
            str(source_root / "config" / "proxy.yaml"),
            str(source_root / "config" / "demo-lock.json"),
        ],
        cwd=source_root,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if hardening.returncode != 0:
        raise RuntimeError(
            f"packaged hardening preflight failed: {hardening.stderr.strip()}"
        )
    if json.loads(hardening.stdout).get("status") != "passed":
        raise RuntimeError("packaged hardening preflight returned an invalid result")
    smoke_proxy_runtime(runtime_path=runtime_path, source_root=source_root)
    licenses_dir = target_root / "LICENSES"
    generate_third_party_notices(licenses_dir / "THIRD_PARTY-NOTICES.txt")
    return runtime_path, licenses_dir


def main() -> int:
    source_root_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=source_root_default)
    parser.add_argument("--output-dir", type=Path, default=source_root_default / "build" / "native")
    parser.add_argument("--target", choices=("windows-x64", "macos-arm64", "macos-x64"))
    args = parser.parse_args()
    target = ReleaseTarget.from_name(args.target) if args.target else None
    runtime, licenses = build_native_runtime(
        source_root=args.source_root,
        output_dir=args.output_dir,
        target=target,
    )
    print(json.dumps({"licenses": str(licenses), "runtime": str(runtime)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
