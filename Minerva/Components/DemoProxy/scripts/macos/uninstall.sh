#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

force="false"
while (($#)); do
    case "$1" in
        --force) force="true"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
demo_init_paths
demo_assert_install_root
if [[ ! -d "${DEMO_APP_DIR}" ]]; then
    echo "DemoProxy is not installed."
    exit 0
fi
if [[ "${force}" != "true" ]]; then
    if [[ ! -t 0 ]]; then
        echo "Re-run with --force for non-interactive uninstall." >&2
        exit 2
    fi
    read -r -p "Uninstall DemoProxy and its recorded login-keychain CA? [y/N] " answer
    [[ "${answer}" == "y" || "${answer}" == "Y" ]] || exit 0
fi

launchctl bootout "gui/$(id -u)" "${DEMO_LAUNCH_AGENT_PATH}" >/dev/null 2>&1 || true
"${SCRIPT_DIR}/disable.sh" --app-dir "${DEMO_APP_DIR}" --force
"${SCRIPT_DIR}/uninstall-ca.sh" --app-dir "${DEMO_APP_DIR}"
rm -f "${DEMO_LAUNCH_AGENT_PATH}"

demo_assert_install_root
expected_log_dir="${HOME}/Library/Logs/DemoResponseProxy"
if [[ "${DEMO_LOG_DIR}" != "${expected_log_dir}" ]]; then
    echo "Unsafe log directory: ${DEMO_LOG_DIR}" >&2
    exit 1
fi
rm -rf "${DEMO_APP_DIR}"
rm -rf "${DEMO_LOG_DIR}"
echo "DemoProxy was uninstalled. Normal browser and system proxy settings were unchanged."
