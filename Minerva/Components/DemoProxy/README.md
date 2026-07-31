# Demo Response Proxy

DemoProxy is a platform-neutral mitmproxy addon that selectively transforms the confirmed Nexus chatbot JSON response. It includes strict configuration validation, request/response matching, buffered JSON transformation, exact fail-open restoration, metadata-only logging, loopback health reporting, exact-host PAC routing, and dedicated Chrome launchers.

## Development setup

```text
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

On Windows, invoke the environment's executables from `.venv\Scripts` instead.

## Validate configuration and tests

```text
.venv/bin/python scripts/common/verify_config.py config/proxy.yaml
.venv/bin/python -m unittest discover -s tests -v
```

## Run the proxy and PAC server

From this directory:

```text
.venv/bin/mitmdump \
  --set confdir=runtime/mitmproxy \
  --set demo_proxy_config=config/proxy.yaml \
  --listen-host 127.0.0.1 \
  --listen-port 8080 \
  -s proxy/addon.py
```

The built-in mitmdump listener arguments are mandatory: mitmdump creates its socket before addon configuration can safely alter it. Platform start scripts must derive these arguments from the validated YAML. The addon starts the PAC server with the proxy and exposes these loopback-only endpoints:

```text
http://127.0.0.1:8081/health
http://127.0.0.1:8081/status
http://127.0.0.1:8765/demo-proxy.pac
```

## Launch the dedicated Chrome profile

Start the proxy first, then invoke the platform launcher:

```text
macOS:   scripts/macos/launch-chrome.sh
Windows: powershell -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\launch-chrome.ps1"
```

The launchers verify the PAC endpoint, create only the dedicated DemoResponseProxy profile, and pass `--proxy-pac-url` to that Chrome process. They do not alter system proxy settings or the normal Chrome profile.

## Windows installation and operation

Run these commands from a 64-bit Windows PowerShell session. Development mode creates a private virtual environment beneath `%LOCALAPPDATA%\DemoResponseProxy`; the packaged mode introduced in Phase 8 will use `bin\mitmdump.exe` instead.

```text
# Install from this source tree, trust the per-machine CA for the current user,
# start the proxy, and optionally register a current-user logon task.
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\windows\install.ps1 -DevelopmentMode
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\windows\install.ps1 -DevelopmentMode -InstallStartupTask

# Operator workflow (run the installed scripts).
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\enable.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\disable.ps1"

# Emergency rollback does not require a healthy proxy.
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\disable.ps1" -Force

# Remove only the recorded current-user CA and the exact application directory.
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\uninstall.ps1" -Force
```

The installation uses `%LOCALAPPDATA%\DemoResponseProxy` exclusively, binds all service ports to `127.0.0.1`, and stores its CA thumbprint and process identity under `runtime\state`. Stop and rollback operations verify both executable path and command-line markers before terminating a recorded PID. The scripts never change Windows or normal-browser proxy settings, and certificate operations are restricted to `Cert:\CurrentUser\Root`.

## macOS installation and operation

Run from Terminal on either Apple Silicon or Intel macOS. Development mode creates a private virtual environment under `~/Library/Application Support/DemoResponseProxy`; Phase 8 packages will provide the self-contained `bin/mitmdump` runtime.

```text
# Install, trust the locally generated CA in the login keychain, and start.
scripts/macos/install.sh --development

# Optionally install a per-user LaunchAgent at login.
scripts/macos/install.sh --development --install-launch-agent

# Operator workflow.
"$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/enable.sh"
"$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/disable.sh"

# Emergency rollback and exact uninstall.
"$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/disable.sh" --force
"$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/uninstall.sh" --force
```

The CA is generated locally and only its public certificate is added to the current user’s login keychain; macOS may request keychain confirmation. The recorded SHA-256 fingerprint is used for exact removal. Process termination verifies the executable and command line before signaling a PID. No system proxy settings, System keychain, LaunchDaemon, or normal Chrome profile are modified.

## Native release packaging

Install the pinned build dependency into the development environment, then run the release build on each native target host:

```text
.venv/bin/python -m pip install -r requirements-build.txt
.venv/bin/python -m release_tools.build_release
```

On Windows, use `.venv\Scripts\python.exe` for the same commands. PyInstaller does not cross-compile, so the command must run separately on Windows x64, macOS arm64, and macOS x64. It produces the matching artifact under `dist/` and refreshes `dist/SHA256SUMS.txt`. No CI or GitHub workflow is required.

Archives are assembled from an explicit allowlist, use deterministic timestamps and permissions, contain a per-file `MANIFEST.json`, and preserve executable modes. They exclude the development environment, tests, logs, browser data, captured payloads, active configuration, and certificate/private-key material. The packaged `config/proxy.yaml` is the sanitized example: configure the extracted package for the approved demo target before running its installer.

The current packages are unsigned internal-development artifacts. Apply organizational Apple signing/notarization or Windows code-signing requirements before broader distribution; do not disable Gatekeeper globally.

## Demo hardening and rehearsal

The approved deployment rules are frozen in `config/demo-lock.json`. Both platform enable commands reject configuration drift before startup. Run the offline preflight with:

```text
.venv/bin/python scripts/common/hardening_check.py --project-root .
```

Add `--live` after enable to verify all three listeners are reachable only through loopback, health is demo-ready, and the PAC retains its exact-host route with direct fallback. See `DEMO_RUNBOOK.md` for installation, field verification, raw-response fallback, emergency rollback, and certificate-pinning stop conditions.

## Transformation boundary

Only responses matching every configured scheme, host, port, method, path, request type, response type, and marker-header rule are eligible. Requests are never changed. Any decoding, size, schema, JSON, serialization, or transformation error restores the exact original response body and headers when fail-open mode is enabled.

Logs and status endpoints contain metadata only. Request bodies, response bodies, authorization values, cookies, API keys, and user-entered content are excluded.
