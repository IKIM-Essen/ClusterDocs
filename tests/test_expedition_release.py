import subprocess
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ExpeditionReleaseTests(unittest.TestCase):
    def test_release_archive_passes_the_dedicated_validator(self):
        subprocess.run(
            [sys.executable, str(ROOT / "tools/validate_expedition_release.py")],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )

    def test_public_site_uses_the_current_production_origin(self):
        self.assertIn(
            "site_url: https://ikim-essen.github.io/ClusterDocs/",
            (ROOT / "mkdocs.yml").read_text(),
        )
        self.assertIn(
            "site_url: https://ikim-essen.github.io/ClusterDocs/",
            (ROOT / "config/public.yml").read_text(),
        )
        self.assertIn(
            "assets/downloads/RCC-Expedition-USB-v1.0.0.zip",
            (ROOT / "docs/index.md").read_text(),
        )

    def test_overview_pages_promote_expedition_near_the_top(self):
        for relative in ("docs/index.md", "docs/tldr.md"):
            page = (ROOT / relative).read_text(encoding="utf-8")
            opening = page[:1_200]
            self.assertIn("[RCC Expedition](rcc-expedition.md)", opening, relative)
            self.assertIn("Windows 11", opening, relative)
            self.assertIn("macOS", opening, relative)


if __name__ == "__main__":
    unittest.main()
