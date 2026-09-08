#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ISO_DIR="$ROOT_DIR/iso"
BUILD_DIR="$ISO_DIR/work"

if [[ "$(id -u)" -eq 0 ]]; then
    echo "Bitte den Build als normaler Benutzer starten; live-build verwendet sudo intern."
    exit 1
fi

missing=()
for command in lb debootstrap mksquashfs xorriso; do
    command -v "$command" >/dev/null || missing+=("$command")
done
if [[ "${#missing[@]}" -gt 0 ]]; then
    printf 'Fehlende Build-Werkzeuge: %s\n' "${missing[*]}"
    echo "Installiere sie mit: ./iso/install-dependencies.sh"
    exit 1
fi

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
lb clean --purge || true
lb config \
    --distribution bookworm \
    --architectures amd64 \
    --archive-areas "main contrib non-free non-free-firmware" \
    --binary-images iso-hybrid \
    --debian-installer live \
    --bootappend-live "boot=live components username=aiuser locales=de_DE.UTF-8"

mkdir -p config/package-lists config/includes.chroot/etc config/includes.chroot/opt/ai-os-linux
cp "$ISO_DIR/config/package-lists/ai-os.list.chroot" config/package-lists/
cp "$ISO_DIR/config/includes.chroot/etc/motd" config/includes.chroot/etc/motd
cp "$ROOT_DIR/scripts/ai_os.py" "$ROOT_DIR/scripts/train.py" "$ROOT_DIR/scripts/finetune.py" config/includes.chroot/opt/ai-os-linux/
cp "$ROOT_DIR/models/catalog.json" "$ROOT_DIR/requirements.txt" config/includes.chroot/opt/ai-os-linux/

lb build
echo "ISO erstellt: $BUILD_DIR/live-image-amd64.hybrid.iso"