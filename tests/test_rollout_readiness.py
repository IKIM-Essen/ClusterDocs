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
    def test_current_v3_candidate_fails_closed_with_known_stage1_blockers(self):
        blockers, warnings, ready = load_readiness().audit()
        joined = "\n".join(blockers)
        self.assertIn("site_status as staging", joined)
        self.assertNotIn("unresolved production configuration", joined)
        self.assertNotIn("videos lack recorded human approval", joined)
        self.assertIn("administrator publication checklist", joined)
        self.assertNotIn("no reviewed main-only ClusterDocs production deployment workflow", joined)
        self.assertIn("ClusterDocs 3 expert content review", joined)
        self.assertIn("zero-SSH novice browser acceptance", joined)
        self.assertIn("advanced-user acceptance", joined)
        self.assertNotIn("canonical Part 1 source still carries the retired", joined)

        warning_text = "\n".join(warnings)
        self.assertIn("production publication is main-only", warning_text)
        self.assertIn("video human approval is deferred to Stage 2", warning_text)
        self.assertIn("Stage 2 video regeneration", warning_text)
        self.assertNotIn("novice acceptance is scheduled after initial rollout", warning_text)

        ready_text = "\n".join(ready)
        self.assertIn("Stage 1 written-site rollout keeps all video player URLs fail-closed", ready_text)
        self.assertIn("all existing video-backed course pages declare in-player English captions", ready_text)
        self.assertIn("Gitea-only main production deployment workflow is present", ready_text)
        self.assertIn("canonical Part 1 source matches the current RCC SSH-key policy", ready_text)

    def test_candidate_is_ready_to_start_fresh_v3_manual_review(self):
        blockers, ready = load_readiness().manual_review_audit()
        self.assertEqual([], blockers)
        joined = "\n".join(ready)
        self.assertIn("expert, novice-browser, and video review guides are present", joined)
        self.assertIn("task-first", joined)
        self.assertIn("data-blind default", joined)
        self.assertIn("no-passphrase RCC SSH-key policy", joined)
        self.assertIn("I/O constraint", joined)
        self.assertIn("VS Code low-I/O defaults", joined)
        self.assertIn("review receipts are reset", joined)

    def test_media_stage_is_inferred_from_fail_closed_link_switch(self):
        readiness = load_readiness()
        manifest = {"publication": {"preview_links": "disabled_until_verified_live"}}
        self.assertEqual("stage1_text_only", readiness.media_release_stage(manifest))
        manifest["publication"]["preview_links"] = "enabled"
        self.assertEqual("stage2_media", readiness.media_release_stage(manifest))

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
