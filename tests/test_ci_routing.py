import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CIRoutingTests(unittest.TestCase):
    def test_gitea_is_the_automatic_validation_authority(self):
        workflow = (ROOT / ".gitea/workflows/validate.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("runs-on: rcc-ci", workflow)
        self.assertIn("/opt/rcc-ci/bin/gitea-ci-checkout", workflow)
        self.assertIn("tools/check_ci_environment.py", workflow)
        self.assertNotIn("pip install", workflow)
        self.assertNotIn("apt-get", workflow)
        self.assertNotIn("actions/checkout", workflow)

    def test_github_validation_is_manual_fallback_only(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("pull_request:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertNotIn("upload-artifact", workflow)

    def test_generated_video_handoff_is_not_versioned(self):
        ignore = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/new-videos/", ignore)


if __name__ == "__main__":
    unittest.main()
