#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${ISAACSIM_PYTHON:-$ROOT/.venv/bin/python}"
ASSET_ROOT="${ISAACSIM_ASSET_ROOT:-$ROOT/assets}"

if [[ ! -x "$PYTHON" ]]; then
    printf 'Isaac Sim Python was not found: %s\n' "$PYTHON" >&2
    printf 'Run scripts/install_isaacsim.sh or set ISAACSIM_PYTHON.\n' >&2
    exit 1
fi
if [[ ! -f "$ASSET_ROOT/Room_3DGS/Scene.usd" ]]; then
    printf 'Room_3DGS assets are missing: %s\n' "$ASSET_ROOT/Room_3DGS/Scene.usd" >&2
    printf 'Provide the data directory through ISAACSIM_ASSET_ROOT.\n' >&2
    exit 1
fi
if [[ -z "${OMNI_KIT_ACCEPT_EULA:-}" ]]; then
    printf 'Read the NVIDIA Omniverse EULA, then set OMNI_KIT_ACCEPT_EULA=YES.\n' >&2
    exit 1
fi

export DISPLAY="${DISPLAY:-:0}"
export ISAACSIM_ASSET_ROOT="$ASSET_ROOT"
if [[ ! -f "$ASSET_ROOT/Room_3DGS/Room_3DGS_With_Lightwheel.usda" ]]; then
    "$PYTHON" "$ROOT/scripts/prepare_room_3dgs.py"
fi

exec "$PYTHON" "$ROOT/scripts/open_room_3dgs.py" "$@"
