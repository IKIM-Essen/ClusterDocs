import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LegacyContentMigrationTests(unittest.TestCase):
    def test_all_legacy_instructional_images_are_preserved(self):
        names = [
            "ConnectMeNow-advanced-setup.png",
            "ConnectMeNow-icon.png",
            "ConnectMeNow-share-setup.png",
            "WinFSP_download.png",
            "jupyter-home.png",
            "jupyter-notebook.png",
            "sshfs_win_manager.png",
            "sshfs_win_manager_conditions.png",
            "sshfs_win_manager_details1.png",
            "sshfs_win_manager_details2.png",
            "sshfs_win_manager_settings.png",
            "vs_code_ssh_remote_explorer.png",
            "vs_code_ssh_remote_folder.png",
            "vs_code_ssh_remote_plugin.png",
        ]
        for name in names:
            path = ROOT / "docs/assets" / name
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 1_000, path)

    def test_restored_images_are_referenced_by_public_guides(self):
        text = "\n".join(path.read_text() for path in (ROOT / "docs").rglob("*.md"))
        for image in (ROOT / "docs/assets").glob("*.png"):
            self.assertIn(image.name, text, image)

    def test_historical_images_have_adjacent_safety_context(self):
        windows = (ROOT / "docs/data/legacy-storage-windows.md").read_text().lower()
        macos = (ROOT / "docs/data/legacy-storage-macos.md").read_text().lower()
        vscode = (ROOT / "docs/reference/access-ssh-vscode.md").read_text().lower()
        jupyter = (ROOT / "docs/course/class-09-python-notebooks.md").read_text().lower()
        self.assertIn("setting up access now? skip this page", windows)
        self.assertIn("setting up access now? skip this page", macos)
        self.assertIn("do not copy target names", vscode)
        self.assertIn("do not reuse those values", jupyter)

    def test_audit_maps_every_legacy_document_and_exclusion(self):
        audit_path = ROOT / "meta/LEGACY_CONTENT_AUDIT.md"
        self.assertTrue(audit_path.is_file())
        audit = audit_path.read_text()
        for name in [
            "access.md",
            "accessing-storage.md",
            "apptainer.md",
            "computing.md",
            "conda.md",
            "first-steps.md",
            "getting-started.md",
            "index.md",
            "jupyter.md",
            "patterns.md",
            "performance.md",
            "resources.md",
            "s3.md",
            "slurm.md",
            "snakemake.md",
            "ssh-setup.md",
            "storage.md",
            "transfer.md",
            "troubleshooting.md",
            "upcoming-rcc-changes.md",
            "vs-code-setup.md",
        ]:
            self.assertIn(name, audit)
        for phrase in ["raw Netcat", "unencrypted legacy FTP", "direct computation outside Slurm"]:
            self.assertIn(phrase, audit)

    def test_overall_tldr_covers_core_boundaries_and_navigation(self):
        page = (ROOT / "docs/tldr.md").read_text().lower()
        for phrase in [
            "clusterdocs 3 tl;dr",
            "ten rules that prevent most problems",
            "approved project",
            "job-local storage",
            "biomedical-data boundary",
            "lab network",
            "verified coscine archive",
            "data-blind by default",
        ]:
            self.assertIn(phrase, page)
        mkdocs = (ROOT / "mkdocs.yml").read_text()
        builder = (ROOT / "tools/build_site.py").read_text()
        self.assertIn("ClusterDocs TL;DR: tldr.md", mkdocs)
        self.assertIn("'ClusterDocs TL;DR','tldr.md'", builder)


if __name__ == "__main__":
    unittest.main()
