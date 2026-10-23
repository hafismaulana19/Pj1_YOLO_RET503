# Humanoid Soccer — YOLO Object Detection

Repositori praktikum RET503 untuk eksperimen deteksi objek **Humanoid Soccer** menggunakan YOLO26n pretrained.

## Ringkasan Proyek

- **Kelas deteksi:** `ball`, `robot`, `goalpost`
- **Subset eksperimen:** 200 gambar — 140 train, 40 validation, 20 test
- **Eksperimen:** E1 (`imgsz=416`) dan E3 (`imgsz=640`)
- **Perangkat pelatihan:** CPU
- **Sumber dataset:** [bit-bots/TORSO_21_dataset](https://github.com/bit-bots/TORSO_21_dataset)

## Hasil Praktik E1 dan E3

Ringkasan metrik validasi dari file `Laporan/hasil_praktik_4222411001_E1_E3_final.csv`:

| Eksperimen | Perubahan | Pretrained | mAP50 | mAP50-95 | Precision | Recall | Inferensi (ms) | Waktu latih (menit) | imgsz |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E1_final | - | Ya | 0.8200 | 0.5754 | 0.9109 | 0.7609 | 10.88 | 24.59 | 416 |
| E3_final | imgsz=640 | Ya | 0.8686 | 0.6252 | 0.8902 | 0.8283 | 24.18 | 57.40 | 640 |

E3 memperoleh mAP50, mAP50-95, dan recall validasi yang lebih tinggi, sedangkan E1 memiliki precision lebih tinggi, inferensi yang lebih cepat, serta waktu latih yang lebih singkat. Hasil evaluasi pada split test disajikan terpisah di [hasil_test_humanoid_soccer.csv](Laporan/hasil_test_humanoid_soccer.csv).

File hasil praktik:
- [CSV metrik E1 dan E3](Laporan/hasil_praktik_4222411001_E1_E3_final.csv)
- [Laporan teks E1 dan E3](Laporan/hasil_praktik_4222411001_E1_E3_final.txt)
- [CSV hasil evaluasi test](Laporan/hasil_test_humanoid_soccer.csv)

## Analisis Hasil

Berdasarkan metrik validasi pada dua eksperimen, E3 (`imgsz=640`) menghasilkan nilai `mAP50` sebesar 0.8686 dan `mAP50-95` sebesar 0.6252, lebih tinggi dibanding E1 (`imgsz=416`) yang masing-masing memperoleh 0.8200 dan 0.5754. Recall E3 juga lebih tinggi, yaitu 0.8283 dibanding 0.7609. Sebaliknya, E1 memperoleh precision lebih tinggi (0.9109 dibanding 0.8902), waktu inferensi lebih singkat (10.88 ms dibanding 24.18 ms), dan waktu pelatihan lebih singkat (24.59 menit dibanding 57.40 menit).

Hasil ini menunjukkan kompromi antara kualitas deteksi validasi dan kecepatan komputasi: E3 unggul pada mAP dan recall validasi, sedangkan E1 lebih cepat dan memiliki precision lebih tinggi.

## Hasil Evaluasi Test

Evaluasi pada split test dilakukan terhadap 20 gambar yang memuat 38 objek berlabel.

| Metrik Test | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50-95 | 0.5886 | 0.5495 |
| Inferensi per gambar | 10.6 ms | 22.9 ms |

Pada subset test ini, E1 memperoleh nilai lebih tinggi pada seluruh metrik deteksi yang dicatat dan memiliki waktu inferensi lebih rendah. Karena jumlah test hanya 20 gambar dan 38 objek, hasil ini perlu dipahami sebagai evaluasi terbatas pada subset praktikum, bukan jaminan kinerja pada seluruh kondisi pertandingan atau lingkungan nyata.

Data lengkap tersedia di [CSV hasil evaluasi test](Laporan/hasil_test_humanoid_soccer.csv).

## Hasil Eksperimen

### E1 — Input 416 px

![E1 training results](<Eksperimen E1 dan E3/E1/results.png>)

![E1 validation predictions](<Eksperimen E1 dan E3/E1/val_batch0_pred.jpg>)

### E3 — Input 640 px

![E3 training results](<Eksperimen E1 dan E3/E3/results.png>)

![E3 validation predictions](<Eksperimen E1 dan E3/E3/val_batch0_pred.jpg>)

### Metrik Validasi

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.9109 | 0.8902 |
| Recall | 0.7609 | 0.8283 |
| mAP50 | 0.8200 | 0.8686 |
| mAP50–95 | 0.5754 | 0.6252 |
| Inferensi per gambar | 10.88 ms | 24.18 ms |
| Waktu pelatihan | 24.59 menit | 57.40 menit |

### Metrik Test

| Metrik | E1 · 416 px | E3 · 640 px |
|---|---:|---:|
| Precision | 0.8990 | 0.8394 |
| Recall | 0.8080 | 0.7333 |
| mAP50 | 0.8723 | 0.7436 |
| mAP50–95 | 0.5886 | 0.5495 |
| Inferensi per gambar | 10.6 ms | 22.9 ms |

Pada validasi, E3 mendapat recall, mAP50, dan mAP50–95 lebih tinggi, tetapi lebih lambat. Pada test subset, E1 memperoleh nilai lebih tinggi pada metrik yang dicatat dan inferensi lebih cepat. Karena test hanya mencakup 20 gambar (38 objek), hasil ini terbatas pada subset praktikum.

## Struktur Repository

Struktur folder yang digunakan dalam proyek:

```text
Pj1_YOLO_RET503/
├── dataset/                 # Gambar, label, dan data.yaml untuk eksperimen
├── data_proyek/             # Panduan proyek dan konfigurasi referensi
├── Eksperimen E1 dan E3/    # Grafik serta hasil eksperimen E1 dan E3
│   ├── E1/
│   └── E3/
├── Laporan/                 # Rekap hasil praktikum CSV/TXT
├── Scripts/                 # Skrip persiapan, validasi, training, evaluasi
├── .gitignore               # Aturan file lokal yang tidak dilacak Git
└── README.md                # Dokumentasi utama
```

### Tampilan folder di halaman GitHub

GitHub mengurutkan folder dan file secara otomatis, bukan mengikuti urutan pada diagram di atas. Karena itu, daftar di halaman utama repository akan tampak seperti ini:

```text
Pj1_YOLO_RET503/
├── Eksperimen E1 dan E3/
├── Laporan/
├── Scripts/
├── data_proyek/
├── dataset/
├── .gitignore
└── README.md
```

Urutan pada halaman GitHub adalah tampilan otomatis berdasarkan nama; struktur folder dan fungsinya tetap sama.
## Isi Folder

- **`dataset/`** — gambar, anotasi, dan konfigurasi dataset yang digunakan.
- **`data_proyek/`** — panduan sumber data dan konfigurasi referensi.
- **`Eksperimen E1 dan E3/`** — grafik training, confusion matrix, `results.csv`, serta contoh prediksi.
- **`Laporan/`** — rekap metrik praktikum dan hasil test.
- **`Scripts/`** — skrip persiapan data, validasi anotasi, konversi, split, training, dan evaluasi.

## Menjalankan Proyek

Pasang dependensi:

```bash
python -m pip install ultralytics opencv-python pyyaml
```

Jalankan dari root repository:

```bash
python Scripts/01_cek_anotasi.py dataset
python Scripts/06_latih_E1_E3.py --nim 4222411001 --nama "HAFIS MAULANA SAPUTRA" --data dataset/data.yaml --device cpu
```

Evaluasi setelah file bobot model tersedia (sesuaikan path bobot dengan hasil training lokal):

```bash
python Scripts/07_evaluasi_test.py --data dataset/data.yaml --e1 path/ke/E1/best.pt --e3 path/ke/E3/best.pt --device cpu --output Laporan/hasil_test_humanoid_soccer.csv
```

Bobot model, cache, dan output training disimpan lokal dan tidak perlu di-commit.

## Penutup

Proyek ini membandingkan dua konfigurasi YOLO26n untuk mendeteksi objek Humanoid Soccer melalui eksperimen E1 dan E3. Hasil validasi dan pengujian menunjukkan adanya perbedaan antara kualitas deteksi dan kecepatan komputasi pada masing-masing konfigurasi. Seluruh hasil, visualisasi, dan rekap metrik disediakan dalam repository ini sebagai dokumentasi proses eksperimen. Karena evaluasi test masih menggunakan subset berukuran terbatas, pengujian dengan data yang lebih beragam diperlukan sebelum menarik kesimpulan untuk penggunaan di kondisi nyata.
