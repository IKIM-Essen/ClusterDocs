import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(path):
    return " ".join(path.read_text().lower().split())


class NewcomerLayOfLandTests(unittest.TestCase):
    def test_homepage_explains_the_complete_plain_language_model(self):
        page = normalized(DOCS / "index.md")
        for phrase in (
            "your personal badge",
            "every user has exactly one",
            "people from different primary groups",
            "project samba share",
            "project vhost",
            "coscine later [not yet released]",
        ):
            self.assertIn(phrase, page)

    def test_main_tldr_connects_identity_projects_instruments_and_services(self):
        page = normalized(DOCS / "tldr.md")
        for phrase in (
            "exactly one primary group",
            "people from different primary groups",
            "approved samba share for its project",
            "future ardia integration",
            "optional protected vhost for that project",
            "planned and not yet a live self-service transfer",
        ):
            self.assertIn(phrase, page)

    def test_data_tldr_is_understandable_without_it_background(self):
        page = normalized(DOCS / "data/data-lifecycle-tldr.md")
        for phrase in (
            "primary group says where you belong",
            "project membership says which collaborative data you may use",
            "samba share",
            "normal network folder",
            "vendor-supported integration",
            "verified coscine archive",
        ):
            self.assertIn(phrase, page)

    def test_project_is_the_common_boundary(self):
        page = normalized(DOCS / "reference/users-groups-projects.md")
        for phrase in (
            "account = your badge",
            "primary group = your home department",
            "project = the shared project room",
            "each future vhost will belong to one project",
            "samba share",
            "coscine",
        ):
            self.assertIn(phrase, page)

    def test_vhost_and_instrument_pages_keep_project_scope(self):
        vhost = normalized(DOCS / "course/class-08-vhosts.md")
        instrument = normalized(DOCS / "data/instrument-data-options.md")
        self.assertIn("request a **vhost for that project**", vhost)
        self.assertIn("each vhost will belong to one project", vhost)
        self.assertIn("project's samba share", instrument)
        self.assertIn("registered instrument -> project samba share", instrument)
        self.assertIn("ardia", instrument)


if __name__ == "__main__":
    unittest.main()
