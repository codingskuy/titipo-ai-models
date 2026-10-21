"""Uji kontrak serving skor vendor (TTP-AI-003). Butuh `jsonschema` (requirements-dev.txt)."""
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "docs" / "serving"


def muat(nama):
    return json.loads((S / nama).read_text())


class KontrakSkor(unittest.TestCase):
    def setUp(self):
        self.req_schema = muat("permintaan-skor.schema.json")
        self.res_schema = muat("respons-skor.schema.json")

    def test_skema_valid(self):
        jsonschema.Draft202012Validator.check_schema(self.req_schema)
        jsonschema.Draft202012Validator.check_schema(self.res_schema)

    def test_contoh_lolos_skema(self):
        jsonschema.validate(muat("contoh-permintaan.json"), self.req_schema)
        jsonschema.validate(muat("contoh-respons.json"), self.res_schema)

    def test_respons_wajib_skor_dan_alasan(self):
        r = muat("contoh-respons.json")
        del r["hasil"][0]["alasan"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(r, self.res_schema)

    def test_skor_di_luar_0_1_ditolak(self):
        r = muat("contoh-respons.json")
        r["hasil"][0]["skor"] = 1.5
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(r, self.res_schema)

    def test_maks_5_hasil(self):
        r = muat("contoh-respons.json")
        r["hasil"] = r["hasil"] * 3
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(r, self.res_schema)

    def test_permintaan_tanpa_pii(self):
        p = muat("contoh-permintaan.json")
        self.assertNotIn("nama", p)
        self.assertNotIn("alamat", p)
        self.assertNotIn("telepon", p)
        self.assertFalse(self.req_schema.get("additionalProperties", True))


class SpesifikasiTeks(unittest.TestCase):
    def setUp(self):
        self.doc = (S / "SPESIFIKASI-SERVING.md").read_text()

    def test_memuat_pin_dan_onnx(self):
        for kata in ["axum 0.8.4", "uuid v7", "ONNX", "STUB_UNTIL", "25%", "2 minggu"]:
            self.assertIn(kata, self.doc)

    def test_pickle_hanya_disebut_sebagai_larangan(self):
        self.assertIn("pickle", self.doc.lower())
        self.assertIn("dilarang", self.doc.lower())

    def test_tidak_ada_bobot_di_repo(self):
        for ext in ("*.onnx", "*.pkl", "*.pt"):
            self.assertEqual(list(ROOT.rglob(ext)), [])


if __name__ == "__main__":
    unittest.main()
