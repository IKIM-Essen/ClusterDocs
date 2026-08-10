import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/course/class-07-nextflow.md"
EXAMPLE = ROOT / "docs/classes/examples/nextflow-rcc/main.nf"


class NextflowDocsTests(unittest.TestCase):
    def test_navigation_contains_nextflow_class(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        builder = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
        self.assertIn("Class 7 - Nextflow on RCC: course/class-07-nextflow.md", nav)
        self.assertIn("('Course','Class 7 · Nextflow','course/class-07-nextflow.md')", builder)

    def test_user_contract_keeps_controller_off_gateways(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("allocation-backed interactive node", text)
        self.assertIn("Do not run Nextflow on `login.ikim.uk-essen.de`", text)
        self.assertNotIn("approved submission host", text)
        self.assertIn("tmux", text)
        self.assertIn("service status — ready now", text.lower())

    def test_all_public_nextflow_summaries_name_the_interactive_shellhost(self):
        paths = (
            ROOT / "README.md",
            ROOT / "docs/tldr.md",
            ROOT / "docs/classes/examples/nextflow-rcc/README.md",
            ROOT / "source/part2.md",
        )
        for path in paths:
            with self.subTest(path=path):
                text = " ".join(path.read_text(encoding="utf-8").lower().split())
                self.assertIn("interactive node", text)
                self.assertIn("shellhost", text)

    def test_work_state_and_scratch_are_distinct(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Never set", text)
        self.assertIn("`/local`", text)
        self.assertIn("label 'rcc_scratch'", text)
        self.assertIn("-resume", text)

    def test_examples_are_bounded_and_synthetic(self):
        text = EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("cpus 1", text)
        self.assertIn("memory 512.MB", text)
        self.assertIn("time 5.m", text)
        self.assertNotIn("patient", text.lower())
        self.assertNotIn("latest", text.lower())

    def test_docs_cover_scheduler_and_container_policy(self):
        text = DOC.read_text(encoding="utf-8")
        for token in ("Slurm", "Apptainer", "rcc_array", "rcc_gpu_a6000", "sacct", "RELEASE_TAG"):
            with self.subTest(token=token):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
