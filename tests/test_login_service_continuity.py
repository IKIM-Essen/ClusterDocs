import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LoginServiceContinuityTests(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / "docs/connecting/stable-endpoints.md").read_text(
            encoding="utf-8"
        )

    def test_navigation_publishes_the_connection_guidance(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("RCC connection name: connecting/stable-endpoints.md", nav)

    def test_guidance_uses_approved_aliases_not_backend_names(self):
        self.assertIn("{{ ssh_alias }}", self.page)
        self.assertIn("same approved alias", self.page)
        self.assertIn("do not create separate workstation targets", self.page)
        self.assertNotIn("HostName login1", self.page)
        self.assertNotIn("HostName login2", self.page)

    def test_timeout_and_host_key_warning_are_distinct(self):
        for token in (
            "For a timeout",
            "changed-host-key warning",
            "infrastructure or security incident",
            "delete the complete `~/.ssh/known_hosts`",
            "`ssh-keygen -R`",
            "`StrictHostKeyChecking no`",
            "`accept-new`",
        ):
            self.assertIn(token, self.page)


if __name__ == "__main__":
    unittest.main()
