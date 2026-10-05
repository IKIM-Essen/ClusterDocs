import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AISafeSampleCourseTests(unittest.TestCase):
    def test_course_is_in_both_navigation_sources(self):
        path = "course/class-18-coding-agents.md"
        self.assertIn(path, (ROOT / "mkdocs.yml").read_text())
        self.assertIn(path, (ROOT / "tools/build_site.py").read_text())

    def test_course_keeps_real_data_inside_rcc(self):
        text = (ROOT / "docs/course/class-18-coding-agents.md").read_text().lower()
        for phrase in (
            "invent every value from scratch",
            "do not “scramble” real rows",
            "real data and real analysis outputs stayed inside",
            "--input and --output",
            "three-point completion check",
            "there is no form and no case-by-case approval",
            "use inside rcc",
            "coding agent",
        ):
            self.assertIn(phrase, text)

    def test_course_has_a_high_resolution_explanatory_figure(self):
        page = (ROOT / "docs/course/class-18-coding-agents.md").read_text()
        asset = ROOT / "docs/assets/course/class18-coding-agent-flow.png"
        self.assertIn("class18-coding-agent-flow.png", page)
        self.assertTrue(asset.is_file())
        self.assertGreater(asset.stat().st_size, 100_000)

    def test_overview_leads_with_the_two_safe_routes(self):
        text = (ROOT / "docs/concepts/how-rcc-works.md").read_text().lower()
        text = text.replace("**", "")
        text = " ".join(text.split())
        for phrase in (
            "off-site coding agents must not receive rcc research data",
            "must not paste, upload, or otherwise make real or pseudonymised",
            "does not authorize it to receive rcc data",
            "a user cannot create the required legal basis",
            "route a: use a coding agent inside rcc",
            "route b: give an off-site coding agent synthetic data only",
            "the documented manual method is available now",
            "real inputs, revealing error messages, and real outputs do not go back",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("approved coding agent", text)

    def test_example_bundle_is_explicitly_synthetic(self):
        bundle = ROOT / "docs/classes/examples/coding-agent-sample"
        for name in ("README.md", "QUESTION.md", "example.csv", "EXPECTED_OUTPUT.md", "PROMPT.txt"):
            self.assertTrue((bundle / name).is_file(), name)
        sample = (bundle / "example.csv").read_text()
        self.assertIn("SYN-001", sample)
        self.assertNotIn("patient", sample.lower())

    def test_video_narration_covers_the_six_step_story(self):
        narration = (ROOT / "narration/RCC_AI_Synthetic_Example_Video_Narration.md").read_text()
        for scene in range(1, 7):
            self.assertIn(f"## Scene {scene}:", narration)


if __name__ == "__main__":
    unittest.main()
