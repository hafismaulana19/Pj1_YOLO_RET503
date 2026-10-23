# Hasil Eksperimen YOLO — Humanoid Soccer TORSO-21

## Dataset
Dataset yang digunakan adalah TORSO-21 bagian reality (gambar dunia nyata).
Terdapat tiga kelas objek:
- ball
- robot
- goalpost

Subset berisi 200 gambar, dengan pembagian:
- Train: 140 gambar
- Validation: 40 gambar
- Test: 20 gambar

## Eksperimen E1 — Baseline
- Model: YOLO26n pretrained
- Ukuran input: 416 piksel
- Epoch maksimum: 100
- Perangkat: CPU

Hasil validasi:
- mAP50: 0.8200
- mAP50-95: 0.5754
- Precision: 0.9109
- Recall: 0.7609

Grafik dan hasil evaluasi tersedia pada folder `E1/`.

## Eksperimen E3 — Perubahan Ukuran Input
- Model: YOLO26n pretrained
- Ukuran input: 640 piksel
- Epoch maksimum: 100
- Perangkat: CPU

Hasil validasi:
- mAP50: 0.8686
- mAP50-95: 0.6252
- Precision: 0.8902
- Recall: 0.8283

Hasil test terpisah:
- mAP50: 0.7436
- mAP50-95: 0.5495

Grafik dan hasil evaluasi tersedia pada folder `E3/`.

## Analisis
E3 menghasilkan mAP50 dan mAP50-95 validasi yang lebih tinggi daripada E1. Namun, precision E3 sedikit lebih rendah. Hasil test E3 juga lebih rendah dibandingkan hasil validasinya, sehingga evaluasi pada data test perlu dibahas secara terpisah.

## Hasil Evaluasi pada Data TEST

Evaluasi dilakukan secara terpisah menggunakan data TEST yang terdiri dari 20 gambar dan 38 objek. Kedua eksperimen dievaluasi menggunakan data TEST yang sama.

| Metrik | E1 (416 piksel) | E3 (640 piksel) |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Waktu inferensi per gambar | 10.6 ms | 22.9 ms |

### Analisis Hasil TEST

Berdasarkan evaluasi pada data TEST, E1 memperoleh nilai Precision, Recall, mAP50, dan mAP50–95 yang lebih tinggi dibandingkan E3. E1 juga memiliki waktu inferensi per gambar yang lebih singkat pada pengujian ini.

Hasil tersebut berbeda dari hasil validasi yang sebelumnya menunjukkan performa E3 lebih tinggi pada beberapa metrik. Perbedaan ini menunjukkan bahwa hasil evaluasi pada data validasi dan data TEST tidak selalu sama. Ukuran input yang lebih besar tidak otomatis menghasilkan performa yang lebih baik pada data yang belum pernah digunakan dalam pelatihan.

Hasil ini berlaku untuk konfigurasi eksperimen dan dataset yang digunakan. Jumlah data TEST yang terbatas, yaitu 20 gambar, perlu dipertimbangkan ketika menarik kesimpulan.

## Struktur Dokumentasi

- `E1/`: grafik, confusion matrix, CSV, dan contoh prediksi E1.
- `E3/`: grafik, confusion matrix, CSV, dan contoh prediksi E3.
