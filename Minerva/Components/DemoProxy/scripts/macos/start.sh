#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

app_dir=""
supervised="false"
while (($#)); do
    case "$1" in
        --app-dir) app_dir="$2"; shift 2 ;;
        --supervised) supervised="true"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
demo_init_paths "${app_dir}"
demo_assert_install_root
demo_create_directories
read -r listen_port health_port pac_port <<<"$(demo_validate_config)"

if demo_process_status proxy; then
    status=0
else
    status=$?
fi
if ((status == 0)); then
    echo "DemoProxy is already running (PID $(<"$(demo_state_path proxy pid)"))."
    exit 0
elif ((status == 2)); then
    echo "Proxy state points to another process. Run disable.sh --force to clear stale state." >&2
    exit 1
fi
demo_clear_process_state proxy

runtime="$(demo_runtime_path)"
addon_path="${DEMO_APP_DIR}/proxy/addon.py"
if [[ ! -f "${addon_path}" ]]; then
    echo "Proxy addon not found: ${addon_path}" >&2
    exit 1
fi
config_option="demo_proxy_config=${DEMO_CONFIG_PATH}"
certificate_trusted="false"
if demo_certificate_trusted; then
    certificate_trusted="true"
fi

DEMO_PROXY_PLATFORM="macos" \
DEMO_PROXY_CERTIFICATE_TRUSTED="${certificate_trusted}" \
nohup "${runtime}" \
    "--listen-host" "127.0.0.1" \
    "--listen-port" "${listen_port}" \
    "--set" "confdir=${DEMO_MITM_CONF_DIR}" \
    "--set" "flow_detail=0" \
    "--set" "${config_option}" \
    "--scripts" "${addon_path}" \
    </dev/null \
    >"${DEMO_PROXY_STDOUT}" 2>"${DEMO_PROXY_STDERR}" &
pid=$!

actual_executable="$(demo_stable_process_executable "${pid}" || true)"
if [[ -z "${actual_executable}" ]]; then
    echo "Proxy process exited during startup. See ${DEMO_PROXY_STDERR}." >&2
    wait "${pid}" || true
    exit 1
fi
demo_write_process_state proxy "${pid}" "${actual_executable}" \
    "${runtime}" "${addon_path}" "${config_option}"

if ! demo_wait_url "http://127.0.0.1:${health_port}/health" 20 >/dev/null ||
   ! demo_wait_url "http://127.0.0.1:${pac_port}/demo-proxy.pac" 10 >/dev/null; then
    demo_stop_tracked_process proxy true || true
    exit 1
fi

echo "DemoProxy started on 127.0.0.1:${listen_port} (PID ${pid})."
if [[ "${supervised}" == "true" ]]; then
    wait "${pid}"
fi
