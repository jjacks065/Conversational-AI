from __future__ import annotations

import copy
import json
import struct
import tempfile
import unittest
from pathlib import Path

import yaml

from proxy.hardening import HardeningError, audit_hardening
from release_tools.assemble import ReleaseTarget, assemble_release, write_checksums


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "proxy.yaml"
LOCK_PATH = PROJECT_ROOT / "config" / "demo-lock.json"


def fake_macho_arm64() -> bytes:
    return struct.pack("<IIIIIIII", 0xFEEDFACF, 0x0100000C, 0, 2, 0, 0, 0, 0)


class HardeningAuditTests(unittest.TestCase):
    def test_real_deployment_config_matches_frozen_rules_and_safety_audit(self) -> None:
        result = audit_hardening(
            project_root=PROJECT_ROOT,
            config_path=CONFIG_PATH,
            lock_path=LOCK_PATH,
        )

        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["targetHost"], "app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net")
        self.assertEqual(len(result["rulesSha256"]), 64)
        self.assertTrue(result["payloadLoggingDisabled"])
        self.assertTrue(result["loopbackConfigured"])
        self.assertTrue(result["directFallbackConfigured"])

    def test_rejects_target_rule_drift(self) -> None:
        source = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
        source["target"]["host"] = "drifted.example.com"
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / "proxy.yaml"
            config_path.write_text(yaml.safe_dump(source, sort_keys=False), encoding="utf-8")

            with self.assertRaisesRegex(HardeningError, "frozen"):
                audit_hardening(
                    project_root=PROJECT_ROOT,
                    config_path=config_path,
                    lock_path=LOCK_PATH,
                )

    def test_rejects_tampered_lock_digest(self) -> None:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["rulesSha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as temporary_directory:
            lock_path = Path(temporary_directory) / "demo-lock.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")

            with self.assertRaisesRegex(HardeningError, "digest"):
                audit_hardening(
                    project_root=PROJECT_ROOT,
                    config_path=CONFIG_PATH,
                    lock_path=lock_path,
                )

    def test_audits_release_manifest_checksum_and_forbidden_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            runtime = temporary / "mitmdump"
            runtime.write_bytes(fake_macho_arm64())
            runtime.chmod(0o755)
            licenses = temporary / "licenses"
            licenses.mkdir()
            (licenses / "NOTICE.txt").write_text("license notice\n", encoding="utf-8")
            output = temporary / "dist"
            artifact = assemble_release(
                source_root=PROJECT_ROOT,
                target=ReleaseTarget.from_name("macos-arm64"),
                runtime_path=runtime,
                licenses_dir=licenses,
                output_dir=output,
                version="0.1.0",
            )
            write_checksums(output)

            result = audit_hardening(
                project_root=PROJECT_ROOT,
                config_path=CONFIG_PATH,
                lock_path=LOCK_PATH,
                artifact_path=artifact,
            )

            self.assertTrue(result["artifactVerified"])

    def test_cli_emits_machine_readable_preflight_result(self) -> None:
        import subprocess

        result = subprocess.run(
            [
                str(PROJECT_ROOT / ".venv/bin/python"),
                str(PROJECT_ROOT / "scripts/common/hardening_check.py"),
                "--project-root",
                str(PROJECT_ROOT),
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "passed")

    def test_explicit_freeze_utility_creates_auditable_sanitized_lock(self) -> None:
        import subprocess

        with tempfile.TemporaryDirectory() as temporary_directory:
            lock_path = Path(temporary_directory) / "demo-lock.json"
            result = subprocess.run(
                [
                    str(PROJECT_ROOT / ".venv/bin/python"),
                    str(PROJECT_ROOT / "scripts/common/freeze_config.py"),
                    "--config",
                    str(PROJECT_ROOT / "config/proxy.example.yaml"),
                    "--output",
                    str(lock_path),
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            audited = audit_hardening(
                project_root=PROJECT_ROOT,
                config_path=PROJECT_ROOT / "config/proxy.example.yaml",
                lock_path=lock_path,
            )
            self.assertEqual(audited["status"], "passed")
            self.assertNotIn("app-prdsrch", lock_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
