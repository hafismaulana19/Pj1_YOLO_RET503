
"""Praktik RET503: eksperimen YOLO E1 dan E3 menggunakan CPU."""
import argparse
import csv
import getpass
import hashlib
import platform
import time
from datetime import datetime
from pathlib import Path

from ultralytics import YOLO

p = argparse.ArgumentParser()
p.add_argument("--nim", required=True)
p.add_argument("--nama", required=True)
p.add_argument("--data", default="dataset_v1/data.yaml")
p.add_argument("--model", default="yolo26n")
p.add_argument("--epochs", type=int, default=100)
p.add_argument("--imgsz", type=int, default=416)
p.add_argument("--batch", type=int, default=4)
p.add_argument("--patience", type=int, default=20)
p.add_argument("--device", default="cpu")
p.add_argument("--ubah", default="imgsz=640")
args = p.parse_args()

kunci, nilai = args.ubah.split("=", 1)
try:
    nilai = int(nilai)
except ValueError:
    try:
        nilai = float(nilai)
    except ValueError:
        pass

DATA = Path(args.data)
if not DATA.exists():
    raise SystemExit(
        f"{DATA} tidak ditemukan. Periksa lokasi dataset terlebih dahulu."
    )

PROJECT = Path("hasil_praktik").resolve()


def sidik_jari_dataset(root):
    h = hashlib.sha256()
    for f in sorted((root / "labels").rglob("*.txt")):
        h.update(f.read_bytes())
    return h.hexdigest()[:12].upper()


def latih(nama, model_file, pretrained, **ubah):
    cfg = dict(
        data=str(DATA),
        epochs=args.epochs,
        patience=args.patience,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        seed=0,
        deterministic=True,
        project=str(PROJECT),
        name=nama,
        exist_ok=False,
        pretrained=pretrained,
        plots=True,
        verbose=False,
    )
    cfg.update(ubah)

    print(
        f"\n=== {nama} ===\n"
        f"Model: {model_file} | pretrained={pretrained}\n"
        f"Perangkat: {args.device} | imgsz={cfg['imgsz']}\n"
        f"Epochs: {cfg['epochs']} | batch={cfg['batch']}"
    )

    model = YOLO(model_file)
    t0 = time.time()
    model.train(**cfg)
    menit = (time.time() - t0) / 60

    best = Path(model.trainer.save_dir) / "weights" / "best.pt"
    if not best.exists():
        raise FileNotFoundError(f"Bobot terbaik tidak ditemukan: {best}")

    m = YOLO(str(best)).val(
        data=str(DATA),
        split="val",
        imgsz=cfg["imgsz"],
        batch=args.batch,
        device=args.device,
        plots=False,
        verbose=False,
    )

    return {
        "eksperimen": nama,
        "perubahan": ", ".join(
            f"{k}={v}" for k, v in ubah.items()
        ) or "-",
        "pretrained": pretrained,
        "mAP50": round(m.box.map50, 4),
        "mAP50-95": round(m.box.map, 4),
        "precision": round(m.box.mp, 4),
        "recall": round(m.box.mr, 4),
        "inferensi_ms": round(m.speed["inference"], 2),
        "waktu_latih_menit": round(menit, 2),
        "imgsz": cfg["imgsz"],
        "bobot": str(best),
    }


# E1: baseline pretrained, imgsz=416
hasil = [
    latih(
        "E1_final",
        f"{args.model}.pt",
        True,
    ),

    # E3: pretrained yang sama, hanya imgsz diubah menjadi 640
    latih(
        "E3_final",
        f"{args.model}.pt",
        True,
        **{kunci: nilai},
    ),
]


garis = "=" * 90
baris = [
    garis,
    "PRAKTIK TERPADU MINGGU 4-7 - RET503",
    garis,
    f"NIM / Nama    : {args.nim} / {args.nama}",
    f"Waktu         : {datetime.now():%d-%m-%Y %H:%M:%S}",
    f"Komputer/user : {platform.node()} / {getpass.getuser()}",
    f"Dataset       : {DATA.parent}",
    f"Sidik jari    : {sidik_jari_dataset(DATA.parent)}",
    f"Pengaturan    : model {args.model}, epochs {args.epochs}, "
    f"imgsz {args.imgsz}, batch {args.batch}, device {args.device}",
    garis,
    f"{'Eksperimen':18s}{'Perubahan':15s}{'mAP50':>9s}"
    f"{'mAP50-95':>11s}{'P':>8s}{'R':>8s}"
    f"{'ms':>8s}{'menit':>9s}",
]

for r in hasil:
    baris.append(
        f"{r['eksperimen']:18s}{r['perubahan']:15s}"
        f"{r['mAP50']:9.3f}{r['mAP50-95']:11.3f}"
        f"{r['precision']:8.3f}{r['recall']:8.3f}"
        f"{r['inferensi_ms']:8.1f}"
        f"{r['waktu_latih_menit']:9.1f}"
    )

baris += [
    garis,
    "Pemilihan model dilakukan berdasarkan mAP50-95 pada data validasi.",
    "Evaluasi TEST dilakukan terpisah setelah model final ditentukan.",
    garis,
]

laporan = "\n".join(baris)
print("\n" + laporan)

Path(f"hasil_praktik_{args.nim}_E1_E3_final.txt").write_text(
    laporan + "\n", encoding="utf-8"
)

with open(
    f"hasil_praktik_{args.nim}_E1_E3_final.csv",
    "w",
    newline="",
    encoding="utf-8",
) as f:
    w = csv.DictWriter(f, fieldnames=list(hasil[0].keys()))
    w.writeheader()
    w.writerows(hasil)

print(
    f"\nLaporan tersimpan untuk NIM {args.nim}."
    f"\nGrafik dan bobot model berada di: {PROJECT}"
)
