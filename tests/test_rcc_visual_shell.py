import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
CONFIG = (ROOT / "config/public.yml").read_text(encoding="utf-8")


class RCCVisualShellTests(unittest.TestCase):
    def test_global_shell_matches_the_rcc_surface_contract(self):
        for token in (
            'aria-label="RCC services"',
            '>Home',
            '>Files',
            'aria-current="page" href="{{ root }}index.html">Documentation',
            'Account & projects',
            'target="_blank" rel="noopener"',
        ):
            with self.subTest(token=token):
                self.assertIn(token, BUILDER)

    def test_service_endpoints_are_configured_not_scattered(self):
        for key in ("rcc_home_url", "files_service_url", "account_service_url"):
            self.assertIn(f"{key}:", CONFIG)
            self.assertIn("{{ " + key + " }}", BUILDER)
        self.assertNotIn("Logo_UME_UKE.svg", BUILDER)
        self.assertNotIn("Documentation online", BUILDER)
        self.assertIn("Documentation · {{ status }}", BUILDER)

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

    def test_rcc_analysis_and_v3_capabilities_are_in_canonical_navigation(self):
        self.assertEqual(BUILDER.count('{{ root }}analysis/rcc-analysis/index.html'), 2)
        self.assertIn(
            "('RCC services','RCC Analysis · Notebook and Workflow · planned','analysis/rcc-analysis.md')",
            BUILDER,
        )
        self.assertIn(
            "('RCC services','What RCC can do','concepts/what-rcc-can-do.md')",
            BUILDER,
        )
        self.assertIn(
            "('RCC services','AI and coding agents · data-blind by default','concepts/agents-and-mcp.md')",
            BUILDER,
        )
        self.assertIn(
            "('Reference','Workbench execution layer · advanced · planned','concepts/workbench-interfaces.md')",
            BUILDER,
        )

    def test_desktop_shell_is_viewport_aligned_not_centered(self):
        self.assertIn(".topbar-inner { width:100%; margin:0;", BUILDER)
        self.assertIn(".shell { width:100%; margin:0;", BUILDER)
        self.assertIn("grid-template-columns:minmax(230px,270px) minmax(0,1fr);", BUILDER)
        self.assertIn("grid-template-columns:minmax(230px,270px) minmax(0,1fr) minmax(280px,340px);", BUILDER)
        self.assertIn("footer { width:100%; margin:0;", BUILDER)
        self.assertNotIn(".shell { max-width:1760px; margin:0 auto;", BUILDER)
        self.assertNotIn("align-items:start; justify-content:center;", BUILDER)
        self.assertNotIn("minmax(0,1000px)", BUILDER)
        self.assertNotIn("minmax(0,780px)", BUILDER)

    def test_breadcrumbs_and_heading_scale_follow_the_design_system(self):
        self.assertIn('aria-label="Breadcrumb"', BUILDER)
        self.assertIn(".content-card h1 { margin:.1rem 0 1.2rem; font-size:1.75rem", BUILDER)
        self.assertIn(".home .content-card h1 { font-size:clamp(2.5rem,5.6vw,4.5rem)", BUILDER)


if __name__ == "__main__":
    unittest.main()
