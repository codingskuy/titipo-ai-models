# Model card — `rekomendasi-vendor`

> STATUS: STUB_UNTIL. Belum ada model terlatih. Produksi tetap memakai aturan jarak terdekat + riwayat. Dokumen ini adalah kerangka wajib (AGENTS.md) dan acuan baseline. Item bertanda **[ASUMSI]** belum punya sumber di dokumen beku v1.0.0 dan perlu dikonfirmasi TownHall.

## Identitas dan versi

| Bidang | Nilai |
|---|---|
| Nama | `rekomendasi-vendor` |
| Versi model | belum ada. Format rilis kelak: `titipo-rekomendasi-vendor-vYYYYMMDD` (`models/RELEASES.md`) |
| Versi kartu | 0.1.0 (stub) |
| Pemilik | Divisi TitipO |
| Tujuan | Urutkan 5 vendor terbaik per rumah tangga; keluaran saran baca saja |
| Bukan tujuan | Menentukan fee 12%, repeat 40%, cutoff 20.00, jendela serah 06.00-08.00 |

## Sumber data

- Event anonim 90 hari dari `titipo-data-pipeline`; tidak membaca DB titipo langsung.
- Fitur rencana **[ASUMSI]**: id area, jadwal keliling, riwayat 30 hari (anonim), `jarak_km`, `rating`, `sisa_kuota`, `prioritas` (nama fitur mengikuti skema `VendorRingkas` di `titipo-backend-service` `docs/api/openapi.yaml`).
- Label **[ASUMSI]**: vendor yang dipilih rumah tangga pada satu sesi daftar vendor. Event pemicu belum didaftarkan di registry 11 event (KONTEKS-LINTAS-DIVISI §3); penambahan event butuh bump versi di TownHall.
- Anonimisasi: rumah tangga dan vendor memakai id samaran; tanpa nama, alamat, telepon.
- Dataset contoh: `contoh/contoh-100-baris.csv`, 60 baris sintetis (12 sesi x 5 vendor), id `RT-NNN` dan `V-SAMAR-NN`. Bukan data nyata.

## Metrik eval

Metrik target (`models/README.md`): CTR pilihan >= 25% dan pembatalan turun.

| Metrik | Definisi kerja **[ASUMSI]** | Target |
|---|---|---|
| `ctr_pilihan_top1` | Persentase sesi saat pilihan rumah tangga jatuh di peringkat 1 | >= 25% (ambang rollback juga 25%, selama 2 minggu) |
| `hit_at_3` | Persentase sesi saat pilihan masuk 3 teratas | dicatat, belum bertarget |
| `tingkat_batal` | Pembatalan per pesanan, dari event pipeline | turun dibanding baseline (angka belum ditetapkan) |

Definisi CTR pilihan belum dibakukan di dokumen beku; tabel di atas hanya definisi kerja.

## Baseline manual

Aturan produksi saat ini: urut jarak naik, pemutus seri riwayat 30 hari turun, lalu `vendor_id`. Implementasi: `eval/baseline_manual.py`; uji: `tests/test_baseline_manual.py`.

Hasil pada dataset contoh sintetis (`python3 models/rekomendasi-vendor/eval/baseline_manual.py`):

| Metrik | Nilai |
|---|---|
| sesi | 12 |
| hit_at_1 / ctr_pilihan_top1 | 0,417 |
| hit_at_3 | 0,833 |

Angka ini hanya membuktikan skrip berjalan. Dataset dibangkitkan acak (seed 7) dan TIDAK mewakili perilaku nyata, jadi tidak boleh dikutip sebagai acuan bisnis. Baseline nyata dihitung ulang dari event pipeline 90 hari sebelum STUB_UNTIL dicabut, lalu dicatat di `models/RELEASES.md`.

## Bobot dan artefak

- Belum ada bobot. Format: ONNX (lihat TTP-AI-003). Tanpa pickle di jalur produksi.
- Berkas > 10 MB tidak masuk repo. Catat di tabel berikut saat rilis pertama:

| Artefak | URL object storage | SHA-256 | Ukuran |
|---|---|---|---|
| (belum ada) | - | - | - |

## Batasan dan risiko

- Cold start: rumah tangga tanpa riwayat jatuh ke aturan jarak.
- Salah peringkat dapat menaikkan vendor jauh; mitigasi STUB_UNTIL dan rollback ke aturan manual.
- Bias popularitas: vendor baru kurang terekspos **[ASUMSI]**.
- Bocor PII: dataset ditolak bila ada nama/alamat/telepon; audit 100 baris contoh tiap rilis.
- Hanya urutan saran; tidak menyentuh pesanan, fee, ledger, atau auth.

## Peninjau dan persetujuan

Peninjau Divisi TitipO: belum ditunjuk. Persetujuan naik produksi: PR TownHall yang mencabut STUB_UNTIL.
