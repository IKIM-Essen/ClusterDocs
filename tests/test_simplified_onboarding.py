import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class SimplifiedOnboardingTests(unittest.TestCase):
    def test_start_pages_are_in_both_navigation_sources(self):
        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        builder = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")
        for relative in (
            "getting-started/index.md",
            "getting-started/macos.md",
            "getting-started/windows.md",
            "getting-started/vscode.md",
            "concepts/jump-shell-compute.md",
            "getting-started/what-changed.md",
            "paths/from-shell-scripts.md",
        ):
            self.assertIn(relative, mkdocs)
            self.assertIn(relative, builder)

        light = (DOCS / "getting-started/index.md").read_text(encoding="utf-8")
        self.assertIn("Expedition Light is the required first-use path", light)
        self.assertIn("full RCC Expedition is optional deeper training", light)

    def test_platform_guides_preserve_the_two_host_boundary(self):
        for relative in ("getting-started/macos.md", "getting-started/windows.md"):
            page = (DOCS / relative).read_text(encoding="utf-8")
            normalized = " ".join(page.split())
            self.assertIn("Host {{ ssh_gateway_alias }}", page)
            self.assertIn("Host {{ ssh_target_alias }}", page)
            self.assertIn("ProxyJump {{ ssh_gateway_alias }}", page)
            self.assertIn("You do not log into the jump host", normalized)
            self.assertIn("ssh -G {{ ssh_target_alias }}", page)

    def test_access_model_separates_gateway_control_and_compute(self):
        page = (DOCS / "concepts/jump-shell-compute.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "Jump host | Guarded doorway",
            "Shell host | Your RCC desk",
            "Compute worker | Scheduled laboratory bench",
            "The shell host is not a free compute node",
            "SSH provides access; Slurm provides compute",
        ):
            self.assertIn(phrase, page)

    def test_vscode_has_a_dedicated_safe_start_section(self):
        page = (DOCS / "getting-started/vscode.md").read_text(encoding="utf-8")
        for phrase in (
            "VS Code is the interface. It does not create a compute allocation",
            "Select `{{ ssh_target_alias }}`",
            "Do not select the jump-host alias",
            "files.watcherExclude",
            "Treat the remote workspace as executable",
            "submits computation through Slurm",
        ):
            self.assertIn(phrase, page)

    def test_large_team_layout_keeps_the_namespace_simple(self):
        page = (DOCS / "reference/users-groups-projects.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "Groups do have benefits—but a different purpose",
            "Organise storage for a large science team",
            "/homes/<user>",
            "/groups/<primary-group>",
            "/projects/<project>",
            "project-internal convention",
        ):
            self.assertIn(phrase, page)

    def test_old_cluster_comparison_has_a_precise_baseline_and_actions(self):
        page = (DOCS / "getting-started/what-changed.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(page.split())
        for phrase in (
            "`8f5b2bd` from 21 July 2026",
            "release v1.0 on 10 August 2026",
            "Use `ssh {{ ssh_target_alias }}`",
            "Keep `ForwardAgent no`",
            "Slurm is the normal execution path",
            "Managed Nextflow-to-Slurm is ready now",
            "Migration checklist for an existing user",
        ):
            self.assertIn(phrase, normalized)

    def test_workflow_conversion_has_safe_repeatable_gates(self):
        page = (DOCS / "paths/from-shell-scripts.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(page.split())
        for phrase in (
            "Snakemake is usually the simplest first choice",
            "Docker daemons do not run on Slurm compute nodes",
            "Do not call `sbatch` inside",
            "small synthetic test passes twice",
            "pinned Apptainer runtime",
            "scientific method, parameters, reference data, and interpretation",
        ):
            self.assertIn(phrase, normalized)


if __name__ == "__main__":
    unittest.main()
