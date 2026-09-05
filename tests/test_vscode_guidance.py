import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VSCodeGuidanceTests(unittest.TestCase):
    def test_vscode_is_the_advanced_developer_route(self):
        overview = (ROOT / "docs/index.md").read_text().lower()
        start = (ROOT / "docs/getting-started/index.md").read_text().lower()
        development = (ROOT / "docs/paths/software-development.md").read_text().lower()

        self.assertIn("browser-first research", overview)
        self.assertIn("advanced command-line/developer access", overview)
        self.assertIn("ssh is optional", start)
        self.assertIn("vs code with remote - ssh", development)
        for phrase in ["slurm", "search", "file watching"]:
            self.assertIn(phrase, development)

    def test_reference_keeps_performance_and_security_boundaries(self):
        page = (ROOT / "docs/reference/access-ssh-vscode.md").read_text().lower()
        for phrase in [
            '"search.followsymlinks": false',
            '"search.useignorefiles": true',
            '"search.exclude"',
            '"files.watcherexclude"',
            "smallest useful folder",
            "workspace trust",
            "remote extension can execute code",
            "does not create a compute allocation",
            "rcc transfer service",
            "host-identity warning",
        ]:
            self.assertIn(phrase, page)


if __name__ == "__main__":
    unittest.main()
