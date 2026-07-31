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
demo_create_directories

if [[ -n "${DEMO_PROXY_PAC_URL:-}" ]]; then
    PAC_URL="${DEMO_PROXY_PAC_URL}"
elif [[ -f "${DEMO_CONFIG_PATH}" ]]; then
    PAC_URL="http://127.0.0.1:$(demo_config_value platform pac_port)/demo-proxy.pac"
else
    PAC_URL="http://127.0.0.1:8765/demo-proxy.pac"
fi
PROFILE_DIR="${DEMO_PROXY_CHROME_PROFILE:-${DEMO_CHROME_PROFILE}}"
START_URL="${DEMO_PROXY_START_URL:-https://nexus-cloud-web-stg.bsc.bscal.com/}"

chrome_candidates=()
if [[ -n "${DEMO_PROXY_CHROME_PATH:-}" ]]; then
    chrome_candidates+=("${DEMO_PROXY_CHROME_PATH}")
fi
chrome_candidates+=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "${HOME}/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

chrome_path=""
for candidate in "${chrome_candidates[@]}"; do
    if [[ -x "${candidate}" ]]; then
        chrome_path="${candidate}"
        break
    fi
done

if [[ -z "${chrome_path}" ]]; then
    echo "Google Chrome was not found. Set DEMO_PROXY_CHROME_PATH." >&2
    exit 1
fi

if ! curl --fail --silent --show-error --max-time 3 "${PAC_URL}" >/dev/null; then
    echo "DemoProxy PAC endpoint is unavailable: ${PAC_URL}" >&2
    exit 1
fi

mkdir -p "${PROFILE_DIR}"

if demo_process_status chrome; then
    chrome_status=0
else
    chrome_status=$?
fi
if ((chrome_status == 0)); then
    echo "Dedicated DemoProxy Chrome is already running (PID $(<"$(demo_state_path chrome pid)"))."
    exit 0
elif ((chrome_status == 2)); then
    echo "Chrome state points to another process. Run disable.sh --force to clear stale state." >&2
    exit 1
fi
demo_clear_process_state chrome

chrome_arguments=(
    "--user-data-dir=${PROFILE_DIR}"
    "--proxy-pac-url=${PAC_URL}"
    "--no-first-run"
    "--no-default-browser-check"
    "${START_URL}"
)
chrome_app=""
case "${chrome_path}" in
    *"/Google Chrome.app/Contents/MacOS/Google Chrome")
        chrome_app="${chrome_path%/Contents/MacOS/Google Chrome}"
        ;;
esac

find_launched_chrome() {
    local candidate_pid candidate_executable candidate_command
    for candidate_pid in $(pgrep -f "user-data-dir=" 2>/dev/null || true); do
        candidate_executable="$(demo_process_executable "${candidate_pid}" 2>/dev/null || true)"
        candidate_command="$(ps -ww -p "${candidate_pid}" -o command= 2>/dev/null || true)"
        if [[ "${candidate_executable}" == "${chrome_path}" &&
              "${candidate_command}" == *"${PROFILE_DIR}"* &&
              "${candidate_command}" == *"${PAC_URL}"* ]]; then
            printf '%s\n' "${candidate_pid}"
            return 0
        fi
    done
    return 1
}

launched_via_services="false"
if [[ -n "${chrome_app}" ]]; then
    launched_via_services="true"
    /usr/bin/open -na "${chrome_app}" --args "${chrome_arguments[@]}" \
        >"${DEMO_LOG_DIR}/chrome.stdout.log" \
        2>"${DEMO_LOG_DIR}/chrome.stderr.log"
    pid=""
    deadline=$((SECONDS + 10))
    while [[ -z "${pid}" ]] && ((SECONDS < deadline)); do
        pid="$(find_launched_chrome || true)"
        [[ -n "${pid}" ]] || sleep 0.1
    done
    if [[ -z "${pid}" ]]; then
        echo "Dedicated Chrome process could not be identified after Launch Services startup." >&2
        exit 1
    fi
else
    nohup "${chrome_path}" "${chrome_arguments[@]}" \
        </dev/null \
        >"${DEMO_LOG_DIR}/chrome.stdout.log" \
        2>"${DEMO_LOG_DIR}/chrome.stderr.log" &
    pid=$!
fi

sleep 0.1
if kill -0 "${pid}" 2>/dev/null; then
    if [[ "${launched_via_services}" == "true" ]]; then
        # find_launched_chrome already verified both the final bundle executable
        # and the dedicated profile/PAC markers. Avoid recording the transient
        # macOS code-sign clone path that may appear during initial sampling.
        executable="${chrome_path}"
    else
        executable="$(demo_stable_process_executable "${pid}" || true)"
    fi
    if [[ -z "${executable}" ]]; then
        kill -TERM "${pid}" 2>/dev/null || true
        wait "${pid}" 2>/dev/null || true
        echo "Chrome executable identity did not stabilize; refusing to record an unsafe PID." >&2
        exit 1
    fi
    demo_write_process_state chrome "${pid}" "${executable}" "${PROFILE_DIR}" "${PAC_URL}"
    echo "Dedicated DemoProxy Chrome launched (PID ${pid})."
else
    wait "${pid}" || true
    echo "Chrome launch command completed before process tracking was established."
fi
