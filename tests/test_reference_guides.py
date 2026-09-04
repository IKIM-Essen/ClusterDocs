from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "docs" / "reference"


class ReferenceGuideTests(unittest.TestCase):
    def test_expected_reference_guides_exist(self):
        expected = {
            "index.md",
            "terminology.md",
            "users-groups-projects.md",
            "account-starter-setups.md",
            "access-ssh-vscode.md",
            "storage-transfer.md",
            "data-sharing.md",
            "software-workflows.md",
            "slurm.md",
            "how-shared-compute-works.md",
            "opportunistic-capacity.md",
            "troubleshooting.md",
            "resources.md",
            "ai-data-science.md",
            "authentication-lifecycle.md",
            "publications-and-rcc-credit.md",
            "usage-accounting.md",
        }
        self.assertEqual(expected, {p.name for p in REF.glob("*.md")})

    def test_migrated_guides_keep_safe_boundaries(self):
        text = "\n".join(p.read_text() for p in REF.glob("*.md")).lower()
        self.assertNotIn("nc -vl", text)
        self.assertNotIn("stricthostkeychecking no", text)
        self.assertNotIn("chmod -r a+r", text)
        self.assertIn("forwardagent no", text)
        self.assertIn("cuda_visible_devices", text)

    def test_user_group_and_project_model(self):
        text = (REF / "users-groups-projects.md").read_text().lower()
        self.assertIn("every user has exactly one primary group", text)
        self.assertIn("external user's primary group is `collab`", text)
        self.assertIn("users from different primary groups can exchange data", text)
        self.assertIn("explicit project membership", text)

    def test_courses_link_to_reference_guides(self):
        linked = "\n".join(p.read_text() for p in (ROOT / "docs" / "course").glob("*.md"))
        for name in (
            "access-ssh-vscode.md",
            "storage-transfer.md",
            "software-workflows.md",
            "slurm.md",
            "troubleshooting.md",
        ):
            self.assertIn(name, linked)


if __name__ == "__main__":
    unittest.main()
