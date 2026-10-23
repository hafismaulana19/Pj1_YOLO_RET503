# Humanoid Soccer — YOLO Object Detection

Repositori praktikum RET503 untuk eksperimen deteksi objek **Humanoid Soccer** menggunakan YOLO26n pretrained.

## Ringkasan Proyek

- **Kelas deteksi:** `ball`, `robot`, `goalpost`
- **Subset eksperimen:** 200 gambar — 140 train, 40 validation, 20 test
- **Eksperimen:** E1 (`imgsz=416`) dan E3 (`imgsz=640`)
- **Perangkat pelatihan:** CPU
- **Sumber dataset:** [bit-bots/TORSO_21_dataset](https://github.com/bit-bots/TORSO_21_dataset)

## Hasil Eksperimen

### E1 — Input 416 px

![E1 training results](<Eksperimen E1 dan E3/E1/results.png>)

![E1 validation predictions](<Eksperimen E1 dan E3/E1/val_batch0_pred.jpg>)

### E3 — Input 640 px

![E3 training results](<Eksperimen E1 dan E3/E3/results.png>)

![E3 validation predictions](<Eksperimen E1 dan E3/E3/val_batch0_pred.jpg>)

### Metrik Validasi

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.9109 | 0.8902 |
| Recall | 0.7609 | 0.8283 |
| mAP50 | 0.8200 | 0.8686 |
| mAP50–95 | 0.5754 | 0.6252 |
| Inferensi per gambar | 10.88 ms | 24.18 ms |
| Waktu pelatihan | 24.59 menit | 57.40 menit |

### Metrik Test

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Inferensi per gambar | 10.6 ms | 22.9 ms |

Pada validasi, E3 mendapat recall, mAP50, dan mAP50–95 lebih tinggi, tetapi lebih lambat. Pada test subset, E1 memperoleh nilai lebih tinggi pada metrik yang dicatat dan inferensi lebih cepat. Karena test hanya mencakup 20 gambar (38 objek), hasil ini terbatas pada subset praktikum.

## Struktur Repository

```text
Pj1_YOLO_RET503/
├── dataset/                 # Gambar, label, dan data.yaml untuk eksperimen
├── data_proyek/             # Panduan proyek dan konfigurasi referensi
├── Eksperimen E1 dan E3/    # Grafik serta hasil eksperimen E1 dan E3
│   ├── E1/
│   └── E3/
├── Laporan/                 # Rekap hasil praktikum CSV/TXT
├── Scripts/                 # Skrip persiapan, validasi, training, evaluasi
├── .gitignore               # Aturan file lokal yang tidak dilacak Git
└── README.md                # Dokumentasi utama
```

## Isi Folder

- **`dataset/`** — gambar, anotasi, dan konfigurasi dataset yang digunakan.
- **`data_proyek/`** — panduan sumber data dan konfigurasi referensi.
- **`Eksperimen E1 dan E3/`** — grafik training, confusion matrix, `results.csv`, serta contoh prediksi.
- **`Laporan/`** — rekap metrik praktikum dan hasil test.
- **`Scripts/`** — skrip persiapan data, validasi anotasi, konversi, split, training, dan evaluasi.

## Menjalankan Proyek

Pasang dependensi:

```bash
python -m pip install ultralytics opencv-python pyyaml
```

Jalankan dari root repository:

```bash
python Scripts/01_cek_anotasi.py dataset
python Scripts/06_latih_E1_E3.py --nim 4222411001 --nama "HAFIS MAULANA SAPUTRA" --data dataset/data.yaml --device cpu
```

Evaluasi setelah file bobot model tersedia (sesuaikan path bobot dengan hasil training lokal):

```bash
python Scripts/07_evaluasi_test.py --data dataset/data.yaml --e1 path/ke/E1/best.pt --e3 path/ke/E3/best.pt --device cpu --output Laporan/hasil_test_humanoid_soccer.csv
```

Bobot model, cache, dan output training disimpan lokal dan tidak perlu di-commit.

## Catatan Dataset

Nama proyek adalah **Humanoid Soccer**; TORSO_21_dataset merupakan sumber data. Patuhi lisensi dan ketentuan atribusi dari repository sumber. Split test adalah subset praktikum, bukan test set resmi sumber data.

## Identitas Praktikum

- **Mata kuliah:** RET503
- **NIM:** 4222411001
- **Nama:** HAFIS MAULANA SAPUTRA
