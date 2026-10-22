#!/usr/bin/env python3
"""Buat subset YOLO dari koleksi real-world TORSO-21.

Jalankan dari root repo TORSO_21_dataset atau berikan --source:
  python scripts/00_preparasi_torso21.py --source ../TORSO_21_dataset/data/reality/train --jumlah 200 --out dataset_yolo

Skrip mengambil gambar dari koleksi REALITY train saja, memilih gambar yang
memiliki minimal satu objek ball/robot/goalpost, lalu mengubah bounding box
TORSO-21 (vector dua titik dalam piksel) menjadi label YOLO ter-normalisasi.
Data yang dihasilkan masih perlu diperiksa dengan scripts/01_cek_anotasi.py
dan dibagi dengan scripts/05_split_dataset_yolo.py.
"""
import argparse
import random
import shutil
from pathlib import Path

import yaml

CLASSES = ["ball", "robot", "goalpost"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def box_to_yolo(vector, width, height):
    """Convert TORSO-21 [[x1,y1],[x2,y2]] pixel corners to YOLO cx,cy,w,h."""
    if not isinstance(vector, list) or len(vector) != 2:
        return None
    try:
        x1, y1 = map(float, vector[0])
        x2, y2 = map(float, vector[1])
    except (TypeError, ValueError):
        return None
    left, right = sorted((x1, x2))
    top, bottom = sorted((y1, y2))
    left, right = max(0.0, left), min(float(width), right)
    top, bottom = max(0.0, top), min(float(height), bottom)
    bw, bh = right - left, bottom - top
    if width <= 0 or height <= 0 or bw <= 0 or bh <= 0:
        return None
    cx = (left + right) / 2 / width
    cy = (top + bottom) / 2 / height
    return cx, cy, bw / width, bh / height


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/reality/train",
                        help="Folder koleksi real-world TORSO-21 train")
    parser.add_argument("--jumlah", type=int, default=200,
                        help="Jumlah maksimum gambar yang dipilih (default: 200)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="dataset_yolo",
                        help="Folder keluaran subset YOLO")
    args = parser.parse_args()

    source = Path(args.source)
    annotations_file = source / "annotations.yaml"
    images_dir = source / "images"
    if not annotations_file.is_file() or not images_dir.is_dir():
        raise SystemExit(
            "Dataset tidak ditemukan. Diperlukan file dan folder berikut:\n"
            f"  {annotations_file}\n  {images_dir}\n"
            "Unduh koleksi reality TORSO-21 terlebih dahulu; lihat README repositori resmi."
        )
    if args.jumlah < 1:
        raise SystemExit("--jumlah harus minimal 1")

    with annotations_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    image_data = data.get("images", {})
    if not isinstance(image_data, dict):
        raise SystemExit("Format annotations.yaml tidak sesuai: kunci 'images' harus berupa mapping.")

    class_ids = {name: i for i, name in enumerate(CLASSES)}
    candidates = []
    valid_rows = {}
    for image_name, info in image_data.items():
        image_path = images_dir / image_name
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
            continue
        width, height = info.get("width"), info.get("height")
        if not width or not height:
            continue
        rows = []
        for ann in info.get("annotations", []) or []:
            if ann.get("type") not in class_ids or ann.get("in_image") is not True:
                continue
            box = box_to_yolo(ann.get("vector"), int(width), int(height))
            if box is None:
                continue
            rows.append((class_ids[ann["type"]], *box))
        if rows:
            candidates.append(image_name)
            valid_rows[image_name] = rows

    if not candidates:
        raise SystemExit("Tidak ditemukan gambar berlabel ball/robot/goalpost. Periksa struktur dataset.")
    rng = random.Random(args.seed)
    rng.shuffle(candidates)
    selected = candidates[:min(args.jumlah, len(candidates))]

    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Folder keluaran {out} sudah berisi data. Pilih folder baru agar data lama tidak tertimpa.")
    (out / "images").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    (out / "classes.txt").write_text("\n".join(CLASSES) + "\n", encoding="utf-8")

    class_counts = [0] * len(CLASSES)
    for image_name in selected:
        shutil.copy2(images_dir / image_name, out / "images" / image_name)
        label_path = out / "labels" / (Path(image_name).stem + ".txt")
        with label_path.open("w", encoding="utf-8") as f:
            for row in valid_rows[image_name]:
                class_id, cx, cy, bw, bh = row
                f.write(f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")
                class_counts[class_id] += 1

    print("Subset TORSO-21 REAL-WORLD selesai dibuat.")
    print(f"Gambar tersedia dengan anotasi: {len(candidates)}")
    print(f"Gambar yang disalin: {len(selected)}")
    print(f"Kelas: {', '.join(CLASSES)}")
    for name, count in zip(CLASSES, class_counts):
        print(f"  {name}: {count} bounding box")
    print(f"Output: {out.resolve()}")
    print("Langkah berikutnya: jalankan scripts/01_cek_anotasi.py pada folder output,")
    print("periksa gambar di folder cek_visual, lalu jalankan scripts/05_split_dataset_yolo.py.")


if __name__ == "__main__":
    main()
