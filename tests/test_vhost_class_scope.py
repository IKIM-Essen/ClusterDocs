import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VhostClassScopeTests(unittest.TestCase):
    def test_class_explains_supported_patterns_and_boundaries(self):
        text = (ROOT / "docs/course/class-06-vhosts.md").read_text().lower()
        for required in [
            "static information site",
            "active read-only application",
            "active application with controlled writes",
            "controlled upload application",
            "what is not in scope",
            "division of responsibility",
            "common mistakes to avoid",
        ]:
            self.assertIn(required, text)

    def test_class_separates_web_interaction_from_cluster_compute(self):
        text = (ROOT / "docs/course/class-06-vhosts.md").read_text().lower()
        self.assertIn("computation belongs in slurm", text)
        self.assertNotRegex(text, r"while\s+true|--array")

    def test_narration_is_recording_length_and_has_chapters(self):
        text = (ROOT / "narration/RCC_Onboarding_Class_6_Narration.md").read_text()
        spoken = re.sub(r"```.*?```", "", text, flags=re.S)
        word_count = len(re.findall(r"\b[\w’'-]+\b", spoken))
        self.assertGreaterEqual(word_count, 1050)
        self.assertLessEqual(word_count, 1700)
        for chapter in ["00:00", "03:03", "06:15", "08:38"]:
            self.assertIn(chapter, text)

    def test_recording_material_keeps_rollout_values_replaceable(self):
        text = (ROOT / "narration/RCC_Onboarding_Class_6_Recording_Brief.md").read_text().lower()
        self.assertIn("leave production urls out", text)
        self.assertIn("replaceable segment", text)


if __name__ == "__main__":
    unittest.main()
