import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WetLabCourseTests(unittest.TestCase):
    def test_course_and_instrument_guides_exist(self):
        required = [
            ROOT / "docs/course/class-14-wet-lab-data-workflows.md",
            ROOT / "docs/data/instrument-data-options.md",
            ROOT / "docs/data/legacy-storage-windows.md",
            ROOT / "docs/data/legacy-storage-macos.md",
            ROOT / "docs/connecting/stable-endpoints.md",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_wet_lab_course_has_safe_handoff_and_completion_gate(self):
        page = (ROOT / "docs/course/class-14-wet-lab-data-workflows.md").read_text().lower()
        for phrase in [
            "authoritative original",
            "verify before deleting",
            "primary identifying",
            "completion gate",
            "project, not a home directory",
            "verified coscine archive set",
        ]:
            self.assertIn(phrase, page)

    def test_navigation_keeps_class_numbering(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text()
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("Class 14 - Wet-lab instrument data", mkdocs)
        self.assertIn("Class 14 · Wet-lab instrument data", builder)

    def test_endpoint_page_uses_configured_alias(self):
        page = (ROOT / "docs/connecting/stable-endpoints.md").read_text()
        self.assertIn("{{ ssh_alias }}", page)
        self.assertNotIn("is2-2", page)
        self.assertNotIn("is2-5", page)

    def test_legacy_mount_guides_are_clearly_historical(self):
        for name in ["legacy-storage-windows.md", "legacy-storage-macos.md"]:
            page = (ROOT / "docs/data" / name).read_text().lower()
            self.assertIn("historical", page)
            self.assertIn("bulk instrument transfer", page)
            self.assertIn("current rcc", page)


if __name__ == "__main__":
    unittest.main()
