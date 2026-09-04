import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").lower().split())


class RccAdminEnrollmentDocsTests(unittest.TestCase):
    def test_enrollment_contract_is_explicit(self):
        page = normalized(DOCS / "getting-started/account-enrollment.md")
        for statement in (
            "invite-only pilot",
            "signed link is valid for seven days",
            "do **not** choose an rcc username, upload an ssh key, or request a project",
            "does not email activation secrets",
            "project membership is requested separately after activation",
            "stacked directly on #1672",
            "https://github.com/ikim-essen/rcc/pull/1672",
            "https://github.com/ikim-essen/rcc/pull/1674",
        ):
            self.assertIn(statement, page)

    def test_enrollment_is_in_both_navigation_systems(self):
        mkdocs = normalized(ROOT / "mkdocs.yml")
        custom_site = normalized(ROOT / "tools/build_site.py")
        path = "getting-started/account-enrollment.md"
        self.assertIn(path, mkdocs)
        self.assertIn(path, custom_site)

    def test_rcc_admin_ready_claims_are_pilot_scoped(self):
        for page in DOCS.rglob("*.md"):
            paragraphs = page.read_text(encoding="utf-8").lower().split("\n\n")
            for paragraph in paragraphs:
                if "rcc admin" in paragraph and "ready now" in paragraph:
                    self.assertIn(
                        "invite-only pilot",
                        " ".join(paragraph.split()),
                        f"{page.relative_to(ROOT)} mixes RCC Admin with a ready-now claim without marking the pilot",
                    )

    def test_access_page_does_not_front_load_ssh_or_project_setup(self):
        page = normalized(DOCS / "reference/access-ssh-vscode.md")
        self.assertIn("invite-only pilot", page)
        self.assertIn("does not ask you to choose a project or upload an ssh key", page)
        self.assertIn("after approval and activation", page)


if __name__ == "__main__":
    unittest.main()
