"""Evaluasi bobot E1 dan E3 pada split test dan simpan CSV metrik.

Contoh:
python scripts/07_evaluasi_test.py --data dataset_humanoid_soccer/data.yaml --e1 hasil_praktik/E1_final/weights/best.pt --e3 hasil_praktik/E3_final/weights/best.pt
"""
import argparse
import csv
from pathlib import Path

import yaml
from ultralytics import YOLO

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--data", default="dataset_humanoid_soccer/data.yaml")
parser.add_argument("--e1", default="hasil_praktik/E1_final/weights/best.pt")
parser.add_argument("--e3", default="hasil_praktik/E3_final/weights/best.pt")
parser.add_argument("--imgsz-e1", type=int, default=416)
parser.add_argument("--imgsz-e3", type=int, default=640)
parser.add_argument("--batch", type=int, default=4)
parser.add_argument("--device", default="cpu")
parser.add_argument("--output", default="laporan/hasil_test_humanoid_soccer.csv")
args = parser.parse_args()

data_yaml = Path(args.data)
if not data_yaml.is_file():
    raise SystemExit(f"File konfigurasi tidak ditemukan: {data_yaml}")

config = yaml.safe_load(data_yaml.read_text(encoding="utf-8")) or {}
dataset_root = Path(config.get("path") or data_yaml.parent)
if not dataset_root.is_absolute():
    dataset_root = (data_yaml.parent / dataset_root).resolve()

test_image_dir = dataset_root / "images" / "test"
test_label_dir = dataset_root / "labels" / "test"
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
number_images = sum(1 for file in test_image_dir.iterdir()
                    if file.is_file() and file.suffix.lower() in image_extensions) if test_image_dir.is_dir() else 0
number_objects = 0
if test_label_dir.is_dir():
    for label_file in test_label_dir.glob("*.txt"):
        number_objects += sum(1 for line in label_file.read_text(encoding="utf-8").splitlines() if line.strip())

experiments = [
    ("E1", Path(args.e1), args.imgsz_e1),
    ("E3", Path(args.e3), args.imgsz_e3),
]
rows = []
for name, weights, image_size in experiments:
    if not weights.is_file():
        raise SystemExit(f"Bobot {name} tidak ditemukan: {weights}")
    print(f"Evaluasi {name}: {weights} | imgsz={image_size}")
    metrics = YOLO(str(weights)).val(
        data=str(data_yaml.resolve()),
        split="test",
        imgsz=image_size,
        batch=args.batch,
        device=args.device,
        plots=True,
        verbose=False,
    )
    rows.append({
        "eksperimen": name,
        "imgsz": image_size,
        "split": "test",
        "jumlah_gambar": number_images,
        "jumlah_objek": number_objects,
        "precision": round(metrics.box.mp, 4),
        "recall": round(metrics.box.mr, 4),
        "mAP50": round(metrics.box.map50, 4),
        "mAP50-95": round(metrics.box.map, 4),
        "inferensi_ms": round(metrics.speed["inference"], 2),
    })

output = Path(args.output)
output.parent.mkdir(parents=True, exist_ok=True)
with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV evaluasi test tersimpan: {output}")
for row in rows:
    print(row)
