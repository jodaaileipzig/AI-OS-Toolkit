#!/usr/bin/env python3
"""AI OS Linux: Hugging Face model management and training commands."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "models" / "catalog.json"
DEFAULT_MODELS_DIR = ROOT / "models" / "downloads"


def load_catalog():
    with CATALOG.open(encoding="utf-8") as file:
        return json.load(file)


def find_model(model_id):
    for model in load_catalog():
        if model["id"] == model_id:
            return model
    known = ", ".join(model["id"] for model in load_catalog())
    raise SystemExit(f"Unbekanntes Modell: {model_id}\nVerfügbar: {known}")


def run(command):
    print("$", " ".join(command))
    subprocess.run(command, check=True)


def list_models(_args):
    print(f"{'ID':28} {'PARAMETER':10} {'VRAM':8} BESCHREIBUNG")
    print("-" * 86)
    for model in load_catalog():
        print(f"{model['id']:28} {model['parameters']:10} {model['vram']:8} {model['description']}")


def model_info(args):
    print(json.dumps(find_model(args.model), indent=2, ensure_ascii=False))


def download(args):
    model = find_model(args.model)
    target = Path(args.output or DEFAULT_MODELS_DIR / model["id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "huggingface_hub", "snapshot-download", model["repo"], "--local-dir", str(target)]
    if args.revision:
        command.extend(["--revision", args.revision])
    run(command)


def require_training_dependencies():
    try:
        import datasets  # noqa: F401
        import transformers  # noqa: F401
    except ImportError as error:
        raise SystemExit("Training benötigt optionale Abhängigkeiten. Installiere sie mit: pip install -r requirements.txt") from error


def train(args):
    require_training_dependencies()
    run([sys.executable, str(ROOT / "scripts" / "train.py"), "--model", args.model, "--data", args.data, "--output", args.output, "--epochs", str(args.epochs)])


def finetune(args):
    require_training_dependencies()
    run([sys.executable, str(ROOT / "scripts" / "finetune.py"), "--model", args.model, "--data", args.data, "--output", args.output, "--epochs", str(args.epochs)])


def build_parser():
    parser = argparse.ArgumentParser(prog="ai-os", description="AI OS Linux Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="Hugging-Face-Modellkatalog anzeigen")
    list_parser.set_defaults(function=list_models)

    info_parser = subparsers.add_parser("info", help="Details zu einem Modell anzeigen")
    info_parser.add_argument("model")
    info_parser.set_defaults(function=model_info)

    download_parser = subparsers.add_parser("download", help="Modell herunterladen")
    download_parser.add_argument("model")
    download_parser.add_argument("--output", help="Lokales Zielverzeichnis")
    download_parser.add_argument("--revision", help="Hugging-Face-Revision oder Tag")
    download_parser.set_defaults(function=download)

    for name, function, help_text in (("train", train, "Modell trainieren"), ("finetune", finetune, "Modell fein tunen")):
        command_parser = subparsers.add_parser(name, help=help_text)
        command_parser.add_argument("--model", required=True, help="Hugging-Face-ID oder lokaler Pfad")
        command_parser.add_argument("--data", required=True, help="JSONL-Datei mit Trainingsdaten")
        command_parser.add_argument("--output", required=True, help="Ausgabeordner")
        command_parser.add_argument("--epochs", type=float, default=1.0)
        command_parser.set_defaults(function=function)
    return parser


if __name__ == "__main__":
    arguments = build_parser().parse_args()
    arguments.function(arguments)