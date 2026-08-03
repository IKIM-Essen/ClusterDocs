import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_readiness():
    path = ROOT / "tools/rollout_readiness.py"
    spec = importlib.util.spec_from_file_location("rollout_readiness", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class RolloutReadinessTests(unittest.TestCase):
    def test_current_candidate_fails_closed_with_known_blockers(self):
        blockers, warnings, ready = load_readiness().audit()
        joined = "\n".join(blockers)
        self.assertIn("site_status as staging", joined)
        self.assertNotIn("unresolved production configuration", joined)
        self.assertIn("videos lack recorded human approval", joined)
        self.assertIn("administrator publication checklist", joined)
        self.assertIn("no reviewed production deployment workflow", joined)
        self.assertTrue(warnings)
        self.assertIn("all 15 course pages declare in-player English captions", ready)

    def test_candidate_is_ready_to_start_manual_review(self):
        blockers, ready = load_readiness().manual_review_audit()
        self.assertEqual([], blockers)
        self.assertIn("expert, novice, and video review guides are present", ready)

    def test_caption_normalizer_uses_readable_technical_terms(self):
        path = ROOT / "tools/build_site.py"
        spec = importlib.util.spec_from_file_location("build_site", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(module)
        source = "S S H, S I F, N V, slash data, and input-output"
        self.assertEqual("SSH, SIF, --nv, /data, and I/O", module.normalize_caption_text(source))

    def test_production_builder_also_requires_production_status(self):
        text = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("cfg.get('site_status') != 'production'", text)


if __name__ == "__main__":
    unittest.main()
