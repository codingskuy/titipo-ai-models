# ADR-0002 — Serving model via API Rust + bobot ONNX

Status: Diusulkan | Tanggal: 2026-10-21

## Konteks

ADR-0001 mengunci pelatihan Python 3.12 + scikit-learn, bobot ONNX, dan serving lewat API Rust. TTP-AI-003 meminta spesifikasi serving yang selaras pin `titipo-backend-service` (axum 0.8, uuid v7) dan kriteria pencabutan STUB_UNTIL. Dokumen beku tidak mendefinisikan rute atau skema skor, jadi kontrak di sini adalah usulan.

## Keputusan

1. Bobot hanya berformat ONNX (hasil `skl2onnx`); pickle dilarang di jalur produksi.
2. Serving oleh service Rust (axum 0.8.4, uuid v7) yang memuat ONNX; tidak ada serving Python.
3. Kontrak respons skor + alasan: `docs/serving/respons-skor.schema.json` (skor 0..1, maks 5 vendor, alasan berkode). Detail di `docs/serving/SPESIFIKASI-SERVING.md`.
4. Rollback otomatis bila CTR pilihan < 25% selama 2 minggu; STUB_UNTIL dicabut hanya lewat PR TownHall.
5. Runtime ONNX di Rust (misalnya crate `ort` atau `tract`) belum dipilih; ditunda ke ADR berikutnya setelah uji kompatibilitas operator.

## Konsekuensi

Satu kontrak ditulis di sini sebelum ada implementasi; bila TownHall/FSD kemudian mendefinisikan rute berbeda, kontrak ini digantikan ADR baru. Perubahan skema = bump versi + ADR (AGENTS.md butir c).
