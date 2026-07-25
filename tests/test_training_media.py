import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_video_builder():
    path = ROOT / "build/build_videos.py"
    spec = importlib.util.spec_from_file_location("build_videos", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class TrainingMediaTests(unittest.TestCase):
    CLASS_SLUGS = {
        1: "class-01-safe-access.md", 2: "class-02-workflows.md",
        3: "class-03-performance.md", 4: "class-04-containers.md",
        5: "class-05-slurm.md", 6: "class-06-vhosts.md",
        7: "class-07-python-notebooks.md", 8: "class-08-r-analysis.md",
        9: "class-09-shiny.md", 10: "class-10-notebook-to-service.md",
        11: "class-11-biomedical-data-privacy.md", 12: "class-12-efficient-io.md",
        13: "class-13-storage-architecture.md", 14: "class-14-wet-lab-data-workflows.md",
        15: "class-15-data-lifecycle.md",
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

    def test_numbered_classes_embed_video_and_accessible_companions(self):
        for part, slug in self.CLASS_SLUGS.items():
            text = (ROOT / "docs/course" / slug).read_text()
            prefix = "Part" if part <= 4 else "Class"
            self.assertIn(
                f"RCC_Onboarding_{prefix}_{part}_Video_Enhanced.mp4", text
            )
            self.assertIn('class="course-video-hero"', text)
            self.assertIn('id="watch-first"', text)
            poster = f"part{part}" if part <= 4 else f"class{part}"
            self.assertIn(f"video-posters/{poster}.png", text)
            self.assertIn(f"RCC_Onboarding_{prefix}_{part}_Captions.srt", text)
            self.assertIn(f"RCC_Onboarding_{prefix}_{part}_Captions.vtt", text)
            self.assertIn('kind="captions"', text)
            narration_suffix = "Narration.md" if part <= 4 else "Video_Narration.md"
            self.assertIn(f"RCC_Onboarding_{prefix}_{part}_{narration_suffix}", text)
            if part <= 4:
                self.assertIn(f"RCC_Onboarding_Part_{part}.pptx", text)

    def test_additional_class_assets_match_report(self):
        report = json.loads((ROOT / "meta/course-video-build-report.json").read_text())
        self.assertEqual(list(range(5, 16)), [item["class"] for item in report])
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
        self.assertEqual(15, text.count('class="video-course-card"'))
        for part in range(1, 5):
            self.assertIn(f"video-posters/part{part}.png", text)
        for number in range(5, 16):
            self.assertIn(f"video-posters/class{number}.png", text)

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
