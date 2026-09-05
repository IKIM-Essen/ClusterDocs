import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_gate():
    path = ROOT / "tools/release_bundle_gate.py"
    spec = importlib.util.spec_from_file_location("release_bundle_gate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class ReleaseBundleGateTests(unittest.TestCase):
    def test_current_candidate_is_blocked_specifically_by_analysis(self):
        blockers, ready = load_gate().audit()
        self.assertEqual([], ready)
        joined = "\n".join(blockers)
        self.assertIn("rcc_analysis=not_yet_released", joined)
        self.assertNotIn("rcc_home=", joined)
        self.assertNotIn("files=", joined)
        self.assertNotIn("rcc_admin=", joined)
        self.assertNotIn("my_rcc=", joined)

    def test_production_workflow_executes_release_bundle_gate(self):
        workflow = (ROOT / ".gitea/workflows/deploy-production.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("tools/release_bundle_gate.py", workflow)
        self.assertIn('test "$GITHUB_REF" = "refs/heads/main"', workflow)


if __name__ == "__main__":
    unittest.main()
