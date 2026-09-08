# Debian-ISO bauen

AI OS Linux verwendet Debian 12 Bookworm als stabile Basis und `live-build` für das bootfähige Hybrid-ISO.

## Voraussetzungen

Auf einem Debian- oder Ubuntu-Buildsystem:

```bash
sudo apt update
sudo apt install live-build debootstrap squashfs-tools xorriso
```

Alternativ installiert das Projekt die Werkzeuge selbst:

```bash
./iso/install-dependencies.sh
```

Der Build benötigt mehrere Gigabyte freien Speicher und eine funktionierende Internetverbindung. Er wird nicht als root gestartet.

## Build

```bash
./iso/build.sh
```

Das Ergebnis liegt danach unter `iso/work/live-image-amd64.hybrid.iso` und kann mit Rufus, Balena Etcher oder `dd` auf einen USB-Stick geschrieben werden.

Zum Testen in QEMU:

```bash
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom iso/work/live-image-amd64.hybrid.iso
```

Die Python-Abhängigkeiten für Training und Fine-Tuning sind bewusst nicht Teil des ISO-Images. Sie können nach dem Start mit `pip install -r /opt/ai-os-linux/requirements.txt` installiert werden; GPU-spezifisches PyTorch sollte passend zur Hardware installiert werden.