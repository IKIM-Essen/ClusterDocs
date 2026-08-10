#!/usr/bin/env python3
"""Fail if the immutable ClusterDocs runner lacks its pinned Python modules."""

from __future__ import annotations

from importlib import import_module


EXPECTED = {
    "jinja2": "3.1.6",
    "mistune": "3.3.3",
    "yaml": "6.0.3",
}


def main() -> None:
    mismatches: list[str] = []
    for module_name, expected in EXPECTED.items():
        module = import_module(module_name)
        actual = str(module.__version__)
        if actual != expected:
            mismatches.append(f"{module_name}: expected {expected}, found {actual}")
    if mismatches:
        raise SystemExit("immutable CI environment mismatch: " + "; ".join(mismatches))
    print("immutable CI environment: PASS")


if __name__ == "__main__":
    main()
