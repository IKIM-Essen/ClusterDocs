import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def normalized(path):
    return " ".join(path.read_text(encoding="utf-8").lower().split())


class FeatureReleaseStatusTests(unittest.TestCase):
    def test_status_registry_matches_the_confirmed_release_state(self):
        config = yaml.safe_load((ROOT / "config/public.yml").read_text())
        self.assertEqual(
            {
                "rcc_admin": "not_yet_released",
                "rcc_admin_self_administration": "not_yet_released",
                "rcc_admin_primary_approval": "not_yet_released",
                "rcc_files": "not_yet_released",
                "rcc_workers": "ready",
                "ssh_shellhost_transfer": "ready",
                "samba_project_shares": "in_service_on_request",
                "headscale_pikvm_access": "not_yet_released",
                "remote_files_macos_backup": "not_yet_released",
                "nextflow_slurm_support": "validating",
                "opportunistic_and_group_capacity": "not_yet_released",
                "project_vhosts": "not_yet_released",
                "ardia_integration": "not_yet_released",
                "rcc_to_coscine_transfer": "not_yet_released",
            },
            config["feature_status"],
        )

    def test_every_public_unreleased_feature_mention_is_marked(self):
        for feature in ("vhost", "ardia", "coscine", "headscale"):
            pages = [
                page
                for page in DOCS.rglob("*.md")
                if re.search(
                    rf"\b{re.escape(feature)}\b",
                    page.read_text(encoding="utf-8").lower(),
                )
            ]
            self.assertTrue(pages, feature)
            for page in pages:
                self.assertIn(
                    "not yet released",
                    normalized(page),
                    f"{page.relative_to(ROOT)} mentions {feature} without its release status",
                )

    def test_every_public_nextflow_page_marks_it_validating(self):
        pages = (
            DOCS / "tldr.md",
            DOCS / "course/class-07-nextflow.md",
            DOCS / "reference/software-workflows.md",
            DOCS / "classes/examples/nextflow-rcc/README.md",
        )
        for page in pages:
            self.assertIn(
                "validating",
                normalized(page),
                f"{page.relative_to(ROOT)} mentions Nextflow without its validating status",
            )

    def test_every_public_samba_page_marks_it_in_service_on_request(self):
        pages = [
            page
            for page in DOCS.rglob("*.md")
            if "samba" in page.read_text(encoding="utf-8").lower()
        ]
        self.assertTrue(pages)
        for page in pages:
            text = normalized(page)
            self.assertIn(
                "in service",
                text,
                f"{page.relative_to(ROOT)} mentions Samba without its in-service status",
            )
            self.assertNotIn("samba shares are **ready now**", text)

    def test_rcc_admin_is_unreleased_and_workers_are_ready(self):
        access = normalized(DOCS / "reference/access-ssh-vscode.md")
        analysis = normalized(DOCS / "paths/data-analysis.md")
        self.assertIn("**the rcc admin self-service portal is not yet released.**", access)
        self.assertNotIn("rcc admin is ready now", access)
        self.assertIn("rcc workers and slurm analysis are **ready now**", analysis)

    def test_withdrawn_browser_services_are_not_presented_as_ready(self):
        for page in DOCS.rglob("*.md"):
            text = normalized(page)
            with self.subTest(page=str(page.relative_to(ROOT))):
                self.assertNotIn("rcc admin is ready now", text)
                self.assertNotIn("| current user path |", text)
                self.assertNotIn("use the **rcc files portal**", text)

    def test_ssh_configuration_names_the_public_jump_host(self):
        for page in DOCS.rglob("*.md"):
            self.assertNotIn(
                "VALUE_FROM_THE_APPROVED_RCC_CONFIGURATION",
                page.read_text(encoding="utf-8"),
                str(page.relative_to(ROOT)),
            )
        self.assertIn(
            "HostName login.ikim.uk-essen.de",
            (DOCS / "getting-started/macos.md").read_text(encoding="utf-8"),
        )

    def test_overview_pages_do_not_duplicate_the_service_availability_table(self):
        for page in (DOCS / "index.md", DOCS / "tldr.md"):
            text = normalized(page)
            self.assertNotIn("service availability", text)
            self.assertNotIn("what is available now?", text)
            self.assertNotIn("| capability | status |", text)


if __name__ == "__main__":
    unittest.main()
