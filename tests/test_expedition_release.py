import subprocess
import sys
from pathlib import Path
import unittest
import zipfile


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
            "[RCC Expedition](rcc-expedition.md)",
            (ROOT / "docs/index.md").read_text(),
        )
        self.assertIn(
            "assets/downloads/RCC-Expedition-USB-v1.0.1.zip",
            (ROOT / "docs/rcc-expedition.md").read_text(),
        )

    def test_overview_promotes_both_supported_starting_paths(self):
        overview = (ROOT / "docs/index.md").read_text(encoding="utf-8")[:1_200]
        self.assertIn("browser-first research", overview)
        self.assertIn("advanced command-line/developer access", overview)
        self.assertIn("[RCC Expedition Light](getting-started/index.md)", overview)
        self.assertIn("[RCC Expedition](rcc-expedition.md)", overview)

        start = (ROOT / "docs/getting-started/index.md").read_text(encoding="utf-8")
        self.assertIn("Windows 11", start)
        self.assertIn("Current macOS", start)

    def test_expedition_can_start_without_installing(self):
        archive = ROOT / "docs/assets/downloads/RCC-Expedition-USB-v1.0.1.zip"
        with zipfile.ZipFile(archive) as release:
            start = release.read("START HERE.html").decode("utf-8")
            readme = release.read("READ ME FIRST.txt").decode("utf-8")

        self.assertIn('href="payload/course/index.html"', start)
        self.assertIn("Start now — no installation", start)
        self.assertIn("FASTEST START — NO INSTALLATION", readme)
        self.assertIn("Optional: add a Desktop shortcut", start)


if __name__ == "__main__":
    unittest.main()
