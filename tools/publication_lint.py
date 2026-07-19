#!/usr/bin/env python3
from __future__ import annotations
import re, shutil, subprocess, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
TEXT_ROOTS=[ROOT/'docs',ROOT/'exercises',ROOT/'source',ROOT/'narration',ROOT/'captions',ROOT/'meta',ROOT/'examples']
TEXT_FILES=[ROOT/'README.md',ROOT/'ADMIN_CHECKLIST.md',ROOT/'config/public.yml',ROOT/'config/media-manifest.yml']
patterns={
 'internal or DMZ IP': re.compile(r'(?<![\d.])(?:10\.240\.\d+\.\d+|132\.252\.143\.\d+|100\.64\.\d+\.\d+)(?![\d.])'),
 'physical infrastructure hostname': re.compile(r'(?<![A-Za-z0-9-])(?:is2-[0-9]+|is-[0-9]+|s2-[0-9]+|c[0-9]{3}|g[0-9]+-[0-9]+)(?![A-Za-z0-9-])',re.I),
 'hardware control-plane detail': re.compile(r'\b(?:PiKVM|BMC|IPMI|MAAS system.?id|power.?cycle endpoint)\b',re.I),
 'likely private key block': re.compile(r'-----BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY-----[\s\S]{40,}?-----END (?:OPENSSH|RSA|EC) PRIVATE KEY-----'),
 'likely secret assignment': re.compile(r'(?i)\b(?:password|token|secret)\s*[:=]\s*["\']?[A-Za-z0-9+/=_-]{12,}'),
 'unbounded retry example': re.compile(r'\bwhile\s+true\b|\bfor\s*\(\s*;\s*;\s*\)',re.I),
 'network scan command': re.compile(r'\b(?:nmap|masscan|zmap)\b',re.I),
}
allow_labels={'docs/security/publication-boundary.md'}
errors=[]

def scan(label,text):
 for name,pat in patterns.items():
  if label in allow_labels and name in {'hardware control-plane detail','network scan command'}: continue
  for m in pat.finditer(text): errors.append(f'{label}:{text.count(chr(10),0,m.start())+1}: {name}: {m.group(0)}')

for item in TEXT_ROOTS:
 for p in item.rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.md','.py','.sh','.ps1','.yml','.yaml','.txt','.srt','.toml'}:
   scan(str(p.relative_to(ROOT)),p.read_text(errors='replace'))
for p in TEXT_FILES:
 if p.exists(): scan(str(p.relative_to(ROOT)),p.read_text(errors='replace'))

# Extract only visible text nodes from DOCX/PPTX XML, avoiding theme/color metadata.
for p in list((ROOT/'docx').glob('*.docx'))+list((ROOT/'slides').glob('*.pptx')):
 chunks=[]
 try:
  with zipfile.ZipFile(p) as z:
   for name in z.namelist():
    if not name.endswith('.xml'): continue
    try: tree=ET.fromstring(z.read(name))
    except ET.ParseError: continue
    for node in tree.iter():
     if node.text and node.tag.rsplit('}',1)[-1] in {'t','instrText'}: chunks.append(node.text)
 except zipfile.BadZipFile:
  errors.append(f'{p.relative_to(ROOT)}: invalid Office archive')
 scan(str(p.relative_to(ROOT)),'\n'.join(chunks))

# PDF text should match the canonical source, but scan it independently when Poppler is available.
pdftotext=shutil.which('pdftotext')
if pdftotext:
 for p in (ROOT/'pdf').glob('*.pdf'):
  result=subprocess.run([pdftotext,str(p),'-'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if result.returncode: errors.append(f'{p.relative_to(ROOT)}: pdftotext failed')
  else: scan(str(p.relative_to(ROOT)),result.stdout)
else:
 print('publication lint warning: pdftotext unavailable; PDF text was not independently scanned',file=sys.stderr)

if errors:
 print('\n'.join(errors),file=sys.stderr); raise SystemExit(1)
print('publication lint: PASS')
