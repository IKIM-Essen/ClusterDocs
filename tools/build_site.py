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
 ('Start here','Expedition Light · first 15 minutes','getting-started/index.md'),
 ('Start here','macOS setup','getting-started/macos.md'),
 ('Start here','Windows 11 setup','getting-started/windows.md'),
 ('Start here','VS Code with RCC','getting-started/vscode.md'),
 ('Start here','Jump host, shell host, and workers','concepts/jump-shell-compute.md'),
 ('Start here','What changed from the old cluster','getting-started/what-changed.md'),
 ('Overview','ClusterDocs NG TL;DR','tldr.md'),
 ('Overview','Coding agents and your data','concepts/how-rcc-works.md'),
 ('Paths','Data analysis','paths/data-analysis.md'),
 ('Paths','Software development','paths/software-development.md'),
 ('Paths','Convert shell scripts into workflows','paths/from-shell-scripts.md'),
 ('Course','Course overview','course/index.md'),
 ('Course','Class 1 · Safe access','course/class-01-safe-access.md'),
 ('Course','Class 2 · Workflows','course/class-02-workflows.md'),
 ('Course','Class 3 · Performance','course/class-03-performance.md'),
 ('Course','Class 4 · Containers','course/class-04-containers.md'),
 ('Course','Class 5 · Slurm','course/class-05-slurm.md'),
 ('Course','Class 6 · Snakemake','course/class-06-snakemake.md'),
 ('Course','Class 7 · Nextflow','course/class-07-nextflow.md'),
 ('Course','Class 8 · Project websites','course/class-08-vhosts.md'),
 ('Course','Class 9 · Python notebooks','course/class-09-python-notebooks.md'),
 ('Course','Class 10 · R analysis','course/class-10-r-analysis.md'),
 ('Course','Class 11 · Shiny apps','course/class-11-shiny.md'),
 ('Course','Class 12 · Notebook to service','course/class-12-notebook-to-service.md'),
 ('Course','Class 13 · Data privacy','course/class-13-biomedical-data-privacy.md'),
 ('Course','Class 14 · Efficient local I/O','course/class-14-efficient-io.md'),
 ('Course','Class 15 · Storage architecture','course/class-15-storage-architecture.md'),
 ('Course','Class 16 · Wet-lab instrument data','course/class-16-wet-lab-data-workflows.md'),
 ('Course','Class 17 · Research data lifecycle','course/class-17-data-lifecycle.md'),
 ('Course','Class 18 · Coding agents without sharing real data','course/class-18-coding-agents.md'),
 ('Data lifecycle','TL;DR · Instrument to Coscine','data/data-lifecycle-tldr.md'),
 ('Data lifecycle','Choosing a transfer path','data/instrument-data-options.md'),
 ('Data lifecycle','Existing Windows SSHFS setup','data/legacy-storage-windows.md'),
 ('Data lifecycle','Existing macOS SSHFS setup','data/legacy-storage-macos.md'),
 ('Data lifecycle','Planned RCC to Coscine archive flow','data/rcc-project-to-coscine.md'),
 ('Examples','Interactive workflows','examples/interactive-workflows.md'),
 ('Examples','Python, R, Shiny and Jupyter','examples/python-r-shiny-jupyter-reference.md'),
 ('Reference','Reference overview','reference/index.md'),
 ('Reference','RCC terminology','reference/terminology.md'),
 ('Reference','Users, groups, and projects','reference/users-groups-projects.md'),
 ('Reference','Account starter setups','reference/account-starter-setups.md'),
 ('Reference','Access, SSH, and VS Code','reference/access-ssh-vscode.md'),
 ('Reference','Storage and transfer','reference/storage-transfer.md'),
 ('Reference','Sharing data','reference/data-sharing.md'),
 ('Reference','Software workflows','reference/software-workflows.md'),
 ('Reference','Slurm commands','reference/slurm.md'),
 ('Reference','How shared compute works','reference/how-shared-compute-works.md'),
 ('Reference','Opportunistic capacity','reference/opportunistic-capacity.md'),
 ('Reference','Troubleshooting','reference/troubleshooting.md'),
 ('Reference','Resources and discovery','reference/resources.md'),
 ('Reference','AI and data science','reference/ai-data-science.md'),
 ('Reference','RCC connection name','connecting/stable-endpoints.md'),
 ('Reference','Safe everyday practice','security/safe-use.md'),
 ('Reference','Biomedical data admission','security/rcc-biomedical-data-admission.md'),
 ('Resources','Who we are','team.md'),
 ('Resources','Lab network properties and remote access','resources/how-it-all-works.md'),
 ('Resources','PiKVM through RCC Headscale · Not yet released','connecting/pikvm-headscale.md'),
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
    <a class="brand" href="https://rcc.ikim.uk-essen.de/" aria-label="RCC home">
      <img src="https://www.uk-essen.de/wp-content/uploads/2021/10/Logo_UME_UKE.svg" alt="Universitätsklinikum Essen">
      <span class="brand-copy"><strong>RCC</strong><span>Research Compute Cluster</span></span>
    </a>
    <div class="topbar-actions">
      <span class="service-status"><span class="service-status-dot"></span>Documentation online</span>
      <a class="topbar-button" href="https://rcc-admin.ikim.uk-essen.de/" target="_blank" rel="noopener" aria-label="Open My RCC (opens in a new tab)">My RCC <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</header>
<div class="shell">
  <details class="mobile-nav">
    <summary>Browse documentation</summary>
    <nav aria-label="Mobile documentation navigation">
      <section><h2>RCC surfaces</h2>
        <a href="https://rcc.ikim.uk-essen.de/">Home</a>
        <a href="https://files.ikim.uk-essen.de/" target="_blank" rel="noopener">Files ↗</a>
        <a aria-current="page" href="{{ root }}index.html">Documentation</a>
        <a href="https://rcc-admin.ikim.uk-essen.de/" target="_blank" rel="noopener">RCC Admin ↗</a>
      </section>
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
        <section class="sidebar-section">
          <p class="sidebar-kicker">RCC surfaces</p>
          <nav class="global-nav" aria-label="RCC services">
            <a href="https://rcc.ikim.uk-essen.de/">Home</a>
            <a href="https://files.ikim.uk-essen.de/" target="_blank" rel="noopener" aria-label="Files (opens in a new tab)">Files <span aria-hidden="true">↗</span></a>
            <a class="current" aria-current="page" href="{{ root }}index.html">Documentation</a>
            <a href="https://rcc-admin.ikim.uk-essen.de/" target="_blank" rel="noopener" aria-label="RCC Admin (opens in a new tab)">RCC Admin <span aria-hidden="true">↗</span></a>
          </nav>
        </section>
        <section class="sidebar-section documentation-tree">
          <div class="sidebar-heading"><span class="status-dot"></span><div><strong>ClusterDocs</strong><span class="stage-badge">{{ status }}</span></div></div>
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
        </section>
        <div class="sidebar-note"><strong>Compute · Data · Projects</strong><span>Practical guidance for working safely and reproducibly on RCC.</span></div>
      </div>
    </aside>
    <main id="content" class="content-card">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>
        <li><a href="https://rcc.ikim.uk-essen.de/">Home</a></li>
        {% if is_home %}<li><span aria-current="page">Documentation</span></li>
        {% else %}<li><a href="{{ root }}index.html">Documentation</a></li><li><span aria-current="page">{{ title }}</span></li>{% endif %}
      </ol></nav>
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
    {% if is_home and home_rail %}<aside class="home-rail" aria-label="RCC Expedition onboarding">
      {{ home_rail }}
    </aside>{% endif %}
  </div>
</div>
<footer>
  <p>RCC · Research Compute Cluster · University Hospital Essen</p>
  <p><a href="{{ root }}index.html">Documentation</a> · <a href="https://rcc-admin.ikim.uk-essen.de/">RCC Admin</a> · <a href="https://files.ikim.uk-essen.de/">File transfer</a></p>
</footer>
</body>
</html>'''
CSS=''':root {
  --navy:#062a46; --navy-2:#0b456e; --cyan:#0a8fb2; --cyan-strong:#0a7a96; --cyan-light:#e9f8fb;
  --green:#2b8a65; --red:#b4233d; --amber:#a56500; --ink:#15202b;
  --muted:#5b6874; --line:#dce3e8; --paper:#fff; --background:#f3f7f9;
  --shadow:0 16px 38px rgba(6,42,70,.12); --shadow-sm:0 9px 24px rgba(6,42,70,.065);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
* { box-sizing:border-box; }
html { min-height:100%; background:var(--background); color:var(--ink); scroll-behavior:smooth; }
body { margin:0; min-height:100%; color:var(--ink); line-height:1.65; background:linear-gradient(180deg,#f9fcfd 0,var(--background) 42rem); }
a { color:var(--navy-2); text-decoration-thickness:1px; text-underline-offset:3px; }
a:hover { color:var(--cyan-strong); }
.skip { position:fixed; left:-9999px; top:.75rem; z-index:100; border-radius:9px; background:var(--navy); color:#fff; padding:.65rem .9rem; }
.skip:focus { left:.75rem; }
.topbar { background:var(--navy); border-bottom:1px solid rgba(255,255,255,.1); color:var(--paper); position:sticky; top:0; z-index:20; }
.topbar-inner { max-width:1760px; margin:0 auto; padding:.8rem 1.5rem; display:flex; align-items:center; justify-content:space-between; gap:1.25rem; }
.brand { display:flex; align-items:center; gap:1rem; text-decoration:none; min-width:0; }
.brand img { width:156px; height:48px; object-fit:contain; object-position:left center; padding:.3rem .45rem; border-radius:8px; background:var(--paper); }
.brand-copy { border-left:1px solid rgba(255,255,255,.25); padding-left:1rem; line-height:1.05; }
.brand-copy strong { display:block; font-size:1.15rem; color:var(--paper); letter-spacing:.02em; }
.brand-copy span { color:rgba(255,255,255,.72); font-size:.72rem; text-transform:uppercase; letter-spacing:.11em; }
.topbar-actions { display:flex; align-items:center; gap:.8rem; }
.service-status { color:rgba(255,255,255,.78); font-size:.82rem; font-weight:700; }
.service-status-dot { display:inline-block; width:.55rem; height:.55rem; margin-right:.45rem; border-radius:50%; background:#58d39c; box-shadow:0 0 0 .22rem rgba(88,211,156,.18); }
.topbar-button { padding:.62rem .85rem; border-radius:11px; background:var(--paper); color:var(--navy); font-size:.9rem; font-weight:700; text-decoration:none; }
.topbar-button:hover { background:var(--cyan-light); color:var(--navy); }
.shell { max-width:1760px; margin:0 auto; padding:0 1.5rem 4rem 0; }
.docs-layout { display:grid; grid-template-columns:minmax(230px,270px) minmax(0,1000px); gap:1.8rem; align-items:start; justify-content:center; }
.home .docs-layout { grid-template-columns:minmax(230px,270px) minmax(0,780px) minmax(280px,340px); }
.home-rail { position:sticky; top:96px; min-width:0; margin-top:1.8rem; }
.sidebar { position:sticky; top:74px; height:calc(100vh - 74px); overflow:auto; scrollbar-width:thin; }
.sidebar-card { min-height:100%; padding:1.35rem 1rem; background:linear-gradient(180deg,var(--navy) 0,#07345f 72%,#052845 100%); color:var(--paper); }
.content-card { min-width:0; margin-top:1.8rem; background:var(--paper); border:1px solid rgba(6,42,70,.1); border-radius:20px; box-shadow:var(--shadow-sm); }
.sidebar-section + .sidebar-section { margin-top:1.35rem; }
.sidebar-kicker { margin:0 0 .55rem; padding:0 .7rem; color:rgba(255,255,255,.58); font-size:.68rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.sidebar-heading { display:flex; align-items:center; gap:.75rem; padding:.25rem .7rem .85rem; border-bottom:1px solid rgba(255,255,255,.14); }
.sidebar-heading strong { display:block; color:var(--paper); font-size:.94rem; }
.status-dot { width:.7rem; height:.7rem; flex:0 0 auto; background:#58d39c; border-radius:50%; box-shadow:0 0 0 .28rem rgba(88,211,156,.18); }
.stage-badge { display:inline-block; margin-top:.25rem; padding:.15rem .45rem; border-radius:999px; background:rgba(255,255,255,.12); color:rgba(255,255,255,.78); font-size:.65rem; line-height:1.35; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.sidebar nav { margin-top:.55rem; }
.sidebar .nav-single { margin-bottom:.18rem; }
.sidebar .nav-section { margin:0; padding:0; border:0; border-radius:9px; background:transparent; }
.sidebar .nav-section + .nav-section { margin-top:.18rem; }
.sidebar .nav-section summary { padding:.52rem .58rem; border-radius:9px; color:rgba(255,255,255,.58); font-size:.7rem; font-weight:800; line-height:1.2; letter-spacing:.11em; text-transform:uppercase; }
.sidebar .nav-section summary:hover { background:rgba(255,255,255,.08); color:var(--paper); }
.sidebar .nav-section[open] summary { color:var(--paper); }
.sidebar .nav-section > div { padding:.15rem 0 .45rem; }
.mobile-nav nav h2 { margin:.2rem .55rem .4rem; color:var(--muted); font-size:.68rem; line-height:1.2; letter-spacing:.12em; text-transform:uppercase; }
.sidebar nav a { display:flex; align-items:center; justify-content:space-between; gap:.65rem; padding:.58rem .68rem; border-radius:10px; color:rgba(255,255,255,.9); font-size:.84rem; line-height:1.25; text-decoration:none; }
.sidebar nav a:hover { background:rgba(255,255,255,.08); color:var(--paper); }
.sidebar nav a[aria-current="page"] { background:linear-gradient(90deg,#1262b0,#0b5a9f); color:var(--paper); font-weight:700; box-shadow:inset 3px 0 0 #3ab0ff; }
.sidebar-note { margin-top:1.5rem; padding:1rem; border:1px solid rgba(255,255,255,.14); border-radius:12px; background:rgba(255,255,255,.05); }
.sidebar-note strong,.sidebar-note span { display:block; }
.sidebar-note strong { font-size:.84rem; }
.sidebar-note span { margin-top:.4rem; color:rgba(255,255,255,.7); font-size:.76rem; line-height:1.45; }
.mobile-nav nav a { display:block; padding:.48rem .58rem; border-radius:9px; color:var(--navy-2); font-size:.86rem; line-height:1.3; text-decoration:none; }
.mobile-nav nav a:hover { background:var(--cyan-light); color:var(--cyan-strong); }
.mobile-nav nav a[aria-current="page"] { background:var(--navy); color:var(--paper); font-weight:700; }
.content-card { min-width:0; padding:clamp(1.4rem,4vw,3.1rem); }
.breadcrumbs { margin:0 0 1.4rem; }
.breadcrumbs ol { display:flex; flex-wrap:wrap; gap:.35rem; margin:0; padding:0; list-style:none; color:var(--muted); font-size:.8rem; }
.breadcrumbs li + li::before { content:"/"; margin-right:.35rem; color:#93a9b8; }
.breadcrumbs a { color:var(--muted); font-weight:600; text-decoration:none; }
.breadcrumbs a:hover { color:var(--cyan-strong); }
.eyebrow { color:var(--cyan); text-transform:uppercase; letter-spacing:.13em; font-size:.75rem; font-weight:800; margin:0 0 .8rem; }
.content-card h1,.content-card h2,.content-card h3,.content-card h4 { color:var(--navy); line-height:1.18; }
.content-card h1 { margin:.1rem 0 1.2rem; font-size:1.75rem; line-height:1.15; letter-spacing:-.02em; }
.home .content-card h1 { font-size:clamp(2.5rem,5.6vw,4.5rem); line-height:.98; letter-spacing:-.045em; }
.content-card h2 { margin:2.4rem 0 .8rem; padding-top:.35rem; font-size:clamp(1.5rem,3vw,2rem); letter-spacing:-.025em; }
.content-card h3 { margin:1.8rem 0 .6rem; font-size:1.25rem; }
.content-card > p:first-of-type:not(.eyebrow),.content-card h1 + p { color:var(--muted); font-size:1.08rem; line-height:1.72; }
.content-card p,.content-card li { max-width:76ch; }
.content-card li + li { margin-top:.34rem; }
.content-card img,.content-card video { display:block; max-width:100%; height:auto; border-radius:14px; }
.course-video-hero { margin:1.25rem 0 3rem; padding:clamp(1.15rem,3vw,2rem); overflow:hidden; border-radius:20px; background:linear-gradient(145deg,var(--navy) 0,var(--navy-2) 72%,#096d86 100%); color:#fff; box-shadow:var(--shadow); }
.content-card .course-video-hero h2 { margin:.15rem 0 .45rem; padding:0; color:#fff; font-size:clamp(1.7rem,4vw,2.5rem); }
.content-card .course-video-hero > p { max-width:68ch; margin:.35rem 0 1.25rem; color:rgba(255,255,255,.88); font-size:1rem; line-height:1.55; }
.content-card .course-video-hero .course-video-kicker { margin:0; color:#8ee7f2; font-size:.76rem; font-weight:850; letter-spacing:.11em; text-transform:uppercase; }
.content-card .course-video-hero video { width:100%; aspect-ratio:16/9; border:1px solid rgba(255,255,255,.28); border-radius:14px; background:#02131f; box-shadow:0 18px 38px rgba(0,0,0,.28); }
.course-video-pending { margin-top:1.25rem; padding:1.1rem 1.2rem; border:1px solid rgba(255,255,255,.32); border-radius:14px; background:rgba(2,19,31,.58); }
.course-video-pending strong { display:block; margin-bottom:.35rem; color:#8ee7f2; font-size:1.08rem; }
.content-card .course-video-hero .course-video-pending p { margin:0; color:#fff; }
.video-course-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1rem 0 2.5rem; }
.content-card .video-course-card { overflow:hidden; border:1px solid rgba(6,42,70,.12); border-radius:16px; background:#fff; color:var(--navy); box-shadow:0 8px 20px rgba(6,42,70,.08); text-decoration:none; transition:transform .16s ease,box-shadow .16s ease; }
.content-card .video-course-card:hover { transform:translateY(-2px); box-shadow:0 14px 30px rgba(6,42,70,.14); }
.content-card .video-course-card img { width:100%; aspect-ratio:16/9; object-fit:cover; border-radius:0; }
.video-course-card span { display:flex; align-items:center; justify-content:space-between; gap:.75rem; padding:.8rem .9rem; }
.video-course-card small { flex:0 0 auto; color:var(--cyan); font-weight:800; }
.people-figure { float:right; width:min(42%,340px); margin:0 0 1.5rem 2rem; overflow:hidden; border:1px solid rgba(6,42,70,.1); border-radius:18px; background:#fff; box-shadow:var(--shadow); }
.people-figure img { width:100%; aspect-ratio:4/5; object-fit:cover; object-position:center 58%; border-radius:0; }
.people-figure figcaption,.research-figure figcaption { padding:.75rem .9rem; color:var(--muted); font-size:.8rem; line-height:1.45; }
.home .content-card h2 { clear:both; }
.research-figure { clear:both; margin:2.5rem 0 0; overflow:hidden; border:1px solid rgba(6,42,70,.1); border-radius:18px; background:#fff; box-shadow:0 9px 24px rgba(6,42,70,.065); }
.research-figure img { width:100%; border-radius:0; }
.content-card hr { border:0; border-top:1px solid var(--line); margin:2rem 0; }
.content-card a { font-weight:600; }
.expedition-callout { position:relative; overflow:hidden; margin:1.6rem 0 2.5rem; padding:clamp(1.35rem,3vw,2rem); border-radius:20px; background:linear-gradient(140deg,var(--navy) 0,var(--navy-2) 70%,#096d86 100%); color:#fff; box-shadow:var(--shadow); }
.home-rail .expedition-callout { margin:0; padding:1.5rem; }
.expedition-callout::after { content:""; position:absolute; width:210px; height:210px; right:-95px; bottom:-120px; border:32px solid rgba(142,231,242,.13); border-radius:50%; }
.expedition-callout h2 { position:relative; z-index:1; margin:.25rem 0 .65rem; padding:0; color:#fff; font-size:clamp(1.55rem,2.3vw,2.25rem); line-height:1.08; }
.expedition-callout > p { position:relative; z-index:1; max-width:68ch; color:rgba(255,255,255,.9); line-height:1.6; }
.expedition-callout .expedition-kicker { margin:0; color:#8ee7f2; font-size:.76rem; font-weight:850; letter-spacing:.11em; text-transform:uppercase; }
.expedition-actions { position:relative; z-index:1; display:flex; align-items:center; flex-wrap:wrap; gap:.75rem 1rem; margin:1.2rem 0; }
.expedition-actions a { color:#fff; font-weight:800; }
.expedition-actions .expedition-primary { padding:.68rem .9rem; border-radius:10px; background:#fff; color:var(--navy); text-decoration:none; }
.expedition-actions .expedition-primary:hover { background:#dff7fa; color:var(--navy); }
.expedition-callout .expedition-privacy { margin-bottom:0; color:rgba(255,255,255,.76); font-size:.88rem; }
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
footer { max-width:1480px; margin:0 auto; padding:1.4rem 1.8rem; border-top:1px solid rgba(6,42,70,.1); color:var(--muted); display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; font-size:.86rem; }
footer p { margin:0; }
@media (max-width:1180px) {
  .home .docs-layout { grid-template-columns:220px minmax(0,1fr); }
  .home-rail { grid-column:2; position:static; }
}
@media (max-width:980px) {
  .docs-layout { grid-template-columns:220px minmax(0,1fr); }
  .content-card { padding:1.6rem; }
}
@media (max-width:760px) {
  .topbar-inner { align-items:flex-start; flex-direction:column; }
  .brand img { width:125px; }
  .brand-copy { display:none; }
  .service-status { display:none; }
  .shell { padding:1rem; }
  .sidebar { display:none; }
  .docs-layout { display:block; }
  .home-rail { margin-top:1rem; }
  .mobile-nav { display:block; margin:0 0 1rem; padding:.72rem 1rem; border:1px solid rgba(6,42,70,.1); border-radius:14px; background:#fff; box-shadow:0 9px 24px rgba(6,42,70,.05); }
  .mobile-nav nav { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; padding-top:1rem; }
  .content-card h1 { font-size:1.75rem; }
  .home .content-card h1 { font-size:clamp(2.4rem,11vw,3.4rem); }
  .people-figure { float:none; width:100%; max-width:430px; margin:0 auto 1.5rem; }
  .people-figure img { aspect-ratio:5/4; object-position:center 57%; }
  .path-grid { grid-template-columns:1fr; }
  .video-course-grid { grid-template-columns:1fr; }
  .path-card { min-height:260px; }
}
@media (max-width:480px) {
  .topbar-actions { width:100%; }
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

def gate_unreleased_videos(text,publication):
    """Do not turn a prepared-but-unpublished media destination into dead links."""
    if (publication.get('status') == 'verified_live'
            and publication.get('preview_links') == 'enabled'):
        return text
    notice='''<div class="course-video-pending" role="status">
    <strong>Video not yet released</strong>
    <p>The videos are waiting for publication on the RCC documentation website. This preview deliberately does not link to a local copy or another host. The complete written lesson is available below.</p>
  </div>'''
    return re.sub(r'<video\b[^>]*>.*?</video>',notice,text,flags=re.S)

def title_of(text):
    m=re.search(r'^#\s+(.+)$',text,re.M); return m.group(1) if m else 'RCC ClusterDocs'

def add_heading_ids(content):
    """Give rendered Markdown headings stable, unique fragment targets."""
    used=set(re.findall(r'\bid="([^"]+)"',content))
    def replace(match):
        level,body=match.groups()
        plain=html.unescape(re.sub(r'<[^>]+>','',body)).lower()
        base=re.sub(r'[^a-z0-9]+','-',plain).strip('-') or 'section'
        slug=base
        suffix=2
        while slug in used:
            slug=f'{base}-{suffix}'
            suffix+=1
        used.add(slug)
        return f'<h{level} id="{slug}">{body}</h{level}>'
    return re.sub(r'<h([1-6])>(.*?)</h\1>',replace,content,flags=re.S)

def out_url(md):
    p=Path(md)
    if p.name=='index.md':
        return str(p.parent/'index.html') if str(p.parent)!='.' else 'index.html'
    return str(p.with_suffix('')/'index.html')

def relroot(out):
    depth=len(Path(out).parts)-1
    return '../'*depth

def srt_to_vtt(text):
    """Convert committed SRT captions to browser-native WebVTT."""
    text=normalize_caption_text(text)
    timestamps=re.sub(
        r'(?m)(\d{2}:\d{2}:\d{2}),(\d{3})',
        r'\1.\2',
        text,
    )
    return 'WEBVTT\n\n'+timestamps.lstrip()

def normalize_caption_text(text):
    """Turn speech-oriented spellings into readable technical captions."""
    replacements=(
        (r'\bS S H\b', 'SSH'),
        (r'\bS I F\b', 'SIF'),
        (r'\bN V\b', '--nv'),
        (r'\bN v i d i a s m i\b', 'nvidia-smi'),
        (r'\binput-output\b', 'I/O'),
        (r'\bInput-output\b', 'I/O'),
        (r'\bslash data\b', '/data'),
        (r'\bslash results\b', '/results'),
        (r'\bslash tmp\b', '/tmp'),
    )
    for pattern,replacement in replacements:
        text=re.sub(pattern,replacement,text)
    return text

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='site'); ap.add_argument('--production',action='store_true'); a=ap.parse_args()
    cfg=yaml.safe_load((ROOT/'config/public.yml').read_text())
    media=yaml.safe_load((ROOT/'config/media-manifest.yml').read_text())['publication']
    if a.production:
        bad=[k for k,v in cfg.items() if isinstance(v,str) and ('TO_BE_' in v or '.invalid' in v or 'STAGING-' in v or 'CLUSTERDOCS-' in v or 'TRANSFER-' in v)]
        if cfg.get('site_status') != 'production': bad.insert(0,'site_status')
        if bad: raise SystemExit('Production build blocked by unresolved config: '+', '.join(bad))
    out=(ROOT/a.output).resolve() if not Path(a.output).is_absolute() else Path(a.output)
    shutil.rmtree(out,ignore_errors=True); (out/'assets').mkdir(parents=True)
    (out/'assets/site.css').write_text(CSS)
    if (DOCS/'assets').exists(): shutil.copytree(DOCS/'assets',out/'assets',dirs_exist_ok=True)
    poster_out=out/'assets/video-posters'; poster_out.mkdir(parents=True,exist_ok=True)
    for part in range(1,5):
        poster=ROOT/'slides/frames'/f'part{part}'/'slide-01.png'
        if poster.exists(): shutil.copy2(poster,poster_out/f'part{part}.png')
    for class_number in range(5,18):
        poster=ROOT/'slides/frames'/f'class{class_number}'/'slide-01.png'
        if poster.exists(): shutil.copy2(poster,poster_out/f'class{class_number}.png')
    md=mistune.create_markdown(escape=False, plugins=['table','strikethrough','task_lists'])
    nav_groups=[]
    for group,label,path in NAV:
        if not nav_groups or nav_groups[-1][0] != group:
            nav_groups.append((group,[]))
        nav_groups[-1][1].append((label,out_url(path)))
    group_for_path={path:group for group,_,path in NAV}
    for src in sorted(DOCS.rglob('*.md')):
        rel=src.relative_to(DOCS); target=out/out_url(str(rel)); target.parent.mkdir(parents=True,exist_ok=True)
        text=substitute(src.read_text(),cfg)
        text=gate_unreleased_videos(text,media)
        content=add_heading_ids(md(text))
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
        is_home=str(rel)=='index.md'
        home_rail=''
        if is_home:
            rail_match=re.search(
                r'<section class="expedition-callout".*?</section>',
                content,
                flags=re.S,
            )
            if rail_match:
                home_rail=rail_match.group(0)
                content=content[:rail_match.start()]+content[rail_match.end():]
        current_url=out_url(str(rel))
        target.write_text(Template(PAGE).render(
            title=title_of(text),
            content=content,
            nav_groups=nav_groups,
            root=relroot(target.relative_to(out)),
            status=cfg['site_status'],
            current_url=current_url,
            page_group=group_for_path.get(str(rel),'Documentation'),
            is_home=is_home,
            home_rail=home_rail,
        ))
    class_examples=DOCS/'classes/examples'
    if class_examples.exists():
        shutil.copytree(class_examples,out/'classes/examples',dirs_exist_ok=True)
    # Keep captions available to the embedded player without publishing the
    # source SRT files or recreating the retired downloads tree.
    caption_out=out/'assets/captions'; caption_out.mkdir(parents=True,exist_ok=True)
    for srt in (ROOT/'captions').glob('*.srt'):
        normalized=normalize_caption_text(srt.read_text())
        (caption_out/f'{srt.stem}.vtt').write_text(srt_to_vtt(normalized))
    print(out)
if __name__=='__main__': main()
