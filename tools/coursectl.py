#!/usr/bin/env python3
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
PATH=Path.home()/'.clusterdocs-progress.json'
def load():
    if not PATH.exists(): return {'version':1,'gates':{}}
    data=json.loads(PATH.read_text());
    if set(data)-{'version','gates'}: raise SystemExit('Unexpected progress-file fields')
    return data
def save(d):
    PATH.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n'); PATH.chmod(0o600)
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
sub.add_parser('status'); m=sub.add_parser('mark'); m.add_argument('class_number',type=int,choices=range(1,12)); m.add_argument('gate')
a=p.parse_args(); d=load()
if a.cmd=='mark':
    key=f'class-{a.class_number}:{a.gate}'
    d['gates'][key]={'completed_at':datetime.now(timezone.utc).isoformat(timespec='seconds')}; save(d); print(f'Marked {key}')
else:
    if not d['gates']: print('No gates recorded locally.')
    for k,v in sorted(d['gates'].items()): print(f"{k}\t{v['completed_at']}")
