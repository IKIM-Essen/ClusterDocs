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
        self.assertNotIn("rsync ", workflow)
        self.assertNotIn("CLUSTERDOCS_DEPLOY_", workflow)

    def test_production_deployment_is_manual_and_gitea_only(self):
        workflow = (ROOT / ".gitea/workflows/deploy-production.yml").read_text()
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("runs-on: rcc-ci", workflow)
        self.assertIn("/opt/rcc-ci/bin/gitea-ci-checkout", workflow)
        self.assertIn('test "$GITHUB_REF" = "refs/heads/clusterdocs-ng"', workflow)
        self.assertIn('test "$(git rev-parse HEAD)" = "$GITHUB_SHA"', workflow)
        self.assertIn("tools/rollout_readiness.py", workflow)
        self.assertIn("tools/build_site.py --production", workflow)
        self.assertIn("git@github.com:IKIM-Essen/ClusterDocs.git", workflow)
        self.assertIn("--branch gh-pages", workflow)
        self.assertIn("push origin HEAD:gh-pages", workflow)
        self.assertIn("touch site-production/.nojekyll", workflow)
        self.assertIn("test ! -e site-production/CNAME", workflow)
        self.assertIn("StrictHostKeyChecking=yes", workflow)
        self.assertNotIn("push --force", workflow)
        self.assertNotIn("uses:", workflow)
        self.assertNotIn("pull_request:", workflow)
        self.assertNotIn("\n  push:", workflow)

    def test_generated_video_handoff_is_not_versioned(self):
        ignore = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/new-videos/", ignore)


if __name__ == "__main__":
    unittest.main()
