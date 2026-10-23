
"""Memeriksa anotasi YOLO untuk dataset flat maupun train/val/test."""
import sys
from collections import Counter
from pathlib import Path

import cv2
import yaml

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dataset_yolo")
ROOT = ROOT.resolve()

if not ROOT.exists():
    sys.exit(f"Folder dataset tidak ditemukan: {ROOT}")

data_yaml = ROOT / "data.yaml"
classes_file = ROOT / "classes.txt"

if data_yaml.exists():
    config = yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    names = config.get("names", [])
    if isinstance(names, dict):
        KELAS = [str(names[k]) for k in sorted(names, key=lambda x: int(x))]
    else:
        KELAS = [str(k) for k in names]
elif classes_file.exists():
    KELAS = [
        k.strip()
        for k in classes_file.read_text(encoding="utf-8").splitlines()
        if k.strip()
    ]
else:
    sys.exit(f"Tidak ditemukan data.yaml atau classes.txt di {ROOT}")

if not KELAS:
    sys.exit("Daftar kelas kosong. Periksa konfigurasi dataset.")

EXT = {".jpg", ".jpeg", ".png"}
WARNA = [(0, 200, 0), (0, 140, 255), (255, 80, 0),
         (200, 0, 200), (0, 200, 200)]
MIN_SISI_PX = 8

# Mendukung dataset flat dan dataset dengan split train/val/test.
splits = []
for split in ("train", "val", "test"):
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split
    if image_dir.is_dir():
        splits.append((split, image_dir, label_dir))

if not splits and (ROOT / "images").is_dir():
    splits.append(("all", ROOT / "images", ROOT / "labels"))

if not splits:
    sys.exit(f"Tidak ditemukan folder gambar yang sesuai di {ROOT / 'images'}")

out_dir = ROOT / "cek_visual"
out_dir.mkdir(exist_ok=True)

hitung = Counter()
masalah = []
total_gambar = tanpa_label = kosong = 0

for split, image_dir, label_dir in splits:
    gambar = sorted(
        p for p in image_dir.iterdir()
        if p.is_file() and p.suffix.lower() in EXT
    )
    total_gambar += len(gambar)
    print(f"\nSplit {split}: {len(gambar)} gambar")

    for img_path in gambar:
        img = cv2.imread(str(img_path))
        if img is None:
            masalah.append(f"{split}/{img_path.name}: gambar tidak dapat dibaca")
            continue

        h, w = img.shape[:2]
        lbl = label_dir / f"{img_path.stem}.txt"

        if not lbl.exists():
            tanpa_label += 1
            masalah.append(f"{split}/{img_path.name}: file label tidak ditemukan")
            continue

        baris = [b for b in lbl.read_text(encoding="utf-8").splitlines() if b.strip()]
        if not baris:
            kosong += 1

        for i, b in enumerate(baris, 1):
            v = b.split()
            if len(v) != 5:
                masalah.append(
                    f"{split}/{lbl.name} baris {i}: harus 5 nilai, ditemukan {len(v)}"
                )
                continue

            try:
                cid_float, cx, cy, bw, bh = map(float, v)
                cid = int(cid_float)
                if cid_float != cid:
                    raise ValueError("class_id bukan bilangan bulat")
            except ValueError:
                masalah.append(f"{split}/{lbl.name} baris {i}: nilai bukan angka yang valid")
                continue

            if not 0 <= cid < len(KELAS):
                masalah.append(f"{split}/{lbl.name} baris {i}: class_id {cid} tidak valid")
                continue

            if not all(0 <= t <= 1 for t in (cx, cy, bw, bh)) or bw <= 0 or bh <= 0:
                masalah.append(f"{split}/{lbl.name} baris {i}: koordinat/ukuran tidak valid")
                continue

            x1 = max(0, min(w - 1, int((cx - bw / 2) * w)))
            y1 = max(0, min(h - 1, int((cy - bh / 2) * h)))
            x2 = max(0, min(w - 1, int((cx + bw / 2) * w)))
            y2 = max(0, min(h - 1, int((cy + bh / 2) * h)))

            if bw * w < MIN_SISI_PX or bh * h < MIN_SISI_PX:
                masalah.append(
                    f"{split}/{lbl.name} baris {i}: kotak sangat kecil "
                    f"({bw*w:.0f}x{bh*h} px)"
                )

            hitung[KELAS[cid]] += 1
            warna = WARNA[cid % len(WARNA)]
            cv2.rectangle(img, (x1, y1), (x2, y2), warna, 2)
            cv2.putText(
                img, KELAS[cid], (x1, max(y1 - 5, 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, warna, 2
            )

        # Pisahkan hasil visual per split agar nama gambar tidak bertabrakan.
        visual_split = out_dir / split
        visual_split.mkdir(exist_ok=True)
        cv2.imwrite(str(visual_split / img_path.name), img)

print("\n===== RINGKASAN VALIDASI =====")
print(f"Total gambar     : {total_gambar}")
print(f"Tanpa file label : {tanpa_label}")
print(f"Label kosong     : {kosong}")
print("Jumlah bounding box per kelas:")
for nama in KELAS:
    print(f"  {nama:10s}: {hitung[nama]}")

print(f"\n{len(masalah)} masalah ditemukan" + (":" if masalah else "."))
for item in masalah[:30]:
    print("  [!]", item)
if len(masalah) > 30:
    print(f"  ... dan {len(masalah) - 30} masalah lainnya")

print(f"\nHasil visual tersimpan di: {out_dir}")
