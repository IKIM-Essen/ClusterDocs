#!/usr/bin/env python3
"""Apply the RCC dark-sidebar visual shell to a rendered ClusterDocs site.

The renderer remains authoritative for content and navigation. This post-build step
changes presentation only and fails closed when the expected generated shell is not
present, so renderer drift cannot silently publish a partially themed site.
"""
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "/* RCC visual shell v2 */"

THEME = r"""
/* RCC visual shell v2 */
body {
  background: linear-gradient(180deg, #ffffff 0, var(--background) 42rem);
}
.topbar {
  background: var(--navy);
  border-bottom-color: rgba(255,255,255,.10);
  color: #fff;
}
.topbar-inner {
  max-width: 1720px;
  padding: .8rem 1.5rem;
}
.brand img {
  padding: .3rem .45rem;
  border-radius: 8px;
  background: #fff;
}
.brand-copy {
  border-left-color: rgba(255,255,255,.25);
}
.brand-copy strong { color: #fff; }
.brand-copy span { color: rgba(255,255,255,.72); }
.service-nav a { color: rgba(255,255,255,.88); }
.service-nav a:hover,
.service-nav a.active {
  background: rgba(255,255,255,.10);
  color: #fff;
}
.service-nav .admin-link {
  background: #fff;
  color: var(--navy);
}
.service-nav .admin-link:hover {
  background: var(--cyan-light);
  color: var(--navy);
}
.shell {
  max-width: 1720px;
  padding: 1.25rem 1.5rem 4rem;
}
.docs-layout {
  grid-template-columns: minmax(245px,285px) minmax(0,1050px);
  gap: 1.25rem;
  justify-content: start;
}
.home .shell { max-width: 1720px; }
.home .docs-layout {
  grid-template-columns: minmax(245px,285px) minmax(0,1fr) minmax(280px,330px);
}
.sidebar {
  top: 92px;
  max-height: calc(100vh - 110px);
}
.sidebar-card {
  padding: 1rem .8rem 1.1rem;
  border-color: rgba(255,255,255,.12);
  background: linear-gradient(180deg, var(--navy) 0, #07345f 72%, #052845 100%);
  color: #fff;
  box-shadow: 0 14px 32px rgba(6,42,70,.16);
}
.sidebar-heading { border-bottom-color: rgba(255,255,255,.14); }
.sidebar-heading strong { color: #fff; }
.stage-badge {
  background: rgba(255,255,255,.10);
  color: #a9edf5;
}
.sidebar .nav-section summary { color: rgba(255,255,255,.58); }
.sidebar .nav-section summary:hover,
.sidebar .nav-section[open] summary {
  background: rgba(255,255,255,.07);
  color: #fff;
}
.sidebar nav a { color: rgba(255,255,255,.88); }
.sidebar nav a:hover {
  background: rgba(255,255,255,.08);
  color: #fff;
}
.sidebar nav a[aria-current="page"] {
  background: linear-gradient(90deg,#1262b0,#0b5a9f);
  color: #fff;
  box-shadow: inset 3px 0 0 #3ab0ff;
}
.content-card {
  border-radius: 20px;
  box-shadow: 0 10px 28px rgba(6,42,70,.07);
}
.home .content-card { padding: clamp(1.5rem,3.2vw,2.7rem); }
.home-rail { top: 92px; }
.expedition-callout {
  background: linear-gradient(135deg,var(--navy) 0,var(--navy-2) 68%,#0d527f 100%);
}
.path-card {
  border-radius: 18px;
  box-shadow: 0 10px 28px rgba(6,42,70,.065);
}
@media (max-width:1180px) {
  .home .docs-layout { grid-template-columns: 240px minmax(0,1fr); }
}
@media (max-width:980px) {
  .docs-layout { grid-template-columns: 220px minmax(0,1fr); }
}
@media (max-width:760px) {
  .topbar { background: var(--navy); }
  .shell { padding: 1rem; }
}
"""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL {message}")


def apply(output: Path) -> None:
    css_path = output / "assets" / "site.css"
    index_path = output / "index.html"
    require(css_path.is_file(), f"missing rendered stylesheet {css_path}")
    require(index_path.is_file(), f"missing rendered home page {index_path}")

    html = index_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    for token in (
        'class="topbar"',
        'class="sidebar"',
        'class="content-card"',
        'alt="Universitätsklinikum Essen"',
        'aria-label="RCC services"',
    ):
        require(token in html, f"rendered ClusterDocs shell lacks expected marker {token}")

    marker_count = css.count(MARKER)
    require(marker_count <= 1, "rendered stylesheet contains duplicate RCC visual-theme markers")
    if marker_count == 0:
        css_path.write_text(css.rstrip() + "\n\n" + THEME.strip() + "\n", encoding="utf-8")

    themed = css_path.read_text(encoding="utf-8")
    require(themed.count(MARKER) == 1, "RCC visual theme must be present exactly once")
    for token in (
        ".sidebar-card",
        "linear-gradient(180deg, var(--navy)",
        '.sidebar nav a[aria-current="page"]',
        ".topbar",
    ):
        require(token in themed, f"themed stylesheet lacks {token}")

    # The theme is intentionally a presentation-only post-build step. It must
    # not introduce a second script/application layer into the generated docs.
    for page in output.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        require("data-access-set" not in text and "role_preview_level" not in text,
                f"generated docs unexpectedly contain role-preview controls: {page}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    apply(args.output)
    print(f"PASS applied RCC visual shell to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
