import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(relative: str) -> tuple[str, str]:
    page = (DOCS / relative).read_text(encoding="utf-8")
    return page, " ".join(page.split())


class AnalysisBrowserFirstContractTests(unittest.TestCase):
    def test_analysis_remains_staged_not_claimed_live(self):
        page, flat = normalized("analysis/rcc-analysis.md")
        self.assertIn("not yet released to users", page.lower())
        self.assertIn("staged source configuration, not a claim of live availability", flat)
        self.assertIn("https://analysis.ikim.uk-essen.de/", page)
        self.assertIn("`/notebook/`", page)

    def test_notebook_is_jupyter_only_and_terminal_is_same_boundary(self):
        page, flat = normalized("concepts/workbench-interfaces.md")
        self.assertIn("RCC does not plan to provide a browser IDE", flat)
        self.assertIn("terminal may be available from JupyterLab as an advanced tool", flat)
        self.assertIn("same Notebook allocation", flat)
        self.assertIn("Jupyter is arbitrary code, not the sandbox", page)
        self.assertIn("private mode-0600 job Unix socket", flat)

    def test_files_visibility_is_all_eligible_regular_projects(self):
        page, flat = normalized("concepts/rcc-files.md")
        self.assertIn("all current Files-enabled Regular projects", flat)
        self.assertIn("primary project may be used as a convenient landing directory", flat)
        self.assertIn("Controlled Data project", page)
        self.assertIn("multi-GiB browser upload", page)
        self.assertIn("same-user/same-project comparison", page)
        self.assertIn("not be “use SSH instead.”", flat)

    def test_browser_users_do_not_choose_compute_profile(self):
        _, flat = normalized("analysis/rcc-analysis.md")
        self.assertIn("For a user with one eligible project, RCC should use it implicitly", flat)
        self.assertIn("Browser users do not choose raw scheduler resources", flat)
        self.assertIn("RCC does not provide a browser IDE in this release", flat)


if __name__ == "__main__":
    unittest.main()
