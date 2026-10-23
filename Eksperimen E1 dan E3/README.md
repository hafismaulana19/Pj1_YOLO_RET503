# Dokumentasi Eksperimen E1 dan E3 — Humanoid Soccer

Dokumentasi ini berisi hasil pelatihan, evaluasi, dan perbandingan dua eksperimen YOLO26n pretrained untuk deteksi objek Humanoid Soccer.

## Dataset

Subset dataset berjumlah 200 gambar dengan pembagian 140 gambar train, 40 validation, dan 20 test. Kelas objek yang digunakan adalah `ball`, `robot`, dan `goalpost`. Data test terdiri dari 20 gambar dengan total 38 objek berlabel.

## Eksperimen E1 — Baseline

- Model: YOLO26n pretrained
- Ukuran input: 416 piksel
- Epoch maksimum: 100
- Perangkat pelatihan: CPU

### Hasil validasi E1

| Metrik | Nilai |
|---|---:|
| Precision | 0.9109 |
| Recall | 0.7609 |
| mAP50 | 0.8200 |
| mAP50–95 | 0.5754 |
| Waktu inferensi per gambar | 10.88 ms |

## Eksperimen E3 — Perubahan Ukuran Input

E3 menggunakan model dan pengaturan dasar yang sama dengan E1, tetapi ukuran input dinaikkan dari 416 menjadi 640 piksel.

- Model: YOLO26n pretrained
- Ukuran input: 640 piksel
- Epoch maksimum: 100
- Perangkat pelatihan: CPU

### Hasil validasi E3

| Metrik | Nilai |
|---|---:|
| Precision | 0.8902 |
| Recall | 0.8283 |
| mAP50 | 0.8686 |
| mAP50–95 | 0.6252 |
| Waktu inferensi per gambar | 24.18 ms |

Pada data validasi, E3 mendapatkan recall, mAP50, dan mAP50–95 yang lebih tinggi daripada E1. Namun, precision E3 lebih rendah dan waktu inferensinya lebih lama.

## Evaluasi pada Data Test

Kedua eksperimen diuji menggunakan subset test yang sama.

| Metrik | E1 (416 piksel) | E3 (640 piksel) |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Waktu inferensi per gambar | 10.6 ms | 22.9 ms |

Pada subset test ini, E1 mengungguli E3 pada seluruh metrik deteksi yang dicatat dan memiliki waktu inferensi yang lebih singkat. Hasil validasi dan test berbeda, sehingga ukuran input yang lebih besar tidak otomatis memberi performa lebih baik pada data yang belum digunakan saat pelatihan.

## Kesimpulan

E3 mendapat hasil lebih tinggi pada beberapa metrik validasi, sedangkan E1 memberi hasil lebih baik pada seluruh metrik test yang dicatat dan lebih cepat saat inferensi. Berdasarkan subset test ini, E1 menjadi pilihan yang lebih baik jika mempertimbangkan kualitas deteksi dan kecepatan secara bersamaan. Kesimpulan tetap terbatas karena data test hanya terdiri dari 20 gambar, sehingga evaluasi pada data lebih banyak diperlukan untuk menilai generalisasi model.

## Isi Folder

- `E1/`: grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E1.
- `E3/`: grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E3.
