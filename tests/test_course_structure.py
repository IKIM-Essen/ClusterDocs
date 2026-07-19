import re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CourseTests(unittest.TestCase):
 def test_eleven_classes_exist(self):
  pages=sorted((ROOT/'docs/course').glob('class-*.md')); self.assertEqual(len(pages),11)
 def test_each_class_has_gate_or_completion(self):
  for p in (ROOT/'docs/course').glob('class-*.md'):
   t=p.read_text().lower(); self.assertRegex(t,r'gate|completion')
 def test_public_docs_do_not_link_admin_files(self):
  text='\n'.join(p.read_text() for p in (ROOT/'docs').rglob('*.md'))
  self.assertNotIn('current-system-understanding',text)
  self.assertNotIn('inventory/hosts.yml',text)
 def test_slurm_gate_is_bounded(self):
  t=(ROOT/'exercises/slurm/bash-hello/job.sbatch').read_text()
  self.assertIn('#SBATCH --time=00:02:00',t); self.assertIn('#SBATCH --cpus-per-task=1',t); self.assertIn('#SBATCH --mem=128M',t)
  self.assertNotIn('--array',t)
 def test_interactive_classes_reference_examples(self):
  refs='\n'.join((ROOT/'docs/course'/name).read_text() for name in ['class-07-python-notebooks.md','class-08-r-analysis.md','class-09-shiny.md'])
  for token in ['examples/interactive-workflows/jupyter','examples/interactive-workflows/python','examples/interactive-workflows/r','examples/interactive-workflows/shiny']:
   self.assertIn(token, refs)
 def test_notebook_to_service_moves_compute_to_slurm(self):
  t=(ROOT/'docs/course/class-10-notebook-to-service.md').read_text().lower()
  self.assertIn('slurm workflow',t)
  self.assertIn('web app only handles',t)
if __name__=='__main__': unittest.main()
