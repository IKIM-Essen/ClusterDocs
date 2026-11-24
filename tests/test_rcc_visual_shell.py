import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")


class RCCVisualShellTests(unittest.TestCase):
    def test_global_shell_matches_the_rcc_surface_contract(self):
        # Released on the RCC origin at /docs/ (operator decisions 2026-11-02):
        # the shell links the live RCC surfaces and continues the RCC Home look.
        for token in (
            'aria-label="RCC services"',
            '<a href="/">Home</a>',
            '<a href="https://files.ikim.uk-essen.de/">Files</a>',
            '<a href="/analysis/">Analysis</a>',
            'aria-current="page" href="{{ root }}index.html">Documentation',
            '<a href="/account/">My RCC</a>',
            '<a class="topbar-button" href="/account/">My RCC</a>',
        ):
            with self.subTest(token=token):
                self.assertIn(token, BUILDER)
        self.assertNotIn("not yet released</small>", BUILDER)

    def test_dark_scheme_follows_the_rcc_site_switch(self):
        # Operator decision 2026-11-02: one dark scheme, off by default, that
        # follows the browser only in builds made with --color-scheme system.
        self.assertIn("ap.add_argument('--color-scheme',choices=('light','system'),default='light')", BUILDER)
        self.assertIn("{% if color_scheme == 'system' %} data-rcc-color-scheme=\"system\"{% endif %}", BUILDER)
        self.assertIn("content=\"{{ 'light dark' if color_scheme == 'system' else 'light' }}\"", BUILDER)
        quotes = "'" * 3
        start = BUILDER.index("CSS=" + quotes) + len("CSS=" + quotes)
        css = BUILDER[start:BUILDER.index(quotes, start)]
        dark = css[css.index("@media (prefers-color-scheme: dark)"):]
        selectors = [
            selector
            for line in dark.splitlines()[1:]
            if "{" in line
            for selector in line.split("{", 1)[0].split(",")
        ]
        self.assertGreater(len(selectors), 20)
        for selector in selectors:
            with self.subTest(selector=selector.strip()[:60]):
                self.assertIn(':root[data-rcc-color-scheme="system"]', selector)

    def test_shell_serves_its_logo_from_the_rcc_origin(self):
        # The RCC /docs/ content policy only admits same-origin images.
        self.assertIn('src="/assets/Logo_UME_UKE.svg"', BUILDER)
        self.assertNotIn("https://www.uk-essen.de/wp-content/", BUILDER)

    def test_every_page_invites_contributions_on_github(self):
        self.assertIn("https://github.com/IKIM-Essen/ClusterDocs/edit/main/docs/{{ source_path }}", BUILDER)
        self.assertIn("https://github.com/IKIM-Essen/ClusterDocs/issues/new?title=", BUILDER)
        self.assertIn("source_path=str(rel)", BUILDER)

    def test_new_rcc_header_and_service_rail_are_present(self):
        for token in (
            ".topbar { background:var(--paper)",
            ".sidebar-card { background:var(--paper)",
            "--navy:#17477e",
            'class="global-nav"',
            "Ask your RCC approver. Lost your passkey?",
            'src:url("/InterVariable.woff2")',
        ):
            with self.subTest(token=token):
                self.assertIn(token, BUILDER)

    def test_documentation_navigation_survives_desktop_and_mobile(self):
        self.assertIn('class="sidebar-section documentation-tree"', BUILDER)
        self.assertIn('class="mobile-nav"', BUILDER)
        self.assertIn("{% for group,items in nav_groups %}", BUILDER)
        self.assertIn('aria-label="Documentation navigation"', BUILDER)
        self.assertIn('aria-label="Mobile documentation navigation"', BUILDER)

    def test_breadcrumbs_and_heading_scale_follow_the_design_system(self):
        self.assertIn('aria-label="Breadcrumb"', BUILDER)
        self.assertIn(".content-card h1 { margin:.1rem 0 1.2rem; font-size:1.75rem", BUILDER)
        self.assertIn(".home .content-card h1 { font-size:clamp(2.5rem,5.6vw,4.5rem)", BUILDER)


if __name__ == "__main__":
    unittest.main()
