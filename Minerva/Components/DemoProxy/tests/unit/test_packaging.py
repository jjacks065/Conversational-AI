from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from release_tools.assemble import (
    ReleaseTarget,
    assemble_release,
    write_checksums,
)
from release_tools.build_runtime import detect_native_target
from release_tools.licenses import generate_third_party_notices
from release_tools.smoke import smoke_proxy_runtime


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def fake_pe_x64() -> bytes:
    payload = bytearray(256)
    payload[:2] = b"MZ"
    struct.pack_into("<I", payload, 0x3C, 0x80)
    payload[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", payload, 0x84, 0x8664)
    return bytes(payload)


def fake_macho(cpu_type: int) -> bytes:
    return struct.pack("<IIIIIIII", 0xFEEDFACF, cpu_type, 0, 2, 0, 0, 0, 0)


class PackagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.licenses = self.root / "licenses"
        self.licenses.mkdir()
        (self.licenses / "THIRD_PARTY-NOTICES.txt").write_text(
            "Test dependency license notice\n", encoding="utf-8"
        )

    def _runtime(self, target: ReleaseTarget) -> Path:
        suffix = ".exe" if target.platform == "windows" else ""
        path = self.root / f"runtime-{target.name}{suffix}"
        if target.name == "windows-x64":
            content = fake_pe_x64()
        elif target.name == "macos-arm64":
            content = fake_macho(0x0100000C)
        else:
            content = fake_macho(0x01000007)
        path.write_bytes(content)
        path.chmod(0o755)
        return path

    def test_builds_all_named_artifact_formats_with_required_layout(self) -> None:
        output = self.root / "dist"
        targets = tuple(ReleaseTarget.from_name(name) for name in (
            "windows-x64",
            "macos-arm64",
            "macos-x64",
        ))
        artifacts = [
            assemble_release(
                source_root=PROJECT_ROOT,
                target=target,
                runtime_path=self._runtime(target),
                licenses_dir=self.licenses,
                output_dir=output,
                version="0.1.0",
            )
            for target in targets
        ]

        self.assertEqual(
            [artifact.name for artifact in artifacts],
            [
                "DemoResponseProxy-0.1.0-windows-x64.zip",
                "DemoResponseProxy-0.1.0-macos-arm64.tar.gz",
                "DemoResponseProxy-0.1.0-macos-x64.tar.gz",
            ],
        )
        for artifact, target in zip(artifacts, targets, strict=True):
            names, read_bytes, mode = self._archive_accessors(artifact)
            prefix = f"DemoResponseProxy-0.1.0-{target.name}/"
            runtime_name = "mitmdump.exe" if target.platform == "windows" else "mitmdump"
            required = {
                f"{prefix}bin/{runtime_name}",
                f"{prefix}config/proxy.yaml",
                f"{prefix}config/proxy.example.yaml",
                f"{prefix}config/demo-lock.json",
                f"{prefix}config/demo-lock.example.json",
                f"{prefix}proxy/addon.py",
                f"{prefix}pac/demo-proxy.pac",
                f"{prefix}scripts/common/verify_config.py",
                f"{prefix}README.md",
                f"{prefix}DEMO_RUNBOOK.md",
                f"{prefix}VERSION",
                f"{prefix}LICENSES/THIRD_PARTY-NOTICES.txt",
            }
            self.assertTrue(required.issubset(names), required - names)
            platform_script = "install.ps1" if target.platform == "windows" else "install.sh"
            self.assertIn(f"{prefix}scripts/{target.platform}/{platform_script}", names)
            self.assertEqual(read_bytes(f"{prefix}VERSION"), b"0.1.0\n")
            self.assertIn(b"api.demo.example.com", read_bytes(f"{prefix}config/proxy.yaml"))
            self.assertNotIn(
                b"app-prdsrch-npn-to-bncp-cus-452",
                read_bytes(f"{prefix}config/proxy.yaml"),
            )
            self.assertEqual(mode(f"{prefix}bin/{runtime_name}") & 0o777, 0o755)

    def test_archives_exclude_private_runtime_and_captured_content(self) -> None:
        target = ReleaseTarget.from_name("macos-arm64")
        artifact = assemble_release(
            source_root=PROJECT_ROOT,
            target=target,
            runtime_path=self._runtime(target),
            licenses_dir=self.licenses,
            output_dir=self.root / "dist",
            version="0.1.0",
        )
        names, _, _ = self._archive_accessors(artifact)

        forbidden_fragments = (
            ".venv",
            "runtime/",
            "chrome-profile",
            "Content-Sample",
            "PROTOCOL_DISCOVERY",
            "tests/",
            ".pem",
            ".cer",
            ".key",
            "proxy.yaml.tmp",
        )
        for name in names:
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, name)

    def test_archives_are_reproducible_and_checksums_are_sorted(self) -> None:
        target = ReleaseTarget.from_name("macos-arm64")
        runtime = self._runtime(target)
        first = assemble_release(
            source_root=PROJECT_ROOT,
            target=target,
            runtime_path=runtime,
            licenses_dir=self.licenses,
            output_dir=self.root / "first",
            version="0.1.0",
            source_date_epoch=0,
        )
        second = assemble_release(
            source_root=PROJECT_ROOT,
            target=target,
            runtime_path=runtime,
            licenses_dir=self.licenses,
            output_dir=self.root / "second",
            version="0.1.0",
            source_date_epoch=0,
        )
        self.assertEqual(first.read_bytes(), second.read_bytes())

        windows = assemble_release(
            source_root=PROJECT_ROOT,
            target=ReleaseTarget.from_name("windows-x64"),
            runtime_path=self._runtime(ReleaseTarget.from_name("windows-x64")),
            licenses_dir=self.licenses,
            output_dir=self.root / "first",
            version="0.1.0",
        )
        checksum_path = write_checksums(self.root / "first")
        lines = checksum_path.read_text(encoding="ascii").splitlines()
        self.assertEqual(lines, sorted(lines, key=lambda line: line.split("  ", 1)[1]))
        for line in lines:
            digest, name = line.split("  ", 1)
            self.assertEqual(
                digest,
                hashlib.sha256((self.root / "first" / name).read_bytes()).hexdigest(),
            )
        self.assertIn(windows.name, checksum_path.read_text(encoding="ascii"))

    def test_rejects_wrong_runtime_architecture_and_unsafe_version(self) -> None:
        with self.assertRaisesRegex(ValueError, "architecture"):
            assemble_release(
                source_root=PROJECT_ROOT,
                target=ReleaseTarget.from_name("macos-x64"),
                runtime_path=self._runtime(ReleaseTarget.from_name("macos-arm64")),
                licenses_dir=self.licenses,
                output_dir=self.root / "dist",
                version="0.1.0",
            )
        with self.assertRaisesRegex(ValueError, "version"):
            assemble_release(
                source_root=PROJECT_ROOT,
                target=ReleaseTarget.from_name("macos-arm64"),
                runtime_path=self._runtime(ReleaseTarget.from_name("macos-arm64")),
                licenses_dir=self.licenses,
                output_dir=self.root / "dist",
                version="../unsafe",
            )

    def test_runtime_entry_validates_config_without_starting_proxy(self) -> None:
        result = subprocess.run(
            [
                str(PROJECT_ROOT / ".venv" / "bin" / "python"),
                str(PROJECT_ROOT / "release_tools" / "runtime_entry.py"),
                "--demo-verify-config",
                str(PROJECT_ROOT / "config" / "proxy.example.yaml"),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["listenHost"], "127.0.0.1")

        hardening = subprocess.run(
            [
                str(PROJECT_ROOT / ".venv" / "bin" / "python"),
                str(PROJECT_ROOT / "release_tools" / "runtime_entry.py"),
                "--demo-hardening-check",
                str(PROJECT_ROOT),
                str(PROJECT_ROOT / "config" / "proxy.yaml"),
                str(PROJECT_ROOT / "config" / "demo-lock.json"),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(hardening.returncode, 0, hardening.stderr)
        self.assertEqual(json.loads(hardening.stdout)["status"], "passed")

    def test_native_target_detection_and_license_generation(self) -> None:
        self.assertEqual(detect_native_target("Darwin", "arm64").name, "macos-arm64")
        self.assertEqual(detect_native_target("Darwin", "x86_64").name, "macos-x64")
        self.assertEqual(detect_native_target("Windows", "AMD64").name, "windows-x64")
        with self.assertRaisesRegex(ValueError, "unsupported"):
            detect_native_target("Linux", "x86_64")

        notices = generate_third_party_notices(self.root / "generated" / "notices.txt")
        content = notices.read_text(encoding="utf-8")
        self.assertIn("Name: mitmproxy", content)
        self.assertIn("Name: PyYAML", content)

    def test_packaged_installers_invoke_embedded_config_validator(self) -> None:
        windows = (PROJECT_ROOT / "scripts/windows/Common.ps1").read_text()
        macos = (PROJECT_ROOT / "scripts/macos/common.sh").read_text()

        self.assertIn("--demo-verify-config", windows)
        self.assertIn("--demo-verify-config", macos)

    def test_development_runtime_passes_release_proxy_smoke(self) -> None:
        result = smoke_proxy_runtime(
            runtime_path=PROJECT_ROOT / ".venv" / "bin" / "mitmdump",
            source_root=PROJECT_ROOT,
        )

        self.assertEqual(result["status"], "passed")

    @staticmethod
    def _archive_accessors(artifact: Path):
        if artifact.suffix == ".zip":
            archive = zipfile.ZipFile(artifact)
            names = set(archive.namelist())
            return (
                names,
                archive.read,
                lambda name: archive.getinfo(name).external_attr >> 16,
            )
        archive = tarfile.open(artifact, "r:gz")
        names = set(archive.getnames())

        def read_bytes(name: str) -> bytes:
            extracted = archive.extractfile(name)
            assert extracted is not None
            return extracted.read()

        return names, read_bytes, lambda name: archive.getmember(name).mode


if __name__ == "__main__":
    unittest.main()
