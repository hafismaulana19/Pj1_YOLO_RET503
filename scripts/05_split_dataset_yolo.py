"""Bagi subset YOLO datar menjadi train/validation/test.

Input: folder berisi images/, labels/, classes.txt.
Output default: dataset_humanoid_soccer/ dengan data.yaml dan split 70/20/10.
Pemakaian: python scripts/05_split_dataset_yolo.py dataset_yolo dataset_humanoid_soccer
"""
import random
import shutil
import sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset_yolo")
DST = Path(sys.argv[2] if len(sys.argv) > 2 else "dataset_humanoid_soccer")
PROPORTIONS = {"train": 0.7, "val": 0.2, "test": 0.1}
SEED = 42


def main():
    classes_file = SRC / "classes.txt"
    images_dir = SRC / "images"
    labels_dir = SRC / "labels"
    if not classes_file.is_file() or not images_dir.is_dir() or not labels_dir.is_dir():
        raise SystemExit(f"Input tidak valid. Diperlukan images/, labels/, dan classes.txt di {SRC}.")
    if DST.exists() and any(DST.iterdir()):
        raise SystemExit(f"Folder output sudah berisi file: {DST}. Gunakan folder kosong yang baru.")

    classes = [name.strip() for name in classes_file.read_text(encoding="utf-8").splitlines() if name.strip()]
    images = sorted(path for path in images_dir.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png"})
    images = [image for image in images if (labels_dir / f"{image.stem}.txt").is_file()]
    if not images:
        raise SystemExit(f"Tidak ada gambar berlabel di {SRC}.")
    random.Random(SEED).shuffle(images)

    count = len(images)
    train_count = int(count * PROPORTIONS["train"])
    val_count = int(count * PROPORTIONS["val"])
    partitions = {
        "train": images[:train_count],
        "val": images[train_count:train_count + val_count],
        "test": images[train_count + val_count:],
    }

    for split_name, split_images in partitions.items():
        split_image_dir = DST / "images" / split_name
        split_label_dir = DST / "labels" / split_name
        split_image_dir.mkdir(parents=True, exist_ok=True)
        split_label_dir.mkdir(parents=True, exist_ok=True)
        for image in split_images:
            shutil.copy2(image, split_image_dir / image.name)
            shutil.copy2(labels_dir / f"{image.stem}.txt", split_label_dir / f"{image.stem}.txt")
        print(f"{split_name:5s}: {len(split_images)} gambar")

    yaml_lines = [
        f"path: {DST.resolve().as_posix()}",
        "train: images/train",
        "val: images/val",
        "test: images/test",
        "names:",
        *[f"  {index}: {name}" for index, name in enumerate(classes)],
    ]
    (DST / "data.yaml").write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")
    print(f"\nKonfigurasi dibuat: {DST / 'data.yaml'}")
    print(f"Seed pembagian: {SEED}")


if __name__ == "__main__":
    main()
