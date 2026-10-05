import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_video_builder():
    path = ROOT / "build/build_videos.py"
    spec = importlib.util.spec_from_file_location("build_videos", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def load_site_builder():
    path = ROOT / "tools/build_site.py"
    spec = importlib.util.spec_from_file_location("build_site", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class TrainingMediaTests(unittest.TestCase):
    CLASS_SLUGS = {
        1: "class-01-safe-access.md", 2: "class-02-workflows.md",
        3: "class-03-performance.md", 4: "class-04-containers.md",
        5: "class-05-slurm.md", 6: "class-06-snakemake.md",
        7: "class-07-nextflow.md", 8: "class-08-vhosts.md",
        9: "class-09-python-notebooks.md", 10: "class-10-r-analysis.md",
        11: "class-11-shiny.md", 12: "class-12-notebook-to-service.md",
        13: "class-13-biomedical-data-privacy.md", 14: "class-14-efficient-io.md",
        15: "class-15-storage-architecture.md", 16: "class-16-wet-lab-data-workflows.md",
        17: "class-17-data-lifecycle.md",
    }

    def test_narration_and_reviewed_frames_match(self):
        builder = load_video_builder()
        expected_counts = {1: 12, 2: 12, 3: 14, 4: 13}
        for part, expected in expected_counts.items():
            narration = builder.parse_narration(
                ROOT / f"narration/RCC_Onboarding_Part_{part}_Narration.md"
            )
            frames = sorted((ROOT / f"slides/frames/part{part}").glob("slide-*.png"))
            self.assertEqual(expected, len(narration))
            self.assertEqual(expected, len(frames))
            self.assertEqual(
                list(range(1, expected + 1)),
                [int(item["slide"]) for item in narration],
            )

    def test_numbered_classes_embed_vhost_video_and_player_captions(self):
        manifest = yaml.safe_load((ROOT / "config/media-manifest.yml").read_text())
        expected_cache_keys = {
            item["video"]: item["sha256"][:8] for item in manifest["assets"]
        }
        embedded = {}
        for part, slug in self.CLASS_SLUGS.items():
            text = (ROOT / "docs/course" / slug).read_text()
            prefix = "Part" if part <= 4 else "Class"
            filename = f"RCC_Onboarding_{prefix}_{part}_Video_Enhanced.mp4"
            match = re.search(
                rf'\{{\{{ media_base_url \}}\}}/({re.escape(filename)})\?v=([0-9a-f]+)',
                text,
            )
            self.assertIsNotNone(match, slug)
            embedded[match.group(1)] = match.group(2)
            self.assertEqual(expected_cache_keys[filename], match.group(2))
            self.assertIn('class="course-video-hero"', text)
            self.assertIn('id="watch-first"', text)
            poster = f"part{part}" if part <= 4 else f"class{part}"
            self.assertIn(f"video-posters/{poster}.png", text)
            self.assertIn(f"RCC_Onboarding_{prefix}_{part}_Captions.vtt", text)
            self.assertIn("../../assets/captions/", text)
            self.assertIn('kind="captions"', text)
            self.assertNotIn("../../downloads/", text)
            self.assertNotIn('course-video-links', text)
            if part <= 4:
                self.assertNotIn(f"RCC_Onboarding_Part_{part}.pptx", text)
        self.assertEqual(expected_cache_keys, embedded)

    def test_player_links_require_both_live_release_flags(self):
        builder = load_site_builder()
        player = '<video src="https://docs.ikim.uk-essen.de/media/lesson.mp4"></video>'
        live = {"status": "verified_live", "preview_links": "enabled"}
        self.assertEqual(player, builder.gate_unreleased_videos(player, live))
        for publication in (
            {"status": "prepared_pending_dns_tls", "preview_links": "enabled"},
            {"status": "verified_live", "preview_links": "disabled_until_verified_live"},
        ):
            gated = builder.gate_unreleased_videos(player, publication)
            self.assertIn("Video not yet released", gated)
            self.assertNotIn("lesson.mp4", gated)

    def test_site_build_keeps_vtt_captions_without_downloads_or_local_media(self):
        import subprocess
        import sys

        with tempfile.TemporaryDirectory() as output_name:
            output = Path(output_name)
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools/build_site.py"), "--output", str(output)],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(17, len(list((output / "assets/captions").glob("*.vtt"))))
            self.assertFalse((output / "downloads").exists())
            self.assertFalse((output / "media").exists())
            self.assertFalse((output / "media/index.html").exists())
            class_pages = list((output / "course").glob("class-*/index.html"))
            self.assertEqual(18, len(class_pages))
            video_pages = [
                page for page in class_pages
                if page.parent.name != "class-18-coding-agents"
            ]
            self.assertEqual(17, len(video_pages))
            for page in video_pages:
                text = page.read_text()
                self.assertIn("Video not yet released", text)
                self.assertNotIn("Video_Enhanced.mp4", text)
                self.assertNotIn("docs.ikim.uk-essen.de/media/", text)
                self.assertNotIn("ikim-essen.github.io/ClusterDocs/media/", text)

    def test_additional_class_assets_match_report(self):
        report = json.loads((ROOT / "meta/course-video-build-report.json").read_text())
        self.assertEqual(list(range(5, 18)), [item["class"] for item in report])
        for item in report:
            number = item["class"]
            frames = sorted((ROOT / f"slides/frames/class{number}").glob("slide-*.png"))
            narration = ROOT / f"narration/RCC_Onboarding_Class_{number}_Video_Narration.md"
            captions = ROOT / f"captions/RCC_Onboarding_Class_{number}_Captions.srt"
            self.assertEqual(item["slide_count"], len(frames))
            self.assertTrue(narration.is_file())
            self.assertTrue(captions.is_file())
            self.assertEqual(2, item["audio_channels"])
            self.assertEqual(64, len(item["video_sha256"]))
            self.assertGreater(item["caption_entries"], item["slide_count"])

    def test_course_overview_promotes_video_first(self):
        text = (ROOT / "docs/course/index.md").read_text()
        self.assertIn("Prefer to learn by video?", text)
        self.assertEqual(17, text.count('class="video-course-card"'))
        for part in range(1, 5):
            self.assertIn(f"video-posters/part{part}.png", text)
        for number in range(5, 18):
            self.assertIn(f"video-posters/class{number}.png", text)

    def test_publication_evidence_covers_the_online_media_gate(self):
        manifest = yaml.safe_load((ROOT / "config/media-manifest.yml").read_text())
        publication = manifest["publication"]
        self.assertEqual("rcc_docs_vhost", publication["method"])
        self.assertEqual(
            "https://docs.ikim.uk-essen.de/media/rcc-onboarding",
            publication["base_url"],
        )
        self.assertEqual(
            "/srv/www/docs/media/rcc-onboarding", publication["web_root"]
        )
        self.assertEqual("prepared_pending_dns_tls", publication["status"])
        self.assertEqual(
            "disabled_until_verified_live", publication["preview_links"]
        )
        staged = publication["staged_asset_set"]
        self.assertEqual("new-videos", staged["source_directory"])
        self.assertEqual(17, staged["video_count"])
        self.assertEqual(122808554, staged["total_size_bytes"])
        self.assertEqual(
            "9bcbc20ff36123e77dc103f7619444b17b08c4d09aaa43fff1a1316bcef1ab11",
            staged["sha256s_file_sha256"],
        )
        self.assertRegex(staged["sha256s_file_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            {
                "manifest_sha256": "passed",
                "exact_sizes": "passed",
                "ffprobe_streams": "passed",
                "durations": "passed",
            },
            staged["verification"],
        )
        for asset in manifest["assets"]:
            self.assertGreater(asset["size_bytes"], 0)

    def test_rcc_publication_runbook_is_complete_and_has_no_fallback_url(self):
        text = (ROOT / "meta/PUBLICATION_RUNBOOK.md").read_text()
        self.assertIn("/srv/www/docs/media/rcc-onboarding", text)
        self.assertIn("python tools/media_gate.py --local-dir new-videos", text)
        self.assertIn("--base-url https://docs.ikim.uk-essen.de/media/rcc-onboarding", text)
        self.assertIn("status: verified_live", text)
        self.assertIn("preview_links: enabled", text)
        self.assertIn("Rollback", text)
        self.assertNotIn("https://ikim-essen.github.io/ClusterDocs/media", text)

    def test_build_report_records_natural_voice_and_complete_outputs(self):
        report = json.loads((ROOT / "meta/video-build-report.json").read_text())
        self.assertEqual([1, 2, 3, 4], [item["part"] for item in report])
        for item in report:
            self.assertEqual("Daniel", item["voice"])
            self.assertEqual("en_GB", item["locale"])
            self.assertEqual(2, item["audio_channels"])
            self.assertGreater(item["duration_seconds"], 7 * 60)
            self.assertEqual(64, len(item["video_sha256"]))
            self.assertGreater(item["caption_entries"], item["slide_count"])


if __name__ == "__main__":
    unittest.main()
