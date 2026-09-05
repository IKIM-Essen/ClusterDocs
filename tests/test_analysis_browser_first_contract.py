import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class AnalysisBrowserFirstContractTests(unittest.TestCase):
    def test_analysis_remains_staged_not_claimed_live(self):
        page = (DOCS / "analysis/rcc-analysis.md").read_text(encoding="utf-8")
        self.assertIn("not yet released to users", page.lower())
        self.assertIn("staged source configuration, not a claim of live", page)
        self.assertIn("https://analysis.ikim.uk-essen.de/", page)
        self.assertIn("`/notebook/`", page)

    def test_notebook_is_jupyter_only_and_terminal_is_same_boundary(self):
        page = (DOCS / "concepts/workbench-interfaces.md").read_text(encoding="utf-8")
        normalized = " ".join(page.split())
        self.assertIn("RCC does not plan to provide a browser IDE", normalized)
        self.assertIn("terminal may be available from JupyterLab as an advanced tool", normalized)
        self.assertIn("same Notebook allocation", normalized)
        self.assertIn("Jupyter is arbitrary code, not the sandbox", page)
        self.assertIn("private mode-0600 job Unix socket", normalized)

    def test_files_visibility_is_all_eligible_regular_projects(self):
        page = (DOCS / "concepts/rcc-files.md").read_text(encoding="utf-8")
        normalized = " ".join(page.split())
        self.assertIn("all current Files-enabled Regular projects", normalized)
        self.assertIn("primary project may be used as a convenient landing directory", normalized)
        self.assertIn("Controlled Data project", page)
        self.assertIn("multi-GiB browser upload", page)
        self.assertIn("same-user/same-project comparison", page)
        self.assertIn("not be “use SSH instead.”", page)

    def test_browser_users_do_not_choose_compute_profile(self):
        page = (DOCS / "analysis/rcc-analysis.md").read_text(encoding="utf-8")
        normalized = " ".join(page.split())
        self.assertIn("For a user with one eligible project, RCC should use it implicitly", normalized)
        self.assertIn("Browser users do not choose raw scheduler resources", normalized)
        self.assertIn("RCC does not provide a browser IDE in this release", normalized)


if __name__ == "__main__":
    unittest.main()
