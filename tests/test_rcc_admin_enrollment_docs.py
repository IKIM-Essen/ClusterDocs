import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(path):
    text = " ".join(path.read_text(encoding="utf-8").lower().split())
    return text.replace("> ", "").replace("**", "")


class RccAdminEnrollmentDocsTests(unittest.TestCase):
    def test_enrollment_contract_is_explicit(self):
        page = normalized(DOCS / "getting-started/account-enrollment.md")
        for statement in (
            "service status — not yet released",
            "withdrawn on 3 october 2026",
            "signed link is valid for seven days",
            "do not choose an rcc username, upload an ssh key, or request a project",
            "does not email activation secrets",
            "project membership is requested separately after activation",
        ):
            self.assertIn(statement, page)
        self.assertNotIn("invite-only pilot", page)
        self.assertNotIn("github.com/ikim-essen/rcc/pull/", page)

    def test_enrollment_is_in_both_navigation_systems(self):
        mkdocs = normalized(ROOT / "mkdocs.yml")
        custom_site = normalized(ROOT / "tools/build_site.py")
        path = "getting-started/account-enrollment.md"
        self.assertIn(path, mkdocs)
        self.assertIn(path, custom_site)

    def test_rcc_admin_ready_claims_are_marked_unreleased(self):
        for page in DOCS.rglob("*.md"):
            paragraphs = page.read_text(encoding="utf-8").lower().split("\n\n")
            for paragraph in paragraphs:
                if "rcc admin" in paragraph and "ready now" in paragraph:
                    paragraph = " ".join(paragraph.split()).replace("> ", "")
                    paragraph = paragraph.replace("**", "")
                    self.assertIn(
                        "not yet released",
                        paragraph,
                        f"{page.relative_to(ROOT)} mixes RCC Admin with a ready-now claim without marking it unreleased",
                    )

    def test_access_page_routes_current_requests_to_support(self):
        page = normalized(DOCS / "reference/access-ssh-vscode.md")
        self.assertIn("the rcc admin self-service portal is not yet released", page)
        self.assertIn("ikim cluster channel on mattermost", page)
        self.assertIn("getting-started/account-enrollment.md", page)
        self.assertNotIn("invite-only pilot", page)


if __name__ == "__main__":
    unittest.main()
