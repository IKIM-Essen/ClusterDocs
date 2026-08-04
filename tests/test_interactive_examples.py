import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class InteractiveExamples(unittest.TestCase):
 def test_validation_script_passes(self):
  result=subprocess.run([sys.executable, str(ROOT/'exercises/interactive/validate-interactive-examples.py')], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  self.assertEqual(result.returncode,0,result.stdout+result.stderr)
 def test_site_build_does_not_publish_download_tree(self):
  result=subprocess.run([sys.executable, str(ROOT/'tools/build_site.py'), '--output', str(ROOT/'site-test')], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  self.assertEqual(result.returncode,0,result.stdout+result.stderr)
  self.assertFalse((ROOT/'site-test/downloads').exists())
if __name__=='__main__': unittest.main()
