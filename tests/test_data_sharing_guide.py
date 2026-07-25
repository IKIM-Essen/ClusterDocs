from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/reference/data-sharing.md"


def guide_text():
    return re.sub(r"\s+", " ", GUIDE.read_text().lower())


class DataSharingGuideTests(unittest.TestCase):
    def test_three_sharing_audiences_and_governance_are_explained(self):
        text = guide_text()
        for phrase in (
            "members of the same project",
            "rcc users outside the current group",
            "external collaborators or the public",
            "technical access does not by itself authorize sharing",
            "public sharing is an irreversible disclosure",
        ):
            self.assertIn(phrase, text)

    def test_unix_groups_setgid_and_multiple_memberships_are_explained(self):
        text = guide_text()
        for phrase in (
            "supplementary groups",
            "belonging to multiple groups is normal",
            "one owner and one owning group",
            "chmod 2770",
            "setgid controls **group inheritance**",
            "does not automatically make files group-writable",
        ):
            self.assertIn(phrase, text)

    def test_project_path_is_primary_and_home_handoff_is_bounded(self):
        text = guide_text()
        self.assertIn("/projects/<project>/", text)
        self.assertIn("/homes/<username>/data-for-others/", text)
        self.assertIn("not the authoritative location", text)
        self.assertIn("do not loosen the permissions of the whole home", text)
        self.assertNotIn("chmod 777 /", text)

    def test_navigation_and_transfer_cross_link_the_guide(self):
        custom_nav = (ROOT / "tools/build_site.py").read_text()
        mkdocs_nav = (ROOT / "mkdocs.yml").read_text()
        transfer = (ROOT / "docs/reference/storage-transfer.md").read_text()
        for text in (custom_nav, mkdocs_nav, transfer):
            self.assertIn("data-sharing.md", text)


if __name__ == "__main__":
    unittest.main()
