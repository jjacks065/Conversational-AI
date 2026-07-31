from __future__ import annotations

import os
import shutil
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MACOS_SCRIPTS = PROJECT_ROOT / "scripts" / "macos"
LAUNCH_AGENT = PROJECT_ROOT / "startup" / "macos" / "com.demo-response-proxy.plist"

REQUIRED_SCRIPTS = (
    "common.sh",
    "install.sh",
    "start.sh",
    "stop.sh",
    "enable.sh",
    "disable.sh",
    "install-ca.sh",
    "uninstall-ca.sh",
    "verify.sh",
    "uninstall.sh",
    "launch-chrome.sh",
)


def read_script(name: str) -> str:
    return (MACOS_SCRIPTS / name).read_text(encoding="utf-8")


class MacOSIntegrationContractTests(unittest.TestCase):
    def test_all_phase_seven_scripts_have_strict_shell_syntax(self) -> None:
        for name in REQUIRED_SCRIPTS:
            with self.subTest(script=name):
                path = MACOS_SCRIPTS / name
                content = path.read_text(encoding="utf-8")
                result = subprocess.run(
                    ["bash", "-n", str(path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("set -euo pipefail", content)

    def test_common_uses_per_user_paths_and_verifies_process_identity(self) -> None:
        content = read_script("common.sh")

        self.assertIn("Library/Application Support/DemoResponseProxy", content)
        self.assertIn("Library/Logs/DemoResponseProxy", content)
        self.assertIn("Library/LaunchAgents", content)
        self.assertIn("demo_process_status", content)
        self.assertIn("ps -p", content)
        self.assertIn("-o comm=", content)
        self.assertIn("-o command=", content)
        self.assertIn("demo_stop_tracked_process", content)
        self.assertIn("kill -TERM", content)
        self.assertIn("demo_write_launch_agent", content)

    def test_start_is_loopback_only_quiet_and_records_process_state(self) -> None:
        content = read_script("start.sh")

        self.assertIn("nohup", content)
        self.assertIn("</dev/null", content)
        self.assertIn("--supervised", content)
        self.assertIn('wait "${pid}"', content)
        self.assertIn('"--listen-host" "127.0.0.1"', content)
        self.assertIn('"--listen-port"', content)
        self.assertIn('"confdir=${DEMO_MITM_CONF_DIR}"', content)
        self.assertIn('"flow_detail=0"', content)
        self.assertIn("demo_proxy_config=", content)
        self.assertIn("demo_write_process_state", content)
        self.assertIn("DEMO_PROXY_CERTIFICATE_TRUSTED", content)

    def test_chrome_launcher_survives_terminal_handoff(self) -> None:
        content = read_script("launch-chrome.sh")

        self.assertIn("nohup", content)
        self.assertIn("</dev/null", content)
        self.assertIn("/usr/bin/open", content)
        self.assertIn("pgrep -f", content)
        self.assertIn('executable="${chrome_path}"', content)

    def test_certificate_management_is_login_keychain_only_and_exact(self) -> None:
        install_content = read_script("install-ca.sh")
        uninstall_content = read_script("uninstall-ca.sh")
        combined = install_content + uninstall_content

        self.assertIn("security add-trusted-cert", install_content)
        self.assertIn('"${DEMO_KEYCHAIN}"', install_content)
        self.assertIn("certificate.sha256", install_content)
        self.assertIn("demo_certificate_trusted", install_content)
        self.assertIn("security delete-certificate -Z", uninstall_content)
        self.assertIn("certificate.sha256", uninstall_content)
        self.assertNotIn("System.keychain", combined)
        self.assertNotIn("sudo", combined)

    def test_install_covers_architecture_runtime_launch_agent_and_smoke_test(self) -> None:
        content = read_script("install.sh")

        self.assertIn("uname -m", content)
        self.assertIn("arm64", content)
        self.assertIn("x86_64", content)
        self.assertIn("--development", content)
        self.assertIn("cp -R", content)
        self.assertIn("install-ca.sh", content)
        self.assertIn("launchctl bootstrap", content)
        self.assertIn("--supervised", read_script("common.sh"))
        self.assertIn("demo_wait_url", content)
        self.assertIn("verify.sh", content)
        self.assertIn("Rollback", content)

    def test_enable_and_force_disable_cover_operator_workflow(self) -> None:
        enable_content = read_script("enable.sh")
        disable_content = read_script("disable.sh")

        for expected in ("verify.sh", "start.sh", "install-ca.sh", "launch-chrome.sh"):
            self.assertIn(expected, enable_content)
        self.assertIn("launchctl kickstart", enable_content)
        self.assertIn('[[ -f "${DEMO_LAUNCH_AGENT_PATH}" ]]', enable_content)
        self.assertIn("--force", disable_content)
        self.assertIn('demo_stop_tracked_process "chrome"', disable_content)
        self.assertIn("stop.sh", disable_content)
        self.assertNotIn("networksetup", disable_content)

    def test_verify_checks_process_ports_health_pac_and_certificate(self) -> None:
        content = read_script("verify.sh")

        self.assertIn("demo_validate_config", content)
        self.assertIn("demo_process_status", content)
        self.assertIn("/health", content)
        self.assertIn("/demo-proxy.pac", content)
        self.assertIn("demo_certificate_trusted", content)
        self.assertIn("demo_port_open", content)

    def test_uninstall_is_scoped_and_removes_only_user_launch_agent(self) -> None:
        content = read_script("uninstall.sh")

        self.assertIn("demo_assert_install_root", content)
        self.assertIn("launchctl bootout", content)
        self.assertIn("uninstall-ca.sh", content)
        self.assertIn('rm -rf "${DEMO_APP_DIR}"', content)
        self.assertIn('rm -rf "${DEMO_LOG_DIR}"', content)
        self.assertNotIn("/Library/LaunchDaemons", content)
        self.assertNotIn("sudo", content)

    def test_launch_agent_is_per_user_and_runs_installed_start_script(self) -> None:
        content = LAUNCH_AGENT.read_text(encoding="utf-8")

        self.assertIn("com.demo-response-proxy", content)
        self.assertIn("__DEMO_PROXY_START_SCRIPT__", content)
        self.assertIn("__DEMO_PROXY_LOG_DIR__", content)
        self.assertIn("<key>RunAtLoad</key>", content)
        self.assertNotIn("UserName", content)

    @unittest.skipUnless(os.uname().sysname == "Darwin", "macOS-only shell behavior")
    def test_common_validates_real_config_and_safely_stops_owned_process(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory)
            app = home / "Library" / "Application Support" / "DemoResponseProxy"
            (app / "config").mkdir(parents=True)
            shutil.copy2(PROJECT_ROOT / "config" / "proxy.yaml", app / "config" / "proxy.yaml")
            common = MACOS_SCRIPTS / "common.sh"
            command = f'''
                set -euo pipefail
                source "{common}"
                demo_init_paths
                demo_assert_install_root
                demo_create_directories
                values="$(demo_validate_config)"
                [[ "$values" == "8080 8081 8765" ]]
                sleep 30 &
                child=$!
                trap 'kill "$child" 2>/dev/null || true' EXIT
                executable="$(demo_process_executable "$child")"
                demo_write_process_state test "$child" "$executable" "sleep" "30"
                demo_process_status test
                demo_stop_tracked_process test true
                ! kill -0 "$child" 2>/dev/null
                trap - EXIT
            '''
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "HOME": str(home)},
            )

            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.uname().sysname == "Darwin", "macOS-only runtime behavior")
    def test_real_proxy_start_and_stop_are_isolated_under_temporary_home(self) -> None:
        def free_port() -> int:
            with socket.socket() as listener:
                listener.bind(("127.0.0.1", 0))
                return int(listener.getsockname()[1])

        ports: set[int] = set()
        while len(ports) < 3:
            ports.add(free_port())
        proxy_port, health_port, pac_port = ports

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            home = temporary / "home"
            app = home / "Library" / "Application Support" / "DemoResponseProxy"
            for relative in ("proxy", "pac", "config", "scripts/common", "scripts/macos"):
                shutil.copytree(PROJECT_ROOT / relative, app / relative)
            os.symlink(PROJECT_ROOT / ".venv", app / ".venv", target_is_directory=True)
            config_path = app / "config" / "proxy.yaml"
            config = config_path.read_text(encoding="utf-8")
            config = config.replace("listen_port: 8080", f"listen_port: {proxy_port}")
            config = config.replace("health_port: 8081", f"health_port: {health_port}")
            config = config.replace("pac_port: 8765", f"pac_port: {pac_port}")
            config_path.write_text(config, encoding="utf-8")
            environment = {**os.environ, "HOME": str(home)}
            start = app / "scripts" / "macos" / "start.sh"
            stop = app / "scripts" / "macos" / "stop.sh"

            start_result = subprocess.run(
                ["bash", str(start), "--app-dir", str(app)],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=False,
                env=environment,
                timeout=30,
            )
            proxy_error_log = home / "Library/Logs/DemoResponseProxy/proxy.stderr.log"
            diagnostics = (
                proxy_error_log.read_text(encoding="utf-8", errors="replace")
                if proxy_error_log.exists()
                else "proxy stderr log missing"
            )
            self.assertEqual(
                start_result.returncode,
                0,
                f"{start_result.stderr}\nproxy log:\n{diagnostics}",
            )
            self.assertTrue((app / "runtime/mitmproxy/mitmproxy-ca-cert.cer").is_file())
            pid_file = app / "runtime/state/proxy.pid"
            self.assertTrue(pid_file.is_file())
            pid = pid_file.read_text(encoding="utf-8").strip()
            process_snapshot = subprocess.run(
                ["ps", "-ww", "-p", pid, "-o", "comm=,command="],
                capture_output=True,
                text=True,
                check=False,
            ).stdout
            state_snapshot = "\n".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in (
                    app / "runtime/state/proxy.executable",
                    app / "runtime/state/proxy.markers",
                )
            )

            stop_result = subprocess.run(
                ["bash", str(stop), "--app-dir", str(app), "--force"],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
                timeout=15,
            )
            self.assertEqual(
                stop_result.returncode,
                0,
                f"{stop_result.stderr}\nprocess:\n{process_snapshot}\nstate:\n{state_snapshot}",
            )
            self.assertFalse((app / "runtime/state/proxy.pid").exists())

    @unittest.skipUnless(os.uname().sysname == "Darwin", "macOS-only keychain workflow")
    def test_certificate_lifecycle_uses_exact_fingerprint_with_mock_keychain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            home = temporary / "home"
            app = home / "Library" / "Application Support" / "DemoResponseProxy"
            scripts = app / "scripts" / "macos"
            shutil.copytree(MACOS_SCRIPTS, scripts)
            certificate_directory = app / "runtime" / "mitmproxy"
            certificate_directory.mkdir(parents=True)
            certificate = certificate_directory / "mitmproxy-ca-cert.cer"
            private_key = temporary / "temporary-test.key"
            subprocess.run(
                [
                    "/usr/bin/openssl",
                    "req",
                    "-x509",
                    "-newkey",
                    "rsa:2048",
                    "-nodes",
                    "-subj",
                    "/CN=DemoProxy Test CA",
                    "-days",
                    "1",
                    "-keyout",
                    str(private_key),
                    "-out",
                    str(certificate),
                ],
                capture_output=True,
                check=True,
            )
            keychain = home / "Library" / "Keychains" / "login.keychain-db"
            keychain.parent.mkdir(parents=True)
            keychain.touch()
            fingerprint = subprocess.run(
                [
                    "/usr/bin/openssl",
                    "x509",
                    "-in",
                    str(certificate),
                    "-noout",
                    "-fingerprint",
                    "-sha256",
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.split("=", 1)[1].replace(":", "").strip()

            fake_bin = temporary / "bin"
            fake_bin.mkdir()
            security_log = temporary / "security.log"
            security_state = temporary / "trusted"
            fake_security = fake_bin / "security"
            fake_security.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' \"$*\" >>\"${SECURITY_LOG}\"
case \"$1\" in
  add-trusted-cert) touch \"${SECURITY_STATE}\" ;;
  find-certificate)
    [[ -f \"${SECURITY_STATE}\" ]] && printf 'SHA-256 hash: %s\\n' \"${EXPECTED_FINGERPRINT}\"
    ;;
  verify-cert) [[ -f \"${SECURITY_STATE}\" ]] ;;
  delete-certificate) rm -f \"${SECURITY_STATE}\" ;;
  *) exit 2 ;;
esac
""",
                encoding="utf-8",
            )
            fake_security.chmod(0o700)
            environment = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
                "SECURITY_LOG": str(security_log),
                "SECURITY_STATE": str(security_state),
                "EXPECTED_FINGERPRINT": fingerprint,
            }

            install_result = subprocess.run(
                ["bash", str(scripts / "install-ca.sh"), "--app-dir", str(app)],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(install_result.returncode, 0, install_result.stderr)
            self.assertEqual(
                (app / "runtime/state/certificate.sha256").read_text().strip(),
                fingerprint,
            )

            uninstall_result = subprocess.run(
                ["bash", str(scripts / "uninstall-ca.sh"), "--app-dir", str(app)],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(uninstall_result.returncode, 0, uninstall_result.stderr)
            self.assertFalse(security_state.exists())
            commands = security_log.read_text(encoding="utf-8")
            self.assertIn(f"delete-certificate -Z {fingerprint} -t {keychain}", commands)
            self.assertNotIn("System.keychain", commands)
            self.assertNotIn(" -d ", f" {commands} ")

    @unittest.skipUnless(os.uname().sysname == "Darwin", "macOS-only plist workflow")
    def test_launch_agent_generation_handles_per_user_paths_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            home = Path(temporary_directory) / "Home With Spaces"
            home.mkdir()
            common = MACOS_SCRIPTS / "common.sh"
            command = f'''
                set -euo pipefail
                source "{common}"
                demo_init_paths
                demo_write_launch_agent
                plutil -lint "${{DEMO_LAUNCH_AGENT_PATH}}" >/dev/null
                [[ "$(plutil -extract Label raw "${{DEMO_LAUNCH_AGENT_PATH}}")" == "com.demo-response-proxy" ]]
                [[ "$(plutil -extract ProgramArguments.0 raw "${{DEMO_LAUNCH_AGENT_PATH}}")" == "${{DEMO_APP_DIR}}/scripts/macos/start.sh" ]]
                [[ "$(plutil -extract ProgramArguments.2 raw "${{DEMO_LAUNCH_AGENT_PATH}}")" == "${{DEMO_APP_DIR}}" ]]
            '''
            result = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "HOME": str(home)},
            )

            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
