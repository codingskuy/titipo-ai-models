# models/ — Katalog stub rekomendasi vendor

> STATUS stub, fase nanti. Belum ada berkas model (`.onnx`, `.pt`, `.pkl`) di repo ini.

## Kartu model yang direncanakan

### 1. `rekomendasi-vendor` (direncanakan)

- Tujuan: urutkan 5 vendor terbaik per rumah tangga.
- Masukan: id area, jadwal keliling, riwayat 30 hari (anonim).
- Keluaran: daftar vendor + skor + alasan singkat.
- Metrik target: CTR pilihan ≥ 25%, pembatalan turun.

### 2. `prediksi-permintaan-harian` (direncanakan)

- Tujuan: estimasi titipan per rute per hari.
- Masukan: event pesanan 90 hari dari pipeline.
- Keluaran: angka per rute + interval keyakinan.

## Kartu model

- `rekomendasi-vendor`: [MODEL_CARD.md](rekomendasi-vendor/MODEL_CARD.md) (stub, baseline manual).

## Aturan berkas

- Bobot model TIDAK di-commit bila > 10 MB — simpan di object storage, catat URL + checksum di sini.
- Dataset contoh maksimal 100 baris, nama samaran.

## Tautan

- TownHall: https://github.com/Coding-Skuy/TitipO-TownHall
- Pipeline sumber event: https://github.com/Coding-Skuy/titipo-data-pipeline
