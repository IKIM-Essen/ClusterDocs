import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EfficientLocalIOClassTests(unittest.TestCase):
    def test_advanced_class_pages_and_examples_exist(self):
        required = [
            ROOT / "docs/course/class-14-efficient-io.md",
            ROOT / "docs/course/class-15-storage-architecture.md",
            ROOT / "docs/classes/examples/make-synthetic-fastq.sh",
            ROOT / "docs/classes/examples/direct-io-demo.sh",
            ROOT / "docs/classes/examples/local-io-demo.sh",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_examples_use_current_job_scratch_pattern(self):
        page = (ROOT / "docs/course/class-14-efficient-io.md").read_text()
        job = (ROOT / "docs/classes/examples/local-io-demo.sh").read_text()
        expected = "/local/work/${USER}/slurm-job-${SLURM_JOB_ID}"
        self.assertIn("SLURM_TMPDIR", page)
        self.assertIn("SLURM_TMPDIR", job)
        self.assertIn(expected, page)
        self.assertIn(expected, job)
        self.assertNotIn('/local/${USER}/${SLURM_JOB_ID}', page)
        self.assertNotIn('/local/${USER}/${SLURM_JOB_ID}', job)

    def test_custom_build_copies_downloadable_examples(self):
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("class_examples=DOCS/'classes/examples'", builder)
        self.assertIn("out/'classes/examples'", builder)

    def test_new_pages_are_part_of_course_navigation(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text()
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertNotIn("Advanced classes:", mkdocs)
        self.assertIn("('Course','Class 14 · Efficient local I/O'", builder)
        self.assertIn("('Course','Class 15 · Storage architecture'", builder)


if __name__ == "__main__":
    unittest.main()
