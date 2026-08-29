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


# Deliberately model the legacy custom-builder service labels. The theme layer is
# the convergence boundary and must normalize these while relocating the rail.
VALID_HTML = """<!doctype html>
<html><body>
<header class="topbar">
  <img alt="Universitätsklinikum Essen">
  <nav class="service-nav" aria-label="RCC services">
    <a href="https://rcc.ikim.uk-essen.de/">About RCC</a>
    <a class="active" href="index.html" aria-current="page">Documentation</a>
    <a href="https://files.ikim.uk-essen.de/">File transfer</a>
    <a class="admin-link" href="https://rcc-admin.ikim.uk-essen.de/">RCC Admin</a>
  </nav>
</header>
<div class="docs-layout">
  <aside class="sidebar"><div class="sidebar-card"><div class="sidebar-heading"></div></div></aside>
  <main class="content-card"></main>
</div>
</body></html>
"""


class RCCVisualThemeTests(unittest.TestCase):
    def make_site(self, html: str = VALID_HTML, css: str = "body { margin: 0; }\n") -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "assets").mkdir()
        (root / "nested").mkdir()
        (root / "index.html").write_text(html, encoding="utf-8")
        nested_html = html.replace('href="index.html"', 'href="../index.html"')
        (root / "nested" / "page.html").write_text(nested_html, encoding="utf-8")
        (root / "assets" / "site.css").write_text(css, encoding="utf-8")
        return root

    def test_theme_is_idempotent_and_moves_canonical_services_into_rail(self) -> None:
        root = self.make_site()
        THEME.apply(root)
        first_css = (root / "assets" / "site.css").read_text(encoding="utf-8")
        first_html = (root / "index.html").read_text(encoding="utf-8")
        THEME.apply(root)
        second_css = (root / "assets" / "site.css").read_text(encoding="utf-8")
        second_html = (root / "index.html").read_text(encoding="utf-8")
        self.assertEqual(first_css, second_css)
        self.assertEqual(first_html, second_html)
        self.assertEqual(second_css.count(THEME.MARKER), 1)
        self.assertEqual(second_html.count(THEME.HTML_MARKER), 1)
        self.assertEqual(second_html.count('aria-label="RCC services"'), 1)
        self.assertIn('class="rcc-service-rail"', second_html)
        self.assertNotIn('aria-label="RCC services"', second_html.split("</header>", 1)[0])
        for label, href in (
            ("Home", "https://rcc.ikim.uk-essen.de/"),
            ("Documentation", "index.html"),
            ("Files", "https://files.ikim.uk-essen.de/web/client"),
            ("My RCC", "https://rcc-admin.ikim.uk-essen.de/myrcc"),
            ("AI assistant", "https://assistant.ikim.uk-essen.de/"),
        ):
            self.assertIn(f'href="{href}"', second_html)
            self.assertIn(f">{label}<", second_html)
        self.assertIn('class="portal-link"', second_html)
        for obsolete in (">About RCC<", ">File transfer<", ">RCC Admin<"):
            self.assertNotIn(obsolete, second_html)

        nested = (root / "nested" / "page.html").read_text(encoding="utf-8")
        self.assertIn('class="rcc-service-rail"', nested)
        self.assertIn('href="../index.html"', nested)
        self.assertIn(">AI assistant<", nested)

    def test_canonicalization_fails_without_one_documentation_link(self) -> None:
        root = self.make_site(html=VALID_HTML.replace(">Documentation<", ">Docs<"))
        with self.assertRaises(SystemExit):
            THEME.apply(root)

    def test_theme_fails_closed_on_renderer_drift(self) -> None:
        root = self.make_site(html=VALID_HTML.replace('class="sidebar-card"', 'class="navigation-card"'))
        with self.assertRaises(SystemExit):
            THEME.apply(root)

    def test_theme_rejects_duplicate_css_marker(self) -> None:
        root = self.make_site(css=f"{THEME.MARKER}\n{THEME.MARKER}\n")
        with self.assertRaises(SystemExit):
            THEME.apply(root)

    def test_theme_rejects_duplicate_html_marker(self) -> None:
        html = VALID_HTML.replace(
            '<div class="sidebar-card">',
            f'<div class="sidebar-card">{THEME.HTML_MARKER}{THEME.HTML_MARKER}',
        )
        root = self.make_site(html=html)
        with self.assertRaises(SystemExit):
            THEME.apply(root)


if __name__ == "__main__":
    unittest.main()
