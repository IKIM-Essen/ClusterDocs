import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class GpuSelectionDocsTests(unittest.TestCase):
    def test_gpu_selection_is_part_of_class_five_navigation(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        builder = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
        self.assertIn("Class 5 - Slurm acceptance patterns: course/class-05-slurm.md", nav)
        self.assertIn("('Course','Class 5 · Slurm','course/class-05-slurm.md')", builder)
        self.assertNotIn("classes/gpu-selection.md", nav)
        self.assertNotIn("classes/gpu-selection.md", builder)

    def test_docs_teach_one_partition_and_typed_selection(self):
        text = (ROOT / "docs/course/class-05-slurm.md").read_text(encoding="utf-8")
        for token in (
            "gpu_nodes",
            "--gpus-per-node=1",
            "--gpus-per-node=rtx_a6000:1",
            "--constraint=gpu_arch_ampere",
            'gpu_model="rtx_a6000"',
            "apptainer exec --nv",
            "sacct -j JOB_ID",
        ):
            self.assertIn(token, text)
        for forbidden in ("--partition=gpu_ampere", "--partition=gpu_blackwell"):
            self.assertNotIn(forbidden, text)

    def test_examples_are_bounded(self):
        for name in ("gpu-any.sbatch", "gpu-rtx-a6000.sbatch"):
            text = (ROOT / "docs/classes/examples" / name).read_text(encoding="utf-8")
            self.assertIn("#SBATCH --partition=gpu_nodes", text)
            self.assertIn("#SBATCH --time=00:05:00", text)
            self.assertIn("#SBATCH --mem=4G", text)
            self.assertNotIn("--array", text)
            self.assertNotIn("srun --nodes", text)

if __name__ == "__main__":
    unittest.main()
