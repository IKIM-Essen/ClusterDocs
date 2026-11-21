import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(relative: str) -> tuple[str, str]:
    page = (DOCS / relative).read_text(encoding="utf-8")
    return page, " ".join(page.replace("**", "").split())


class AnalysisBrowserFirstContractTests(unittest.TestCase):
    def test_draft_analysis_status_describes_the_planned_route(self):
        # The release candidate's Analysis status is separate from Coscine.
        page, flat = normalized("analysis/rcc-analysis.md")
        _, status, _ = page.split("\n\n", 2)
        self.assertIn("Service status — not yet released", status)
        self.assertNotIn("https://rcc.ikim.uk-essen.de/analysis/", status)
        self.assertIn("`https://rcc.ikim.uk-essen.de/analysis/`", page)
        self.assertIn("RCC-to-Coscine transfer is not yet released", flat)
        self.assertNotIn("analysis.ikim.uk-essen.de", page)
        self.assertIn("`/notebook/`", page)

    def test_data_analysis_keeps_available_compute_distinct_from_the_browser_pilot(self):
        _, path = normalized("paths/data-analysis.md")
        _, services = normalized("concepts/rcc-services.md")
        self.assertIn("RCC workers and Slurm analysis are ready now", path)
        self.assertIn("browser-based RCC Analysis is not yet released", path)
        self.assertNotIn("https://rcc.ikim.uk-essen.de/analysis/", path)
        self.assertIn("| RCC Analysis | explore data in a notebook or run a repeatable governed workflow | not yet released |",
                      services)

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
