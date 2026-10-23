#!/usr/bin/env python3
"""Buat subset YOLO TORSO-21 dengan memastikan setiap kelas terwakili.

Kelas target: ball, robot, goalpost.
Contoh:
python scripts/00_preparasi_torso21_balanced.py --source "C:/.../TORSO_21_dataset/data/reality/train" --jumlah 200 --out dataset_yolo_v2
"""
import argparse
import random
import shutil
from pathlib import Path

import yaml

CLASSES = ["ball", "robot", "goalpost"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def box_to_yolo(vector, width, height):
    """Konversi vector TORSO-21 dua titik atau poligon empat titik ke YOLO."""
    if not isinstance(vector, list) or len(vector) < 2:
        return None
    try:
        points = [(float(point[0]), float(point[1])) for point in vector]
    except (TypeError, ValueError, IndexError):
        return None
    if len(points) < 2:
        return None

    # TORSO-21 dapat menyimpan goalpost sebagai poligon empat titik.
    # Ambil bounding rectangle dari semua titik untuk format YOLO.
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)
    left, right = max(0.0, left), min(float(width), right)
    top, bottom = max(0.0, top), min(float(height), bottom)
    bw, bh = right - left, bottom - top
    if width <= 0 or height <= 0 or bw <= 0 or bh <= 0:
        return None
    return ((left + right) / 2 / width, (top + bottom) / 2 / height,
            bw / width, bh / height)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="data/reality/train",
                        help="Folder TORSO-21 reality/train")
    parser.add_argument("--jumlah", type=int, default=200,
                        help="Jumlah maksimum gambar subset")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="dataset_yolo_v2",
                        help="Folder keluaran baru; jangan gunakan folder yang sudah berisi data")
    args = parser.parse_args()

    source = Path(args.source)
    annotations_file = source / "annotations.yaml"
    images_dir = source / "images"
    if not annotations_file.is_file() or not images_dir.is_dir():
        raise SystemExit(f"Dataset tidak lengkap. Diperlukan:\n  {annotations_file}\n  {images_dir}")
    if args.jumlah < len(CLASSES):
        raise SystemExit("--jumlah harus minimal 3 agar setiap kelas bisa diwakili.")

    with annotations_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    image_data = data.get("images", {})
    if not isinstance(image_data, dict):
        raise SystemExit("Format annotations.yaml tidak sesuai: 'images' harus berupa mapping.")

    class_ids = {name: i for i, name in enumerate(CLASSES)}
    candidates = []
    valid_rows = {}
    classes_by_image = {}
    for image_name, info in image_data.items():
        image_path = images_dir / image_name
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
            continue
        width, height = info.get("width"), info.get("height")
        if not width or not height:
            continue
        rows = []
        for ann in info.get("annotations", []) or []:
            class_name = ann.get("type")
            if class_name not in class_ids or ann.get("in_image") is not True:
                continue
            box = box_to_yolo(ann.get("vector"), int(width), int(height))
            if box is not None:
                rows.append((class_ids[class_name], *box))
        if rows:
            candidates.append(image_name)
            valid_rows[image_name] = rows
            classes_by_image[image_name] = {CLASSES[row[0]] for row in rows}

    if not candidates:
        raise SystemExit("Tidak ditemukan gambar berlabel ball/robot/goalpost.")

    rng = random.Random(args.seed)
    rng.shuffle(candidates)

    # Greedy set-cover: pilih gambar yang menutup kelas yang belum terwakili.
    selected = []
    uncovered = set(CLASSES)
    remaining = set(candidates)
    while uncovered and remaining and len(selected) < args.jumlah:
        best = max(remaining, key=lambda name: len(classes_by_image[name] & uncovered))
        gain = classes_by_image[best] & uncovered
        if not gain:
            break
        selected.append(best)
        remaining.remove(best)
        uncovered -= gain

    if uncovered:
        raise SystemExit(
            "Tidak dapat mewakili semua kelas dari kandidat yang valid: "
            + ", ".join(sorted(uncovered))
            + ". Periksa struktur anotasi dan nilai in_image."
        )

    # Isi sisa subset secara acak tanpa duplikasi.
    for name in candidates:
        if len(selected) >= min(args.jumlah, len(candidates)):
            break
        if name in remaining:
            selected.append(name)
            remaining.remove(name)

    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Folder keluaran sudah berisi data: {out}. Pilih nama folder baru.")
    (out / "images").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    (out / "classes.txt").write_text("\n".join(CLASSES) + "\n", encoding="utf-8")

    class_counts = [0] * len(CLASSES)
    images_per_class = {name: 0 for name in CLASSES}
    for image_name in selected:
        shutil.copy2(images_dir / image_name, out / "images" / image_name)
        with (out / "labels" / (Path(image_name).stem + ".txt")).open("w", encoding="utf-8") as f:
            for row in valid_rows[image_name]:
                class_id, cx, cy, bw, bh = row
                f.write(f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")
                class_counts[class_id] += 1
        for class_name in classes_by_image[image_name]:
            images_per_class[class_name] += 1

    print("Subset TORSO-21 REAL-WORLD seimbang selesai dibuat.")
    print(f"Gambar tersedia dengan anotasi: {len(candidates)}")
    print(f"Gambar yang disalin: {len(selected)}")
    print("Kelas:", ", ".join(CLASSES))
    for class_id, class_name in enumerate(CLASSES):
        print(f"  {class_name}: {class_counts[class_id]} bounding box pada {images_per_class[class_name]} gambar")
    print(f"Output: {out.resolve()}")
    print("Langkah berikutnya: validasi dengan scripts/01_cek_anotasi.py.")


if __name__ == "__main__":
    main()
