#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

app_dir=""
while (($#)); do
    case "$1" in
        --app-dir) app_dir="$2"; shift 2 ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
demo_init_paths "${app_dir}"
demo_assert_install_root
"${SCRIPT_DIR}/verify.sh" --app-dir "${DEMO_APP_DIR}" --configuration-only
demo_hardening_check

certificate_path="${DEMO_MITM_CONF_DIR}/mitmproxy-ca-cert.cer"
if [[ ! -f "${certificate_path}" ]]; then
    "${SCRIPT_DIR}/start.sh" --app-dir "${DEMO_APP_DIR}"
    deadline=$((SECONDS + 15))
    while [[ ! -f "${certificate_path}" ]] && ((SECONDS < deadline)); do
        sleep 0.25
    done
    if [[ ! -f "${certificate_path}" ]]; then
        echo "mitmproxy did not generate its local CA certificate." >&2
        exit 1
    fi
fi

was_trusted="false"
if demo_certificate_trusted; then
    was_trusted="true"
fi
"${SCRIPT_DIR}/install-ca.sh" --app-dir "${DEMO_APP_DIR}"

launch_agent_domain="gui/$(id -u)/${DEMO_LAUNCH_AGENT_LABEL}"
if [[ -f "${DEMO_LAUNCH_AGENT_PATH}" ]] &&
   launchctl print "${launch_agent_domain}" >/dev/null 2>&1; then
    "${SCRIPT_DIR}/stop.sh" --app-dir "${DEMO_APP_DIR}" --force
    launchctl kickstart -k "${launch_agent_domain}"
    health_port="$(demo_config_value platform health_port)"
    demo_wait_url "http://127.0.0.1:${health_port}/health" 20 >/dev/null
else
    if demo_process_status proxy; then
        running_status=0
    else
        running_status=$?
    fi
    if ((running_status == 0)) && [[ "${was_trusted}" != "true" ]]; then
        "${SCRIPT_DIR}/stop.sh" --app-dir "${DEMO_APP_DIR}"
    fi
    "${SCRIPT_DIR}/start.sh" --app-dir "${DEMO_APP_DIR}"
fi
"${SCRIPT_DIR}/verify.sh" --app-dir "${DEMO_APP_DIR}"
"${SCRIPT_DIR}/launch-chrome.sh" --app-dir "${DEMO_APP_DIR}"
"${SCRIPT_DIR}/verify.sh" --app-dir "${DEMO_APP_DIR}"

health_port="$(demo_config_value platform health_port)"
echo "DemoProxy enabled. Operator status: http://127.0.0.1:${health_port}/status"
