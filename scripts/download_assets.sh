#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPOSITORY="vigorlee/lightwheel-room-mesh-isaacsim-repro"
VERSION="v1.0.0"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/lightwheel-room-mesh-isaacsim-repro"
ROOM_ARCHIVE="$CACHE_DIR/Room_Mesh.zip"
ROOM_SHA256="0be5acc7fe75d1982decd9c4f934c79e32b8c183cfc3928bd1d5b82819e1babc"
ASSETS=(
    "room-mesh-v1.0.0.zip.part-00"
    "room-mesh-v1.0.0.zip.part-01"
    "lightwheel-samples-v1.0.0.tar.zst"
)

for command in gh sha256sum unzip tar unzstd; do
    if ! command -v "$command" >/dev/null 2>&1; then
        printf 'Required command is missing: %s\n' "$command" >&2
        exit 1
    fi
done

mkdir -p "$CACHE_DIR" "$ROOT/assets/Room_Mesh" "$ROOT/assets"
for asset in "${ASSETS[@]}"; do
    if [[ ! -f "$CACHE_DIR/$asset" ]]; then
        gh release download "$VERSION" \
            --repo "$REPOSITORY" \
            --dir "$CACHE_DIR" \
            --pattern "$asset"
    fi
done

(
    cd "$CACHE_DIR"
    sha256sum --check "$ROOT/checksums/release-assets.sha256"
)

ASSEMBLING="$ROOM_ARCHIVE.partial"
: > "$ASSEMBLING"
for part in "$CACHE_DIR"/room-mesh-v1.0.0.zip.part-*; do
    cat "$part" >> "$ASSEMBLING"
done
mv "$ASSEMBLING" "$ROOM_ARCHIVE"
printf '%s  %s\n' "$ROOM_SHA256" "$ROOM_ARCHIVE" | sha256sum --check --status
unzip -tq "$ROOM_ARCHIVE" >/dev/null
unzip -oq "$ROOM_ARCHIVE" -d "$ROOT/assets/Room_Mesh"
tar --use-compress-program=unzstd \
    -xf "$CACHE_DIR/lightwheel-samples-v1.0.0.tar.zst" \
    -C "$ROOT/assets"

python3 "$ROOT/scripts/verify_package.py"
printf 'Assets extracted and verified under %s/assets\n' "$ROOT"
