import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class ExternalReaderContractTests(unittest.TestCase):
    def test_external_reader_review_is_recorded(self):
        review = ROOT / "meta/EXTERNAL_READER_REVIEW_2026-09-05.md"
        self.assertTrue(review.is_file())
        text = review.read_text(encoding="utf-8").lower()
        for phrase in (
            "the project is the center of rcc",
            "data-blind by default",
            "i/o behavior is a foundational engineering principle",
            "current state versus target state",
        ):
            self.assertIn(phrase, text)

    def test_home_makes_analysis_part_of_the_release_bundle(self):
        home = (DOCS / "index.md").read_text(encoding="utf-8").lower()
        self.assertIn("## clusterdocs 3 release bundle", home)
        self.assertNotIn("## coming next", home)
        for phrase in (
            "rcc home",
            "files",
            "rcc analysis",
            "my rcc",
            "rcc admin",
            "must be ready together before publication",
            "rcc analysis remains a release blocker",
        ):
            self.assertIn(phrase, home)

    def test_advanced_capability_page_uses_integrated_browser_baseline(self):
        page = (DOCS / "concepts/what-rcc-can-do.md").read_text(encoding="utf-8").lower()
        self.assertIn("## the integrated browser baseline", page)
        self.assertIn("rcc home, files, rcc analysis, my rcc, and rcc admin", page)
        self.assertIn("must all be ready before clusterdocs 3 is published", page)
        self.assertIn("rcc_analysis", page)


if __name__ == "__main__":
    unittest.main()
