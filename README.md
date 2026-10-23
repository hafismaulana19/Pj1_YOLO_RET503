# Humanoid Soccer — YOLO Object Detection

Repositori praktikum RET503 untuk menyiapkan dataset dan mengevaluasi deteksi objek **Humanoid Soccer** menggunakan YOLO26n pretrained.

## Ringkasan

- **Dataset:** gambar kondisi nyata (*reality*)
- **Jumlah gambar:** 200
- **Kelas:** `ball`, `robot`, `goalpost`
- **Pembagian:** 140 train, 40 validation, 20 test
- **Eksperimen:** E1 dengan input 416 px dan E3 dengan input 640 px
- **Perangkat pelatihan:** CPU

Gambar dan label dataset tidak disimpan di GitHub. Ikuti [panduan persiapan dataset](data_proyek/README_HUMANOID_SOCCER.md) untuk membangunnya secara lokal.

## Struktur repositori

```text
.
├── data_proyek/
│   ├── README_HUMANOID_SOCCER.md
│   └── data.yaml
├── dokumentasi_humanoid_soccer/
│   ├── E1/                 # Grafik, confusion matrix, dan contoh prediksi
│   ├── E3/                 # Grafik, confusion matrix, dan contoh prediksi
│   └── README.md           # Metrik validasi dan test
├── laporan/
│   ├── hasil_praktik_4222411001_E1_E3_final.csv
│   ├── hasil_praktik_4222411001_E1_E3_final.txt
│   └── hasil_test_humanoid_soccer.csv
├── scripts/
│   ├── 00_preparasi_humanoid_soccer.py
│   ├── 01_cek_anotasi.py
│   ├── 02_yolo_ke_coco.py
│   ├── 03_coco_ke_yolo.py
│   ├── 05_split_dataset_yolo.py
│   ├── 06_latih_E1_E3.py
│   └── 07_evaluasi_test.py
└── .gitignore
```

## Persiapan lingkungan

Disarankan menggunakan Python virtual environment.

```bash
python -m pip install ultralytics opencv-python pyyaml
```

Pastikan PyTorch dan Ultralytics dapat berjalan pada perangkat yang dipilih. Eksperimen yang dilaporkan di sini dilatih menggunakan CPU.

## Alur kerja

1. Siapkan data gambar dan anotasi sesuai panduan di `data_proyek/README_HUMANOID_SOCCER.md`.
2. Buat subset YOLO dengan `scripts/00_preparasi_humanoid_soccer.py`.
3. Jalankan pemeriksaan anotasi dengan `scripts/01_cek_anotasi.py dataset_yolo`.
4. Periksa gambar pada folder `cek_visual/`; pastikan kotak label mengelilingi objek dengan benar.
5. Bagi data menggunakan `scripts/05_split_dataset_yolo.py dataset_yolo dataset_humanoid_soccer`.
6. Latih E1 dan E3 menggunakan `scripts/06_latih_E1_E3.py`.
7. Evaluasi pada test set menggunakan `scripts/07_evaluasi_test.py` setelah file bobot terbaik tersedia.

Contoh pelatihan:

```bash
python scripts/06_latih_E1_E3.py --nim 4222411001 --nama "HAFIS MAULANA SAPUTRA" --data dataset_humanoid_soccer/data.yaml --device cpu
```

Simpan bobot, dataset, cache, dan hasil training di lokal; file besar tersebut dikecualikan melalui `.gitignore`. Jangan menggunakan test set untuk memilih konfigurasi selama pengembangan.

## Hasil eksperimen

### Validasi

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.9109 | 0.8902 |
| Recall | 0.7609 | 0.8283 |
| mAP50 | 0.8200 | 0.8686 |
| mAP50–95 | 0.5754 | 0.6252 |
| Inferensi per gambar | 10.88 ms | 24.18 ms |
| Waktu pelatihan | 24.59 menit | 57.40 menit |

### Test

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Inferensi per gambar | 10.6 ms | 22.9 ms |

Pada validasi, E3 lebih tinggi pada recall, mAP50, dan mAP50–95; precision-nya lebih rendah dan inferensinya lebih lambat. Pada test, E1 lebih tinggi pada semua metrik deteksi yang dicatat dan lebih cepat. Test set hanya berisi 20 gambar (38 objek), jadi hasil ini perlu dibaca sebagai hasil pada subset praktikum, bukan jaminan generalisasi untuk semua kondisi.

Lihat [dokumentasi eksperimen terperinci](dokumentasi_humanoid_soccer/README.md) dan CSV di folder `laporan/`.

## Catatan reproduksibilitas dan dataset

- Dataset tidak disertakan di repositori karena ukuran dan lisensinya; bangun secara lokal mengikuti panduan.
- Split test di sini dibuat dari subset praktikum dan bukan test set resmi sumber dataset.
- Gunakan seed yang sama ketika membuat subset dan split agar hasil pemrosesan dapat direproduksi.
- Hormati ketentuan lisensi dataset sumber dan berikan atribusi saat memublikasikan hasil.

## Identitas praktikum

- **Mata kuliah:** RET503
- **NIM:** 4222411001
- **Nama:** HAFIS MAULANA SAPUTRA
