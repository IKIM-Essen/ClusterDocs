from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BranchAndPRAuditTests(unittest.TestCase):
    def test_every_pr_number_and_surviving_branch_class_is_disposed(self):
        audit = (ROOT / "meta/BRANCH_PR_AUDIT.md").read_text()
        for marker in (
            "#1",
            "#2–8, #10–30",
            "#31",
            "#32–41",
            "#42",
            "#43",
            "#44",
            "#45–47",
            "#48",
            "#49–56",
            "#57",
            "#58–59",
            "#60–61",
            "`main`",
            "`clusterdocs-ng`",
            "`gh-pages`",
            "`doc/apptainer`",
            "`johanneskoester-patch-1`",
            "`vscode/patterns`",
        ):
            self.assertIn(marker, audit)

    def test_unsafe_open_cleanup_pr_is_not_imported(self):
        public_docs = "\n".join(path.read_text() for path in (ROOT / "docs").rglob("*.md"))
        self.assertNotIn('rm -rf /local/work/$USER', public_docs)
        self.assertIn("$SLURM_TMPDIR", public_docs)

    def test_open_vscode_and_main_module_intents_are_already_present(self):
        vscode = (ROOT / "docs/reference/access-ssh-vscode.md").read_text()
        software = (ROOT / "docs/reference/software-workflows.md").read_text()
        self.assertIn('"search.exclude"', vscode)
        self.assertIn('"files.watcherExclude"', vscode)
        self.assertIn("does not use Environment Modules or Lmod", software)


if __name__ == "__main__":
    unittest.main()
