#!/usr/bin/env python3
import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlparse


RCC_ORIGIN_LINKS = frozenset({"/", "/account/", "/assets/Logo_UME_UKE.svg"})
RCC_DOCS_PREFIX = "/docs/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        for name in ("href", "src"):
            if attributes.get(name):
                self.refs.append(attributes[name])


def main():
    parser = argparse.ArgumentParser(description="Check generated local links and fragments.")
    parser.add_argument("site", nargs="?", default="site", type=Path)
    parser.add_argument(
        "--rcc-docs-mount", action="store_true",
        help="Resolve /docs/ against this build. Leave the shared RCC origin links to deployment checks.",
    )
    args = parser.parse_args()
    root = args.site.resolve()

    errors = []
    pages = {}
    for path in root.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(errors="replace"))
        pages[path.resolve()] = page
        duplicates = sorted({value for value in page.ids if page.ids.count(value) > 1})
        if duplicates:
            errors.append(f"{path.relative_to(root)}: duplicate ids: {', '.join(duplicates)}")

    for path, page in pages.items():
        for ref in page.refs:
            url = urlparse(ref)
            if url.scheme or url.netloc:
                continue
            if args.rcc_docs_mount and ref in RCC_ORIGIN_LINKS:
                continue
            relative_path = unquote(url.path)
            if args.rcc_docs_mount and relative_path.startswith(RCC_DOCS_PREFIX):
                target = (root / relative_path.removeprefix(RCC_DOCS_PREFIX)).resolve()
            else:
                target = (path.parent / relative_path).resolve() if relative_path else path
            if target.is_dir():
                target = (target / "index.html").resolve()
            source = path.relative_to(root)
            if not target.is_relative_to(root):
                errors.append(f"{source}: path escapes site: {ref}")
            elif not target.exists():
                errors.append(f"{source}: missing {ref}")
            elif url.fragment and target.suffix == ".html":
                target_page = pages.get(target)
                if target_page is None or unquote(url.fragment) not in target_page.ids:
                    errors.append(f"{source}: missing fragment {ref}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("site links: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
