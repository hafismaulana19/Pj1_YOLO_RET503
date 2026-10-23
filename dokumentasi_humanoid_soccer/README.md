# Hasil Eksperimen YOLO — Humanoid Soccer

## 1. Dataset

Dataset yang digunakan adalah kumpulan gambar **Humanoid Soccer** dari bagian `reality`, yaitu gambar dalam kondisi dunia nyata. Pada praktikum ini digunakan tiga kelas objek:

- `ball`
- `robot`
- `goalpost`

Subset dataset berjumlah 200 gambar dengan pembagian berikut:

| Pembagian | Jumlah gambar |
|---|---:|
| Train | 140 |
| Validation | 40 |
| Test | 20 |
| **Total** | **200** |

Jumlah data test adalah 20 gambar dengan total 38 objek berlabel.

## 2. Eksperimen E1 — Baseline

E1 digunakan sebagai eksperimen baseline.

- Model: YOLO26n pretrained
- Ukuran input: 416 piksel
- Epoch maksimum: 100
- Perangkat: CPU

### Hasil validasi E1

| Metrik | Nilai |
|---|---:|
| Precision | 0.9109 |
| Recall | 0.7609 |
| mAP50 | 0.8200 |
| mAP50–95 | 0.5754 |
| Waktu inferensi per gambar | 10.88 ms |

## 3. Eksperimen E3 — Perubahan Ukuran Input

E3 menggunakan model dan pengaturan dasar yang sama dengan E1, dengan perubahan ukuran input dari 416 menjadi 640 piksel.

- Model: YOLO26n pretrained
- Ukuran input: 640 piksel
- Epoch maksimum: 100
- Perangkat: CPU

### Hasil validasi E3

| Metrik | Nilai |
|---|---:|
| Precision | 0.8902 |
| Recall | 0.8283 |
| mAP50 | 0.8686 |
| mAP50–95 | 0.6252 |
| Waktu inferensi per gambar | 24.18 ms |

Pada data validasi, E3 menghasilkan recall, mAP50, dan mAP50–95 yang lebih tinggi daripada E1. Namun, precision E3 lebih rendah dan waktu inferensinya lebih lama.

## 4. Hasil Evaluasi pada Data Test

Kedua eksperimen dievaluasi secara terpisah menggunakan subset test yang sama, yang terdiri dari 20 gambar dan 38 objek.

| Metrik | E1 (416 piksel) | E3 (640 piksel) |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Waktu inferensi per gambar | 10.6 ms | 22.9 ms |

### Analisis hasil test

Pada subset test yang digunakan, E1 memperoleh nilai precision, recall, mAP50, dan mAP50–95 lebih tinggi dibandingkan E3. E1 juga memiliki waktu inferensi per gambar yang lebih singkat.

Hasil test ini berbeda dari hasil validasi, ketika E3 memperoleh nilai recall, mAP50, dan mAP50–95 yang lebih tinggi. Perbedaan tersebut menunjukkan bahwa hasil validasi tidak selalu mencerminkan hasil pada data test. Ukuran input yang lebih besar juga tidak otomatis menghasilkan performa yang lebih baik pada data yang belum digunakan saat pelatihan.

## 5. Kesimpulan

Eksperimen membandingkan YOLO26n pretrained dengan ukuran input 416 piksel pada E1 dan 640 piksel pada E3. E3 memperoleh hasil lebih tinggi pada beberapa metrik validasi, yaitu recall, mAP50, dan mAP50–95. Namun, pada data test, E1 unggul pada seluruh metrik performa yang dicatat dan memiliki waktu inferensi yang lebih singkat.

Berdasarkan hasil pada subset test ini, E1 merupakan pilihan yang lebih baik apabila mempertimbangkan kualitas deteksi dan kecepatan inferensi secara bersamaan. Kesimpulan tetap terbatas pada konfigurasi eksperimen dan subset test yang hanya berisi 20 gambar, sehingga diperlukan evaluasi pada data yang lebih banyak untuk menilai generalisasi model dengan lebih kuat.

## 6. Struktur Dokumentasi

- `E1/`: grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E1.
- `E3/`: grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E3.

Dokumentasi memuat metrik validasi serta evaluasi test untuk membandingkan kedua eksperimen.