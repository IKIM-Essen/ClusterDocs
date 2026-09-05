import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CredentialGuidanceTests(unittest.TestCase):
    def test_active_user_guidance_does_not_recommend_ssh_key_passphrases(self):
        paths = (
            "docs/getting-started/macos.md",
            "docs/getting-started/windows.md",
            "docs/course/class-01-safe-access.md",
            "docs/reference/access-ssh-vscode.md",
            "docs/reference/authentication-lifecycle.md",
            "docs/security/safe-use.md",
            "docs/getting-started/what-changed.md",
        )
        forbidden = (
            "use a strong passphrase",
            "protect it with a strong passphrase",
            "a strong key passphrase is still expected",
            "use a separate passphrase to protect the private key",
        )
        for relative in paths:
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            with self.subTest(relative=relative):
                for phrase in forbidden:
                    self.assertNotIn(phrase, text)
                self.assertIn("without a passphrase", text)

    def test_platform_setup_makes_empty_ssh_passphrase_explicit(self):
        for relative in (
            "docs/getting-started/macos.md",
            "docs/getting-started/windows.md",
            "docs/course/class-01-safe-access.md",
            "docs/reference/access-ssh-vscode.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative):
                self.assertIn('-N ""', text)

    def test_password_manager_guidance_is_for_web_account_credentials(self):
        for relative in (
            "docs/getting-started/macos.md",
            "docs/getting-started/windows.md",
            "docs/reference/authentication-lifecycle.md",
            "docs/security/safe-use.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            with self.subTest(relative=relative):
                self.assertIn("password", text)
                self.assertIn("passkey", text)
                self.assertIn("ssh", text)

    def test_part1_narration_and_captions_use_v3_policy(self):
        narration = (ROOT / "narration/RCC_Onboarding_Part_1_Narration.md").read_text(encoding="utf-8").lower()
        captions = (ROOT / "captions/RCC_Onboarding_Part_1_Captions.srt").read_text(encoding="utf-8").lower()
        self.assertIn("does not recommend adding a passphrase", narration)
        self.assertIn("does not recommend a passphrase", captions)
        self.assertNotIn("a passphrase protects the private key", narration)
        self.assertNotIn("a passphrase protects the private key", captions)


if __name__ == "__main__":
    unittest.main()
