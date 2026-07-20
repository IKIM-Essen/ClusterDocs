from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "docs" / "reference"


class ReferenceGuideTests(unittest.TestCase):
    def test_expected_reference_guides_exist(self):
        expected = {
            "index.md",
            "account-starter-setups.md",
            "access-ssh-vscode.md",
            "storage-transfer.md",
            "software-workflows.md",
            "slurm.md",
            "troubleshooting.md",
            "resources.md",
            "ai-data-science.md",
        }
        self.assertEqual(expected, {p.name for p in REF.glob("*.md")})

    def test_migrated_guides_keep_safe_boundaries(self):
        text = "\n".join(p.read_text() for p in REF.glob("*.md")).lower()
        self.assertNotIn("nc -vl", text)
        self.assertNotIn("stricthostkeychecking no", text)
        self.assertNotIn("chmod -r a+r", text)
        self.assertIn("forwardagent no", text)
        self.assertIn("cuda_visible_devices", text)

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
