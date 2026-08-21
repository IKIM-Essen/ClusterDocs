import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WetLabCourseTests(unittest.TestCase):
    def test_course_and_instrument_guides_exist(self):
        required = [
            ROOT / "docs/course/class-16-wet-lab-data-workflows.md",
            ROOT / "docs/data/instrument-data-options.md",
            ROOT / "docs/data/legacy-storage-windows.md",
            ROOT / "docs/data/legacy-storage-macos.md",
            ROOT / "docs/connecting/stable-endpoints.md",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_wet_lab_course_has_safe_handoff_and_completion_gate(self):
        page = (ROOT / "docs/course/class-16-wet-lab-data-workflows.md").read_text().lower()
        for phrase in [
            "authoritative original",
            "verify before deleting",
            "primary identifying",
            "completion gate",
            "project, not a home directory",
            "verified coscine archive set",
            "lab network",
            "general direct internet connectivity",
            "explicitly approved server endpoints",
            "http proxy",
        ]:
            self.assertIn(phrase, page)

    def test_navigation_keeps_class_numbering(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text()
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("Class 16 - Wet-lab instrument data", mkdocs)
        self.assertIn("Class 16 · Wet-lab instrument data", builder)

    def test_endpoint_page_uses_configured_alias(self):
        page = (ROOT / "docs/connecting/stable-endpoints.md").read_text()
        self.assertIn("{{ ssh_gateway_alias }}", page)
        self.assertIn("{{ ssh_target_alias }}", page)
        self.assertNotIn("is2-2", page)
        self.assertNotIn("is2-5", page)

    def test_existing_mount_guides_give_direct_user_instructions(self):
        for name in ["legacy-storage-windows.md", "legacy-storage-macos.md"]:
            page = (ROOT / "docs/data" / name).read_text().lower()
            self.assertIn("setting up access now? skip this page", page)
            self.assertIn("do not copy", page)
            self.assertIn("connection settings you were given", page)
            self.assertIn("do not use it for", page)


if __name__ == "__main__":
    unittest.main()
