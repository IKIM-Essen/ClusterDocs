import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VSCodeGuidanceTests(unittest.TestCase):
    def test_vscode_is_the_recommended_route_for_most_users(self):
        pages = [
            ROOT / "docs/tldr.md",
            ROOT / "docs/course/class-01-safe-access.md",
            ROOT / "docs/course/class-02-workflows.md",
            ROOT / "docs/course/class-09-python-notebooks.md",
            ROOT / "docs/course/class-10-r-analysis.md",
            ROOT / "docs/paths/software-development.md",
        ]
        text = "\n".join(path.read_text().lower() for path in pages)
        self.assertGreaterEqual(text.count("vs code with remote - ssh"), 5)
        for phrase in ["most users", "slurm", "search", "file watching"]:
            self.assertIn(phrase, text)

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
