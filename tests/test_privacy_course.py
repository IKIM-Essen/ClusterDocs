import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASS = ROOT / "docs/course/class-11-biomedical-data-privacy.md"
QUICK = ROOT / "docs/security/rcc-biomedical-data-admission.md"


class PrivacyCourseTests(unittest.TestCase):
    def test_course_has_official_sources_and_contact(self):
        text = CLASS.read_text(encoding="utf-8")
        for token in [
            "eur-lex.europa.eu/eli/reg/2016/679/oj",
            "gesetze-im-internet.de/bdsg_2018/__22.html",
            "gesetze-im-internet.de/gdng/",
            "gesetze-im-internet.de/gdng/__7.html",
            "gesetze-im-internet.de/stgb/__203.html",
            "www.uk-essen.de/datenschutz",
            "datenschutz@uk-essen.de",
            "Christian Hecke",
        ]:
            self.assertIn(token, text)

    def test_course_permits_governed_genomic_and_imaging_research(self):
        text = CLASS.read_text(encoding="utf-8").lower()
        self.assertIn("not direct identifiers in the same sense", text)
        self.assertIn("approved genomic data", text)
        self.assertIn("approved x-ray, ct, mri", text)
        self.assertIn("controlled research enclave", text)
        self.assertIn("re-identification key stay outside rcc", text)

    def test_defacing_is_not_a_default_requirement(self):
        text = CLASS.read_text(encoding="utf-8").lower()
        self.assertIn("not necessary", text)
        self.assertIn("not a default requirement", text)
        self.assertIn("can remove relevant anatomy", text)

    def test_training_does_not_claim_machine_or_legal_validation(self):
        text = CLASS.read_text(encoding="utf-8").lower()
        self.assertIn("does not use an automated research-file scanner", text)
        self.assertNotIn("validate_data_admission.py", text)
        self.assertFalse((ROOT / "exercises/privacy").exists())

    def test_quick_guide_has_direct_identifier_boundary(self):
        text = QUICK.read_text(encoding="utf-8").lower()
        self.assertIn("may process approved biomedical research data", text)
        self.assertIn("patient, case, insurance", text)
        self.assertIn("defacing", text)


if __name__ == "__main__":
    unittest.main()
