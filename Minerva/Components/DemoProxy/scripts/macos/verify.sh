#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

app_dir=""
configuration_only="false"
while (($#)); do
    case "$1" in
        --app-dir) app_dir="$2"; shift 2 ;;
        --configuration-only) configuration_only="true"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
demo_init_paths "${app_dir}"
demo_assert_install_root
read -r listen_port health_port pac_port <<<"$(demo_validate_config)"
echo "Configuration: valid and loopback-only."
if [[ "${configuration_only}" == "true" ]]; then
    exit 0
fi

if ! demo_process_status proxy; then
    echo "Proxy process identity verification failed." >&2
    exit 1
fi
if ! demo_port_open "${listen_port}"; then
    echo "Proxy port is not listening on 127.0.0.1:${listen_port}." >&2
    exit 1
fi
health="$(demo_wait_url "http://127.0.0.1:${health_port}/health" 5)"
for required in '"status":"ok"' '"proxyListening":true' '"pacServerListening":true' '"certificateTrusted":true'; do
    if [[ "${health}" != *"${required}"* ]]; then
        echo "Health endpoint reports an incomplete startup: ${required}" >&2
        exit 1
    fi
done
pac="$(demo_wait_url "http://127.0.0.1:${pac_port}/demo-proxy.pac" 5)"
target_host="$(demo_config_value target host)"
if [[ "${pac}" != *"FindProxyForURL"* || "${pac}" != *"${target_host}"* ]]; then
    echo "PAC endpoint does not contain the configured exact-host route." >&2
    exit 1
fi
if ! demo_certificate_trusted; then
    echo "The recorded DemoProxy CA is not trusted in the login keychain." >&2
    exit 1
fi

echo "Verification passed: process, proxy port, health, PAC, and certificate trust."
