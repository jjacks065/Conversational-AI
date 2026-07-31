from __future__ import annotations

import shutil
import subprocess
import os
import tempfile
import time
import unittest
from pathlib import Path

from proxy.pac_server import PacServer, render_pac


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MACOS_LAUNCHER = PROJECT_ROOT / "scripts" / "macos" / "launch-chrome.sh"
WINDOWS_LAUNCHER = PROJECT_ROOT / "scripts" / "windows" / "launch-chrome.ps1"


class MacOSLauncherTests(unittest.TestCase):
    def test_shell_syntax_and_required_dedicated_profile_flags(self) -> None:
        result = subprocess.run(
            ["bash", "-n", str(MACOS_LAUNCHER)],
            capture_output=True,
            text=True,
            check=False,
        )
        content = MACOS_LAUNCHER.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("set -euo pipefail", content)
        self.assertIn("--user-data-dir=", content)
        self.assertIn("--proxy-pac-url=", content)
        self.assertIn("--no-first-run", content)
        self.assertIn("127.0.0.1:8765/demo-proxy.pac", content)
        self.assertIn("${HOME}/Applications/Google Chrome.app", content)
        self.assertNotIn("networksetup", content)
        self.assertNotIn("--proxy-server", content)

    def test_launcher_passes_isolated_profile_and_pac_arguments(self) -> None:
        pac_content = render_pac(
            PROJECT_ROOT / "pac" / "demo-proxy.pac",
            target_host="api.example.com",
            proxy_host="127.0.0.1",
            proxy_port=8080,
        )
        server = PacServer(pac_content, port=0)
        server.start()
        self.addCleanup(server.stop)
        host, port = server.address

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary = Path(temporary_directory)
            fake_chrome = temporary / "Google Chrome"
            argument_output = temporary / "arguments.txt"
            profile = temporary / "chrome-profile"
            fake_chrome.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$@" > "$ARG_OUTPUT"\n'
                "trap 'exit 0' TERM INT\nwhile :; do sleep 1; done\n",
                encoding="utf-8",
            )
            fake_chrome.chmod(0o755)
            environment = {
                **os.environ,
                "HOME": str(temporary),
                "ARG_OUTPUT": str(argument_output),
                "DEMO_PROXY_CHROME_PATH": str(fake_chrome),
                "DEMO_PROXY_CHROME_PROFILE": str(profile),
                "DEMO_PROXY_PAC_URL": f"http://{host}:{port}/demo-proxy.pac",
                "DEMO_PROXY_START_URL": "https://nexus.example.com/",
            }

            result = subprocess.run(
                ["bash", str(MACOS_LAUNCHER)],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            chrome_error = (
                temporary
                / "Library"
                / "Logs"
                / "DemoResponseProxy"
                / "chrome.stderr.log"
            )
            deadline = time.monotonic() + 2
            while not argument_output.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(
                argument_output.is_file(),
                f"stdout={result.stdout!r} stderr={result.stderr!r} "
                f"chrome_stderr={chrome_error.read_text() if chrome_error.exists() else 'missing'}",
            )
            arguments = argument_output.read_text(encoding="utf-8").splitlines()
            self.assertIn(f"--user-data-dir={profile}", arguments)
            self.assertIn(
                f"--proxy-pac-url=http://{host}:{port}/demo-proxy.pac", arguments
            )
            self.assertIn("--no-first-run", arguments)
            self.assertIn("https://nexus.example.com/", arguments)
            self.assertTrue(profile.is_dir())

            disable_result = subprocess.run(
                [
                    "bash",
                    str(PROJECT_ROOT / "scripts" / "macos" / "disable.sh"),
                    "--force",
                ],
                capture_output=True,
                text=True,
                check=False,
                env=environment,
            )
            self.assertEqual(disable_result.returncode, 0, disable_result.stderr)


class WindowsLauncherTests(unittest.TestCase):
    def test_required_paths_flags_and_no_system_proxy_mutation(self) -> None:
        content = WINDOWS_LAUNCHER.read_text(encoding="utf-8")

        self.assertIn("Set-StrictMode -Version Latest", content)
        self.assertIn("$env:ProgramFiles", content)
        self.assertIn("${env:ProgramFiles(x86)}", content)
        self.assertIn("$env:LOCALAPPDATA", content)
        self.assertIn("--user-data-dir=", content)
        self.assertIn('"--proxy-pac-url=$PacUrl"', content)
        self.assertIn("--no-first-run", content)
        self.assertIn("Start-Process", content)
        self.assertNotIn("Set-ItemProperty", content)
        self.assertNotIn("--proxy-server", content)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_parser_accepts_script(self) -> None:
        command = (
            "$errors=$null; "
            f"[void][System.Management.Automation.Language.Parser]::ParseFile('{WINDOWS_LAUNCHER}',"
            "[ref]$null,[ref]$errors); if($errors.Count){exit 1}"
        )
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
