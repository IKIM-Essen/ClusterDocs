#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'site').resolve()
class P(HTMLParser):
 def __init__(self): super().__init__(); self.refs=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  for k in ('href','src'):
   if k in d: self.refs.append(d[k])
errors=[]
for page in ROOT.rglob('*.html'):
 p=P(); p.feed(page.read_text(errors='replace'))
 for ref in p.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc or ref.startswith(('#','mailto:')): continue
  path=unquote(u.path)
  if not path: continue
  target=(page.parent/path).resolve()
  try: target.relative_to(ROOT)
  except ValueError: errors.append(f'{page.relative_to(ROOT)}: path escapes site: {ref}'); continue
  if not target.exists(): errors.append(f'{page.relative_to(ROOT)}: missing {ref}')
if errors:
 print('\n'.join(errors),file=sys.stderr); raise SystemExit(1)
print('site links: PASS')
