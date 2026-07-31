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

fingerprint_file="${DEMO_STATE_DIR}/certificate.sha256"
if [[ ! -f "${fingerprint_file}" ]]; then
    echo "No recorded DemoProxy certificate is installed."
    exit 0
fi
fingerprint="$(<"${fingerprint_file}")"
if [[ ! "${fingerprint}" =~ ^[A-F0-9]{64}$ ]]; then
    echo "Recorded certificate fingerprint is invalid; refusing broad removal." >&2
    exit 1
fi

if [[ -f "${DEMO_KEYCHAIN}" ]] &&
   security find-certificate -a -Z "${DEMO_KEYCHAIN}" 2>/dev/null |
       grep -Fq "SHA-256 hash: ${fingerprint}"; then
    security delete-certificate -Z "${fingerprint}" -t "${DEMO_KEYCHAIN}"
fi
rm -f "${fingerprint_file}"
echo "Recorded DemoProxy CA and user trust settings were removed."
