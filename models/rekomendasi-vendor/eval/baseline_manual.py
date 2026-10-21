"""Baseline manual rekomendasi vendor: jarak terdekat, pemutus seri riwayat 30 hari.

Ini aturan yang TETAP berlaku di produksi selama STUB_UNTIL aktif. Skrip ini
hanya mengukur seberapa sering aturan itu menebak pilihan rumah tangga pada
dataset contoh, sebagai acuan pembanding model kelak. Hanya pustaka standar.
"""
import csv
import sys
from pathlib import Path

CONTOH = Path(__file__).resolve().parents[1] / "contoh" / "contoh-100-baris.csv"


def muat_sesi(path):
    sesi = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            sesi.setdefault(r["sesi_id"], []).append(
                {
                    "vendor_id": r["vendor_id"],
                    "jarak_km": float(r["jarak_km"]),
                    "riwayat_30h": int(r["riwayat_30h"]),
                    "dipilih": int(r["dipilih"]),
                }
            )
    return sesi


def urutkan(kandidat):
    """Jarak naik, lalu riwayat turun, lalu vendor_id (deterministik)."""
    return sorted(kandidat, key=lambda k: (k["jarak_km"], -k["riwayat_30h"], k["vendor_id"]))


def hitung_metrik(sesi, k=3):
    n = len(sesi)
    hit1 = hitk = 0
    for kandidat in sesi.values():
        urut = urutkan(kandidat)
        if urut[0]["dipilih"]:
            hit1 += 1
        if any(x["dipilih"] for x in urut[:k]):
            hitk += 1
    return {
        "sesi": n,
        "hit_at_1": hit1 / n if n else 0.0,
        f"hit_at_{k}": hitk / n if n else 0.0,
        # CTR pilihan top-1: pilihan jatuh di vendor peringkat 1 (definisi kerja, asumsi)
        "ctr_pilihan_top1": hit1 / n if n else 0.0,
    }


def main(path=CONTOH):
    m = hitung_metrik(muat_sesi(path), k=3)
    print("STUB: dataset contoh sintetis, bukan bukti produksi")
    for kunci, nilai in m.items():
        print(f"{kunci}: {nilai if isinstance(nilai, int) else round(nilai, 3)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
