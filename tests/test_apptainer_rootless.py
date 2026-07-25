from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ApptainerRootlessTests(unittest.TestCase):
    def test_course_explains_concept_reason_and_boundary(self):
        text = (ROOT / "docs/course/class-04-containers.md").read_text().lower()
        for phrase in (
            "rootless",
            "not as the host's `root` user",
            "privileged docker-style daemon",
            "shared research cluster",
            "rootless does **not** mean harmless",
            "any host file that your user can access",
        ):
            self.assertIn(phrase, text)

    def test_reference_and_video_narration_match_the_course(self):
        reference = (ROOT / "docs/reference/software-workflows.md").read_text().lower()
        narration = (ROOT / "narration/RCC_Onboarding_Part_4_Narration.md").read_text().lower()
        for text in (reference, narration):
            self.assertIn("rootless", text)
            self.assertIn("slurm", text)
            self.assertIn("privileged docker-style daemon", text)
            self.assertIn("fakeroot", text)


if __name__ == "__main__":
    unittest.main()
