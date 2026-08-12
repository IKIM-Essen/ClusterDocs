import re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CourseTests(unittest.TestCase):
 def test_eighteen_classes_exist(self):
  pages=sorted((ROOT/'docs/course').glob('class-*.md')); self.assertEqual(len(pages),18)
  self.assertEqual([f'class-{number:02d}' for number in range(1,19)],[page.stem[:8] for page in pages])
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
  refs='\n'.join((ROOT/'docs/course'/name).read_text() for name in ['class-09-python-notebooks.md','class-10-r-analysis.md','class-11-shiny.md'])
  for token in ['examples/interactive-workflows/jupyter','examples/interactive-workflows/python','examples/interactive-workflows/r','examples/interactive-workflows/shiny']:
   self.assertIn(token, refs)
 def test_notebook_to_service_moves_compute_to_slurm(self):
  t=(ROOT/'docs/course/class-12-notebook-to-service.md').read_text().lower()
  self.assertIn('slurm workflow',t)
  self.assertIn('web app only handles',t)
 def test_nf_core_class_example_is_pinned_and_bounded(self):
  page=(ROOT/'docs/course/class-07-nextflow.md').read_text()
  config=(ROOT/'docs/classes/examples/nf-core/rcc-test.config').read_text()
  runner=(ROOT/'docs/classes/examples/nf-core/run-demo.sh').read_text()
  params=(ROOT/'docs/classes/examples/nf-core/params-rnaseq.example.json').read_text()
  self.assertIn('nf-core/demo',page)
  self.assertIn('service status — ready now',page.lower())
  self.assertIn('rcc-test.config',page)
  self.assertIn("executor = 'slurm'",config)
  self.assertIn("queue = 'cpu_short'",config)
  self.assertIn('scratch = true',config)
  self.assertIn('queueSize = 4',config)
  self.assertIn('cpus: 4',config)
  self.assertIn('memory: 16.GB',config)
  self.assertIn('time: 30.m',config)
  self.assertIn('-r 1.2.0',runner)
  self.assertIn('-profile test,apptainer',runner)
  self.assertIn('Required command not found',runner)
  self.assertIn('rcc-nextflow --project-root',runner)
  self.assertNotIn('for command_name in nextflow ',runner)
  self.assertNotIn(':latest',runner)
  self.assertNotIn('--array',runner)
  self.assertIn('/projects/PROJECT/inputs/samplesheet.csv',params)
 def test_snakemake_class_is_ready_bounded_and_managed(self):
  page=(ROOT/'docs/course/class-06-snakemake.md').read_text()
  snakefile=(ROOT/'docs/classes/examples/snakemake-rcc/Snakefile').read_text()
  self.assertIn('ready now',page.lower())
  self.assertIn('snakemake --profile IKIM --jobs 4',page)
  self.assertIn('snakemake --dry-run',page)
  self.assertIn('slurm_partition="cpu_short"',snakefile)
  self.assertIn('runtime=5',snakefile)
  self.assertNotIn('--array',snakefile)
 def test_canonical_sources_have_no_release_placeholders(self):
  source='\n'.join(path.read_text() for path in sorted((ROOT/'source').glob('part*.md')))
  self.assertNotIn('[ADMIN:',source)
  self.assertNotIn('RCC_PROFILE',source)
  self.assertNotIn('administrators must complete',source.lower())
if __name__=='__main__': unittest.main()
