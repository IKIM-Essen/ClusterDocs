import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "connecting" / "remote-files-macos.md"


class RemoteFilesMacDocsTests(unittest.TestCase):
    def test_service_stays_explicitly_unreleased(self):
        text = " ".join(GUIDE.read_text(encoding="utf-8").lower().split())
        self.assertIn("service status: not yet released", text)
        self.assertIn("do not remove an existing backup disk", text)

    def test_security_and_recovery_contract_is_present(self):
        text = GUIDE.read_text(encoding="utf-8").lower()
        for phrase in (
            "strong rcc two-factor authentication",
            "filevault is required",
            "backup bundle itself must be encrypted",
            "backing filesystem must be encrypted at rest",
            "approved recovery-custody",
            "migration assistant",
            "verify backups",
            "tcp/445 is not opened directly to eduroam",
        ):
            self.assertIn(phrase, text)

    def test_group_publication_boundary_is_present(self):
        text = GUIDE.read_text(encoding="utf-8").lower()
        for phrase in (
            "only the user's primary working group",
            "move project-like material",
            "/projects/<project>",
            "explicit review before publication",
            "project storage is deliberately not exposed",
        ):
            self.assertIn(phrase, text)

    def test_feature_registry_remains_closed(self):
        config = yaml.safe_load((ROOT / "config/public.yml").read_text())
        self.assertEqual(config["feature_status"]["remote_files_mac_access"], "not_yet_released")
        self.assertEqual(config["feature_status"]["remote_files_time_machine_backup"], "not_yet_released")


if __name__ == "__main__":
    unittest.main()
