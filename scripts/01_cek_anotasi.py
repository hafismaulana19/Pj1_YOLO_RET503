"""Validasi label YOLO dan simpan visualisasi bounding box untuk inspeksi.

Mendukung dataset datar (images/, labels/, classes.txt) maupun split
Ultralytics (images/train|val|test, labels/train|val|test, data.yaml).
Pemakaian: python scripts/01_cek_anotasi.py dataset_yolo
           python scripts/01_cek_anotasi.py dataset_humanoid_soccer
"""
import sys
from collections import Counter
from pathlib import Path

import cv2
import yaml

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset_yolo")
IMAGE_ROOT = ROOT / "images"
if not IMAGE_ROOT.is_dir():
    raise SystemExit(f"Folder gambar tidak ditemukan: {IMAGE_ROOT}")

yaml_path = ROOT / "data.yaml"
classes_path = ROOT / "classes.txt"
if yaml_path.is_file():
    config = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    names = config.get("names", {})
    if isinstance(names, list):
        KELAS = [str(name) for name in names]
    elif isinstance(names, dict):
        KELAS = [str(names[key]) for key in sorted(names, key=lambda value: int(value))]
    else:
        raise SystemExit("data.yaml harus memiliki 'names' berupa list atau mapping.")
elif classes_path.is_file():
    KELAS = [name.strip() for name in classes_path.read_text(encoding="utf-8").splitlines() if name.strip()]
else:
    raise SystemExit(f"Tidak ditemukan {yaml_path} atau {classes_path}.")

MIN_SIDE_PX = 8
COLORS = [(0, 200, 0), (0, 140, 255), (255, 80, 0), (200, 0, 200), (0, 200, 200)]
images = sorted(path for path in IMAGE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"})
visual_root = ROOT / "cek_visual"
counts = Counter()
issues = []
missing_labels = 0
empty_labels = 0
processed = 0

if not images:
    raise SystemExit(f"Tidak ada file gambar di {IMAGE_ROOT}.")

for image_path in images:
    relative_image = image_path.relative_to(IMAGE_ROOT)
    label_path = (ROOT / "labels" / relative_image).with_suffix(".txt")
    image = cv2.imread(str(image_path))
    if image is None:
        issues.append(f"{relative_image.as_posix()}: gambar tidak bisa dibaca")
        continue

    height, width = image.shape[:2]
    if not label_path.is_file():
        missing_labels += 1
        issues.append(f"{relative_image.as_posix()}: file label tidak ditemukan")
        continue

    lines = [line for line in label_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        empty_labels += 1

    for line_number, line in enumerate(lines, start=1):
        values = line.split()
        if len(values) != 5:
            issues.append(f"{label_path.relative_to(ROOT).as_posix()} baris {line_number}: harus 5 nilai")
            continue
        try:
            class_id = int(values[0])
            cx, cy, box_w, box_h = map(float, values[1:])
        except ValueError:
            issues.append(f"{label_path.relative_to(ROOT).as_posix()} baris {line_number}: nilai bukan angka")
            continue
        if not 0 <= class_id < len(KELAS):
            issues.append(f"{label_path.relative_to(ROOT).as_posix()} baris {line_number}: class_id {class_id} di luar rentang")
            continue
        if not all(0 <= value <= 1 for value in (cx, cy, box_w, box_h)):
            issues.append(f"{label_path.relative_to(ROOT).as_posix()} baris {line_number}: nilai tidak ternormalisasi")
        x1, y1 = int((cx - box_w / 2) * width), int((cy - box_h / 2) * height)
        x2, y2 = int((cx + box_w / 2) * width), int((cy + box_h / 2) * height)
        if box_w * width < MIN_SIDE_PX or box_h * height < MIN_SIDE_PX:
            issues.append(f"{label_path.relative_to(ROOT).as_posix()} baris {line_number}: kotak sangat kecil ({box_w * width:.0f}x{box_h * height:.0f} px)")
        counts[KELAS[class_id]] += 1
        color = COLORS[class_id % len(COLORS)]
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, KELAS[class_id], (x1, max(y1 - 5, 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    output_path = visual_root / relative_image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    processed += 1

print(f"Root dataset       : {ROOT}")
print(f"Gambar ditemukan   : {len(images)}")
print(f"Gambar diproses    : {processed}")
print(f"Label hilang       : {missing_labels}")
print(f"Label kosong       : {empty_labels}")
print("Jumlah bounding box:")
for name in KELAS:
    print(f"  {name:10s}: {counts[name]}")
print(f"Masalah/peringatan : {len(issues)}")
for issue in issues[:30]:
    print("  [!] ", issue)
print(f"Visualisasi        : {visual_root.resolve()}")
