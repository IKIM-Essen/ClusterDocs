#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, os, re, shutil
from pathlib import Path
import yaml, mistune
from jinja2 import Template
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
NAV=[
 ('Overview','Home','index.md'),
 ('Paths','Data analysis','paths/data-analysis.md'),
 ('Paths','Software development','paths/software-development.md'),
 ('Course','Course overview','course/index.md'),
 ('Course','Class 1 · Safe access','course/class-01-safe-access.md'),
 ('Course','Class 2 · Workflows','course/class-02-workflows.md'),
 ('Course','Class 3 · Performance','course/class-03-performance.md'),
 ('Course','Class 4 · Containers','course/class-04-containers.md'),
 ('Course','Class 5 · Slurm','course/class-05-slurm.md'),
 ('Course','Class 6 · Project websites','course/class-06-vhosts.md'),
 ('Course','Class 7 · Python notebooks','course/class-07-python-notebooks.md'),
 ('Course','Class 8 · R analysis','course/class-08-r-analysis.md'),
 ('Course','Class 9 · Shiny apps','course/class-09-shiny.md'),
 ('Course','Class 10 · Notebook to service','course/class-10-notebook-to-service.md'),
 ('Course','Class 11 · Data privacy','course/class-11-biomedical-data-privacy.md'),
 ('Examples','Interactive workflows','examples/interactive-workflows.md'),
 ('Examples','Python, R, Shiny and Jupyter','examples/python-r-shiny-jupyter-reference.md'),
 ('Reference','Reference overview','reference/index.md'),
 ('Reference','Account starter setups','reference/account-starter-setups.md'),
 ('Reference','Access, SSH, and VS Code','reference/access-ssh-vscode.md'),
 ('Reference','Storage and transfer','reference/storage-transfer.md'),
 ('Reference','Software workflows','reference/software-workflows.md'),
 ('Reference','Slurm commands','reference/slurm.md'),
 ('Reference','Troubleshooting','reference/troubleshooting.md'),
 ('Reference','Resources and discovery','reference/resources.md'),
 ('Reference','AI and data science','reference/ai-data-science.md'),
 ('Policies','How shared compute works','policies/slurm-resource-sharing.md'),
 ('Governance','What is changing','rollout/index.md'),
 ('Governance','Safe everyday practice','security/safe-use.md'),
 ('Governance','Biomedical data admission','security/rcc-biomedical-data-admission.md'),
 ('Resources','Who we are','team.md'),
 ('Resources','How it all works','resources/how-it-all-works.md'),
 ('Resources','Media and downloads','media/index.md'),
]
PAGE='''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="Safe, practical RCC training for biomedical researchers">
  <title>{{ title }} · RCC ClusterDocs</title>
  <link rel="stylesheet" href="{{ root }}assets/site.css">
</head>
<body class="{% if is_home %}home{% endif %}">
<a class="skip" href="#content">Skip to content</a>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{{ root }}index.html" aria-label="RCC ClusterDocs home">
      <img src="https://www.uk-essen.de/wp-content/uploads/2021/10/Logo_UME_UKE.svg" alt="Universitätsklinikum Essen">
      <span class="brand-copy"><strong>ClusterDocs</strong><span>Research Compute Cluster</span></span>
    </a>
    <nav class="service-nav" aria-label="RCC services">
      <a href="https://rcc.ikim.uk-essen.de/">About RCC</a>
      <a class="active" href="{{ root }}index.html" aria-current="page">Documentation</a>
      <a href="https://files.ikim.uk-essen.de/">File transfer</a>
      <a class="admin-link" href="https://rcc-admin.ikim.uk-essen.de/">RCC Admin</a>
    </nav>
  </div>
</header>
<div class="shell">
  <details class="mobile-nav">
    <summary>Browse documentation</summary>
    <nav aria-label="Mobile documentation navigation">
      {% for group,items in nav_groups %}
      {% if items|length == 1 %}
      <section class="nav-group-single"><a {% if items[0][1] == current_url %}aria-current="page"{% endif %} href="{{ root }}{{ items[0][1] }}">{{ items[0][0] }}</a></section>
      {% else %}
      <section><h2>{{ group }}</h2>{% for label,url in items %}<a {% if url == current_url %}aria-current="page"{% endif %} href="{{ root }}{{ url }}">{{ label }}</a>{% endfor %}</section>
      {% endif %}
      {% endfor %}
    </nav>
  </details>
  <div class="docs-layout">
    <aside class="sidebar">
      <div class="sidebar-card">
        <div class="sidebar-heading"><span class="status-dot"></span><div><strong>RCC learning path</strong><span class="stage-badge">{{ status }}</span></div></div>
        <nav aria-label="Documentation navigation">
          {% for group,items in nav_groups %}
          {% if items|length == 1 %}
          <a class="nav-single" {% if items[0][1] == current_url %}aria-current="page"{% endif %} href="{{ root }}{{ items[0][1] }}">{{ items[0][0] }}</a>
          {% else %}
          <details class="nav-section" {% if group == page_group or (is_home and group == 'Paths') %}open{% endif %}>
            <summary>{{ group }}</summary>
            <div>{% for label,url in items %}<a {% if url == current_url %}aria-current="page"{% endif %} href="{{ root }}{{ url }}">{{ label }}</a>{% endfor %}</div>
          </details>
          {% endif %}
          {% endfor %}
        </nav>
      </div>
    </aside>
    <main id="content" class="content-card">
      <p class="eyebrow">{{ page_group }} · RCC ClusterDocs</p>
      {% if is_home %}<figure class="people-figure">
        <img src="assets/cluster-barnraiser.webp" alt="RCC team members installing and checking equipment inside the cluster racks">
        <figcaption>RCC is built by scientists for other scientists. <a href="team/index.html">Meet the team.</a></figcaption>
      </figure>{% endif %}
      {{ content }}
      {% if is_home %}<figure class="research-figure">
        <img src="assets/biomedical-data-analysis-tools.webp" alt="A genome connected to Python, R, GPUs, Shiny, Jupyter notebooks, and biomedical data-science tools">
        <figcaption>One research environment for statistics, data science, reproducible AI, distributed computation, visualization, and governed sharing.</figcaption>
      </figure>{% endif %}
    </main>
  </div>
</div>
<footer>
  <p>RCC · Research Compute Cluster · University Hospital Essen</p>
  <p><a href="{{ root }}index.html">Documentation</a> · <a href="https://rcc-admin.ikim.uk-essen.de/">RCC Admin</a> · <a href="https://files.ikim.uk-essen.de/">File transfer</a></p>
</footer>
</body>
</html>'''
CSS=''':root {
  --navy:#062a46; --navy-2:#0b456e; --cyan:#0a8fb2; --cyan-light:#e9f8fb;
  --green:#2b8a65; --red:#b4233d; --amber:#a56500; --ink:#15202b;
  --muted:#5b6874; --line:#dce3e8; --paper:#fff; --background:#f3f7f9;
  --shadow:0 16px 38px rgba(6,42,70,.12);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
* { box-sizing:border-box; }
html { min-height:100%; background:var(--background); color:var(--ink); scroll-behavior:smooth; }
body { margin:0; min-height:100%; color:var(--ink); line-height:1.65; background:radial-gradient(circle at 90% 0%,rgba(10,143,178,.13),transparent 28rem),linear-gradient(180deg,#f9fcfd 0,var(--background) 36rem); }
a { color:var(--navy-2); text-decoration-thickness:1px; text-underline-offset:3px; }
a:hover { color:var(--cyan); }
.skip { position:fixed; left:-9999px; top:.75rem; z-index:100; border-radius:9px; background:var(--navy); color:#fff; padding:.65rem .9rem; }
.skip:focus { left:.75rem; }
.topbar { background:rgba(255,255,255,.94); border-bottom:1px solid rgba(6,42,70,.11); position:sticky; top:0; z-index:10; backdrop-filter:blur(14px); }
.topbar-inner { max-width:1280px; margin:0 auto; padding:.85rem 1.4rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; }
.brand { display:flex; align-items:center; gap:1rem; text-decoration:none; min-width:0; }
.brand img { width:156px; height:48px; object-fit:contain; object-position:left center; }
.brand-copy { border-left:1px solid var(--line); padding-left:1rem; line-height:1.05; }
.brand-copy strong { display:block; font-size:1.15rem; color:var(--navy); letter-spacing:.02em; }
.brand-copy span { color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.1em; }
.service-nav { display:flex; align-items:center; gap:.45rem; flex-wrap:wrap; justify-content:flex-end; }
.service-nav a { text-decoration:none; font-weight:650; font-size:.9rem; padding:.55rem .72rem; border-radius:999px; }
.service-nav a:hover,.service-nav a.active { background:var(--cyan-light); color:var(--navy-2); }
.service-nav .admin-link { background:var(--navy); color:#fff; }
.service-nav .admin-link:hover { background:var(--navy-2); color:#fff; }
.shell { max-width:1280px; margin:0 auto; padding:2rem 1.4rem 4rem; }
.docs-layout { display:grid; grid-template-columns:minmax(230px,270px) minmax(0,900px); gap:1.5rem; align-items:start; justify-content:center; }
.sidebar { position:sticky; top:94px; max-height:calc(100vh - 112px); overflow:auto; scrollbar-width:thin; }
.sidebar-card,.content-card { background:var(--paper); border:1px solid rgba(6,42,70,.1); border-radius:20px; box-shadow:0 9px 24px rgba(6,42,70,.065); }
.sidebar-card { padding:1rem; }
.sidebar-heading { display:flex; align-items:center; gap:.75rem; padding:.25rem .35rem 1rem; border-bottom:1px solid var(--line); }
.sidebar-heading strong { display:block; color:var(--navy); font-size:.94rem; }
.status-dot { width:.7rem; height:.7rem; flex:0 0 auto; background:#58d39c; border-radius:50%; box-shadow:0 0 0 .28rem rgba(88,211,156,.18); }
.stage-badge { display:inline-block; margin-top:.25rem; padding:.15rem .45rem; border-radius:999px; background:var(--cyan-light); color:var(--navy-2); font-size:.65rem; line-height:1.35; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.sidebar nav { margin-top:.55rem; }
.sidebar .nav-single { margin-bottom:.18rem; }
.sidebar .nav-section { margin:0; padding:0; border:0; border-radius:9px; background:transparent; }
.sidebar .nav-section + .nav-section { margin-top:.18rem; }
.sidebar .nav-section summary { padding:.52rem .58rem; border-radius:9px; color:var(--muted); font-size:.7rem; font-weight:850; line-height:1.2; letter-spacing:.11em; text-transform:uppercase; }
.sidebar .nav-section summary:hover { background:var(--cyan-light); color:var(--navy-2); }
.sidebar .nav-section[open] summary { color:var(--navy); }
.sidebar .nav-section > div { padding:.15rem 0 .45rem; }
.mobile-nav nav h2 { margin:.2rem .55rem .4rem; color:var(--muted); font-size:.68rem; line-height:1.2; letter-spacing:.12em; text-transform:uppercase; }
.sidebar nav a,.mobile-nav nav a { display:block; padding:.48rem .58rem; border-radius:9px; color:var(--navy-2); font-size:.86rem; line-height:1.3; text-decoration:none; }
.sidebar nav a:hover,.mobile-nav nav a:hover { background:var(--cyan-light); color:var(--cyan); }
.sidebar nav a[aria-current="page"],.mobile-nav nav a[aria-current="page"] { background:var(--navy); color:#fff; font-weight:750; box-shadow:0 5px 14px rgba(6,42,70,.16); }
.content-card { min-width:0; padding:clamp(1.4rem,4vw,3.1rem); }
.eyebrow { color:var(--cyan); text-transform:uppercase; letter-spacing:.13em; font-size:.75rem; font-weight:800; margin:0 0 .8rem; }
.content-card h1,.content-card h2,.content-card h3,.content-card h4 { color:var(--navy); line-height:1.18; }
.content-card h1 { margin:.1rem 0 1.2rem; font-size:clamp(2.25rem,5vw,4rem); line-height:1.02; letter-spacing:-.045em; }
.content-card h2 { margin:2.4rem 0 .8rem; padding-top:.35rem; font-size:clamp(1.5rem,3vw,2rem); letter-spacing:-.025em; }
.content-card h3 { margin:1.8rem 0 .6rem; font-size:1.25rem; }
.content-card > p:first-of-type:not(.eyebrow),.content-card h1 + p { color:var(--muted); font-size:1.08rem; line-height:1.72; }
.content-card p,.content-card li { max-width:76ch; }
.content-card li + li { margin-top:.34rem; }
.content-card img,.content-card video { display:block; max-width:100%; height:auto; border-radius:14px; }
.people-figure { float:right; width:min(42%,340px); margin:0 0 1.5rem 2rem; overflow:hidden; border:1px solid rgba(6,42,70,.1); border-radius:18px; background:#fff; box-shadow:var(--shadow); }
.people-figure img { width:100%; aspect-ratio:4/5; object-fit:cover; object-position:center 58%; border-radius:0; }
.people-figure figcaption,.research-figure figcaption { padding:.75rem .9rem; color:var(--muted); font-size:.8rem; line-height:1.45; }
.home .content-card h2 { clear:both; }
.research-figure { clear:both; margin:2.5rem 0 0; overflow:hidden; border:1px solid rgba(6,42,70,.1); border-radius:18px; background:#fff; box-shadow:0 9px 24px rgba(6,42,70,.065); }
.research-figure img { width:100%; border-radius:0; }
.content-card hr { border:0; border-top:1px solid var(--line); margin:2rem 0; }
.content-card a { font-weight:600; }
.path-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1.15rem 0 2.4rem; }
.path-card { position:relative; display:flex; min-height:310px; flex-direction:column; overflow:hidden; padding:1.45rem; border:1px solid rgba(6,42,70,.1); border-radius:18px; background:linear-gradient(150deg,#fff 0,#f6fbfc 100%); box-shadow:0 9px 24px rgba(6,42,70,.065); }
.path-card::after { content:""; position:absolute; width:150px; height:150px; right:-70px; bottom:-80px; border:25px solid rgba(10,143,178,.08); border-radius:50%; }
.path-card.development-path::after { border-color:rgba(6,42,70,.07); }
.path-number { align-self:flex-start; padding:.24rem .55rem; border-radius:999px; background:var(--cyan-light); color:var(--cyan); font-size:.72rem; font-weight:850; letter-spacing:.08em; }
.path-label { margin:1rem 0 .25rem; color:var(--cyan); font-size:.74rem; font-weight:850; letter-spacing:.12em; text-transform:uppercase; }
.path-card h3 { margin:.2rem 0 .65rem; font-size:1.35rem; }
.path-card p:not(.path-label) { color:var(--muted); line-height:1.55; }
.path-action { position:relative; z-index:1; margin-top:auto; align-self:flex-start; color:var(--navy); font-weight:800!important; text-decoration:none; }
.path-action:hover { color:var(--cyan); }
code { border-radius:5px; background:#eef3f6; color:#173b54; padding:.12rem .3rem; font: .9em ui-monospace,SFMono-Regular,Consolas,monospace; }
pre { margin:1.2rem 0; padding:1rem 1.15rem; overflow:auto; border:1px solid #cfdae0; border-left:4px solid var(--cyan); border-radius:0 12px 12px 0; background:#edf3f6; box-shadow:inset 0 1px 1px rgba(6,42,70,.03); }
pre code { padding:0; background:transparent; color:#15364b; }
blockquote { margin:1.4rem 0; padding:.9rem 1.1rem; border-left:4px solid var(--cyan); border-radius:0 10px 10px 0; background:var(--cyan-light); color:var(--navy); }
blockquote > :first-child { margin-top:0; } blockquote > :last-child { margin-bottom:0; }
table { display:block; width:100%; overflow-x:auto; border-collapse:collapse; font-size:.91rem; }
th,td { padding:.72rem .62rem; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }
th { color:var(--navy); background:#f7fafb; font-size:.75rem; text-transform:uppercase; letter-spacing:.06em; }
tr:hover td { background:#fbfdfe; }
details { margin:1rem 0; padding:.8rem 1rem; border:1px solid var(--line); border-radius:12px; background:#fbfdfe; }
summary { color:var(--navy); font-weight:750; cursor:pointer; }
.mobile-nav { display:none; }
footer { max-width:1280px; margin:0 auto; padding:1.4rem; border-top:1px solid rgba(6,42,70,.1); color:var(--muted); display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; font-size:.88rem; }
footer p { margin:0; }
@media (max-width:980px) {
  .docs-layout { grid-template-columns:220px minmax(0,1fr); }
  .content-card { padding:1.6rem; }
}
@media (max-width:760px) {
  .topbar-inner { align-items:flex-start; flex-direction:column; }
  .brand img { width:125px; }
  .brand-copy { display:none; }
  .service-nav { justify-content:flex-start; }
  .shell { padding:1rem; }
  .sidebar { display:none; }
  .docs-layout { display:block; }
  .mobile-nav { display:block; margin:0 0 1rem; padding:.72rem 1rem; border:1px solid rgba(6,42,70,.1); border-radius:14px; background:#fff; box-shadow:0 9px 24px rgba(6,42,70,.05); }
  .mobile-nav nav { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; padding-top:1rem; }
  .content-card h1 { font-size:clamp(2rem,11vw,3rem); }
  .people-figure { float:none; width:100%; max-width:430px; margin:0 auto 1.5rem; }
  .people-figure img { aspect-ratio:5/4; object-position:center 57%; }
  .path-grid { grid-template-columns:1fr; }
  .path-card { min-height:260px; }
}
@media (max-width:480px) {
  .service-nav a { padding:.45rem .55rem; font-size:.82rem; }
  .mobile-nav nav { grid-template-columns:1fr; }
  .content-card { padding:1.25rem; border-radius:16px; }
}
@media print {
  .topbar,.sidebar,.mobile-nav,footer,.skip { display:none!important; }
  body { background:#fff; }
  .shell { max-width:none; padding:0; }
  .docs-layout { display:block; }
  .content-card { border:0; box-shadow:none; padding:0; }
}'''

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
    if (DOCS/'assets').exists(): shutil.copytree(DOCS/'assets',out/'assets',dirs_exist_ok=True)
    md=mistune.create_markdown(escape=False, plugins=['table','strikethrough','task_lists'])
    nav_groups=[]
    for group,label,path in NAV:
        if not nav_groups or nav_groups[-1][0] != group:
            nav_groups.append((group,[]))
        nav_groups[-1][1].append((label,out_url(path)))
    group_for_path={path:group for group,_,path in NAV}
    for src in sorted(DOCS.rglob('*.md')):
        rel=src.relative_to(DOCS); target=out/out_url(str(rel)); target.parent.mkdir(parents=True,exist_ok=True)
        text=substitute(src.read_text(),cfg); content=md(text)
        def rewrite_local(match):
            attribute=match.group(1); value=match.group(2)
            path,separator,fragment=value.partition('#')
            resolved=(rel.parent/path).as_posix()
            # Rewrite local documentation pages and assets from the generated
            # page's depth. Downloadable files outside docs retain literal paths.
            if not (DOCS/resolved).is_file():
                return match.group(0)
            built=out/out_url(resolved) if attribute == 'href' and resolved.endswith('.md') else out/resolved
            rewritten=Path(os.path.relpath(built,target.parent)).as_posix()
            if separator: rewritten+=separator+fragment
            return attribute+'="'+rewritten+'"'
        content=re.sub(r'(href|src)="([^"]+)"', rewrite_local, content)
        current_url=out_url(str(rel))
        target.write_text(Template(PAGE).render(
            title=title_of(text),
            content=content,
            nav_groups=nav_groups,
            root=relroot(target.relative_to(out)),
            status=cfg['site_status'],
            current_url=current_url,
            page_group=group_for_path.get(str(rel),'Documentation'),
            is_home=str(rel)=='index.md',
        ))
    # Copy learner exercises and reviewable text assets, never credentials.
    shutil.copytree(ROOT/'exercises',out/'downloads/exercises')
    if (ROOT/'examples').exists():
        shutil.copytree(ROOT/'examples',out/'downloads/examples')
        if (ROOT/'examples/account-setup').exists():
            shutil.make_archive(
                str(out/'downloads/rcc-account-setup'),
                'zip',
                root_dir=ROOT/'examples',
                base_dir='account-setup',
            )
    for name in ['captions','narration','pdf','slides']:
        if (ROOT/name).exists(): shutil.copytree(ROOT/name,out/'downloads'/name)
    if a.include_media and (ROOT/'videos-enhanced').exists():
        shutil.copytree(ROOT/'videos-enhanced',out/'media',dirs_exist_ok=True)
    print(out)
if __name__=='__main__': main()
