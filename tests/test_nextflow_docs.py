import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/course/class-07-nextflow.md"
EXAMPLE = ROOT / "docs/classes/examples/nextflow-rcc/main.nf"
RUNNER = ROOT / "docs/classes/examples/nextflow-rcc/run-rcc-nextflow.sh"
RESOURCE_EXAMPLE = ROOT / "docs/classes/examples/nextflow-rcc/resources.config.example"


class NextflowDocsTests(unittest.TestCase):
    def test_navigation_contains_nextflow_class(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        builder = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
        self.assertIn("Class 7 - Nextflow on RCC (not yet released): course/class-07-nextflow.md", nav)
        self.assertIn("('Course','Class 7 · Nextflow · Not yet released','course/class-07-nextflow.md')", builder)

    def test_user_contract_keeps_controller_off_gateways(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("interactive node (`shellhost`)", text)
        self.assertIn("Do not run Nextflow on `login.ikim.uk-essen.de`", text)
        self.assertNotIn("approved submission host", text)
        self.assertIn("tmux", text)
        self.assertIn("one active Nextflow controller", text)
        self.assertIn("not yet released", text.lower())

    def test_all_public_nextflow_summaries_name_the_interactive_shellhost(self):
        paths = (
            ROOT / "README.md",
            ROOT / "docs/index.md",
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
        self.assertIn("Copying a multi-terabyte input", text)

    def test_examples_are_bounded_and_synthetic(self):
        text = EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("cpus 1", text)
        self.assertIn("memory 512.MB", text)
        self.assertIn("time 5.m", text)
        self.assertNotIn("patient", text.lower())
        self.assertNotIn("latest", text.lower())

    def test_docs_cover_scheduler_container_and_measurement_policy(self):
        text = DOC.read_text(encoding="utf-8")
        for token in (
            "Slurm",
            "Apptainer",
            "rcc_array",
            "rcc_gpu_a6000",
            "sacct",
            "RELEASE_TAG",
            "terminated by the external system",
            "unknown userid",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)
        self.assertIn("pilot, measure, tune, then scale", text.lower())

    def test_docs_forbid_user_site_config_reimplementation(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("Do not copy a complete `slurm.config`", text)
        for token in (
            "process.executor",
            "executor.queueSize",
            "executor.submitRateLimit",
            "apptainer.cacheDir",
        ):
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_teaching_runner_prevents_duplicate_controller_and_preserves_log(self):
        text = RUNNER.read_text(encoding="utf-8")
        self.assertIn("flock -n 9", text)
        self.assertIn(".rcc-nextflow-controller.lock", text)
        self.assertIn("Use -resume only after the previous controller has stopped", text)
        self.assertIn('logs/nextflow-${stamp}.log', text)
        self.assertIn("exec rcc-nextflow", text)

    def test_resource_example_cannot_be_mistaken_for_site_config(self):
        text = RESOURCE_EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("withName:", text)
        self.assertIn("cpus = 8", text)
        self.assertIn("memory = 32.GB", text)
        self.assertIn("time = 6.h", text)
        for forbidden in (
            "executor =",
            "queue =",
            "clusterOptions =",
            "queueSize =",
            "submitRateLimit =",
            "workDir =",
            "apptainer.enabled =",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
