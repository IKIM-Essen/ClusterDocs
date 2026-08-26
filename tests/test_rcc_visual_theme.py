from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "apply_rcc_visual_theme.py"
SPEC = importlib.util.spec_from_file_location("apply_rcc_visual_theme", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
THEME = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(THEME)


VALID_HTML = """<!doctype html>
<html><body>
<header class="topbar"><img alt="Universitätsklinikum Essen"></header>
<nav aria-label="RCC services"></nav>
<aside class="sidebar"></aside>
<main class="content-card"></main>
</body></html>
"""


class RCCVisualThemeTests(unittest.TestCase):
    def make_site(self, html: str = VALID_HTML, css: str = "body { margin: 0; }\n") -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "assets").mkdir()
        (root / "index.html").write_text(html, encoding="utf-8")
        (root / "assets" / "site.css").write_text(css, encoding="utf-8")
        return root

    def test_theme_is_idempotent(self) -> None:
        root = self.make_site()
        THEME.apply(root)
        first = (root / "assets" / "site.css").read_text(encoding="utf-8")
        THEME.apply(root)
        second = (root / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertEqual(second.count(THEME.MARKER), 1)

    def test_theme_fails_closed_on_renderer_drift(self) -> None:
        root = self.make_site(html=VALID_HTML.replace('class="sidebar"', 'class="navigation"'))
        with self.assertRaises(SystemExit):
            THEME.apply(root)

    def test_theme_rejects_duplicate_marker(self) -> None:
        root = self.make_site(css=f"{THEME.MARKER}\n{THEME.MARKER}\n")
        with self.assertRaises(SystemExit):
            THEME.apply(root)


if __name__ == "__main__":
    unittest.main()
