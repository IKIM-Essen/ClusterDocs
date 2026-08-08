from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GUIDE = DOCS / "connecting" / "pikvm-headscale.md"


class HeadscalePiKVMDocsTests(unittest.TestCase):
    def test_replacement_boundary_and_release_status_are_explicit(self):
        text = re.sub(r"\s+", " ", GUIDE.read_text(encoding="utf-8").lower())
        for phrase in (
            "service status: not yet released",
            "headscale replaces the hosted tailscale control plane",
            "tailscale-compatible client",
            "no personal tailscale saas account",
            "already encrypted traffic",
        ):
            self.assertIn(phrase, text)

    def test_public_page_excludes_enrollment_secrets_and_commands(self):
        text = GUIDE.read_text(encoding="utf-8").lower()
        for forbidden in ("--authkey", "hskey-auth-", "preauthkeys create"):
            self.assertNotIn(forbidden, text)

    def test_obsolete_hosted_service_license_warnings_are_absent(self):
        corpus = "\n".join(
            page.read_text(encoding="utf-8", errors="replace")
            for page in DOCS.rglob("*.md")
        )
        for pattern in (
            r"free\s*\(for private use\)",
            r"tailscale (?:paid )?(?:license|plan) (?:is )?required",
            r"tailscale (?:saas )?subscription (?:is )?required",
            r"tailscale account (?:is )?required",
        ):
            self.assertIsNone(re.search(pattern, corpus, flags=re.IGNORECASE), pattern)

    def test_navigation_builder_and_public_status_include_the_guide(self):
        self.assertIn("connecting/pikvm-headscale.md", (ROOT / "mkdocs.yml").read_text())
        self.assertIn(
            "connecting/pikvm-headscale.md",
            (ROOT / "tools/build_site.py").read_text(),
        )
        config = (ROOT / "config/public.yml").read_text()
        self.assertIn("lab_remote_access_name: RCC Headscale", config)
        self.assertIn("headscale_pikvm_access: not_yet_released", config)

    def test_publication_lint_limits_pikvm_to_reviewed_guides(self):
        lint = (ROOT / "tools/publication_lint.py").read_text()
        self.assertIn("obsolete Tailscale licensing warning", lint)
        self.assertIn("docs/connecting/pikvm-headscale.md", lint)


if __name__ == "__main__":
    unittest.main()
