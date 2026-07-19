import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReadinessTests(unittest.TestCase):
 def test_ssh_is_single_attempt_and_strict(self):
  t=(ROOT/'exercises/readiness/rcc-readiness.sh').read_text()
  for x in ['ConnectionAttempts=1','ConnectTimeout=10','StrictHostKeyChecking=yes','BatchMode=yes']: self.assertIn(x,t)
  self.assertNotIn('StrictHostKeyChecking=no',t)
 def test_scripts_do_not_print_private_key(self):
  for p in (ROOT/'exercises/readiness').iterdir():
   if p.is_file(): self.assertNotRegex(p.read_text(),r'\bcat\s+["\']?\$?KEY\b')
if __name__=='__main__': unittest.main()
