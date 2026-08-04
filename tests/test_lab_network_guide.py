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
            "ardia",
            "research compute cluster",
            "slurm",
        ):
            self.assertIn(phrase, text)

    def test_figure_is_present_and_linked(self):
        self.assertTrue(FIGURE.is_file())
        self.assertIn("lab-network-flow.svg", GUIDE.read_text())

    def test_security_model_explains_direct_and_proxy_access(self):
        text = GUIDE.read_text().lower()
        for phrase in (
            "removing general direct internet",
            "direct access to explicit server endpoints",
            "limited outbound web access",
            "no unsolicited inbound internet access",
            "exposure reduction, not automatic trust",
        ):
            self.assertIn(phrase, text)

    def test_public_guide_avoids_internal_topology(self):
        text = GUIDE.read_text()
        self.assertNotRegex(text, r"\b10\.\d+\.\d+\.\d+\b")
        self.assertNotIn("samba_project_gateway", text)
        self.assertNotIn("rcc:samba=enabled", text)

    def test_configuration_comes_from_the_live_information_page(self):
        text = GUIDE.read_text().lower()
        for phrase in (
            "lab-network information page",
            "set to dhcp",
            "current http proxy address and port",
            "do not copy a proxy address",
            "does not reproduce internal proxy",
        ):
            self.assertIn(phrase, text)

    def test_remote_console_is_private_and_governed(self):
        text = GUIDE.read_text().lower()
        for phrase in (
            "raspberry pi and pikvm",
            "no public port forwarding",
            "tailscale",
            "institution-owned tailnet",
            "do not use tailscale funnel",
            "personal/non-commercial use",
            "no direct incoming",
        ):
            self.assertIn(phrase, text)

    def test_publication_lint_allows_pikvm_only_in_this_guide(self):
        lint = (ROOT / "tools" / "publication_lint.py").read_text()
        self.assertIn("PUBLIC_HARDWARE_GUIDES={'docs/resources/how-it-all-works.md'}", lint)
        self.assertIn("hardware control-plane detail", lint)


if __name__ == "__main__":
    unittest.main()
