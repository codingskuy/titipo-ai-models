"""Uji baseline manual rekomendasi vendor (TTP-AI-002). Hanya stdlib."""
import csv
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RV = ROOT / "models" / "rekomendasi-vendor"
sys.path.insert(0, str(RV / "eval"))

import baseline_manual as bm  # noqa: E402


class DatasetContoh(unittest.TestCase):
    def test_maks_100_baris(self):
        with open(RV / "contoh" / "contoh-100-baris.csv", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertLessEqual(len(rows), 100)

    def test_tanpa_pii_nama_samaran(self):
        with open(RV / "contoh" / "contoh-100-baris.csv", newline="") as f:
            for r in csv.DictReader(f):
                self.assertRegex(r["rumah_tangga"], r"^RT-\d{3}$")
                self.assertRegex(r["vendor_id"], r"^V-SAMAR-\d{2}$")

    def test_satu_pilihan_per_sesi(self):
        sesi = bm.muat_sesi(RV / "contoh" / "contoh-100-baris.csv")
        for kandidat in sesi.values():
            self.assertEqual(sum(k["dipilih"] for k in kandidat), 1)


class UrutanBaseline(unittest.TestCase):
    def test_jarak_terdekat_dulu(self):
        k = [
            {"vendor_id": "A", "jarak_km": 2.0, "riwayat_30h": 9, "dipilih": 0},
            {"vendor_id": "B", "jarak_km": 0.5, "riwayat_30h": 0, "dipilih": 1},
        ]
        self.assertEqual([x["vendor_id"] for x in bm.urutkan(k)], ["B", "A"])

    def test_riwayat_pemutus_seri(self):
        k = [
            {"vendor_id": "A", "jarak_km": 1.0, "riwayat_30h": 1, "dipilih": 0},
            {"vendor_id": "B", "jarak_km": 1.0, "riwayat_30h": 5, "dipilih": 1},
        ]
        self.assertEqual(bm.urutkan(k)[0]["vendor_id"], "B")

    def test_metrik_hit_dan_ctr(self):
        sesi = {
            "S1": [
                {"vendor_id": "A", "jarak_km": 1, "riwayat_30h": 0, "dipilih": 1},
                {"vendor_id": "B", "jarak_km": 2, "riwayat_30h": 0, "dipilih": 0},
            ],
            "S2": [
                {"vendor_id": "A", "jarak_km": 1, "riwayat_30h": 0, "dipilih": 0},
                {"vendor_id": "B", "jarak_km": 2, "riwayat_30h": 0, "dipilih": 1},
            ],
        }
        m = bm.hitung_metrik(sesi, k=1)
        self.assertEqual(m["sesi"], 2)
        self.assertAlmostEqual(m["hit_at_1"], 0.5)
        self.assertAlmostEqual(m["ctr_pilihan_top1"], 0.5)

    def test_cli_menghasilkan_ringkasan(self):
        out = subprocess.run(
            [sys.executable, str(RV / "eval" / "baseline_manual.py")],
            capture_output=True, text=True, check=True,
        ).stdout
        self.assertIn("hit_at_1", out)
        self.assertIn("STUB", out)


if __name__ == "__main__":
    unittest.main()
