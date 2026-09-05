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

    def test_home_distinguishes_current_foundation_from_target_state(self):
        home = (DOCS / "index.md").read_text(encoding="utf-8").lower()
        self.assertIn("## rcc today", home)
        self.assertIn("## coming next", home)

        current = home[home.index("## rcc today"):home.index("## coming next")]
        for phrase in (
            "files is the current browser data path",
            "account and project self-service is ready now",
            "rcc workers and slurm analysis are ready now",
            "managed nextflow-to-slurm support is ready now",
            "project samba shares are ready now",
        ):
            self.assertIn(phrase, current)

        future = home[home.index("## coming next"):home.index("## what rcc can do")]
        for phrase in (
            "rcc analysis notebook and workflow are not yet released",
            "rcc-to-coscine self-service transfer is not yet released",
            "protected project vhosts are not yet released",
            "ardia integration is not yet released",
        ):
            self.assertIn(phrase, future)

    def test_advanced_capability_page_repeats_status_boundary_once(self):
        page = (DOCS / "concepts/what-rcc-can-do.md").read_text(encoding="utf-8").lower()
        self.assertIn("## current foundation versus integrated target", page)
        self.assertIn("current rcc is already a substantial research-computing foundation", page)
        self.assertIn("not yet released", page)


if __name__ == "__main__":
    unittest.main()
