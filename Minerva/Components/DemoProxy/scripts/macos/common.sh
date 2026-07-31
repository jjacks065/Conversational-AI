#!/usr/bin/env bash
set -euo pipefail

DEMO_LAUNCH_AGENT_LABEL="com.demo-response-proxy"

demo_init_paths() {
    local app_dir="${1:-}"
    if [[ -z "${HOME:-}" ]]; then
        echo "HOME is required." >&2
        return 1
    fi
    DEMO_APP_DIR="${app_dir:-${HOME}/Library/Application Support/DemoResponseProxy}"
    DEMO_CONFIG_PATH="${DEMO_APP_DIR}/config/proxy.yaml"
    DEMO_RUNTIME_DIR="${DEMO_APP_DIR}/runtime"
    DEMO_MITM_CONF_DIR="${DEMO_RUNTIME_DIR}/mitmproxy"
    DEMO_STATE_DIR="${DEMO_RUNTIME_DIR}/state"
    DEMO_CHROME_PROFILE="${DEMO_APP_DIR}/chrome-profile"
    DEMO_LOG_DIR="${HOME}/Library/Logs/DemoResponseProxy"
    DEMO_PROXY_STDOUT="${DEMO_LOG_DIR}/proxy.stdout.log"
    DEMO_PROXY_STDERR="${DEMO_LOG_DIR}/proxy.stderr.log"
    DEMO_KEYCHAIN="${HOME}/Library/Keychains/login.keychain-db"
    DEMO_LAUNCH_AGENT_PATH="${HOME}/Library/LaunchAgents/${DEMO_LAUNCH_AGENT_LABEL}.plist"
    export DEMO_APP_DIR DEMO_CONFIG_PATH DEMO_RUNTIME_DIR DEMO_MITM_CONF_DIR
    export DEMO_STATE_DIR DEMO_CHROME_PROFILE DEMO_LOG_DIR DEMO_PROXY_STDOUT
    export DEMO_PROXY_STDERR DEMO_KEYCHAIN DEMO_LAUNCH_AGENT_PATH
}

demo_require_macos() {
    if [[ "$(uname -s)" != "Darwin" ]]; then
        echo "This script must run on macOS." >&2
        return 1
    fi
}

demo_assert_install_root() {
    local expected="${HOME}/Library/Application Support/DemoResponseProxy"
    if [[ "${DEMO_APP_DIR}" != "${expected}" ]]; then
        echo "Unsafe application directory. Expected exactly: ${expected}" >&2
        return 1
    fi
}

demo_create_directories() {
    mkdir -p \
        "${DEMO_APP_DIR}" \
        "${DEMO_APP_DIR}/config" \
        "${DEMO_RUNTIME_DIR}" \
        "${DEMO_MITM_CONF_DIR}" \
        "${DEMO_STATE_DIR}" \
        "${DEMO_CHROME_PROFILE}" \
        "${DEMO_LOG_DIR}"
    chmod 700 "${DEMO_RUNTIME_DIR}" "${DEMO_MITM_CONF_DIR}" "${DEMO_STATE_DIR}"
}

demo_config_value() {
    local section="$1"
    local key="$2"
    local config_path="${3:-${DEMO_CONFIG_PATH}}"
    local value
    if [[ ! -f "${config_path}" ]]; then
        echo "Configuration file not found: ${config_path}" >&2
        return 1
    fi
    value="$(awk -v wanted_section="${section}" -v wanted_key="${key}" '
        /^[A-Za-z_][A-Za-z0-9_-]*:[[:space:]]*$/ {
            active = ($0 == wanted_section ":")
            next
        }
        active {
            line = $0
            sub(/^[[:space:]]+/, "", line)
            separator = index(line, ":")
            if (separator > 0 && substr(line, 1, separator - 1) == wanted_key) {
                value = substr(line, separator + 1)
                sub(/^[[:space:]]+/, "", value)
                sub(/[[:space:]]+$/, "", value)
                if ((substr(value, 1, 1) == "\"" && substr(value, length(value), 1) == "\"") ||
                    (substr(value, 1, 1) == "\047" && substr(value, length(value), 1) == "\047")) {
                    value = substr(value, 2, length(value) - 2)
                }
                print value
                exit
            }
        }
    ' "${config_path}")"
    if [[ -z "${value}" ]]; then
        echo "Missing configuration value: ${section}.${key}" >&2
        return 1
    fi
    printf '%s\n' "${value}"
}

demo_validate_port() {
    local value="$1"
    local name="$2"
    if [[ ! "${value}" =~ ^[0-9]+$ ]] || (( value < 1 || value > 65535 )); then
        echo "${name} must be a port from 1 through 65535." >&2
        return 1
    fi
}

demo_validate_config() {
    local listen_host listen_port health_port pac_port validator python packaged_validator
    listen_host="$(demo_config_value proxy listen_host)"
    listen_port="$(demo_config_value proxy listen_port)"
    health_port="$(demo_config_value platform health_port)"
    pac_port="$(demo_config_value platform pac_port)"
    if [[ "${listen_host}" != "127.0.0.1" ]]; then
        echo "proxy.listen_host must be 127.0.0.1 for macOS integration." >&2
        return 1
    fi
    demo_validate_port "${listen_port}" "proxy.listen_port"
    demo_validate_port "${health_port}" "platform.health_port"
    demo_validate_port "${pac_port}" "platform.pac_port"
    if [[ "${listen_port}" == "${health_port}" || "${listen_port}" == "${pac_port}" || "${health_port}" == "${pac_port}" ]]; then
        echo "Proxy, health, and PAC ports must be distinct." >&2
        return 1
    fi
    validator="${DEMO_APP_DIR}/scripts/common/verify_config.py"
    python="${DEMO_APP_DIR}/.venv/bin/python"
    packaged_validator="${DEMO_APP_DIR}/bin/mitmdump"
    if [[ -x "${packaged_validator}" ]]; then
        "${packaged_validator}" --demo-verify-config "${DEMO_CONFIG_PATH}" >/dev/null
    elif [[ -x "${python}" && -f "${validator}" ]]; then
        "${python}" "${validator}" "${DEMO_CONFIG_PATH}" >/dev/null
    fi
    printf '%s %s %s\n' "${listen_port}" "${health_port}" "${pac_port}"
}

demo_hardening_check() {
    local lock_path="${DEMO_APP_DIR}/config/demo-lock.json"
    local packaged_validator="${DEMO_APP_DIR}/bin/mitmdump"
    local python="${DEMO_APP_DIR}/.venv/bin/python"
    local checker="${DEMO_APP_DIR}/scripts/common/hardening_check.py"
    if [[ ! -f "${lock_path}" ]]; then
        echo "Frozen demo rule lock not found: ${lock_path}" >&2
        return 1
    fi
    if [[ -x "${packaged_validator}" ]]; then
        "${packaged_validator}" --demo-hardening-check \
            "${DEMO_APP_DIR}" "${DEMO_CONFIG_PATH}" "${lock_path}" >/dev/null
    elif [[ -x "${python}" && -f "${checker}" ]]; then
        "${python}" "${checker}" \
            --project-root "${DEMO_APP_DIR}" \
            --config "${DEMO_CONFIG_PATH}" \
            --lock "${lock_path}" >/dev/null
    else
        echo "No hardening checker is available in ${DEMO_APP_DIR}." >&2
        return 1
    fi
}

demo_runtime_path() {
    local candidate
    for candidate in \
        "${DEMO_APP_DIR}/bin/mitmdump" \
        "${DEMO_APP_DIR}/.venv/bin/mitmdump"; do
        if [[ -x "${candidate}" ]]; then
            printf '%s\n' "${candidate}"
            return 0
        fi
    done
    echo "DemoProxy runtime was not found. Reinstall with a packaged runtime or --development." >&2
    return 1
}

demo_state_path() {
    local kind="$1"
    local field="$2"
    printf '%s/%s.%s\n' "${DEMO_STATE_DIR}" "${kind}" "${field}"
}

demo_clear_process_state() {
    local kind="$1"
    rm -f \
        "$(demo_state_path "${kind}" pid)" \
        "$(demo_state_path "${kind}" executable)" \
        "$(demo_state_path "${kind}" markers)"
}

demo_process_executable() {
    local pid="$1"
    local executable=""
    if [[ -x /usr/sbin/lsof ]]; then
        executable="$(/usr/sbin/lsof -a -p "${pid}" -d txt -Fn 2>/dev/null |
            awk '/^n/ {sub(/^n/, ""); print; exit}')"
    fi
    if [[ -z "${executable}" ]]; then
        executable="$(ps -p "${pid}" -o comm= | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    fi
    printf '%s\n' "${executable}"
}

demo_stable_process_executable() {
    local pid="$1"
    local current=""
    local previous=""
    local stable_samples=0
    sleep 0.2
    for _ in {1..20}; do
        current="$(demo_process_executable "${pid}" 2>/dev/null || true)"
        if [[ -n "${current}" && "${current}" == "${previous}" ]]; then
            stable_samples=$((stable_samples + 1))
            if ((stable_samples >= 2)); then
                printf '%s\n' "${current}"
                return 0
            fi
        else
            stable_samples=0
        fi
        previous="${current}"
        sleep 0.05
    done
    return 1
}

demo_write_process_state() {
    local kind="$1"
    local pid="$2"
    local executable="$3"
    shift 3
    local temporary
    mkdir -p "${DEMO_STATE_DIR}"
    temporary="$(mktemp -d "${DEMO_STATE_DIR}/.${kind}.XXXXXX")"
    if [[ ! "${pid}" =~ ^[0-9]+$ || -z "${executable}" ]]; then
        rm -rf "${temporary}"
        echo "Invalid process state for ${kind}." >&2
        return 1
    fi
    printf '%s\n' "${pid}" >"${temporary}/pid"
    printf '%s\n' "${executable}" >"${temporary}/executable"
    printf '%s\n' "$@" >"${temporary}/markers"
    chmod 600 "${temporary}/pid" "${temporary}/executable" "${temporary}/markers"
    mv -f "${temporary}/pid" "$(demo_state_path "${kind}" pid)"
    mv -f "${temporary}/executable" "$(demo_state_path "${kind}" executable)"
    mv -f "${temporary}/markers" "$(demo_state_path "${kind}" markers)"
    rmdir "${temporary}"
}

demo_process_status() {
    local kind="$1"
    local pid_file executable_file markers_file pid expected_executable actual_executable command marker
    pid_file="$(demo_state_path "${kind}" pid)"
    executable_file="$(demo_state_path "${kind}" executable)"
    markers_file="$(demo_state_path "${kind}" markers)"
    if [[ ! -f "${pid_file}" || ! -f "${executable_file}" || ! -f "${markers_file}" ]]; then
        return 1
    fi
    pid="$(<"${pid_file}")"
    expected_executable="$(<"${executable_file}")"
    if [[ ! "${pid}" =~ ^[0-9]+$ ]] || ! kill -0 "${pid}" 2>/dev/null; then
        return 1
    fi
    actual_executable="$(demo_process_executable "${pid}")"
    command="$(ps -ww -p "${pid}" -o command= | sed -e 's/^[[:space:]]*//')"
    if [[ -z "${actual_executable}" || "${actual_executable}" != "${expected_executable}" ]]; then
        return 2
    fi
    while IFS= read -r marker; do
        if [[ -z "${marker}" || "${command}" != *"${marker}"* ]]; then
            return 2
        fi
    done <"${markers_file}"
    return 0
}

demo_stop_tracked_process() {
    local kind="$1"
    local force="${2:-false}"
    local pid status deadline
    if demo_process_status "${kind}"; then
        status=0
    else
        status=$?
    fi
    if (( status == 1 )); then
        demo_clear_process_state "${kind}"
        return 0
    fi
    if (( status == 2 )); then
        if [[ "${force}" == "true" ]]; then
            demo_clear_process_state "${kind}"
        fi
        echo "Refusing to terminate ${kind}: executable or command line does not match recorded state." >&2
        return 2
    fi
    pid="$(<"$(demo_state_path "${kind}" pid)")"
    kill -TERM "${pid}"
    deadline=$((SECONDS + 10))
    while kill -0 "${pid}" 2>/dev/null && (( SECONDS < deadline )); do
        sleep 0.1
    done
    if kill -0 "${pid}" 2>/dev/null; then
        if [[ "${force}" != "true" ]]; then
            echo "${kind} process ${pid} did not stop." >&2
            return 1
        fi
        kill -KILL "${pid}"
    fi
    demo_clear_process_state "${kind}"
}

demo_wait_url() {
    local url="$1"
    local timeout_seconds="${2:-15}"
    local deadline=$((SECONDS + timeout_seconds))
    while (( SECONDS < deadline )); do
        if curl --fail --silent --show-error --max-time 2 "${url}"; then
            return 0
        fi
        sleep 0.25
    done
    echo "Timed out waiting for: ${url}" >&2
    return 1
}

demo_port_open() {
    local port="$1"
    nc -z -w 1 127.0.0.1 "${port}" >/dev/null 2>&1
}

demo_certificate_fingerprint() {
    local certificate_path="$1"
    /usr/bin/openssl x509 -in "${certificate_path}" -noout -fingerprint -sha256 |
        awk -F= '{gsub(":", "", $2); print toupper($2)}'
}

demo_certificate_trusted() {
    local fingerprint_file="${DEMO_STATE_DIR}/certificate.sha256"
    local certificate_path="${DEMO_MITM_CONF_DIR}/mitmproxy-ca-cert.cer"
    local fingerprint
    if [[ ! -f "${fingerprint_file}" || ! -f "${certificate_path}" || ! -f "${DEMO_KEYCHAIN}" ]]; then
        return 1
    fi
    fingerprint="$(<"${fingerprint_file}")"
    if [[ ! "${fingerprint}" =~ ^[A-F0-9]{64}$ ]]; then
        return 1
    fi
    security find-certificate -a -Z "${DEMO_KEYCHAIN}" 2>/dev/null |
        grep -Fq "SHA-256 hash: ${fingerprint}" || return 1
    security verify-cert -q -l -c "${certificate_path}" -k "${DEMO_KEYCHAIN}" >/dev/null 2>&1
}

demo_write_launch_agent() {
    local temporary_plist
    mkdir -p "$(dirname "${DEMO_LAUNCH_AGENT_PATH}")"
    temporary_plist="$(mktemp "${DEMO_LAUNCH_AGENT_PATH}.XXXXXX")"
    plutil -create xml1 "${temporary_plist}"
    plutil -insert Label -string "${DEMO_LAUNCH_AGENT_LABEL}" "${temporary_plist}"
    plutil -insert ProgramArguments -array "${temporary_plist}"
    plutil -insert ProgramArguments.0 -string "${DEMO_APP_DIR}/scripts/macos/start.sh" "${temporary_plist}"
    plutil -insert ProgramArguments.1 -string "--app-dir" "${temporary_plist}"
    plutil -insert ProgramArguments.2 -string "${DEMO_APP_DIR}" "${temporary_plist}"
    plutil -insert ProgramArguments.3 -string "--supervised" "${temporary_plist}"
    plutil -insert WorkingDirectory -string "${DEMO_APP_DIR}" "${temporary_plist}"
    plutil -insert RunAtLoad -bool true "${temporary_plist}"
    plutil -insert KeepAlive -bool false "${temporary_plist}"
    plutil -insert ProcessType -string "Background" "${temporary_plist}"
    plutil -insert StandardOutPath -string "${DEMO_LOG_DIR}/launch-agent.stdout.log" "${temporary_plist}"
    plutil -insert StandardErrorPath -string "${DEMO_LOG_DIR}/launch-agent.stderr.log" "${temporary_plist}"
    plutil -lint "${temporary_plist}" >/dev/null
    chmod 600 "${temporary_plist}"
    mv -f "${temporary_plist}" "${DEMO_LAUNCH_AGENT_PATH}"
}
