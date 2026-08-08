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
                "rcc_admin": "ready",
                "rcc_admin_self_administration": "ready",
                "rcc_admin_primary_approval": "ready",
                "rcc_workers": "ready",
                "samba_project_shares": "ready",
                "headscale_pikvm_access": "not_yet_released",
                "nextflow_slurm_support": "not_yet_released",
                "project_vhosts": "not_yet_released",
                "ardia_integration": "not_yet_released",
                "rcc_to_coscine_transfer": "not_yet_released",
            },
            config["feature_status"],
        )

    def test_every_public_unreleased_feature_mention_is_marked(self):
        for feature in ("vhost", "ardia", "coscine", "nextflow", "headscale"):
            pages = [
                page
                for page in DOCS.rglob("*.md")
                if feature in page.read_text(encoding="utf-8").lower()
            ]
            self.assertTrue(pages, feature)
            for page in pages:
                self.assertIn(
                    "not yet released",
                    normalized(page),
                    f"{page.relative_to(ROOT)} mentions {feature} without its release status",
                )

    def test_every_public_samba_page_marks_it_ready(self):
        pages = [
            page
            for page in DOCS.rglob("*.md")
            if "samba" in page.read_text(encoding="utf-8").lower()
        ]
        self.assertTrue(pages)
        for page in pages:
            self.assertIn(
                "ready now",
                normalized(page),
                f"{page.relative_to(ROOT)} mentions Samba without its ready status",
            )

    def test_rcc_admin_and_workers_are_not_described_as_pending(self):
        homepage = normalized(DOCS / "index.md")
        access = normalized(DOCS / "reference/access-ssh-vscode.md")
        self.assertIn("rcc admin self-administration and primary-approver workflow | **ready now**", homepage)
        self.assertIn("rcc workers and slurm computation | **ready now**", homepage)
        self.assertIn("**rcc admin is ready now**", access)
        self.assertNotIn("rcc admin request flow when it is available", access)


if __name__ == "__main__":
    unittest.main()
