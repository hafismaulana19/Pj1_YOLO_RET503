# Dataset Humanoid Soccer — TORSO-21 Real-World

## Tujuan
Praktikum Pj1 menggunakan citra nyata dari kamera robot pada domain RoboCup Humanoid Soccer. Dataset sumber adalah [TORSO-21](https://github.com/bit-bots/TORSO_21_dataset), khusus koleksi `reality`, bukan koleksi `simulation`.

## Kelas subset
Skrip persiapan memilih tiga kelas yang tersedia dalam anotasi TORSO-21:
- `0: ball`
- `1: robot`
- `2: goalpost`

Subset awal ditargetkan maksimal 200 gambar berlabel. Jumlah aktual dan jumlah bounding box per kelas dicatat oleh skrip saat dijalankan; jangan menulis angka hasil sebelum proses benar-benar selesai.

## Mengunduh dataset sumber

Unduhan koleksi real-world train cukup besar (dokumentasi resmi memperkirakan sekitar 10 GB). Pastikan ruang disk tersedia. Jangan mengunggah arsip dataset penuh ke repositori praktikum.

1. Clone repositori dataset resmi di luar folder repositori praktikum:

   ```bash
   git clone https://github.com/bit-bots/TORSO_21_dataset.git
   cd TORSO_21_dataset
   ```

2. Unduh citra koleksi real-world train:

   ```bash
   python scripts/download_dataset.py --real --train
   ```

3. Unduh file anotasi untuk koleksi yang sama:

   ```bash
   python scripts/download_dataset.py --real --train --annotations
   ```

Setelah selesai, pastikan dua path berikut ada:
- `data/reality/train/images/`
- `data/reality/train/annotations.yaml`

Dokumentasi resmi juga menyediakan unduhan manual di https://data.bit-bots.de/TORSO-21/.

## Membuat subset berlabel YOLO

Jalankan skrip dari root repositori praktikum. Sesuaikan path `--source` dengan lokasi clone TORSO-21:

```bash
python -m pip install pyyaml
python scripts/00_preparasi_torso21.py --source ../TORSO_21_dataset/data/reality/train --jumlah 200 --out dataset_yolo
```

Skrip menyalin gambar yang dipilih, mengubah bounding box TORSO-21 dari dua titik piksel menjadi format YOLO ternormalisasi `class_id cx cy width height`, dan membuat `classes.txt`. Gambar tanpa objek dari tiga kelas yang dipilih tidak dimasukkan dalam subset ini.

## Validasi anotasi dan pembagian data

1. Jalankan pemeriksaan anotasi:

   ```bash
   python scripts/01_cek_anotasi.py dataset_yolo
   ```

2. Buka gambar hasil anotasi visual dalam `dataset_yolo/cek_visual/` dan pastikan kotak benar-benar mengelilingi objek.

3. Setelah pemeriksaan bersih, bagi subset dengan skrip praktikum:

   ```bash
   python scripts/05_split_dataset_yolo.py dataset_yolo dataset_v1
   ```

Skrip pembagian membuat split 70% train, 20% validation, dan 10% test serta file `dataset_v1/data.yaml`.

## Reproduksibilitas dan batasan

- Dataset gambar dan label hasil ekstraksi tidak disimpan di GitHub. Simpan dataset lokal dan gunakan skrip untuk membangunnya ulang.
- Subset diambil dari koleksi `reality/train`, lalu dibagi secara acak untuk kebutuhan praktikum. Karena itu, bagian test pada subset ini **bukan** official TORSO-21 test set.
- Gunakan seed yang sama untuk menghasilkan subset yang dapat direproduksi.
- Periksa lisensi dan sertakan sitasi TORSO-21 saat melaporkan hasil.

## Sitasi dataset

Bestmann, M., Engelke, T., Fiedler, N., Güldenstein, J., Gutsche, J., Hagge, J., & Vahl, F. (2021). *TORSO-21 Dataset: Typical Objects in RoboCup Soccer 2021*. RoboCup 2021: Robot World Cup XXIV. https://doi.org/10.1007/978-3-030-98682-7_6

Sumber dataset dan petunjuk resmi: https://github.com/bit-bots/TORSO_21_dataset
