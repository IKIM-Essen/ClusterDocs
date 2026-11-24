"""A deployment overlay adds pages to tools/build_site.py output and never replaces one."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_site.py"


def _overlay(root: Path, nav: str, pages: dict[str, str]) -> Path:
    overlay = root / "overlay"
    for rel, text in pages.items():
        path = overlay / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    overlay.mkdir(exist_ok=True)
    (overlay / "nav.yml").write_text(nav, encoding="utf-8")
    return overlay


def _build(overlay: Path, out: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BUILDER), "--output", str(out), "--overlay", str(overlay)],
        cwd=ROOT, capture_output=True, text=True,
    )


NAV_OK = """pages:
  - group: Reference
    label: Machines in this installation
    path: reference/site-machines.md
    after: reference/resources.md
"""


class SiteOverlayTests(unittest.TestCase):
    def test_overlay_page_is_built_and_listed_after_its_anchor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            overlay = _overlay(root, NAV_OK, {"reference/site-machines.md": "# Machines\n\nFixture page.\n"})
            result = _build(overlay, root / "site")
            self.assertEqual(result.returncode, 0, result.stderr)
            page = root / "site" / "reference" / "site-machines" / "index.html"
            self.assertTrue(page.is_file())
            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            resources = home.index("Resources and discovery")
            machines = home.index("Machines in this installation")
            self.assertLess(resources, machines)
            self.assertNotIn("Machines in this installation", home[:resources])

    def test_overlay_cannot_replace_a_clusterdocs_page(self):
        nav = NAV_OK.replace("reference/site-machines.md", "reference/resources.md")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            overlay = _overlay(root, nav, {"reference/resources.md": "# Replaced\n"})
            result = _build(overlay, root / "site")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not replace", result.stderr)

    def test_overlay_pages_and_nav_must_match(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            overlay = _overlay(root, NAV_OK, {
                "reference/site-machines.md": "# Machines\n",
                "reference/unlisted.md": "# Unlisted\n",
            })
            result = _build(overlay, root / "site")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must match exactly", result.stderr)

    def test_overlay_entry_must_follow_a_page_of_its_group(self):
        nav = NAV_OK.replace("group: Reference", "group: Start here")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            overlay = _overlay(root, nav, {"reference/site-machines.md": "# Machines\n"})
            result = _build(overlay, root / "site")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must follow one existing page", result.stderr)


if __name__ == "__main__":
    unittest.main()
