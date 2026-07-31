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

certificate_path="${DEMO_MITM_CONF_DIR}/mitmproxy-ca-cert.cer"
fingerprint_file="${DEMO_STATE_DIR}/certificate.sha256"
if [[ ! -f "${certificate_path}" ]]; then
    echo "Local mitmproxy CA was not generated: ${certificate_path}" >&2
    exit 1
fi
if [[ ! -f "${DEMO_KEYCHAIN}" ]]; then
    echo "Login keychain was not found: ${DEMO_KEYCHAIN}" >&2
    exit 1
fi
fingerprint="$(demo_certificate_fingerprint "${certificate_path}")"
if [[ ! "${fingerprint}" =~ ^[A-F0-9]{64}$ ]]; then
    echo "Unable to calculate the local CA SHA-256 fingerprint." >&2
    exit 1
fi

printf '%s\n' "${fingerprint}" >"${fingerprint_file}.tmp"
chmod 600 "${fingerprint_file}.tmp"
mv -f "${fingerprint_file}.tmp" "${fingerprint_file}"

if ! demo_certificate_trusted; then
    security add-trusted-cert \
        -r trustRoot \
        -k "${DEMO_KEYCHAIN}" \
        "${certificate_path}"
fi
if ! demo_certificate_trusted; then
    rm -f "${fingerprint_file}"
    echo "DemoProxy CA trust verification failed." >&2
    exit 1
fi

echo "DemoProxy CA trusted in the current user's login keychain (${fingerprint})."
