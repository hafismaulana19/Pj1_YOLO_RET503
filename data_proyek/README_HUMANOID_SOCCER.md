# Panduan Dataset Humanoid Soccer

## Tujuan

Panduan untuk menyiapkan subset citra kondisi nyata (*reality*) guna mendeteksi tiga kelas: `ball`, `robot`, dan `goalpost`.

Repository ini menggunakan folder `dataset/` sebagai dataset subset eksperimen yang sudah tersedia. Jika ingin membuat ulang dataset secara lokal, gunakan alur persiapan di bawah ini; dataset hasil unduhan besar dan data sementara sebaiknya tidak dimasukkan ke Git.

## Struktur dataset yang digunakan

```text
dataset/
├── data.yaml
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

Subset eksperimen berisi 200 gambar: 140 train, 40 validation, dan 20 test. Test subset berisi 38 objek berlabel.

## 1. Siapkan sumber data

Gunakan dataset Humanoid Soccer real-world/reality yang tersedia melalui [repositori sumber bit-bots](https://github.com/bit-bots/TORSO_21_dataset). Ikuti instruksi unduh resmi dari sumber data dan pastikan tersedia `data/reality/train/images/` serta `data/reality/train/annotations.yaml`.

Simpan hasil download sumber di luar folder repository ini, misalnya di `../TORSO_21_dataset/`.

## 2. Pasang dependensi

```bash
python -m pip install pyyaml opencv-python ultralytics
```

## 3. Buat subset YOLO sementara

Jalankan dari root repository; perintah ini membuat folder sementara bernama `dataset_yolo/`:

```bash
python Scripts/00_preparasi_humanoid_soccer.py --source "../TORSO_21_dataset/data/reality/train" --jumlah 200 --seed 42 --out dataset_yolo
```

Skrip memilih gambar yang berisi setidaknya satu objek dari tiga kelas dan mengubah anotasinya menjadi format YOLO ternormalisasi.

## 4. Periksa anotasi

```bash
python Scripts/01_cek_anotasi.py dataset_yolo
```

Periksa laporan terminal dan visualisasi bounding box yang dihasilkan di `dataset_yolo/cek_visual/`. Pastikan label tersedia dan kotak sesuai dengan objek.

## 5. Bagi dataset

Setelah anotasi diperiksa, buat dataset split di folder sementara `dataset_rebuild/`:

```bash
python Scripts/05_split_dataset_yolo.py dataset_yolo dataset_rebuild
```

Skrip menggunakan seed tetap serta split 70%/20%/10% (140/40/20 gambar). Setelah memastikan hasilnya benar, salin atau ganti isi `dataset/` secara lokal sesuai kebutuhan. Periksa kembali `dataset/data.yaml` sebelum menjalankan training.

## 6. Konfigurasi kelas

File konfigurasi yang digunakan pada training adalah `dataset/data.yaml`. Urutan kelas harus sesuai:

| ID | Kelas |
|---:|---|
| 0 | ball |
| 1 | robot |
| 2 | goalpost |

## Catatan

- Folder `dataset/` adalah subset yang dipakai dan tersedia pada repository ini.
- Folder download sumber, dataset temporer, cache, bobot model, dan output training tidak perlu di-commit.
- Test set adalah subset praktikum berisi 20 gambar, bukan test set resmi sumber data.
- Berikan atribusi dan patuhi lisensi dataset sumber.
