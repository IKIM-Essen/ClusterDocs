import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LoginServiceContinuityTests(unittest.TestCase):
    def setUp(self):
        self.page = (ROOT / "docs/connecting/stable-endpoints.md").read_text(
            encoding="utf-8"
        )
        self.concept = (ROOT / "docs/concepts/jump-shell-compute.md").read_text(
            encoding="utf-8"
        )
        self.transfer = (ROOT / "docs/reference/storage-transfer.md").read_text(
            encoding="utf-8"
        )

    def test_navigation_publishes_the_connection_guidance(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("RCC connection name: connecting/stable-endpoints.md", nav)

    def test_guidance_uses_service_names_not_physical_backends(self):
        self.assertIn("login.ikim.uk-essen.de", self.page)
        self.assertIn("shellhost.ikim.uk-essen.de", self.page)
        self.assertIn("ProxyJump login.ikim.uk-essen.de", self.page)
        self.assertNotIn("HostName login1", self.page)
        self.assertNotIn("HostName login2", self.page)
        self.assertNotIn("HostName is-2", self.page)
        self.assertNotIn("HostName is2-2", self.page)

    def test_gateway_and_destination_are_separate(self):
        self.assertIn("Host login.ikim.uk-essen.de", self.page)
        self.assertIn("Host shellhost", self.page)
        self.assertIn("HostName shellhost.ikim.uk-essen.de", self.page)
        self.assertIn("forwarding-only", self.page)
        self.assertRegex(self.page, r"will not provide an\s+interactive shell")
        self.assertIn("jump service does not contain the RCC research filesystem namespace", self.page)
        for mount in ("/homes", "/groups", "/projects"):
            self.assertIn(mount, self.page)

    def test_transfer_examples_target_shellhost_through_login(self):
        canonical = "scp -J login.ikim.uk-essen.de shellhost:/groups/blubb/demo.test1 ."
        self.assertIn(canonical, self.page)
        self.assertIn(canonical, self.concept)
        self.assertIn(canonical, self.transfer)
        self.assertIn("sftp -J login.ikim.uk-essen.de shellhost", self.page)
        self.assertIn("sftp -J login.ikim.uk-essen.de shellhost", self.transfer)
        self.assertIn("-e 'ssh -J login.ikim.uk-essen.de'", self.transfer)
        self.assertIn("shellhost:/projects/<project>/incoming/dataset/", self.transfer)
        self.assertIn("Do **not** use `login.ikim.uk-essen.de` as the source or destination", self.transfer)
        self.assertNotIn("login.ikim.uk-essen.de:/projects", self.transfer)
        self.assertNotIn("login.ikim.uk-essen.de:/groups", self.transfer)
        self.assertNotIn("login.ikim.uk-essen.de:/homes", self.transfer)

    def test_concept_keeps_compute_and_transfer_roles_distinct(self):
        self.assertIn("Jump host | Guarded doorway", self.concept)
        self.assertIn("Shell host | Your RCC desk and SSH file endpoint", self.concept)
        self.assertIn("jump host is **not** the SFTP, SCP,", self.concept)
        self.assertIn("Slurm workers perform the scientific tasks", self.concept)

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
