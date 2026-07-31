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
demo_stop_tracked_process proxy "${force}"
echo "DemoProxy stopped."
