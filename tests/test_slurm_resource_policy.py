#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/policies/slurm-resource-sharing.md"


class SlurmResourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.text = DOC.read_text(encoding="utf-8")

    def test_policy_explains_owner_borrow_shared_and_interactive_paths(self):
        for phrase in (
            "reclaimable compute entitlement",
            "Shared capacity",
            "Owner capacity",
            "Borrowed capacity",
            "Interactive use",
            "interactive_backfill",
            "requeued",
            "fair-share",
        ):
            self.assertIn(phrase, self.text)

    def test_plain_language_summary_precedes_technical_details(self):
        self.assertIn("Most users do not need to choose", self.text)
        self.assertIn("If you are unsure, use the normal shared partition", self.text)
        self.assertLess(
            self.text.index("## What this means for you"),
            self.text.index("## Technical policy details"),
        )

    def test_examples_are_explicitly_fictional(self):
        self.assertIn("fictional examples", self.text)
        self.assertIn("group-alpha", self.text)
        self.assertIn("compute-alpha-01", self.text)

    def test_examples_do_not_claim_to_be_the_live_mapping(self):
        self.assertIn("do not identify real RCC groups", self.text)
        self.assertIn(
            "public site does not publish the private node-to-group mapping",
            " ".join(self.text.split()),
        )

    def test_navigation_exposes_the_policy(self):
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        custom_nav = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
        self.assertIn("policies/slurm-resource-sharing.md", nav)
        self.assertIn("policies/slurm-resource-sharing.md", custom_nav)


if __name__ == "__main__":
    unittest.main()
