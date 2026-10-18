# Pj1 YOLO RET503 — Object Detection

## Identitas Mahasiswa

- **NIM:** 4222411001
- **Nama:** HAFIS MAULANA SAPUTRA
- **Mata Kuliah:** RET503

## Deskripsi Proyek

Proyek praktikum ini menerapkan YOLO26n untuk mendeteksi dua objek komponen robotika, yaitu MG90S Servo Motor dan PCA9685 Servo Driver. Eksperimen dilakukan menggunakan model pretrained dengan perangkat CPU, kemudian membandingkan hasil berdasarkan ukuran gambar input yang berbeda.

## Dataset

Dataset yang digunakan adalah `dataset_v1`, dengan rincian:

- **Total gambar:** 150
- **Training:** 105 gambar
- **Validation:** 30 gambar
- **Test:** 15 gambar
- **Jumlah kelas:** 2

| ID | Kelas |
|---|---|
| 0 | MG90S |
| 1 | PCA9685 |

Dataset dibagi menjadi data training, validation, dan test. Gambar serta label dataset tidak disertakan dalam repository ini dan perlu disiapkan secara terpisah.

## Instalasi dan Persiapan

### Persyaratan

- Python
- pip
- PyTorch
- Ultralytics YOLO

### Instalasi Dependensi

Aktifkan environment Python yang akan digunakan, kemudian instal Ultralytics:

```bash
pip install ultralytics
```

Pastikan PyTorch dan dependensi lainnya terpasang sesuai environment yang digunakan. Eksperimen pada proyek ini dilakukan menggunakan CPU.

### Persiapan Dataset

1. Siapkan folder `dataset_v1` yang berisi gambar dan label.
2. Pastikan dataset memiliki pembagian `train`, `val`, dan `test`.
3. Periksa konfigurasi pada `data_proyek/data.yaml`.
4. Sesuaikan path dataset dengan lokasi penyimpanan pada komputer yang digunakan.
5. Periksa anotasi sebelum menjalankan pelatihan atau evaluasi.

### Alur Penggunaan

Script pemrosesan dataset dan pelatihan tersedia di folder `scripts/`. Secara umum, alur pengerjaan meliputi:

1. Persiapan dan pemeriksaan dataset.
2. Pemeriksaan serta konversi anotasi jika diperlukan.
3. Pembagian dataset ke dalam training, validation, dan test.
4. Pelatihan eksperimen E1 dan E3.
5. Evaluasi model dan pemeriksaan hasil eksperimen.

Periksa isi setiap script untuk mengetahui argumen, konfigurasi, dan dependensi yang diperlukan sebelum menjalankannya.

## Rancangan Eksperimen

### E1 — Baseline

- **Model:** YOLO26n pretrained
- **Image size:** 416
- **Epoch maksimum:** 100
- **Batch size:** 4
- **Device:** CPU

E1 digunakan sebagai eksperimen baseline untuk memperoleh hasil awal performa model.

### E3 — Hyperparameter Tuning

- **Model:** YOLO26n pretrained
- **Image size:** 640
- **Epoch maksimum:** 100
- **Batch size:** 4
- **Device:** CPU
- **Parameter yang diubah:** `imgsz`

E3 mengubah ukuran gambar input dari 416 menjadi 640, sedangkan parameter pelatihan lainnya dipertahankan sama untuk membandingkan hasil eksperimen.

## Hasil Validasi

| Metrik | E1 | E3 |
|---|---:|---:|
| Precision | 0.995 | 0.996 |
| Recall | 1.000 | 1.000 |
| mAP50 | 0.995 | 0.995 |
| mAP50-95 | 0.852 | 0.886 |
| Inferensi (ms/gambar) | 13.9 | 25.1 |
| Waktu pelatihan (menit) | 9.6 | 38.6 |

E3 dipilih sebagai kandidat model final berdasarkan nilai mAP50-95 validation yang lebih tinggi, yaitu 0.886 dibandingkan 0.852 pada E1. Peningkatan ini disertai waktu inferensi dan waktu pelatihan yang lebih lama.

## Hasil Evaluasi Test E3

| Metrik | Hasil |
|---|---:|
| Precision | 0.9852 |
| Recall | 1.0000 |
| mAP50 | 0.9950 |
| mAP50-95 | 0.8774 |
| Inferensi (ms/gambar) | 23.95 |

Evaluasi dilakukan pada test set yang berisi 15 gambar. Karena jumlah data test terbatas, hasil perlu ditafsirkan secara hati-hati dan belum cukup untuk menyimpulkan kemampuan generalisasi model pada berbagai kondisi objek.

Test set telah dievaluasi pada eksperimen sebelumnya. Oleh karena itu, hasil yang dilaporkan merupakan evaluasi tambahan dan bukan pengujian pertama terhadap test set.

## Struktur Repository

```text
Pj1_YOLO_RET503/
|-- data_proyek/
|   |-- data.yaml
|   `-- README.md
|-- eksperimen/
|   |-- E1_final/
|   `-- E3_final/
|-- evaluasi_test/
|   `-- E3_test_final/
|-- laporan/
|   |-- hasil_praktik_4222411001_E1_E3_final.txt
|   `-- hasil_praktik_4222411001_E1_E3_final.csv
|-- scripts/
`-- README.md
```

### Fungsi Folder

- `data_proyek/`: konfigurasi dan dokumentasi dataset.
- `scripts/`: script persiapan dataset, pemeriksaan anotasi, konversi format, pembagian dataset, dan pelatihan.
- `eksperimen/E1_final/`: hasil dan artefak eksperimen E1.
- `eksperimen/E3_final/`: hasil dan artefak eksperimen E3.
- `evaluasi_test/E3_test_final/`: hasil evaluasi test, kurva, confusion matrix, dan contoh prediksi.
- `laporan/`: laporan hasil eksperimen dalam format TXT dan CSV.

## Keterbatasan

1. Test set hanya berisi 15 gambar sehingga hasil evaluasi perlu ditafsirkan dengan hati-hati.
2. Pengujian pada dataset yang lebih besar dan lebih bervariasi diperlukan untuk menilai kemampuan generalisasi model secara lebih kuat.
3. Eksperimen dilakukan menggunakan CPU, sehingga waktu pelatihan dan inferensi dapat berbeda pada perangkat keras lain.
4. Dataset gambar dan label tidak disertakan dalam repository.

## Catatan Reproduksibilitas

Repository ini berisi script, konfigurasi, dokumentasi, dan artefak eksperimen. Untuk menjalankan ulang pelatihan atau evaluasi, pengguna perlu menyiapkan dataset secara terpisah, memasang dependensi yang sesuai, dan menyesuaikan path dataset pada konfigurasi.

Hasil pelatihan yang dicantumkan dalam README mengacu pada artefak eksperimen yang tersimpan di repository.

## Kesimpulan

Berdasarkan hasil validasi, E3 memperoleh mAP50-95 sebesar 0.886, lebih tinggi daripada E1 sebesar 0.852. Dengan demikian, E3 dipilih sebagai kandidat model final berdasarkan metrik tersebut. Namun, E3 membutuhkan waktu inferensi yang lebih lama. Pada evaluasi test, E3 memperoleh mAP50-95 sebesar 0.8774. Hasil ini menjadi indikasi awal performa model dan perlu dievaluasi lebih lanjut menggunakan dataset yang lebih besar dan beragam.