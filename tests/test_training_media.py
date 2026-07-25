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
        slugs = {
            1: "class-01-safe-access.md",
            2: "class-02-workflows.md",
            3: "class-03-performance.md",
            4: "class-04-containers.md",
        }
        for part, slug in slugs.items():
            text = (ROOT / "docs/course" / slug).read_text()
            self.assertIn(
                f"RCC_Onboarding_Part_{part}_Video_Enhanced.mp4", text
            )
            self.assertIn('class="course-video-hero"', text)
            self.assertIn('id="watch-first"', text)
            self.assertIn(f"video-posters/part{part}.png", text)
            self.assertIn(f"RCC_Onboarding_Part_{part}_Captions.srt", text)
            self.assertIn(f"RCC_Onboarding_Part_{part}_Narration.md", text)
            self.assertIn(f"RCC_Onboarding_Part_{part}.pptx", text)

    def test_course_overview_promotes_video_first(self):
        text = (ROOT / "docs/course/index.md").read_text()
        self.assertIn("Prefer to learn by video?", text)
        self.assertEqual(4, text.count('class="video-course-card"'))
        for part in range(1, 5):
            self.assertIn(f"video-posters/part{part}.png", text)

    def test_build_report_records_natural_voice_and_complete_outputs(self):
        report = json.loads((ROOT / "meta/video-build-report.json").read_text())
        self.assertEqual([1, 2, 3, 4], [item["part"] for item in report])
        for item in report:
            self.assertEqual("Daniel", item["voice"])
            self.assertEqual("en_GB", item["locale"])
            self.assertGreater(item["duration_seconds"], 7 * 60)
            self.assertEqual(64, len(item["video_sha256"]))
            self.assertGreater(item["caption_entries"], item["slide_count"])


if __name__ == "__main__":
    unittest.main()
