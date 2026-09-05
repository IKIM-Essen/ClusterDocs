import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def text(relative):
    return (DOCS / relative).read_text(encoding="utf-8")


def normalized(relative):
    return " ".join(text(relative).lower().split())


class ClusterDocs3ProductModelTests(unittest.TestCase):
    def test_home_is_task_first_and_capability_complete(self):
        home = normalized("index.md")
        for phrase in (
            "what do you want to do?",
            "instrument-to-project ingestion",
            "s3/object storage",
            "ai and coding-agent assistance without exporting protected project data",
            "coscine preservation",
            "domain applications such as seqlab",
        ):
            self.assertIn(phrase, home)

    def test_browser_path_precedes_advanced_cluster_topology(self):
        start = text("getting-started/index.md")
        browser = start.index("## Browser-first research")
        advanced = start.index("## Advanced/current compute path")
        ascii_model = start.index("Mac or Windows")
        self.assertLess(browser, advanced)
        self.assertLess(advanced, ascii_model)
        self.assertNotIn("ssh {{", start[browser:advanced].lower())

    def test_agent_boundary_is_data_blind_by_default(self):
        agents = normalized("concepts/agents-and-mcp.md")
        for phrase in (
            "data-blind by default",
            "the agent does not need the real rows",
            "rcc—not the agent—decides",
            "explicit exception",
        ):
            self.assertIn(phrase, agents)

    def test_advanced_capability_page_preserves_release_truth(self):
        capabilities = normalized("concepts/what-rcc-can-do.md")
        for phrase in (
            "sequencers, microscopes, mass spectrometers",
            "project s3/object storage",
            "slurm, gpus",
            "seqlab",
            "not yet released",
            "data-blind by default",
            "ready now",
        ):
            self.assertIn(phrase, capabilities)

    def test_novice_review_is_zero_ssh_and_pre_broad_rollout(self):
        guide = (ROOT / "meta/NOVICE_REVIEW_GUIDE.md").read_text(encoding="utf-8").lower()
        self.assertIn("before broad exposure", guide)
        self.assertIn("zero-ssh", guide)
        self.assertIn("files -> analysis -> files", guide)
        self.assertNotIn("set up or inspect ssh", guide)

    def test_old_expert_receipt_is_not_reused(self):
        guide = (ROOT / "meta/EXPERT_REVIEW_GUIDE.md").read_text(encoding="utf-8").lower()
        self.assertIn("required for the clusterdocs 3 candidate", guide)
        self.assertIn("does not approve", guide)

    def test_capability_page_is_in_mkdocs_navigation(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("concepts/what-rcc-can-do.md", mkdocs)


if __name__ == "__main__":
    unittest.main()
