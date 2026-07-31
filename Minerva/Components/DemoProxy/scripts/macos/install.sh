#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
source "${SCRIPT_DIR}/common.sh"

development="false"
install_launch_agent="false"
while (($#)); do
    case "$1" in
        --development) development="true"; shift ;;
        --install-launch-agent) install_launch_agent="true"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

demo_require_macos
architecture="$(uname -m)"
case "${architecture}" in
    arm64|x86_64) ;;
    *) echo "Unsupported macOS architecture: ${architecture}" >&2; exit 1 ;;
esac

demo_init_paths
demo_assert_install_root

rollback_message() {
    echo "Installation did not complete." >&2
    echo "Rollback: ${DEMO_APP_DIR}/scripts/macos/disable.sh --force" >&2
    echo "Remove trust: ${DEMO_APP_DIR}/scripts/macos/uninstall-ca.sh" >&2
}
trap rollback_message ERR

demo_create_directories
if [[ "${SOURCE_ROOT}" != "${DEMO_APP_DIR}" ]]; then
    for relative_directory in \
        proxy \
        pac \
        scripts/common \
        scripts/macos \
        startup/macos; do
        source_directory="${SOURCE_ROOT}/${relative_directory}"
        destination_directory="${DEMO_APP_DIR}/${relative_directory}"
        if [[ ! -d "${source_directory}" ]]; then
            echo "Required install source directory is missing: ${source_directory}" >&2
            exit 1
        fi
        mkdir -p "${destination_directory}"
        cp -R "${source_directory}/." "${destination_directory}/"
    done
    for relative_file in requirements.txt pyproject.toml; do
        if [[ -f "${SOURCE_ROOT}/${relative_file}" ]]; then
            cp "${SOURCE_ROOT}/${relative_file}" "${DEMO_APP_DIR}/${relative_file}"
        fi
    done
    if [[ -d "${SOURCE_ROOT}/bin" ]]; then
        mkdir -p "${DEMO_APP_DIR}/bin"
        cp -R "${SOURCE_ROOT}/bin/." "${DEMO_APP_DIR}/bin/"
    fi
    if [[ ! -f "${DEMO_CONFIG_PATH}" ]]; then
        cp "${SOURCE_ROOT}/config/proxy.yaml" "${DEMO_CONFIG_PATH}"
    fi
    if [[ ! -f "${DEMO_APP_DIR}/config/demo-lock.json" ]]; then
        cp "${SOURCE_ROOT}/config/demo-lock.json" "${DEMO_APP_DIR}/config/demo-lock.json"
    fi
    cp "${SOURCE_ROOT}/config/proxy.example.yaml" "${DEMO_APP_DIR}/config/proxy.example.yaml"
    cp "${SOURCE_ROOT}/config/demo-lock.example.json" "${DEMO_APP_DIR}/config/demo-lock.example.json"
fi
find "${DEMO_APP_DIR}/scripts/macos" -type f -name '*.sh' -exec chmod 700 {} +

if [[ "${development}" == "true" ]]; then
    python_command="$(command -v python3 || true)"
    if [[ -z "${python_command}" ]]; then
        echo "Python 3.12 or newer is required for --development." >&2
        exit 1
    fi
    if ! "${python_command}" -c 'import sys; raise SystemExit(sys.version_info < (3, 12))'; then
        echo "Python 3.12 or newer is required for --development." >&2
        exit 1
    fi
    if [[ ! -x "${DEMO_APP_DIR}/.venv/bin/python" ]]; then
        "${python_command}" -m venv "${DEMO_APP_DIR}/.venv"
    fi
    "${DEMO_APP_DIR}/.venv/bin/python" -m pip install \
        --disable-pip-version-check \
        -r "${DEMO_APP_DIR}/requirements.txt"
fi

demo_runtime_path >/dev/null
"${DEMO_APP_DIR}/scripts/macos/verify.sh" \
    --app-dir "${DEMO_APP_DIR}" \
    --configuration-only
demo_hardening_check
"${DEMO_APP_DIR}/scripts/macos/start.sh" --app-dir "${DEMO_APP_DIR}"

certificate_path="${DEMO_MITM_CONF_DIR}/mitmproxy-ca-cert.cer"
deadline=$((SECONDS + 15))
while [[ ! -f "${certificate_path}" ]] && ((SECONDS < deadline)); do
    sleep 0.25
done
if [[ ! -f "${certificate_path}" ]]; then
    echo "mitmdump did not generate its local CA certificate." >&2
    exit 1
fi
"${DEMO_APP_DIR}/scripts/macos/install-ca.sh" --app-dir "${DEMO_APP_DIR}"

# Restart so the health process inherits the verified keychain trust state.
"${DEMO_APP_DIR}/scripts/macos/stop.sh" --app-dir "${DEMO_APP_DIR}"
"${DEMO_APP_DIR}/scripts/macos/start.sh" --app-dir "${DEMO_APP_DIR}"

if [[ "${install_launch_agent}" == "true" ]]; then
    demo_write_launch_agent
    "${DEMO_APP_DIR}/scripts/macos/stop.sh" --app-dir "${DEMO_APP_DIR}"
    launchctl bootout "gui/$(id -u)" "${DEMO_LAUNCH_AGENT_PATH}" >/dev/null 2>&1 || true
    launchctl bootstrap "gui/$(id -u)" "${DEMO_LAUNCH_AGENT_PATH}"
    health_port="$(demo_config_value platform health_port)"
    demo_wait_url "http://127.0.0.1:${health_port}/health" 20 >/dev/null
fi

"${DEMO_APP_DIR}/scripts/macos/verify.sh" --app-dir "${DEMO_APP_DIR}"
trap - ERR
echo "DemoProxy installation completed for ${architecture}."
echo "Enable: ${DEMO_APP_DIR}/scripts/macos/enable.sh"
echo "Rollback: ${DEMO_APP_DIR}/scripts/macos/disable.sh --force"
echo "Uninstall: ${DEMO_APP_DIR}/scripts/macos/uninstall.sh --force"
