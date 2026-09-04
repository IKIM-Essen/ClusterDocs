import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")


class RCCVisualShellTests(unittest.TestCase):
    def test_global_shell_matches_the_rcc_surface_contract(self):
        for token in (
            'aria-label="RCC services"',
            '>Home',
            '>Files',
            'aria-current="page" href="{{ root }}index.html">Documentation',
            '>RCC Admin',
            '>My RCC',
            'target="_blank" rel="noopener"',
        ):
            with self.subTest(token=token):
                self.assertIn(token, BUILDER)

    def test_new_rcc_header_and_service_rail_are_present(self):
        for token in (
            ".topbar { background:var(--navy)",
            ".sidebar-card { min-height:100%;",
            "background:linear-gradient(180deg,var(--navy)",
            'class="global-nav"',
            "#1262b0",
            "#3ab0ff",
            "Compute · Data · Projects",
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
