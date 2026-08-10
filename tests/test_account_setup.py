from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "examples" / "account-setup"


class AccountSetupTests(unittest.TestCase):
    def test_shell_files_parse(self):
        for path in KIT.rglob("*.sh"):
            subprocess.run(["bash", "-n", str(path)], check=True)

    def test_default_is_a_non_mutating_dry_run(self):
        with tempfile.TemporaryDirectory() as home:
            environment = os.environ.copy()
            environment["HOME"] = home
            environment.pop("XDG_CONFIG_HOME", None)
            result = subprocess.run(
                ["bash", str(KIT / "install.sh")],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertIn("DRY-RUN", result.stdout)
            self.assertFalse((Path(home) / ".config").exists())

    def test_examples_keep_safe_boundaries(self):
        text = "\n".join(path.read_text() for path in KIT.rglob("*") if path.is_file())
        self.assertNotIn("0.0.0.0", text)
        self.assertNotIn("curl | bash", text)
        self.assertIn("127.0.0.1", text)
        self.assertIn("#SBATCH", text)
        self.assertNotIn(">> $HOME/.bashrc", text)


if __name__ == "__main__":
    unittest.main()
