from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WINDOWS_SCRIPTS = PROJECT_ROOT / "scripts" / "windows"
STARTUP_TASK = PROJECT_ROOT / "startup" / "windows" / "scheduled-task.xml"

REQUIRED_SCRIPTS = (
    "Common.ps1",
    "install.ps1",
    "start.ps1",
    "stop.ps1",
    "enable.ps1",
    "disable.ps1",
    "install-ca.ps1",
    "uninstall-ca.ps1",
    "verify.ps1",
    "uninstall.ps1",
    "launch-chrome.ps1",
)


def read_script(name: str) -> str:
    return (WINDOWS_SCRIPTS / name).read_text(encoding="utf-8")


class WindowsIntegrationContractTests(unittest.TestCase):
    def test_all_phase_six_scripts_use_strict_error_handling(self) -> None:
        for name in REQUIRED_SCRIPTS:
            with self.subTest(script=name):
                content = read_script(name)
                self.assertIn("Set-StrictMode -Version Latest", content)
                self.assertIn('$ErrorActionPreference = "Stop"', content)

    def test_common_paths_are_per_user_and_process_stops_verify_identity(self) -> None:
        content = read_script("Common.ps1")

        self.assertIn('$env:LOCALAPPDATA', content)
        self.assertIn('"DemoResponseProxy"', content)
        self.assertIn('function Test-DemoTrackedProcess', content)
        self.assertIn('Win32_Process', content)
        self.assertIn('ExecutablePath', content)
        self.assertIn('CommandLine', content)
        self.assertIn('commandLineMarkers', content)
        self.assertIn('function Stop-DemoTrackedProcess', content)
        self.assertIn('Stop-Process', content)

        for name in REQUIRED_SCRIPTS:
            if name != "Common.ps1":
                self.assertNotIn("Stop-Process", read_script(name), name)

    def test_start_is_loopback_only_and_records_runtime_identity(self) -> None:
        content = read_script("start.ps1")

        self.assertIn('"--listen-host"', content)
        self.assertIn('"127.0.0.1"', content)
        self.assertIn('"--listen-port"', content)
        self.assertIn('"--set"', content)
        self.assertIn('"flow_detail=0"', content)
        self.assertIn('"demo_proxy_config=', content)
        self.assertIn('"confdir=$($Paths.MitmConf)"', content)
        self.assertIn('RedirectStandardOutput', content)
        self.assertIn('RedirectStandardError', content)
        self.assertIn('commandLineMarkers', content)
        self.assertIn('Write-DemoJsonState', content)

    def test_stop_delegates_to_verified_process_helper(self) -> None:
        content = read_script("stop.ps1")

        self.assertIn('Stop-DemoTrackedProcess', content)
        self.assertIn('-ExpectedKind "proxy"', content)
        self.assertIn('-Force:$Force', content)

    def test_certificate_scripts_use_only_current_user_root_and_exact_thumbprint(self) -> None:
        install_content = read_script("install-ca.ps1")
        uninstall_content = read_script("uninstall-ca.ps1")
        combined = install_content + uninstall_content

        self.assertIn('Import-Certificate', install_content)
        self.assertIn('Cert:\\CurrentUser\\Root', install_content)
        self.assertIn('thumbprint', install_content)
        self.assertIn('Write-DemoJsonState', install_content)
        self.assertIn('thumbprint', uninstall_content)
        self.assertIn('Cert:\\CurrentUser\\Root', uninstall_content)
        self.assertIn('Remove-Item -LiteralPath', uninstall_content)
        self.assertNotIn('LocalMachine', combined)

    def test_enable_and_force_disable_cover_operator_and_emergency_workflows(self) -> None:
        enable_content = read_script("enable.ps1")
        disable_content = read_script("disable.ps1")

        for expected in (
            "verify.ps1",
            "start.ps1",
            "install-ca.ps1",
            "launch-chrome.ps1",
        ):
            self.assertIn(expected, enable_content)
        self.assertIn('Stop-DemoTrackedProcess', disable_content)
        self.assertIn('-ExpectedKind "chrome"', disable_content)
        self.assertIn('stop.ps1', disable_content)
        self.assertIn('[switch]$Force', disable_content)
        self.assertNotIn('Set-ItemProperty', disable_content)
        self.assertNotIn('Internet Settings', disable_content)
        self.assertNotIn('netsh', disable_content)

    def test_install_covers_architecture_local_ca_startup_validation_and_smoke_test(self) -> None:
        content = read_script("install.ps1")

        self.assertIn('PROCESSOR_ARCHITECTURE', content)
        self.assertIn('Copy-Item', content)
        self.assertIn('mitmdump', content)
        self.assertIn('install-ca.ps1', content)
        self.assertIn('Register-ScheduledTask', content)
        self.assertIn('verify.ps1', content)
        self.assertIn('start.ps1', content)
        self.assertIn('Rollback', content)
        self.assertIn('[switch]$InstallStartupTask', content)
        self.assertIn('[switch]$DevelopmentMode', content)

    def test_verification_checks_config_health_pac_certificate_and_ports(self) -> None:
        content = read_script("verify.ps1")

        self.assertIn('Test-DemoConfig', content)
        self.assertIn('/health', content)
        self.assertIn('/demo-proxy.pac', content)
        self.assertIn('Test-DemoCertificateTrust', content)
        self.assertIn('Test-DemoPortOpen', content)

    def test_uninstall_is_scoped_to_exact_app_directory(self) -> None:
        content = read_script("uninstall.ps1")

        self.assertIn('Assert-DemoInstallRoot', content)
        self.assertIn('disable.ps1', content)
        self.assertIn('uninstall-ca.ps1', content)
        self.assertIn('Unregister-ScheduledTask', content)
        self.assertIn('Remove-Item -LiteralPath $Paths.Root -Recurse -Force', content)
        self.assertNotIn('Remove-Item $env:LOCALAPPDATA', content)

    def test_scheduled_task_is_current_user_logon_and_least_privilege(self) -> None:
        content = STARTUP_TASK.read_text(encoding="utf-8")

        self.assertIn('<LogonTrigger>', content)
        self.assertIn('__DEMO_PROXY_USER__', content)
        self.assertIn('__DEMO_PROXY_START_SCRIPT__', content)
        self.assertIn('<RunLevel>LeastPrivilege</RunLevel>', content)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_parser_accepts_all_scripts(self) -> None:
        quoted_paths = ",".join(
            "'" + str(WINDOWS_SCRIPTS / name).replace("'", "''") + "'"
            for name in REQUIRED_SCRIPTS
        )
        command = (
            f"$files=@({quoted_paths}); foreach($file in $files){{"
            "$tokens=$null; $errors=$null; "
            "[void][System.Management.Automation.Language.Parser]::ParseFile("
            "$file,[ref]$tokens,[ref]$errors); if($errors.Count){"
            "$errors | Out-String | Write-Error; exit 1}}}"
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
