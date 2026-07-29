#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    printf 'Python 3.12 is required. Set PYTHON_BIN to its executable.\n' >&2
    exit 1
fi

"$PYTHON_BIN" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/python" -m pip install \
    "isaacsim[all,extscache]==6.0.0.1" \
    --extra-index-url https://pypi.nvidia.com

printf 'Isaac Sim 6.0.0.1 installed in %s/.venv\n' "$ROOT"
