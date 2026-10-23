# Hasil Eksperimen YOLO — Humanoid Soccer

## 1. Dataset

Dataset yang digunakan adalah Humanoid Soccer bagian `reality`, yaitu kumpulan gambar dari kondisi dunia nyata. Dataset yang digunakan dalam praktikum memiliki tiga kelas objek:

- `ball`
- `robot`
- `goalpost`

Subset yang digunakan berjumlah 200 gambar, dengan pembagian sebagai berikut:

| Pembagian | Jumlah gambar |
|---|---:|
| Train | 140 |
| Validation | 40 |
| Test | 20 |
| **Total** | **200** |

## 2. Eksperimen E1 — Baseline

E1 digunakan sebagai eksperimen baseline dengan konfigurasi berikut:

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

Hasil pelatihan dan evaluasi E1 digunakan sebagai pembanding untuk eksperimen berikutnya.

## 3. Eksperimen E3 — Perubahan Ukuran Input

E3 menggunakan model dan pengaturan dasar yang sama dengan E1, tetapi ukuran input diubah dari 416 menjadi 640 piksel.

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

Pada data validasi, E3 memperoleh nilai mAP50, mAP50–95, dan recall lebih tinggi daripada E1. Namun, precision E3 lebih rendah.

## 4. Hasil Evaluasi pada Data Test

Evaluasi test dilakukan secara terpisah setelah eksperimen selesai. Kedua model dievaluasi menggunakan subset test yang sama, yaitu 20 gambar dengan total 38 objek.

| Metrik | E1 (416 piksel) | E3 (640 piksel) |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Waktu inferensi per gambar | 10.6 ms | 22.9 ms |

### Analisis hasil test

Berdasarkan evaluasi pada data test, E1 memperoleh nilai precision, recall, mAP50, dan mAP50–95 yang lebih tinggi dibandingkan E3. E1 juga memiliki waktu inferensi per gambar yang lebih singkat pada pengujian ini.

Hasil tersebut berbeda dari hasil validasi, yang menunjukkan bahwa E3 unggul pada beberapa metrik. Perbedaan ini menunjukkan bahwa performa pada data validasi tidak selalu mencerminkan performa pada data test. Peningkatan ukuran input juga tidak otomatis menghasilkan performa yang lebih baik pada data yang belum pernah digunakan dalam pelatihan.

Pada konfigurasi dan subset yang diuji, E1 memberikan hasil test yang lebih baik sekaligus waktu inferensi yang lebih singkat. Meskipun demikian, jumlah data test yang terbatas, yaitu 20 gambar, perlu dipertimbangkan sebelum menarik kesimpulan yang lebih umum.

## 5. Kesimpulan

Eksperimen membandingkan YOLO26n pretrained dengan ukuran input 416 piksel pada E1 dan 640 piksel pada E3. E3 memperoleh hasil validasi yang lebih tinggi pada mAP50, mAP50–95, dan recall. Sebaliknya, pada evaluasi test, E1 memperoleh hasil lebih tinggi pada seluruh metrik performa yang dicatat dan memiliki waktu inferensi lebih singkat.

Dengan demikian, E1 menjadi pilihan yang lebih baik berdasarkan hasil evaluasi test pada subset yang digunakan dalam praktikum ini. Kesimpulan tersebut terbatas pada konfigurasi eksperimen dan jumlah data yang diuji.

## 6. Struktur Dokumentasi

Dokumentasi eksperimen mencakup:

- **E1:** grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E1.
- **E3:** grafik hasil pelatihan, confusion matrix, file CSV, dan contoh prediksi E3.
- **CSV hasil eksperimen:** mencatat metrik validasi dan informasi konfigurasi eksperimen.
- **CSV hasil test:** mencatat metrik evaluasi test dan waktu inferensi masing-masing eksperimen.
