import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class IOArchitectureGuidanceTests(unittest.TestCase):
    def test_architecture_makes_io_the_primary_constraint(self):
        page = (DOCS / "concepts/why-not-kubernetes-everywhere.md").read_text().lower()
        for phrase in (
            "i/o patterns were the most important design constraint",
            "no shared filesystem can make an adversarial access pattern free",
            "ceph",
            "slurm",
            "nomad",
            "node-local scratch",
        ):
            self.assertIn(phrase, page)

    def test_capability_overview_exposes_io_first_architecture(self):
        page = (DOCS / "concepts/what-rcc-can-do.md").read_text().lower()
        self.assertIn("the architecture starts with i/o behavior", page)
        self.assertIn("ceph", page)
        self.assertIn("kubernetes", page)
        self.assertIn("rcc-safe vs code defaults", page)

    def test_returning_user_page_highlights_io_and_short_video_plan(self):
        page = (DOCS / "getting-started/what-changed.md").read_text().lower()
        self.assertIn("i/o pattern matters more than raw storage bandwidth", page)
        self.assertIn("3–4 minute", page)
        self.assertIn("stage-2 video plan", page)
        self.assertIn("rcc-safe vs code defaults", page)

    def test_vscode_first_use_page_contains_low_io_settings(self):
        page = (DOCS / "getting-started/vscode.md").read_text()
        for token in (
            '"search.followSymlinks": false',
            '"search.useIgnoreFiles": true',
            '"files.watcherExclude"',
            '"search.exclude"',
            '"**/.snakemake/**"',
            '"**/.nextflow/**"',
            '"**/data/**"',
            '"**/results/**"',
        ):
            self.assertIn(token, page)

    def test_storage_lesson_is_backend_neutral_and_migration_aware(self):
        page = (DOCS / "course/class-15-storage-architecture.md").read_text().lower()
        self.assertIn("s3-compatible object layer", page)
        self.assertIn("minio", page)
        self.assertIn("seaweedfs", page)
        self.assertIn("do not build a scientific workflow around either product name", page)
        self.assertIn("good performance comes primarily from good i/o patterns", page)

    def test_short_video_narration_is_staged_but_not_a_stage1_dependency(self):
        narration = ROOT / "narration/RCC_What_Changed_From_Old_Cluster_Narration.md"
        self.assertTrue(narration.is_file())
        text = narration.read_text().lower()
        self.assertIn("target length", text)
        self.assertIn("3–4 minutes", text)
        self.assertIn("stage 2 media", text)
        self.assertIn("i/o pattern dominates", text)


if __name__ == "__main__":
    unittest.main()
