#!/usr/bin/env python3
"""Buat subset YOLO dari citra Humanoid Soccer pada kondisi reality.

Contoh:
python scripts/00_preparasi_humanoid_soccer.py --source "../TORSO_21_dataset/data/reality/train" --jumlah 200 --seed 42 --out dataset_yolo

Keluaran memiliki images/, labels/, dan classes.txt. Periksa anotasi sebelum
membagi dataset atau memulai training.
"""
import argparse
import random
import shutil
from pathlib import Path

import yaml

CLASSES = ["ball", "robot", "goalpost"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def box_to_yolo(vector, width, height):
    """Konversi dua titik atau poligon anotasi menjadi bounding box YOLO."""
    if not isinstance(vector, list) or len(vector) < 2 or width <= 0 or height <= 0:
        return None
    try:
        points = [(float(point[0]), float(point[1])) for point in vector]
    except (TypeError, ValueError, IndexError):
        return None

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    left = max(0.0, min(xs))
    right = min(float(width), max(xs))
    top = max(0.0, min(ys))
    bottom = min(float(height), max(ys))
    box_w, box_h = right - left, bottom - top
    if box_w <= 0 or box_h <= 0:
        return None

    return (
        (left + right) / (2 * width),
        (top + bottom) / (2 * height),
        box_w / width,
        box_h / height,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="data/reality/train",
                        help="Folder berisi images/ dan annotations.yaml")
    parser.add_argument("--jumlah", type=int, default=200,
                        help="Jumlah maksimum gambar berlabel yang dipilih")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="dataset_yolo",
                        help="Folder keluaran subset datar")
    args = parser.parse_args()

    source = Path(args.source)
    annotations_file = source / "annotations.yaml"
    images_dir = source / "images"
    if args.jumlah < 1:
        raise SystemExit("--jumlah harus minimal 1")
    if not annotations_file.is_file() or not images_dir.is_dir():
        raise SystemExit(
            "Sumber dataset tidak lengkap. Diperlukan:\n"
            f"  {annotations_file}\n  {images_dir}\n"
            "Pastikan folder reality/train sudah diunduh."
        )

    with annotations_file.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    image_data = data.get("images", {})
    if not isinstance(image_data, dict):
        raise SystemExit("Format anotasi tidak valid: kunci 'images' harus berupa mapping.")

    class_ids = {name: index for index, name in enumerate(CLASSES)}
    candidates, valid_rows, classes_by_image = [], {}, {}
    for image_name, info in image_data.items():
        image_path = images_dir / image_name
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
            continue
        width, height = info.get("width"), info.get("height")
        if not width or not height:
            continue

        rows = []
        for annotation in info.get("annotations", []) or []:
            class_name = annotation.get("type")
            if class_name not in class_ids or annotation.get("in_image") is not True:
                continue
            box = box_to_yolo(annotation.get("vector"), int(width), int(height))
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
    target = min(args.jumlah, len(candidates))

    # Pilih gambar yang mewakili semua kelas terlebih dahulu.
    selected, remaining = [], set(candidates)
    uncovered = set(CLASSES)
    while uncovered and remaining and len(selected) < target:
        best = max(remaining, key=lambda name: len(classes_by_image[name] & uncovered))
        gain = classes_by_image[best] & uncovered
        if not gain:
            break
        selected.append(best)
        remaining.remove(best)
        uncovered -= gain
    if uncovered:
        raise SystemExit("Kelas belum terwakili pada anotasi sumber: " + ", ".join(sorted(uncovered)))

    for name in candidates:
        if len(selected) >= target:
            break
        if name in remaining:
            selected.append(name)
            remaining.remove(name)

    output = Path(args.out)
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Folder output sudah berisi file: {output}. Gunakan folder kosong yang baru.")
    (output / "images").mkdir(parents=True, exist_ok=True)
    (output / "labels").mkdir(parents=True, exist_ok=True)
    (output / "classes.txt").write_text("\n".join(CLASSES) + "\n", encoding="utf-8")

    box_counts = {name: 0 for name in CLASSES}
    for image_name in selected:
        shutil.copy2(images_dir / image_name, output / "images" / image_name)
        label_path = output / "labels" / (Path(image_name).stem + ".txt")
        with label_path.open("w", encoding="utf-8") as file:
            for row in valid_rows[image_name]:
                class_id, cx, cy, box_w, box_h = row
                file.write(f"{class_id} {cx:.6f} {cy:.6f} {box_w:.6f} {box_h:.6f}\n")
                box_counts[CLASSES[class_id]] += 1

    print("Subset Humanoid Soccer selesai dibuat.")
    print(f"Gambar yang memenuhi syarat: {len(candidates)}")
    print(f"Gambar terpilih: {len(selected)}")
    for name in CLASSES:
        print(f"  {name}: {box_counts[name]} bounding box")
    print(f"Output: {output.resolve()}")
    print(f"Langkah berikutnya: python scripts/01_cek_anotasi.py {output}")


if __name__ == "__main__":
    main()
