#!/usr/bin/env python3
"""Apply the RCC dark-sidebar visual shell to a rendered ClusterDocs site.

The renderer remains authoritative for documentation content and navigation. This
post-build step changes presentation only and fails closed when the expected shell
is not present. The RCC service navigation is relocated from the top bar into the
left rail and normalized to the stable RCC user-facing service destinations so
ClusterDocs reads as one RCC surface without becoming another RCC application
dashboard.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

MARKER = "/* RCC visual shell v3 */"
HTML_MARKER = "<!-- RCC service rail v1 -->"
SERVICE_NAV_RE = re.compile(
    r"\s*<nav class=\"service-nav\" aria-label=\"RCC services\">.*?</nav>",
    re.DOTALL,
)
DOCUMENTATION_LINK_RE = re.compile(
    r'<a\s+class="active"\s+href="([^"]+)"(?:\s+aria-current="page")?\s*>Documentation</a>'
)
SIDEBAR_CARD = '<div class="sidebar-card">'

THEME = r"""
/* RCC visual shell v3 */
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
  justify-content: flex-start;
}
.brand img {
  padding: .3rem .45rem;
  border-radius: 8px;
  background: #fff;
}
.brand-copy { border-left-color: rgba(255,255,255,.25); }
.brand-copy strong { color: #fff; }
.brand-copy span { color: rgba(255,255,255,.72); }
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
.rcc-service-rail {
  margin: -.15rem -.1rem .85rem;
  padding: .15rem .1rem .85rem;
  border-bottom: 1px solid rgba(255,255,255,.14);
}
.rcc-sidebar-kicker {
  margin: 0 0 .45rem;
  padding: 0 .55rem;
  color: rgba(255,255,255,.58);
  font-size: .66rem;
  font-weight: 850;
  letter-spacing: .12em;
  text-transform: uppercase;
}
.rcc-service-rail .service-nav {
  display: grid;
  gap: .2rem;
}
.rcc-service-rail .service-nav a {
  display: block;
  padding: .55rem .58rem;
  border-radius: 9px;
  color: rgba(255,255,255,.88);
  font-size: .86rem;
  font-weight: 700;
  text-decoration: none;
}
.rcc-service-rail .service-nav a:hover {
  background: rgba(255,255,255,.08);
  color: #fff;
}
.rcc-service-rail .service-nav a.active {
  background: linear-gradient(90deg,#1262b0,#0b5a9f);
  color: #fff;
  box-shadow: inset 3px 0 0 #3ab0ff;
}
.rcc-service-rail .service-nav .portal-link {
  background: rgba(255,255,255,.06);
  color: rgba(255,255,255,.92);
}
.rcc-service-rail .service-nav .portal-link:hover {
  background: rgba(255,255,255,.12);
  color: #fff;
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


def _canonical_service_nav(service_nav: str) -> str:
    """Return the one stable user-facing RCC service navigation.

    The custom builder historically emitted About RCC / File transfer / RCC Admin.
    The visual-shell transformer is the convergence boundary, so generated sites
    get the same stable service semantics even while renderer internals evolve.
    The current page's relative Documentation href is preserved exactly.
    """
    matches = DOCUMENTATION_LINK_RE.findall(service_nav)
    require(
        len(matches) == 1,
        "generated RCC service navigation must contain one active Documentation link",
    )
    documentation_href = matches[0]
    return (
        '<nav class="service-nav" aria-label="RCC services">\n'
        '      <a href="https://rcc.ikim.uk-essen.de/">Home</a>\n'
        f'      <a class="active" href="{documentation_href}" aria-current="page">Documentation</a>\n'
        '      <a href="https://files.ikim.uk-essen.de/web/client">Files</a>\n'
        '      <a class="portal-link" href="https://rcc-admin.ikim.uk-essen.de/myrcc">My RCC</a>\n'
        '      <a href="https://assistant.ikim.uk-essen.de/">AI assistant</a>\n'
        '    </nav>'
    )


def _relocate_service_nav(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    marker_count = html.count(HTML_MARKER)
    require(marker_count <= 1, f"{path} contains duplicate RCC service-rail markers")

    if marker_count == 0:
        matches = list(SERVICE_NAV_RE.finditer(html))
        require(len(matches) == 1, f"{path} must contain exactly one RCC service navigation")
        match = matches[0]
        service_nav = _canonical_service_nav(match.group(0).strip())
        html = html[: match.start()] + html[match.end() :]
        require(SIDEBAR_CARD in html, f"{path} lacks the generated sidebar card")
        rail = (
            SIDEBAR_CARD
            + "\n        "
            + HTML_MARKER
            + '\n        <section class="rcc-service-rail">'
            + '\n          <p class="rcc-sidebar-kicker">RCC services</p>\n          '
            + service_nav
            + "\n        </section>"
        )
        html = html.replace(SIDEBAR_CARD, rail, 1)
        path.write_text(html, encoding="utf-8")

    themed = path.read_text(encoding="utf-8")
    require(themed.count(HTML_MARKER) == 1, f"{path} must contain one service-rail marker")
    require(themed.count('aria-label="RCC services"') == 1,
            f"{path} must contain one RCC service navigation after theming")
    header = themed.split("</header>", 1)[0]
    require('aria-label="RCC services"' not in header,
            f"{path} still renders RCC services in the top bar")
    require('class="rcc-service-rail"' in themed,
            f"{path} does not render RCC services in the left rail")
    for label, href in (
        ("Home", "https://rcc.ikim.uk-essen.de/"),
        ("Files", "https://files.ikim.uk-essen.de/web/client"),
        ("My RCC", "https://rcc-admin.ikim.uk-essen.de/myrcc"),
        ("AI assistant", "https://assistant.ikim.uk-essen.de/"),
    ):
        require(f'href="{href}"' in themed and f'>{label}<' in themed,
                f"{path} lacks canonical RCC service link {label}")
    for obsolete in (">About RCC<", ">File transfer<", ">RCC Admin<"):
        require(obsolete not in themed, f"{path} retains obsolete RCC service label {obsolete}")


def apply(output: Path) -> None:
    css_path = output / "assets" / "site.css"
    index_path = output / "index.html"
    require(css_path.is_file(), f"missing rendered stylesheet {css_path}")
    require(index_path.is_file(), f"missing rendered home page {index_path}")

    html_paths = sorted(output.rglob("*.html"))
    require(html_paths, "rendered ClusterDocs site contains no HTML pages")
    for path in html_paths:
        _relocate_service_nav(path)

    html = index_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    for token in (
        'class="topbar"',
        'class="sidebar"',
        'class="sidebar-card"',
        'class="content-card"',
        'alt="Universitätsklinikum Essen"',
        'class="rcc-service-rail"',
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
        ".rcc-service-rail",
        ".sidebar-card",
        "linear-gradient(180deg, var(--navy)",
        '.sidebar nav a[aria-current="page"]',
        ".topbar",
    ):
        require(token in themed, f"themed stylesheet lacks {token}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    apply(args.output)
    print(f"PASS applied RCC visual shell to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
