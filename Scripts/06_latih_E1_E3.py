"""Latih dan evaluasi validasi untuk eksperimen E1 dan E3 menggunakan YOLO26n."""
import argparse
import csv
import getpass
import hashlib
import platform
import time
from datetime import datetime
from pathlib import Path

from ultralytics import YOLO

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--nim", required=True)
parser.add_argument("--nama", required=True)
parser.add_argument("--data", default="dataset_humanoid_soccer/data.yaml")
parser.add_argument("--model", default="yolo26n")
parser.add_argument("--epochs", type=int, default=100)
parser.add_argument("--imgsz", type=int, default=416)
parser.add_argument("--batch", type=int, default=4)
parser.add_argument("--patience", type=int, default=20)
parser.add_argument("--device", default="cpu")
parser.add_argument("--ubah", default="imgsz=640", help="Parameter E3 yang diubah, format key=value")
args = parser.parse_args()

key, value = args.ubah.split("=", 1)
try:
    value = int(value)
except ValueError:
    try:
        value = float(value)
    except ValueError:
        pass

data_yaml = Path(args.data)
if not data_yaml.is_file():
    raise SystemExit(f"File konfigurasi tidak ditemukan: {data_yaml}. Siapkan dataset lebih dulu.")

project_dir = Path("hasil_praktik").resolve()
report_dir = Path("laporan")
report_dir.mkdir(parents=True, exist_ok=True)


def dataset_fingerprint(dataset_root):
    digest = hashlib.sha256()
    label_root = dataset_root / "labels"
    for label_file in sorted(label_root.rglob("*.txt")):
        digest.update(label_file.read_bytes())
    return digest.hexdigest()[:12].upper()


def train_experiment(name, model_file, pretrained, **changes):
    config = {
        "data": str(data_yaml.resolve()),
        "epochs": args.epochs,
        "patience": args.patience,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "seed": 0,
        "deterministic": True,
        "project": str(project_dir),
        "name": name,
        "exist_ok": False,
        "pretrained": pretrained,
        "plots": True,
        "verbose": False,
    }
    config.update(changes)
    print(f"\n=== {name} ===")
    print(f"Model: {model_file} | imgsz={config['imgsz']} | device={args.device}")

    model = YOLO(model_file)
    start = time.time()
    model.train(**config)
    training_minutes = (time.time() - start) / 60

    best_weights = Path(model.trainer.save_dir) / "weights" / "best.pt"
    if not best_weights.is_file():
        raise FileNotFoundError(f"Bobot terbaik tidak ditemukan: {best_weights}")

    metrics = YOLO(str(best_weights)).val(
        data=str(data_yaml.resolve()),
        split="val",
        imgsz=config["imgsz"],
        batch=args.batch,
        device=args.device,
        plots=True,
        verbose=False,
    )
    return {
        "eksperimen": name,
        "perubahan": ", ".join(f"{key}={val}" for key, val in changes.items()) or "-",
        "pretrained": pretrained,
        "mAP50": round(metrics.box.map50, 4),
        "mAP50-95": round(metrics.box.map, 4),
        "precision": round(metrics.box.mp, 4),
        "recall": round(metrics.box.mr, 4),
        "inferensi_ms": round(metrics.speed["inference"], 2),
        "waktu_latih_menit": round(training_minutes, 2),
        "imgsz": config["imgsz"],
        "bobot": best_weights.as_posix(),
    }


results = [
    train_experiment("E1_final", f"{args.model}.pt", True),
    train_experiment("E3_final", f"{args.model}.pt", True, **{key: value}),
]

dataset_root = data_yaml.parent
fingerprint = dataset_fingerprint(dataset_root)
lines = [
    "=" * 86,
    "HASIL EKSPERIMEN YOLO — HUMANOID SOCCER",
    "=" * 86,
    f"NIM / Nama    : {args.nim} / {args.nama}",
    f"Waktu         : {datetime.now():%d-%m-%Y %H:%M:%S}",
    f"Komputer/user : {platform.node()} / {getpass.getuser()}",
    f"Dataset       : {dataset_root}",
    f"Sidik jari    : {fingerprint}",
    f"Model         : {args.model} | epochs={args.epochs} | batch={args.batch} | device={args.device}",
    "=" * 86,
    f"{'Eksperimen':18s}{'imgsz':>8s}{'mAP50':>10s}{'mAP50-95':>11s}{'P':>9s}{'R':>9s}{'ms':>9s}{'menit':>9s}",
]
for result in results:
    lines.append(
        f"{result['eksperimen']:18s}{result['imgsz']:8d}{result['mAP50']:10.4f}"
        f"{result['mAP50-95']:11.4f}{result['precision']:9.4f}{result['recall']:9.4f}"
        f"{result['inferensi_ms']:9.2f}{result['waktu_latih_menit']:9.2f}"
    )
lines += [
    "=" * 86,
    "Metrik di atas berasal dari split validation. Evaluasi test dilakukan dengan skrip terpisah.",
    "=" * 86,
]
report_text = "\n".join(lines) + "\n"
print("\n" + report_text)

txt_path = report_dir / f"hasil_praktik_{args.nim}_E1_E3_final.txt"
csv_path = report_dir / f"hasil_praktik_{args.nim}_E1_E3_final.csv"
txt_path.write_text(report_text, encoding="utf-8")
with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

print(f"Laporan TXT: {txt_path}")
print(f"Laporan CSV: {csv_path}")
print(f"Grafik dan bobot lokal: {project_dir}")
