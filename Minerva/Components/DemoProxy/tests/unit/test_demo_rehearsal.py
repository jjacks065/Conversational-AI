from __future__ import annotations

import json
import os
import signal
import shutil
import subprocess
import tempfile
import threading
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class _RawHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        body = b'raw-api-fallback-ok'
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@unittest.skipUnless(os.uname().sysname == "Darwin", "macOS native rehearsal")
class DemoRehearsalTests(unittest.TestCase):
    def test_enable_live_preflight_force_disable_and_raw_fallback(self) -> None:
        raw_server = ThreadingHTTPServer(("127.0.0.1", 0), _RawHandler)
        raw_thread = threading.Thread(target=raw_server.serve_forever, daemon=True)
        raw_thread.start()
        self.addCleanup(raw_server.shutdown)
        self.addCleanup(raw_server.server_close)

        raw_url = f"http://127.0.0.1:{raw_server.server_address[1]}/raw"
        with urllib.request.urlopen(raw_url, timeout=2) as response:
            self.assertEqual(response.read(), b"raw-api-fallback-ok")

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            home = temporary / "home"
            app = home / "Library" / "Application Support" / "DemoResponseProxy"
            for relative in (
                "proxy",
                "pac",
                "config",
                "scripts/common",
                "scripts/macos",
            ):
                shutil.copytree(PROJECT_ROOT / relative, app / relative)
            os.symlink(PROJECT_ROOT / ".venv", app / ".venv", target_is_directory=True)

            keychain = home / "Library" / "Keychains" / "login.keychain-db"
            keychain.parent.mkdir(parents=True)
            keychain.touch()
            fake_bin = temporary / "bin"
            fake_bin.mkdir()
            security_state = temporary / "trusted"
            security_log = temporary / "security.log"
            fake_security = fake_bin / "security"
            fake_security.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' \"$*\" >>\"${SECURITY_LOG}\"
case \"$1\" in
  add-trusted-cert) touch \"${SECURITY_STATE}\" ;;
  find-certificate)
    if [[ -f \"${SECURITY_STATE}\" && -f \"${CERT_FINGERPRINT_FILE}\" ]]; then
      printf 'SHA-256 hash: %s\\n' \"$(<\"${CERT_FINGERPRINT_FILE}\")\"
    fi
    ;;
  verify-cert) [[ -f \"${SECURITY_STATE}\" ]] ;;
  delete-certificate) rm -f \"${SECURITY_STATE}\" ;;
  *) exit 2 ;;
esac
""",
                encoding="utf-8",
            )
            fake_security.chmod(0o700)

            chrome_arguments = temporary / "chrome-arguments.txt"
            fake_chrome = temporary / "Google Chrome"
            fake_chrome.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' \"$@\" >\"${CHROME_ARGUMENTS}\"
trap 'exit 0' TERM INT
while :; do sleep 1; done
""",
                encoding="utf-8",
            )
            fake_chrome.chmod(0o700)
            environment = {
                **os.environ,
                "CERT_FINGERPRINT_FILE": str(app / "runtime/state/certificate.sha256"),
                "CHROME_ARGUMENTS": str(chrome_arguments),
                "DEMO_PROXY_CHROME_PATH": str(fake_chrome),
                "HOME": str(home),
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
                "SECURITY_LOG": str(security_log),
                "SECURITY_STATE": str(security_state),
            }
            enable = app / "scripts/macos/enable.sh"
            disable = app / "scripts/macos/disable.sh"
            uninstall_ca = app / "scripts/macos/uninstall-ca.sh"
            system_proxy_before = subprocess.run(
                ["scutil", "--proxy"], capture_output=True, check=False
            ).stdout

            chrome_pid: int | None = None
            chrome_snapshot = ""
            try:
                enable_result = subprocess.run(
                    ["bash", str(enable), "--app-dir", str(app)],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                    timeout=45,
                )
                proxy_log = home / "Library/Logs/DemoResponseProxy/proxy.stderr.log"
                diagnostics = proxy_log.read_text(errors="replace") if proxy_log.exists() else ""
                self.assertEqual(
                    enable_result.returncode,
                    0,
                    f"{enable_result.stderr}\nproxy log:\n{diagnostics}",
                )
                self.assertTrue(security_state.exists())
                self.assertTrue(chrome_arguments.is_file())
                arguments = chrome_arguments.read_text(encoding="utf-8").splitlines()
                self.assertIn(f"--user-data-dir={app / 'chrome-profile'}", arguments)
                self.assertIn(
                    "--proxy-pac-url=http://127.0.0.1:8765/demo-proxy.pac",
                    arguments,
                )
                chrome_pid = int((app / "runtime/state/chrome.pid").read_text())
                chrome_snapshot = subprocess.run(
                    ["ps", "-ww", "-p", str(chrome_pid), "-o", "comm=,command="],
                    capture_output=True,
                    text=True,
                    check=False,
                ).stdout
                chrome_state = "\n".join(
                    path.read_text(encoding="utf-8", errors="replace")
                    for path in (
                        app / "runtime/state/chrome.executable",
                        app / "runtime/state/chrome.markers",
                    )
                )
                chrome_identity = subprocess.run(
                    [
                        "bash",
                        "-c",
                        f'source "{app / "scripts/macos/common.sh"}"; '
                        f'demo_init_paths "{app}"; demo_process_status chrome',
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                )
                self.assertEqual(
                    chrome_identity.returncode,
                    0,
                    f"{chrome_identity.stderr}\nprocess:\n{chrome_snapshot}\nstate:\n{chrome_state}",
                )

                preflight_result = subprocess.run(
                    [
                        str(PROJECT_ROOT / ".venv/bin/python"),
                        str(PROJECT_ROOT / "scripts/common/hardening_check.py"),
                        "--project-root",
                        str(PROJECT_ROOT),
                        "--config",
                        str(app / "config/proxy.yaml"),
                        "--live",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                )
                self.assertEqual(preflight_result.returncode, 0, preflight_result.stdout)
                self.assertTrue(json.loads(preflight_result.stdout)["liveVerified"])

                disable_result = subprocess.run(
                    ["bash", str(disable), "--app-dir", str(app), "--force"],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=environment,
                    timeout=20,
                )
                self.assertEqual(
                    disable_result.returncode,
                    0,
                    f"{disable_result.stderr}\nchrome process:\n{chrome_snapshot}",
                )
                for state_name in ("proxy.pid", "chrome.pid"):
                    self.assertFalse((app / "runtime/state" / state_name).exists())
                with self.assertRaises(ProcessLookupError):
                    os.kill(chrome_pid, 0)
            finally:
                subprocess.run(
                    ["bash", str(disable), "--app-dir", str(app), "--force"],
                    capture_output=True,
                    check=False,
                    env=environment,
                    timeout=20,
                )
                if chrome_pid is not None:
                    try:
                        os.kill(chrome_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

            uninstall_result = subprocess.run(
                ["bash", str(uninstall_ca), "--app-dir", str(app)],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(uninstall_result.returncode, 0, uninstall_result.stderr)
            self.assertFalse(security_state.exists())
            self.assertEqual(
                system_proxy_before,
                subprocess.run(
                    ["scutil", "--proxy"], capture_output=True, check=False
                ).stdout,
            )
            with urllib.request.urlopen(raw_url, timeout=2) as response:
                self.assertEqual(response.read(), b"raw-api-fallback-ok")


if __name__ == "__main__":
    unittest.main()
