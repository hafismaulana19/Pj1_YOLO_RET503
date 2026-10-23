# Panduan Dataset Humanoid Soccer

## Tujuan

Panduan ini menjelaskan cara menyiapkan subset citra kondisi nyata (*reality*) untuk deteksi tiga kelas: `ball`, `robot`, dan `goalpost`. Dataset gambar dan anotasi disimpan secara lokal, bukan di repositori Git.

## Struktur keluaran

Setelah semua langkah selesai, struktur lokal yang diharapkan adalah:

```text
dataset_humanoid_soccer/
├── data.yaml
├── images/
│   ├── train/  # 140 gambar
│   ├── val/    # 40 gambar
│   └── test/   # 20 gambar
└── labels/
    ├── train/
    ├── val/
    └── test/
```

Subset eksperimen berisi 200 gambar: 140 train, 40 validation, dan 20 test. Data test berisi 38 objek berlabel. Gambar dan label tidak di-commit ke GitHub.

## 1. Siapkan sumber gambar dan anotasi

Gunakan dataset Humanoid Soccer real-world/reality yang tersedia melalui [repositori sumber bit-bots](https://github.com/bit-bots/TORSO_21_dataset). Ikuti petunjuk pengunduhan resmi pada repositori sumber dan pastikan folder berikut tersedia di komputer:

- `data/reality/train/images/`
- `data/reality/train/annotations.yaml`

Simpan hasil unduhan di luar folder repositori praktikum agar tidak ikut terunggah ke Git.

## 2. Pasang dependensi

```bash
python -m pip install pyyaml opencv-python ultralytics
```

## 3. Buat subset YOLO

Dari root repositori praktikum, ganti nilai `--source` agar mengarah ke folder `reality/train` di komputer:

```bash
python scripts/00_preparasi_humanoid_soccer.py --source "../TORSO_21_dataset/data/reality/train" --jumlah 200 --seed 42 --out dataset_yolo
```

Skrip memilih gambar yang memuat setidaknya satu objek dari tiga kelas yang digunakan, lalu mengubah koordinat kotak anotasi menjadi format YOLO ternormalisasi. Jika lokasi sumber berbeda, ubah nilai `--source`.

## 4. Periksa anotasi

```bash
python scripts/01_cek_anotasi.py dataset_yolo
```

Periksa laporan terminal dan gambar ber-kotak yang dihasilkan di `dataset_yolo/cek_visual/`. Pastikan tidak ada file label hilang dan kotak benar-benar mengelilingi objek. Tinjau secara manual peringatan tentang kotak sangat kecil karena sebagian objek dapat terlihat tipis pada citra.

## 5. Bagi dataset

Setelah anotasi diperiksa:

```bash
python scripts/05_split_dataset_yolo.py dataset_yolo dataset_humanoid_soccer
```

Skrip memakai seed tetap dan pembagian 70%/20%/10%, sehingga 200 gambar terbagi menjadi 140 train, 40 validation, dan 20 test. File `dataset_humanoid_soccer/data.yaml` dibuat otomatis oleh skrip.

## 6. Validasi konfigurasi

File `data_proyek/data.yaml` adalah contoh konfigurasi yang dapat dibaca di repositori; skrip pelatihan sebaiknya menggunakan file yang dibuat bersama dataset lokal: `dataset_humanoid_soccer/data.yaml`. Pastikan kelas berurutan sebagai berikut:

| ID | Kelas |
|---:|---|
| 0 | ball |
| 1 | robot |
| 2 | goalpost |

## Catatan penting

- Jangan commit folder dataset, arsip unduhan, cache, bobot model, atau hasil pelatihan berukuran besar.
- Split test adalah subset praktikum yang diturunkan dari bagian reality, bukan test set resmi dataset sumber.
- Jangan mengubah hasil metrik menjadi klaim generalisasi luas karena ukuran test hanya 20 gambar.
- Berikan atribusi dan patuhi lisensi dataset sumber jika hasil ini dibagikan atau dipublikasikan.
