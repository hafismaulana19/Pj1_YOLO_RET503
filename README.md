# Humanoid Soccer — YOLO Object Detection

Repositori praktikum RET503 untuk deteksi objek **Humanoid Soccer** menggunakan YOLO26n pretrained.

## Ringkasan Proyek

- **Dataset:** gambar kondisi nyata (*reality*) dari dataset sumber bit-bots
- **Subset eksperimen:** 200 gambar
- **Kelas:** `ball`, `robot`, `goalpost`
- **Pembagian:** 140 train, 40 validation, 20 test
- **Model:** YOLO26n pretrained
- **Eksperimen:** E1 (imgsz 416) dan E3 (imgsz 640)
- **Perangkat pelatihan:** CPU

## Hasil Visual Eksperimen

### E1 — Input 416 px

![E1 training results](<Eksperimen E1 dan E3/E1/results.png>)

Contoh prediksi validasi E1:

![E1 validation predictions](<Eksperimen E1 dan E3/E1/val_batch0_pred.jpg>)

### E3 — Input 640 px

![E3 training results](<Eksperimen E1 dan E3/E3/results.png>)

Contoh prediksi validasi E3:

![E3 validation predictions](<Eksperimen E1 dan E3/E3/val_batch0_pred.jpg>)

## Ringkasan Metrik

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

Pada validasi, E3 memperoleh recall, mAP50, dan mAP50–95 lebih tinggi, tetapi lebih lambat. Pada test subset, E1 memperoleh nilai lebih tinggi di semua metrik deteksi yang dicatat dan inferensi yang lebih cepat. Perlu diperhatikan bahwa test hanya berisi 20 gambar (38 objek), sehingga hasil ini terbatas pada subset praktikum dan bukan jaminan performa pada semua kondisi.

## Menyiapkan Dataset

Dataset disimpan di folder `dataset/` pada repositori. File konfigurasi dataset tersedia di `dataset/data.yaml`.

Sumber dataset: [bit-bots/TORSO_21_dataset](https://github.com/bit-bots/TORSO_21_dataset). Nama proyek ini **Humanoid Soccer**; TORSO_21_dataset hanya dicantumkan sebagai sumber data. Pastikan mematuhi lisensi dan ketentuan atribusi dataset sumber.

## Menjalankan Proyek

Pasang dependensi utama:

```bash
python -m pip install ultralytics opencv-python pyyaml
```

Alur kerja dari root repositori:

1. Periksa anotasi: `python scripts/01_cek_anotasi.py dataset`.
2. Latih E1 dan E3: `python scripts/06_latih_E1_E3.py --nim 4222411001 --nama "HAFIS MAULANA SAPUTRA" --data dataset/data.yaml --device cpu`.
3. Evaluasi test menggunakan `scripts/07_evaluasi_test.py` setelah bobot model terbaik tersedia.

Dataset, bobot model, cache, dan keluaran training disimpan lokal sesuai pengaturan Git. Lihat [dokumentasi eksperimen lengkap](<Eksperimen E1 dan E3/README.md>) dan tabel CSV di folder `laporan/`.

## Struktur Repositori

- `data_proyek/` — konfigurasi dan panduan dataset
- `dataset/` — gambar, label, dan konfigurasi dataset
- `scripts/` — persiapan data, pengecekan anotasi, pelatihan, dan evaluasi
- `Eksperimen E1 dan E3/` — grafik eksperimen dan contoh prediksi E1/E3
- `laporan/` — ringkasan metrik CSV/TXT

## Identitas Praktikum

- **Mata kuliah:** RET503
- **NIM:** 4222411001
- **Nama:** HAFIS MAULANA SAPUTRA
