# Spesifikasi serving skor vendor (TTP-AI-003)

> STATUS: STUB_UNTIL. Belum ada service atau bobot. Dokumen ini adalah spesifikasi target; kontrak bertanda **[ASUMSI]** adalah usulan, bukan kontrak beku (lihat ADR-0002, status Diusulkan).

## 1. Format bobot

- Satu-satunya format produksi: ONNX. Konversi dari scikit-learn dengan `skl2onnx` **[ASUMSI alat]**, opset dikunci per rilis dan dicatat di `models/RELEASES.md`.
- pickle (`.pkl`, `joblib`) dan `.pt` dilarang di jalur produksi; `.gitignore` sudah menolak `*.onnx`, `*.pt`, `*.pkl`.
- Berkas > 10 MB tidak masuk repo; simpan di object storage, catat URL + SHA-256 di kartu model. Service memverifikasi SHA-256 saat memuat; checksum tidak cocok = gagal start, jatuh ke aturan manual.

## 2. Service Rust

- axum 0.8.4 + uuid v7, selaras `titipo-backend-service` (`Cargo.toml` backend saat ini menulis `axum = "0.8"`; patch 0.8.4 dikunci lewat `Cargo.lock`, perlu dicek saat implementasi). Tokio sebagai runtime.
- Runtime inferensi ONNX: belum dipilih (ADR-0002 butir 5).
- Hanya baca: tidak ada tulis ke DB titipo; data masukan dikirim pemanggil, tidak diambil dari DB.
- Pemanggil: `titipo-backend-service` server-ke-server memakai `X-Titipo-Service-Key` (pola yang sudah ada di AGENTS.md backend) **[ASUMSI]**. Klien (KMP/web) tidak memanggil service ini dan tidak menghitung model; backend meneruskan hasil skor.

## 3. Kontrak **[ASUMSI]**

`POST /v1/rekomendasi-vendor/skor` (rute belum ada di FSD beku). Idempotensi: aman diulang (baca saja), kunci idempoten ULID tidak diperlukan.

- Permintaan: `permintaan-skor.schema.json` (contoh `contoh-permintaan.json`). Fitur mengikuti `VendorRingkas` backend ditambah `riwayat_30h`. ID rumah tangga samaran; tanpa nama, alamat, telepon (skema menolak properti lain).
- Respons 200: `respons-skor.schema.json` (contoh `contoh-respons.json`).
  - `skor` 0..1 (tidak berdimensi uang atau berat).
  - `alasan` 1-3 butir berkode (`JARAK_DEKAT`, `SERING_DIPESAN`, `RATING_TINGGI`, `KUOTA_TERSEDIA`, `VENDOR_PRIORITAS`) + teks pendek; klien menampilkan teks apa adanya.
  - `sumber`: `model` atau `aturan_manual`. Pada STUB_UNTIL, service (atau backend) selalu menjawab `aturan_manual` (urut jarak lalu riwayat).
  - `versi_model`: format `titipo-<nama>-vYYYYMMDD`.
- Galat: memakai bentuk `AppError` backend (`kode`, `pesan`, `detail`) **[ASUMSI]**: 400 `PERMINTAAN_TIDAK_VALID`, 401/403 kunci layanan salah, 503 `MODEL_TIDAK_SIAP` (backend lalu jatuh ke aturan manual). Kode-kode ini usulan.
- Model bukan penentu fee 12%, repeat 40%, cutoff 20.00, atau jendela serah 06.00-08.00; kontrak tidak memuat bidang tersebut.

## 4. Kriteria pencabutan STUB_UNTIL dan rollback

Syarat mencabut STUB_UNTIL (semua, lewat PR TownHall):
1. Model card lengkap dan baseline nyata dari event pipeline 90 hari (TTP-AI-002) tercatat.
2. Bobot ONNX di object storage dengan checksum; tanpa pickle.
3. Kontrak ini disetujui TownHall (ADR-0002 menjadi Diterima).
4. Uji kontrak lulus; peninjau Divisi TitipO ditunjuk.

Ambang rollback: CTR pilihan di bawah 25% selama 2 minggu berturut-turut mengaktifkan kembali STUB_UNTIL; rollback = matikan flag saran dan kembali ke urutan jarak terdekat, tanpa migrasi data. Definisi CTR pilihan belum dibakukan (lihat model card, **[ASUMSI]**).

## 5. Uji

`pip install -r requirements-dev.txt && python3 -m unittest discover -s tests` memvalidasi skema dan contoh. Uji beban, latensi, dan inferensi ONNX nyata belum ada karena belum ada service.
