import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DataLifecycleCourseTests(unittest.TestCase):
    def test_course_and_planned_flow_exist(self):
        required = [
            ROOT / "docs/course/class-15-data-lifecycle.md",
            ROOT / "docs/data/rcc-project-to-coscine.md",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_course_covers_coscine_and_safe_archive_acceptance(self):
        page = (ROOT / "docs/course/class-15-data-lifecycle.md").read_text().lower()
        for phrase in [
            "coscine as an archive option",
            "planned, not yet a live self-service service",
            "authoritative copy",
            "completion gate",
            "before deleting any source",
        ]:
            self.assertIn(phrase, page)

    def test_planned_flow_has_required_control_points(self):
        page = (ROOT / "docs/data/rcc-project-to-coscine.md").read_text().lower()
        for phrase in [
            "service status: planned",
            "eligibility decision",
            "freeze and describe",
            "verify and accept",
            "keep the rcc source",
        ]:
            self.assertIn(phrase, page)

    def test_navigation_keeps_class_numbering_and_flow_link(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text()
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("Class 15 - Research data lifecycle", mkdocs)
        self.assertIn("Class 15 · Research data lifecycle", builder)
        self.assertIn("data/rcc-project-to-coscine.md", mkdocs)
        self.assertIn("data/rcc-project-to-coscine.md", builder)

    def test_coursectl_accepts_class_fifteen(self):
        coursectl = (ROOT / "tools/coursectl.py").read_text()
        self.assertIn("choices=range(1,16)", coursectl)


if __name__ == "__main__":
    unittest.main()
