# Demo Response Proxy Runbook

This runbook covers the approved Chrome-based Nexus demo. It does not authorize certificate-pinning bypass, native-application interception, system-wide proxy changes, or production use.

## 1. Approve and freeze the deployment rules

Review `config/proxy.yaml` before every demo. The approved configuration must retain:

- loopback listener `127.0.0.1:8080`;
- exact host `app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net`;
- `POST` and exact path `^/api/chatbot/ask$`;
- exact Nexus Origin marker;
- JSON request and response types;
- fail-open behavior and disabled body logging.

After an intentional approved change, regenerate the lock explicitly:

```text
.venv/bin/python scripts/common/freeze_config.py \
  --config config/proxy.yaml \
  --output config/demo-lock.json \
  --force
```

An unexplained preflight drift failure is a stop condition. Do not regenerate the lock merely to silence it.

## 2. Preflight

From the DemoProxy directory:

```text
.venv/bin/python scripts/common/hardening_check.py \
  --project-root . \
  --artifact dist/DemoResponseProxy-0.1.0-macos-arm64.tar.gz
```

Confirm the result is `"status":"passed"`. Verify the package checksum against `dist/SHA256SUMS.txt`. Packaged archives contain sanitized configuration; apply the approved deployment configuration and freeze it before installation.

Confirm Chrome is installed, ports `8080`, `8081`, and `8765` are available, and the normal browser is not configured to use DemoProxy.

## 3. Install

Development installation:

```text
macOS:   scripts/macos/install.sh --development
Windows: powershell -NoProfile -ExecutionPolicy Bypass -File scripts\windows\install.ps1 -DevelopmentMode
```

For an extracted native package, omit the development flag. Add `--install-launch-agent` on macOS or `-InstallStartupTask` on Windows only when automatic user-logon startup is required.

The CA must be generated locally. Trust only the recorded DemoProxy public CA in the current-user store or login keychain.

## 4. Enable and verify

```text
macOS:   "$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/enable.sh"
Windows: powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\enable.ps1"
```

Enable performs the frozen-rule preflight before starting. It then verifies configuration, proxy/PAC health, certificate trust, and launches only the dedicated Chrome profile.

Open the operator page at `http://127.0.0.1:8081/status`. Before presenting, confirm:

1. Proxy, PAC routing, certificate, and target rule show ready/active.
2. The browser profile directory is the dedicated DemoResponseProxy path.
3. The chatbot request remains an unchanged HTTPS `POST` to `/api/chatbot/ask`.
4. The matching JSON response renders transformed paragraph and horizontal-rule markup.
5. A non-target site remains direct.
6. Logs contain metadata only—never prompts, responses, authorization values, or cookies.

For a live command-line preflight in development mode:

```text
.venv/bin/python scripts/common/hardening_check.py --project-root . --live
```

For a native package, run:

```text
bin/mitmdump --demo-hardening-check . config/proxy.yaml config/demo-lock.json --live
```

## 5. Normal disable and raw fallback

```text
macOS:   "$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/disable.sh"
Windows: powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\disable.ps1"
```

Confirm the dedicated profile closes and ports `8080`, `8081`, and `8765` stop listening. Open Nexus through the normal browser path and confirm the unmodified/raw API experience is available. DemoProxy never changes normal-browser or system proxy settings.

## 6. Emergency rollback

Rollback does not depend on proxy health:

```text
macOS:   "$HOME/Library/Application Support/DemoResponseProxy/scripts/macos/disable.sh" --force
Windows: powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\DemoResponseProxy\scripts\windows\disable.ps1" -Force
```

If trust must also be removed, run the platform `uninstall-ca` script. These scripts remove only the recorded fingerprint/thumbprint and refuse to terminate a PID whose executable and command line cannot be verified.

## 7. Stop conditions

Do not proceed when:

- frozen rules do not match configuration;
- any listener is reachable through a non-loopback address;
- certificate trust cannot be verified;
- the client is a native application or rejects the local CA because of pinning;
- a package checksum or per-file manifest fails;
- payload or credential data appears in logs;
- emergency rollback does not restore direct browsing.

Certificate pinning is unsupported. Prefer a configurable local reverse-proxy endpoint when the client cannot use the per-machine CA through the dedicated Chrome profile.
