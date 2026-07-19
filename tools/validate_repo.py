#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
checks=[
 [sys.executable,str(ROOT/'tools/publication_lint.py')],
 [sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],
 [sys.executable,'-m','unittest','discover','-s',str(ROOT/'exercises/vhost/protected-app'),'-v'],
]
for cmd in checks: subprocess.run(cmd,check=True,cwd=ROOT)
yaml.safe_load((ROOT/'config/public.yml').read_text())
build=[sys.executable,str(ROOT/'tools/build_site.py'),'--output','site-test']
if all((ROOT/'videos-enhanced'/f'RCC_Onboarding_Part_{i}_Video_Enhanced.mp4').exists() for i in range(1,5)): build.append('--include-media')
subprocess.run(build,check=True,cwd=ROOT)
subprocess.run([sys.executable,str(ROOT/'tools/check_site_links.py'),str(ROOT/'site-test')],check=True,cwd=ROOT)
subprocess.run(['rm','-rf',str(ROOT/'site-test')],check=True)
for p in ROOT.rglob('*.py'): compile(p.read_text(),str(p),'exec')
print('repository validation: PASS')
