from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs" / "reference" / "slurm.md"


class SlurmExecutionModelTests(unittest.TestCase):
    def test_reference_explains_all_three_cpu_modes(self):
        text = REFERENCE.read_text()
        for phrase in ("cpu_short", "interactive", "cpu_nodes"):
            self.assertIn(phrase, text)
        self.assertIn("two hours", text.lower())
        self.assertIn("long runners", text.lower())
        self.assertIn("human-in-the-loop", text.lower())

    def test_reference_does_not_equate_allocation_with_whole_node(self):
        text = REFERENCE.read_text().lower()
        self.assertIn("not normally an exclusive reservation", text)
        self.assertIn("--nodes=1", text)
        self.assertIn("does not make that node exclusive", text)

    def test_short_training_jobs_use_short_queue(self):
        for script in (ROOT / "exercises" / "slurm").glob("*/job.sbatch"):
            self.assertIn("#SBATCH --partition=cpu_short", script.read_text())

    def test_interactive_examples_are_bounded(self):
        examples = ROOT / "examples" / "interactive-workflows"
        for name in ("jupyter", "shiny"):
            text = (examples / name / f"{name}.sbatch").read_text()
            self.assertIn("#SBATCH --partition=interactive", text)
            self.assertIn("#SBATCH --time=04:00:00", text)


if __name__ == "__main__":
    unittest.main()
