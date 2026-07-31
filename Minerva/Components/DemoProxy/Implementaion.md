
# Cross-Platform Local Response-Transformation Proxy

## 1. Objective

Build a local proxy that runs on both Windows and macOS and:

1. Routes only the designated API hostname through the proxy whenever possible.
2. Passes requests to the original API without modifying them.
3. Transforms only responses matching strict host, method, path, header, and content-type rules.
4. Leaves all other traffic direct and untouched.
5. Supports ordinary JSON responses and, when required, Server-Sent Events or WebSockets.
6. Fails open by returning the original response when transformation fails.
7. Provides platform-specific installation, certificate, startup, and rollback scripts.
8. Uses the same proxy code, configuration, tests, and transformation logic on both platforms.

The setup is intended as a local prototype of a planned presentation layer.

---

# 2. Recommended Technology

Use:

```text
mitmdump
+ Python addon
+ YAML configuration
+ Proxy Auto-Configuration file
+ dedicated Chrome demo profile
```

The Python implementation must be platform-independent.

Platform differences should be isolated to:

* Installation scripts.
* Certificate-store management.
* Proxy configuration.
* Automatic startup.
* Process management.
* Application paths.

---

# 3. Architecture

```text
┌──────────────────────────────┐
│ Dedicated Chrome demo profile│
└──────────────┬───────────────┘
               │
               │ PAC routing
               ▼
┌──────────────────────────────┐
│ Target API hostname          │──────► 127.0.0.1:8080
│ All other hostnames          │──────► DIRECT
└──────────────────────────────┘

Target flow:

Browser
   ↓
Local mitmdump proxy
   ↓
Original API
   ↓
Response transformer
   ↓
Browser
```

The request must be forwarded unchanged.

Only the matching server response is eligible for transformation.

---

# 4. Routing Strategy

Use a PAC file so only the target API host is sent through the proxy.

Example:

```javascript
function FindProxyForURL(url, host) {
    if (dnsDomainIs(host, "api.demo.example.com")) {
        return "PROXY 127.0.0.1:8080";
    }

    return "DIRECT";
}
```

This approach works on both Windows and macOS.

Benefits:

* Unrelated traffic never enters the proxy.
* Authentication traffic to other domains remains direct.
* Certificate interception is limited to the target host.
* Browser performance impact is minimal.
* Rollback is straightforward.

Avoid sending all system traffic through the proxy unless the calling application cannot use selective routing.

---

# 5. Repository Layout

```text
demo-response-proxy/
├── README.md
├── pyproject.toml
├── requirements.txt
├── config/
│   ├── proxy.example.yaml
│   └── proxy.yaml
├── proxy/
│   ├── __init__.py
│   ├── addon.py
│   ├── config.py
│   ├── matcher.py
│   ├── transformer.py
│   ├── sse.py
│   ├── websocket.py
│   ├── health.py
│   └── logging_config.py
├── pac/
│   └── demo-proxy.pac
├── scripts/
│   ├── common/
│   │   ├── verify_config.py
│   │   └── smoke_test.py
│   ├── windows/
│   │   ├── install.ps1
│   │   ├── start.ps1
│   │   ├── stop.ps1
│   │   ├── enable.ps1
│   │   ├── disable.ps1
│   │   ├── install-ca.ps1
│   │   ├── uninstall-ca.ps1
│   │   ├── verify.ps1
│   │   └── uninstall.ps1
│   └── macos/
│       ├── install.sh
│       ├── start.sh
│       ├── stop.sh
│       ├── enable.sh
│       ├── disable.sh
│       ├── install-ca.sh
│       ├── uninstall-ca.sh
│       ├── verify.sh
│       └── uninstall.sh
├── startup/
│   ├── windows/
│   │   └── scheduled-task.xml
│   └── macos/
│       └── com.example.demo-response-proxy.plist
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── runtime/
    ├── logs/
    └── state/
```

No operating-system logic should exist inside `proxy/`.

---

# 6. Shared Configuration

Example `proxy.yaml`:

```yaml
proxy:
  listen_host: "127.0.0.1"
  listen_port: 8080
  fail_open: true
  max_buffer_bytes: 10485760

target:
  scheme: "https"
  host: "api.demo.example.com"
  port: 443
  methods:
    - "POST"
  paths:
    - "^/v1/chat/completions$"
  request_content_types:
    - "application/json"
  response_content_types:
    - "application/json"
    - "text/event-stream"

matching:
  required_request_headers:
    x-demo-client: "^future-ui-demo$"

transformation:
  enabled: true
  mode: "deterministic"
  preserve_unknown_fields: true
  transformer_version: "1.0.0"

logging:
  level: "INFO"
  log_request_bodies: false
  log_response_bodies: false
  log_match_decisions: true
  redact_headers:
    - "authorization"
    - "cookie"
    - "set-cookie"
    - "x-api-key"

platform:
  browser_profile_name: "DemoProxyProfile"
  health_port: 8081
```

The same file should work on Windows and macOS.

Path handling must use Python path abstractions rather than hard-coded path separators.

---

# 7. Response Matching

A response should be transformed only when all configured conditions match:

```text
Hostname       Exact match
Port           Exact match
HTTP method    Allowlisted
Request path   Full regular-expression match
Request type   Allowlisted
Response type  Allowlisted
Marker header  Present and valid
Direction      Server to client
```

Use a demo-specific request marker where possible:

```http
X-Demo-Client: future-ui-demo
```

The matching layer must be independently unit tested.

---

# 8. Shared Transformation Engine

Implement the transformation as a deterministic pure function:

```python
def transform_payload(payload: dict) -> dict:
    ...
```

Requirements:

* No platform-dependent behavior.
* No secondary API or model call.
* No network access.
* No modification of the original request.
* No invention of factual content.
* No modification of tool-call arguments.
* No modification of authentication, usage, or billing fields.
* Preserve unknown response fields.
* Produce valid output for the original client.
* Be idempotent.

Example property:

```python
transform_payload(transform_payload(payload)) == transform_payload(payload)
```

The transformer may:

* Normalize whitespace.
* Improve heading structure.
* Remove known repeated boilerplate.
* Convert known references into display-friendly structures.
* Add namespaced presentation metadata.
* Normalize markdown presentation.

---

# 9. HTTP Response Modes

## Buffered JSON

For `application/json` responses:

1. Store the original raw response.
2. Decode using mitmproxy’s response API.
3. Parse JSON.
4. Validate the expected schema.
5. Transform the selected fields.
6. Serialize the response.
7. Remove or recalculate stale length and encoding headers.
8. Return the transformed response.
9. Restore the original response on any exception.

## Server-Sent Events

For `text/event-stream`:

* Parse complete SSE event records.
* Do not transform arbitrary transport chunks.
* Preserve comments, IDs, event names, retry fields, and terminal markers.
* Handle both LF and CRLF boundaries.
* Preserve incomplete data until a full event arrives.
* Leave malformed events unchanged.
* Avoid transformations requiring full-response context unless buffering is intentional.

## WebSockets

For WebSocket traffic:

* Match the original handshake host and path.
* Modify only server-to-client text messages.
* Leave client messages untouched.
* Leave binary frames untouched.
* Preserve ordering and close behavior.
* Return malformed or unknown messages unchanged.

Streaming support should be implemented only after confirming which protocol the actual application uses.

---

# 10. TLS Certificate Model

Each machine should generate its own local mitmproxy Certificate Authority.

Do not distribute one shared CA private key between machines.

Common requirements:

* Generate the CA locally.
* Install only the public certificate into the appropriate trust store.
* Record the certificate thumbprint or fingerprint.
* Remove the exact certificate during uninstall.
* Never commit CA files.
* Never copy CA private keys into deployment packages.

## Windows

Install into:

```text
Current User Trusted Root Certification Authorities
```

Use the machine-wide store only when required.

PowerShell example:

```powershell
Import-Certificate `
    -FilePath $CertPath `
    -CertStoreLocation "Cert:\CurrentUser\Root"
```

## macOS

Install into the current user’s login keychain where possible.

Illustrative command:

```bash
security add-trusted-cert \
  -d \
  -r trustRoot \
  -k "$HOME/Library/Keychains/login.keychain-db" \
  "$CERT_PATH"
```

Machine-wide installation into the System keychain may require administrator privileges.

The macOS script must verify that the certificate is trusted after installation.

---

# 11. Browser Setup

Use a dedicated Chrome profile on both platforms.

Benefits:

* Does not disturb the presenter’s normal browser profile.
* Avoids extensions, cookies, and policies from unrelated profiles.
* Keeps demo proxy settings isolated.
* Makes cleanup easier.

## Windows Chrome path discovery

Check common locations:

```text
%ProgramFiles%\Google\Chrome\Application\chrome.exe
%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe
%LocalAppData%\Google\Chrome\Application\chrome.exe
```

## macOS Chrome path

Default:

```text
/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

Also support user-local application installations when present.

## Chrome launch model

Launch with:

```text
--user-data-dir=<dedicated-profile-directory>
--proxy-pac-url=http://127.0.0.1:8765/demo-proxy.pac
--no-first-run
```

Serve the PAC file from a local loopback-only HTTP server rather than relying on a `file:` PAC URL.

The local PAC server should:

* Bind to `127.0.0.1`.
* Serve only the PAC file.
* Require no external dependencies beyond the packaged runtime.
* Start and stop with the proxy.

---

# 12. Installation Paths

Use platform-appropriate defaults.

## Windows

Application:

```text
%LOCALAPPDATA%\DemoResponseProxy
```

Configuration:

```text
%LOCALAPPDATA%\DemoResponseProxy\config
```

Logs:

```text
%LOCALAPPDATA%\DemoResponseProxy\logs
```

Chrome profile:

```text
%LOCALAPPDATA%\DemoResponseProxy\chrome-profile
```

## macOS

Application:

```text
~/Library/Application Support/DemoResponseProxy
```

Configuration:

```text
~/Library/Application Support/DemoResponseProxy/config
```

Logs:

```text
~/Library/Logs/DemoResponseProxy
```

Chrome profile:

```text
~/Library/Application Support/DemoResponseProxy/chrome-profile
```

The core Python code should resolve these paths through a platform abstraction module or environment variables.

---

# 13. Dependency Installation

Support two deployment modes.

## Preferred: self-contained packaged runtime

Package the proxy as a standalone application for each platform so the user does not need to install Python manually.

Possible outputs:

```text
DemoResponseProxy-Windows-x64.zip
DemoResponseProxy-macOS-arm64.tar.gz
DemoResponseProxy-macOS-x64.tar.gz
```

The package should include:

* Proxy executable or embedded Python runtime.
* Required Python dependencies.
* Addon code.
* Configuration template.
* Platform scripts.
* PAC server.
* Verification utility.

## Development mode

Allow developers to use:

```text
Python virtual environment
+ pip-installed dependencies
```

Development setup should not be the primary installation method for demo operators.

---

# 14. Platform-Specific Installation

## Windows `install.ps1`

Responsibilities:

1. Enable strict PowerShell behavior.
2. Detect Windows architecture.
3. Verify required permissions.
4. Copy files to the application directory.
5. Create config, logs, runtime, and profile directories.
6. Start mitmproxy once to generate the local CA.
7. Install the CA in the selected Windows certificate store.
8. Record the certificate thumbprint.
9. Install the startup task when requested.
10. Run configuration validation.
11. Start the proxy.
12. Run smoke tests.
13. Print rollback instructions.

The script must be idempotent.

## macOS `install.sh`

Responsibilities:

1. Use strict shell behavior:

```bash
set -euo pipefail
```

2. Detect Intel versus Apple Silicon.
3. Copy the correct packaged runtime.
4. Create Application Support, Logs, and profile directories.
5. Start mitmproxy once to generate the local CA.
6. Install and trust the certificate in the chosen keychain.
7. Record the certificate fingerprint.
8. Install a LaunchAgent when requested.
9. Validate configuration.
10. Start the proxy.
11. Run smoke tests.
12. Print rollback instructions.

The script must be idempotent.

---

# 15. Process Management

Use shared state files where practical:

```text
proxy.pid
pac-server.pid
proxy.status.json
previous-settings.json
```

Do not assume that a PID still belongs to the proxy. Verify the process executable and command line before terminating it.

## Windows

Manual mode:

```text
start.ps1
stop.ps1
```

Automatic mode:

```text
Windows Scheduled Task at user logon
```

## macOS

Manual mode:

```text
start.sh
stop.sh
```

Automatic mode:

```text
LaunchAgent in ~/Library/LaunchAgents
```

Use a per-user LaunchAgent rather than a system LaunchDaemon unless machine-wide execution is necessary.

---

# 16. Enable and Disable Workflow

The operator experience should be equivalent on both platforms.

## Enable

```text
1. Validate configuration.
2. Start proxy.
3. Start PAC server.
4. Confirm health endpoint.
5. Confirm certificate trust.
6. Launch dedicated Chrome profile.
7. Verify target routing.
8. Show operator status.
```

Commands:

```text
Windows: scripts\windows\enable.ps1
macOS:   scripts/macos/enable.sh
```

## Disable

```text
1. Close dedicated Chrome profile.
2. Stop PAC server.
3. Stop proxy.
4. Verify processes are stopped.
5. Confirm normal direct browsing.
```

Commands:

```text
Windows: scripts\windows\disable.ps1
macOS:   scripts/macos/disable.sh
```

Since the proxy is launched only through the dedicated Chrome profile, normal browser and system proxy settings should not require modification.

---

# 17. Emergency Rollback

Rollback must not depend on the proxy being healthy.

Provide one command per platform:

```text
Windows: scripts\windows\disable.ps1 -Force
macOS:   scripts/macos/disable.sh --force
```

Emergency rollback should:

* Terminate the dedicated Chrome profile.
* Stop the proxy process.
* Stop the PAC server.
* Remove stale PID files.
* Leave the normal browser configuration untouched.
* Confirm the proxy port is no longer listening.

A second command should remove certificate trust if necessary:

```text
Windows: uninstall-ca.ps1
macOS:   uninstall-ca.sh
```

---

# 18. Health and Operator Status

Expose a local-only health endpoint:

```text
http://127.0.0.1:8081/health
```

Example response:

```json
{
  "status": "ok",
  "platform": "macos-arm64",
  "proxyListening": true,
  "pacServerListening": true,
  "configurationLoaded": true,
  "certificateTrusted": true,
  "targetHost": "api.demo.example.com",
  "transformerVersion": "1.0.0"
}
```

Provide a small local operator page:

```text
http://127.0.0.1:8081/status
```

It should display:

```text
Proxy: Active
PAC routing: Active
Certificate: Trusted
Target rule: Ready
Last matching request: 14:32:11
Last transformation: Successful
Fail-open mode: Enabled
```

The status page must not display prompts, response text, tokens, cookies, or credentials.

---

# 19. Logging

Use the same structured logging format on both systems.

Log metadata only:

* Timestamp.
* Platform.
* Proxy version.
* Request correlation ID.
* Match result.
* Method.
* Host.
* Path template.
* Status code.
* Content type.
* Transformation duration.
* Original and transformed byte counts.
* Fail-open status.
* Exception category.

Do not log:

* Authorization headers.
* Cookies.
* API keys.
* Request bodies.
* Response bodies.
* User-entered chat content.

Use platform-specific log directories but identical log schemas.

---

# 20. Testing Matrix

The shared test suite must run on:

```text
Windows x64
macOS Apple Silicon
macOS Intel, when supported by the deployment environment
```

## Unit tests

Test:

* Exact host matching.
* Similar host rejection.
* Path matching.
* Query-string handling.
* Method filtering.
* Marker-header filtering.
* JSON transformation.
* Idempotence.
* Unicode.
* Invalid schemas.
* Fail-open restoration.
* Header preservation.
* Log redaction.
* Cross-platform path handling.

## Integration tests

Test:

* Ordinary JSON.
* Gzip and uncompressed content.
* SSE chunk boundaries.
* WebSocket text messages.
* 401, 429, and 500 responses.
* Connection interruption.
* Proxy restart.
* PAC routing.
* Certificate trust.
* Dedicated Chrome launch.
* Emergency disable.
* Uninstall.

## Platform installation tests

Windows:

* Clean user profile.
* Existing installation.
* Nonadministrator installation.
* Administrator certificate installation.
* Scheduled Task start and removal.

macOS:

* Apple Silicon.
* Intel when required.
* Login keychain installation.
* System keychain installation when required.
* LaunchAgent start and removal.
* Gatekeeper and executable permission handling.

---

# 21. Continuous Integration

Configure CI to run shared tests on:

```text
windows-latest
macos-latest
```

CI should validate:

* Python formatting and linting.
* Type checking.
* Unit tests.
* Fixture transformations.
* Package creation.
* Platform scripts where feasible.
* Absence of private keys and certificate files.
* Absence of committed secrets.
* Configuration-schema validity.

Produce separate signed or checksummed artifacts for each supported architecture.

---

# 22. Packaging

Recommended release artifacts:

```text
DemoResponseProxy-1.0.0-windows-x64.zip
DemoResponseProxy-1.0.0-macos-arm64.tar.gz
DemoResponseProxy-1.0.0-macos-x64.tar.gz
SHA256SUMS.txt
```

Each package should contain:

```text
bin/
config/
proxy/
pac/
scripts/
README.md
VERSION
LICENSES/
```

Do not package:

* Generated CA files.
* Local configuration containing real hostnames when those are sensitive.
* Logs.
* Browser profile contents.
* Captured API payloads.
* Credentials.

---

# 23. macOS Code-Signing Considerations

For internal development, unsigned scripts and binaries may be acceptable, but operators may encounter Gatekeeper warnings.

For repeatable distribution:

* Sign packaged executables with an appropriate Apple Developer certificate.
* Notarize the final macOS package when organizational policy requires it.
* Preserve executable permissions in the archive.
* Avoid asking operators to disable Gatekeeper globally.

These packaging concerns must not affect the shared Python implementation.

---

# 24. Certificate-Pinning Boundary

Do not attempt to bypass certificate pinning.

If the calling client rejects the local CA:

1. Determine whether the traffic originates from Chrome or a native application.
2. Prefer changing the demo application’s API base URL.
3. Use a local reverse proxy instead of a forward proxy.
4. Limit interception to an application explicitly configured to trust the development endpoint.

The project should document certificate pinning as an unsupported boundary.

---

# 25. Preferred Alternative: Local Reverse Proxy

When the application can use a configurable API base URL, prefer:

```text
Demo application
    ↓
https://localhost:<port>
    ↓
Local reverse proxy
    ↓
Original API
```

This approach is naturally portable across Windows and macOS and avoids browser-wide TLS interception.

Use the forward proxy and PAC design only when the existing application cannot point to a local API gateway.

---

# 26. Acceptance Criteria

The cross-platform implementation is complete when:

1. Shared proxy code runs unchanged on Windows and macOS.
2. Platform logic exists only in installation and integration layers.
3. Both platforms route only the target hostname through the proxy.
4. Non-target traffic remains direct.
5. Requests reach the original API unchanged.
6. Only strictly matching responses are transformed.
7. JSON transformation works on both platforms.
8. Streaming works when required.
9. Transformation failures return the original response.
10. Certificates are generated separately on each machine.
11. Certificate install and removal work on each platform.
12. Dedicated Chrome profiles launch correctly.
13. Enable and disable require one command on each platform.
14. Automatic startup works through Scheduled Tasks and LaunchAgents.
15. Uninstall removes files, startup entries, certificates, and runtime state.
16. Logs contain no prompts, responses, cookies, or credentials.
17. CI passes on Windows and macOS.
18. Platform packages are checksummed and reproducible.
19. Emergency rollback works without a functioning proxy.
20. The demo can continue with raw API output after rollback.

---

# 27. Codex Implementation Order

## Phase 1: Protocol discovery

Confirm:

* Target hostname.
* Endpoint.
* Method.
* Request marker.
* Response schema.
* Response content type.
* JSON, SSE, or WebSocket behavior.
* Compression.
* HTTP version.
* Chrome versus native client.
* Certificate-pinning behavior.

## Phase 2: Shared transformer

Implement the pure transformation functions against sanitized fixtures.

## Phase 3: Shared proxy addon

Implement:

* Configuration loading.
* Strict matching.
* JSON response transformation.
* Fail-open behavior.
* Structured logging.
* Health reporting.

## Phase 4: Streaming support

Implement SSE or WebSocket handling only if required by the captured protocol.

## Phase 5: PAC and Chrome launcher

Implement the loopback PAC server and dedicated profile launcher for both operating systems.

## Phase 6: Windows integration

Implement:

* PowerShell installation.
* Certificate management.
* Process management.
* Scheduled Task.
* Verification.
* Uninstall.

## Phase 7: macOS integration

Implement:

* Shell installation.
* Keychain management.
* Process management.
* LaunchAgent.
* Architecture detection.
* Verification.
* Uninstall.

## Phase 8: Packaging and CI

Create platform-specific artifacts, checksums, and automated tests.

## Phase 9: Demo hardening

* Disable payload logging.
* Freeze target matching rules.
* Verify loopback-only listeners.
* Rehearse enable, disable, and rollback.
* Test with the actual demo browser profile.
* Confirm the raw API experience remains available as fallback.

---

# 28. Final Technical Direction

Codex should implement:

```text
One shared Python proxy and transformer
+ one shared YAML configuration format
+ one shared PAC file
+ one shared test suite
+ Windows PowerShell integration
+ macOS shell integration
+ Windows Scheduled Task support
+ macOS LaunchAgent support
+ per-machine local CA generation
+ dedicated Chrome profiles
+ deterministic fail-open transformation
```

The core proxy must remain entirely platform-neutral. Windows and macOS differences should be treated as adapters around the same local service, not as separate implementations.
