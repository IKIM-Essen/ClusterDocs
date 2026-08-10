#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys
ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'site').resolve()
class P(HTMLParser):
 def __init__(self): super().__init__(); self.refs=[]; self.ids=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if d.get('id'): self.ids.append(d['id'])
  for k in ('href','src'):
   if k in d: self.refs.append(d[k])
errors=[]
pages={}
for page in ROOT.rglob('*.html'):
 p=P(); p.feed(page.read_text(errors='replace')); pages[page.resolve()]=p
 duplicates=sorted({value for value in p.ids if p.ids.count(value)>1})
 if duplicates: errors.append(f'{page.relative_to(ROOT)}: duplicate ids: {", ".join(duplicates)}')
for page,p in pages.items():
 for ref in p.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc or ref.startswith('mailto:'): continue
  path=unquote(u.path)
  target=(page.parent/path).resolve() if path else page
  try: target.relative_to(ROOT)
  except ValueError: errors.append(f'{page.relative_to(ROOT)}: path escapes site: {ref}'); continue
  if target.is_dir(): target=(target/'index.html').resolve()
  if not target.exists(): errors.append(f'{page.relative_to(ROOT)}: missing {ref}'); continue
  if u.fragment and target.suffix == '.html':
   target_page=pages.get(target)
   fragment=unquote(u.fragment)
   if target_page is None or fragment not in target_page.ids:
    errors.append(f'{page.relative_to(ROOT)}: missing fragment {ref}')
if errors:
 print('\n'.join(errors),file=sys.stderr); raise SystemExit(1)
print('site links: PASS')
