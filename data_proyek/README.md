# Dokumentasi Dataset YOLO

## Informasi Dataset

- **Nama dataset:** `dataset_v1`
- **Jumlah gambar:** 150 gambar
- **Jumlah data train:** 105 gambar
- **Jumlah data validation:** 30 gambar
- **Jumlah data test:** 15 gambar
- **Jumlah kelas:** 2 kelas

## Kelas Objek

| ID | Nama Kelas |
|---|---|
| 0 | MG90S |
| 1 | PCA9685 |

## Struktur Dataset

```text
dataset_v1/
|-- data.yaml
|-- images/
|   |-- train/
|   |-- val/
|   `-- test/
`-- labels/
    |-- train/
    |-- val/
    `-- test/
```

## Konfigurasi

File `data.yaml` berisi lokasi data train, validation, test, dan nama kelas yang digunakan dalam eksperimen YOLO.

**Catatan:** Folder gambar dan label dataset tidak disertakan dalam repository ini. Dataset harus disediakan secara terpisah agar pelatihan dan evaluasi dapat dijalankan kembali.