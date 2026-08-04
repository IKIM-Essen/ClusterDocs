import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.build_site import add_heading_ids


ROOT = Path(__file__).resolve().parents[1]


class SiteFragmentTests(unittest.TestCase):
    def test_heading_ids_are_stable_and_unique(self):
        rendered = add_heading_ids(
            '<h2>Customize VS Code without creating performance problems</h2>'
            '<h2>Repeated heading</h2><h2>Repeated heading</h2>'
        )
        self.assertIn(
            'id="customize-vs-code-without-creating-performance-problems"',
            rendered,
        )
        self.assertIn('id="repeated-heading"', rendered)
        self.assertIn('id="repeated-heading-2"', rendered)

    def test_link_checker_rejects_missing_fragment(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / 'index.html').write_text(
                '<h1 id="home">Home</h1><a href="other/index.html#missing">Bad</a>'
            )
            (site / 'other').mkdir()
            (site / 'other/index.html').write_text('<h1 id="present">Other</h1>')
            result = subprocess.run(
                [sys.executable, str(ROOT / 'tools/check_site_links.py'), str(site)],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing fragment', result.stderr)


if __name__ == '__main__':
    unittest.main()
