from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "resources" / "how-it-all-works.md"
FIGURE = ROOT / "docs" / "assets" / "lab-network-flow.svg"


class LabNetworkGuideTests(unittest.TestCase):
    def test_user_facing_services_are_explained(self):
        text = GUIDE.read_text().lower()
        for phrase in (
            "lab network",
            "unrouted layer 2 enclave",
            "dhcp",
            "http proxy",
            "samba",
            "adria",
            "research compute cluster",
            "slurm",
        ):
            self.assertIn(phrase, text)

    def test_figure_is_present_and_linked(self):
        self.assertTrue(FIGURE.is_file())
        self.assertIn("lab-network-flow.svg", GUIDE.read_text())

    def test_public_guide_avoids_internal_topology(self):
        text = GUIDE.read_text()
        self.assertNotRegex(text, r"\b10\.\d+\.\d+\.\d+\b")
        self.assertNotIn("samba_project_gateway", text)
        self.assertNotIn("rcc:samba=enabled", text)


if __name__ == "__main__":
    unittest.main()
