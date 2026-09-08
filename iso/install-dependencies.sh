#!/usr/bin/env bash
set -euo pipefail

if [[ "$(id -u)" -eq 0 ]]; then
    apt-get update
    apt-get install -y live-build debootstrap squashfs-tools xorriso
else
    command -v sudo >/dev/null || {
        echo "sudo fehlt. Starte dieses Skript als root oder installiere sudo."
        exit 1
    }
    sudo apt-get update
    sudo apt-get install -y live-build debootstrap squashfs-tools xorriso
fi

echo "Alle Debian-ISO-Abhängigkeiten sind installiert."