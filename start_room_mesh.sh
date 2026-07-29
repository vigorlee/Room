#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${ISAACSIM_PYTHON:-$ROOT/.venv/bin/python}"

if [[ ! -x "$PYTHON" ]]; then
    printf 'Isaac Sim Python was not found: %s\n' "$PYTHON" >&2
    printf 'Run scripts/install_isaacsim.sh or set ISAACSIM_PYTHON.\n' >&2
    exit 1
fi
if [[ ! -f "$ROOT/assets/Room_Mesh/Scene.usd" ]]; then
    printf 'Room_Mesh assets are missing. Run scripts/download_assets.sh first.\n' >&2
    exit 1
fi
if [[ -z "${OMNI_KIT_ACCEPT_EULA:-}" ]]; then
    printf 'Read the NVIDIA Omniverse EULA, then set OMNI_KIT_ACCEPT_EULA=YES.\n' >&2
    exit 1
fi

export DISPLAY="${DISPLAY:-:0}"
if [[ ! -f "$ROOT/assets/Room_Mesh/Room_With_Lightwheel.usda" ]]; then
    "$PYTHON" "$ROOT/scripts/prepare_scene.py"
fi

exec "$PYTHON" "$ROOT/scripts/open_scene.py" "$@"
