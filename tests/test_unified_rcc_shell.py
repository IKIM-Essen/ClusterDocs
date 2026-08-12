from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class UnifiedRccShellTests(unittest.TestCase):
    def test_mkdocs_fallback_uses_the_unified_shell(self) -> None:
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

        self.assertEqual(config["theme"]["custom_dir"], "overrides")
        self.assertIn("stylesheets/rcc-shell.css", config["extra_css"])
        shell = config["extra"]["rcc_shell"]
        self.assertEqual(shell["myrcc_url"], "https://rcc-admin.ikim.uk-essen.de/myrcc")
        self.assertEqual(shell["files_url"], "https://files.ikim.uk-essen.de/web/client")
        self.assertEqual(shell["docs_url"], "https://ikim-essen.github.io/ClusterDocs/")

    def test_production_builder_uses_user_facing_service_navigation(self) -> None:
        builder = (ROOT / "tools/build_site.py").read_text(encoding="utf-8")

        for label, url in (
            ("Home", "https://rcc.ikim.uk-essen.de/"),
            ("Documentation", "{{ root }}index.html"),
            ("Files", "https://files.ikim.uk-essen.de/web/client"),
            ("My RCC", "https://rcc-admin.ikim.uk-essen.de/myrcc"),
            ("AI assistant", "https://assistant.ikim.uk-essen.de/"),
        ):
            self.assertIn(f'href="{url}"', builder)
            self.assertIn(f">{label}<", builder)

        service_nav = builder.split('<nav class="service-nav"', 1)[1].split("</nav>", 1)[0]
        self.assertNotIn(">RCC Admin<", service_nav)


if __name__ == "__main__":
    unittest.main()
