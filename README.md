# Pj1 YOLO RET503 — Object Detection

## Identitas Mahasiswa
- **NIM:** 4222411001
- **Nama:** HAFIS MAULANA SAPUTRA
- **Mata Kuliah:** RET503

## Deskripsi
Praktikum ini menerapkan YOLO26n untuk mendeteksi dua objek: MG90S Servo Motor dan PCA9685 Servo Driver.

## Dataset
- Total gambar: 150
- Train: 105 gambar
- Validation: 30 gambar
- Test: 15 gambar
- Kelas: `MG90S` dan `PCA9685`

## Instalasi dan Penggunaan

### Persyaratan

- Python
- pip
- PyTorch
- Ultralytics YOLO

### Instalasi Dependensi

Buka terminal pada folder proyek, kemudian jalankan:

```bash
pip install ultralytics
```

Pastikan PyTorch dan dependensi lain telah terpasang sesuai environment yang digunakan.

### Menjalankan Proyek

Script pemrosesan dataset dan pelatihan tersedia di folder `scripts/`. Periksa argumen dan konfigurasi di setiap script sebelum menjalankannya, serta pastikan lokasi dataset sudah sesuai dengan struktur folder lokal.

Model hasil pelatihan dan artefak eksperimen tersedia di folder `eksperimen/`.

## Eksperimen

### E1 — Baseline
- Model: YOLO26n pretrained
- Image size: 416
- Epoch maksimum: 100
- Batch size: 4
- Device: CPU

### E3 — Hyperparameter Tuning
- Model: YOLO26n pretrained
- Image size: 640
- Epoch maksimum: 100
- Batch size: 4
- Device: CPU
- Parameter yang diubah: `imgsz`

## Hasil Validasi

| Metrik | E1 | E3 |
|---|---:|---:|
| Precision | 0.995 | 0.996 |
| Recall | 1.000 | 1.000 |
| mAP50 | 0.995 | 0.995 |
| mAP50-95 | 0.852 | 0.886 |
| Inferensi (ms/gambar) | 13.9 | 25.1 |
| Waktu pelatihan (menit) | 9.6 | 38.6 |

E3 dipilih berdasarkan mAP50-95 validation yang lebih tinggi.

## Hasil Test E3

| Metrik | Hasil |
|---|---:|
| Precision | 0.9852 |
| Recall | 1.0000 |
| mAP50 | 0.9950 |
| mAP50-95 | 0.8774 |
| Inferensi (ms/gambar) | 23.95 |

Test set berisi 15 gambar. Hasil perlu ditafsirkan dengan mempertimbangkan ukuran test set yang terbatas. Test set sudah pernah dievaluasi pada eksperimen sebelumnya, sehingga evaluasi yang dicatat merupakan evaluasi tambahan.

## Struktur Repository
- `scripts/`: script pemrosesan dataset dan pelatihan.
- `eksperimen/E1_final/`: artefak eksperimen E1.
- `eksperimen/E3_final/`: artefak eksperimen E3.
- `evaluasi_test/E3_test_final/`: kurva, confusion matrix, dan contoh prediksi test E3.
- `laporan/`: laporan TXT dan CSV.

## Kesimpulan
E3 memperoleh mAP50-95 validation sebesar 0.886, lebih tinggi daripada E1 sebesar 0.852. E3 menjadi kandidat model final berdasarkan validation, dengan waktu inferensi yang lebih lama. Pada test set, E3 memperoleh mAP50-95 sebesar 0.8774.

## Keterbatasan

Test set terdiri dari 15 gambar sehingga hasil evaluasi perlu ditafsirkan secara hati-hati. Pengujian pada dataset yang lebih besar dan lebih bervariasi diperlukan untuk menilai kemampuan generalisasi model secara lebih kuat.

## Catatan Dataset

Repository ini menyimpan konfigurasi dan dokumentasi dataset, tetapi tidak menyertakan seluruh gambar dan label. Dataset perlu disiapkan secara terpisah sebelum menjalankan ulang pelatihan atau evaluasi.

Konfigurasi dataset tersedia di `data_proyek/data.yaml`. Sesuaikan path dataset dengan lokasi penyimpanan di komputer yang digunakan.

