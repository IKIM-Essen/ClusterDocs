#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, os, re, shutil
from pathlib import Path
import yaml, mistune
from jinja2 import Template
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
NAV=[
 ('Home','index.md'),
 ('Course','course/index.md'),
 ('Class 1','course/class-01-safe-access.md'),
 ('Class 2','course/class-02-workflows.md'),
 ('Class 3','course/class-03-performance.md'),
 ('Class 4','course/class-04-containers.md'),
 ('Class 5','course/class-05-slurm.md'),
 ('Class 6','course/class-06-vhosts.md'),
 ('Class 7','course/class-07-python-notebooks.md'),
 ('Class 8','course/class-08-r-analysis.md'),
 ('Class 9','course/class-09-shiny.md'),
 ('Class 10','course/class-10-notebook-to-service.md'),
 ('Class 11','course/class-11-biomedical-data-privacy.md'),
 ('Interactive examples','examples/interactive-workflows.md'),
 ('Rollout','rollout/index.md'),
 ('Messages','rollout/messages.md'),
 ('Safe use','security/safe-use.md'),
 ('Data privacy','security/rcc-biomedical-data-admission.md'),
 ('Media','media/index.md'),
 ('Operator checklist','instructors/operator-checklist.md'),
 ('Repository strategy','instructors/repository-strategy.md'),
]
PAGE='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{ title }} · RCC ClusterDocs</title><link rel="stylesheet" href="{{ root }}assets/site.css"></head><body><a class="skip" href="#content">Skip to content</a><header><strong>RCC ClusterDocs NG</strong><span class="status">{{ status }}</span></header><div class="layout"><nav aria-label="Course navigation">{% for label,url in nav %}<a href="{{ root }}{{ url }}">{{ label }}</a>{% endfor %}</nav><main id="content">{{ content }}</main></div><footer>Staged user documentation. Do not publish unresolved placeholders.</footer></body></html>'''
CSS='''body{font-family:system-ui,-apple-system,Segoe UI,sans-serif;margin:0;color:#18232d;background:#fff;line-height:1.55}header{padding:1rem 1.5rem;background:#16324f;color:#fff;display:flex;gap:1rem;align-items:center}.status{font-size:.8rem;background:#fff;color:#16324f;padding:.15rem .5rem;border-radius:1rem}.layout{display:grid;grid-template-columns:15rem minmax(0,52rem);gap:2rem;max-width:76rem;margin:auto;padding:1.5rem}nav{display:flex;flex-direction:column;gap:.35rem}nav a{padding:.35rem .5rem;text-decoration:none;color:#164c73}main img,main video{max-width:100%}code{background:#eef3f6;padding:.1rem .25rem}pre{background:#eef3f6;padding:1rem;overflow:auto;border-left:4px solid #24737a}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ccd5dc;padding:.45rem;text-align:left}details{border:1px solid #ccd5dc;padding:.6rem;margin:.7rem 0}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:white;padding:.5rem}footer{padding:1rem;text-align:center;border-top:1px solid #ddd}@media(max-width:760px){.layout{grid-template-columns:1fr}nav{display:grid;grid-template-columns:repeat(2,1fr)}}'''

def substitute(text,cfg):
    for k,v in cfg.items():
        if isinstance(v,(str,int,float)): text=text.replace('{{ '+k+' }}',str(v))
    return text

def title_of(text):
    m=re.search(r'^#\s+(.+)$',text,re.M); return m.group(1) if m else 'RCC ClusterDocs'

def out_url(md):
    p=Path(md)
    if p.name=='index.md':
        return str(p.parent/'index.html') if str(p.parent)!='.' else 'index.html'
    return str(p.with_suffix('')/'index.html')

def relroot(out):
    depth=len(Path(out).parts)-1
    return '../'*depth

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='site'); ap.add_argument('--production',action='store_true'); ap.add_argument('--include-media',action='store_true'); a=ap.parse_args()
    cfg=yaml.safe_load((ROOT/'config/public.yml').read_text())
    if a.include_media:
        cfg=dict(cfg); cfg['media_base_url']='.'
    if a.production:
        bad=[k for k,v in cfg.items() if isinstance(v,str) and ('TO_BE_' in v or '.invalid' in v or 'STAGING-' in v or 'CLUSTERDOCS-' in v or 'TRANSFER-' in v)]
        if bad: raise SystemExit('Production build blocked by unresolved config: '+', '.join(bad))
    out=(ROOT/a.output).resolve() if not Path(a.output).is_absolute() else Path(a.output)
    shutil.rmtree(out,ignore_errors=True); (out/'assets').mkdir(parents=True)
    (out/'assets/site.css').write_text(CSS)
    md=mistune.create_markdown(escape=False, plugins=['table','strikethrough','task_lists'])
    nav=[(label,out_url(path)) for label,path in NAV]
    for src in sorted(DOCS.rglob('*.md')):
        rel=src.relative_to(DOCS); target=out/out_url(str(rel)); target.parent.mkdir(parents=True,exist_ok=True)
        text=substitute(src.read_text(),cfg); content=md(text)
        def rewrite(match):
            href=match.group(1); anchor=match.group(2) or ''
            resolved=(rel.parent/href).as_posix()
            # Rewrite links only when they refer to another source page under docs/.
            # Downloadable Markdown assets copied into site/downloads must retain
            # their literal .md path.
            if not (DOCS/resolved).is_file():
                return match.group(0)
            built=out/out_url(resolved)
            return 'href="'+Path(os.path.relpath(built,target.parent)).as_posix()+anchor+'"'
        content=re.sub(r'href="([^"#:]+\.md)(#[^"]*)?"', rewrite, content)
        target.write_text(Template(PAGE).render(title=title_of(text),content=content,nav=nav,root=relroot(target.relative_to(out)),status=cfg['site_status']))
    # Copy learner exercises and reviewable text assets, never credentials.
    shutil.copytree(ROOT/'exercises',out/'downloads/exercises')
    if (ROOT/'examples').exists(): shutil.copytree(ROOT/'examples',out/'downloads/examples')
    for name in ['captions','narration','pdf','slides']:
        if (ROOT/name).exists(): shutil.copytree(ROOT/name,out/'downloads'/name)
    if a.include_media and (ROOT/'videos-enhanced').exists():
        shutil.copytree(ROOT/'videos-enhanced',out/'media',dirs_exist_ok=True)
    print(out)
if __name__=='__main__': main()
