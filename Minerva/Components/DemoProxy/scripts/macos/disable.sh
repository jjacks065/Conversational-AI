#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

app_dir=""
force="false"
while (($#)); do
    case "$1" in
        --app-dir) app_dir="$2"; shift 2 ;;
        --force) force="true"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
demo_init_paths "${app_dir}"
demo_assert_install_root

if demo_stop_tracked_process "chrome" "${force}"; then
    chrome_status=0
else
    chrome_status=$?
fi
if ((chrome_status != 0)) && [[ "${force}" != "true" ]]; then
    exit "${chrome_status}"
fi

stop_arguments=(--app-dir "${DEMO_APP_DIR}")
if [[ "${force}" == "true" ]]; then
    stop_arguments+=(--force)
fi
if "${SCRIPT_DIR}/stop.sh" "${stop_arguments[@]}"; then
    proxy_status=0
else
    proxy_status=$?
fi
if ((proxy_status != 0)) && [[ "${force}" != "true" ]]; then
    exit "${proxy_status}"
fi

if [[ -f "${DEMO_CONFIG_PATH}" ]]; then
    listen_port="$(demo_config_value proxy listen_port)"
    if demo_port_open "${listen_port}"; then
        echo "Port ${listen_port} is still listening; no unverified process was terminated." >&2
        exit 1
    fi
fi
echo "DemoProxy disabled. Normal browser and system proxy settings were unchanged."
