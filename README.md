# AI OS Linux

Ein schlankes Toolkit zum Herunterladen, Trainieren und Fine-Tunen von Hugging-Face-Sprachmodellen unter Linux. Die Befehle funktionieren mit CPU; für sinnvolle Trainingsgeschwindigkeit wird eine passende CUDA- oder ROCm-PyTorch-Installation empfohlen.

Die geplante Systembasis ist Debian 12 Bookworm. Der Debian-Live-ISO-Prototyp und seine Build-Anleitung liegen in `iso/`.

## Installation

```bash
git clone https://github.com/jodaaileipzig/ai-os-linux.git
cd ai-os-linux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Für NVIDIA-GPUs sollte PyTorch aus dem offiziellen PyTorch-Index passend zur installierten CUDA-Version installiert werden.

## Modellliste

```bash
python scripts/ai_os.py list
python scripts/ai_os.py info qwen2.5-0.5b
```

Die Liste liegt in `models/catalog.json` und kann um weitere Hugging-Face-Repositories ergänzt werden. Modelle mit Zugriffsbeschränkung, etwa Llama, benötigen vorher eine bestätigte Lizenz und einen Hugging-Face-Login:

```bash
huggingface-cli login
```

## Modelle herunterladen

```bash
python scripts/ai_os.py download qwen2.5-0.5b
python scripts/ai_os.py download mistral-7b --output /data/models/mistral-7b
```

Standardmäßig landen Modelle unter `models/downloads/<modell-id>`. Der Download verwendet `huggingface_hub snapshot-download` und unterstützt optional `--revision`.

## Datenformat

Trainingsdaten sind JSONL-Dateien mit einem `text`-Feld, eine Zeile pro Beispiel:

```json
{"text": "Frage: Was ist Linux? Antwort: Ein freies Betriebssystem."}
{"text": "Frage: Was ist Fine-Tuning? Antwort: Das Anpassen eines vortrainierten Modells."}
```

## Trainieren und Fine-Tunen

```bash
python scripts/ai_os.py train \
	--model models/downloads/qwen2.5-0.5b \
	--data data/train.jsonl \
	--output outputs/qwen-trained \
	--epochs 1

python scripts/ai_os.py finetune \
	--model models/downloads/qwen2.5-0.5b \
	--data data/train.jsonl \
	--output outputs/qwen-lora \
	--epochs 1
```

`finetune` verwendet LoRA und benötigt deutlich weniger GPU-Speicher. Die ungefähren VRAM-Werte in der Modellliste beziehen sich auf Inferenz; Training benötigt zusätzlich Speicher für Aktivierungen und Optimizer.

## CLI-Hilfe

```bash
python scripts/ai_os.py --help
```

## Debian-ISO

Voraussetzungen und Build-Schritte stehen in [iso/README.md](iso/README.md):

```bash
sudo apt install live-build debootstrap squashfs-tools xorriso
./iso/build.sh
```

Wenn `live-build fehlt` erscheint, zuerst einmal `./iso/install-dependencies.sh` ausführen.

Das Projekt ist bewusst modular gehalten: Modellkatalog, Download, Volltraining und LoRA-Fine-Tuning können später um eine Weboberfläche, Quantisierung oder lokale Inferenz ergänzt werden.