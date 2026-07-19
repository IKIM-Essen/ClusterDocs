#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EX = ROOT / "examples" / "interactive-workflows"
errors: list[str] = []

required = [
    EX / "python" / "analysis.py",
    EX / "python" / "environment.yml",
    EX / "python" / "python.sbatch",
    EX / "r" / "analysis.R",
    EX / "r" / "environment.yml",
    EX / "r" / "r.sbatch",
    EX / "jupyter" / "environment.yml",
    EX / "jupyter" / "jupyter.sbatch",
    EX / "shiny" / "app.R",
    EX / "shiny" / "environment.yml",
    EX / "shiny" / "shiny.sbatch",
    EX / "notebooks" / "python-large-data.ipynb",
    EX / "notebooks" / "r-large-data.ipynb",
]
for path in required:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")

for sbatch in [EX / "jupyter" / "jupyter.sbatch", EX / "shiny" / "shiny.sbatch"]:
    text = sbatch.read_text()
    if "--ip=127.0.0.1" not in text and "host='127.0.0.1'" not in text:
        errors.append(f"{sbatch.relative_to(ROOT)} does not bind to loopback")
    if "--time=04:00:00" not in text:
        errors.append(f"{sbatch.relative_to(ROOT)} should have a bounded four-hour development window")
    if re.search(r"0\.0\.0\.0|--ip=\*", text):
        errors.append(f"{sbatch.relative_to(ROOT)} exposes a public listener")
    if re.search(r"while\s+true|for\s*\(\s*;", text, re.I):
        errors.append(f"{sbatch.relative_to(ROOT)} contains an unbounded loop")

for sbatch in [EX / "python" / "python.sbatch", EX / "r" / "r.sbatch"]:
    text = sbatch.read_text()
    if "#SBATCH --partition=cpu_short" not in text:
        errors.append(f"{sbatch.relative_to(ROOT)} should use the bounded short CPU partition")
    if not re.search(r"#SBATCH --time=00:(20|30):00", text):
        errors.append(f"{sbatch.relative_to(ROOT)} should be short-running")

for notebook in [EX / "notebooks" / "python-large-data.ipynb", EX / "notebooks" / "r-large-data.ipynb"]:
    nb = json.loads(notebook.read_text())
    if nb.get("nbformat") != 4:
        errors.append(f"{notebook.relative_to(ROOT)} is not a v4 notebook")
    cell_text = "\n".join("".join(c.get("source", [])) for c in nb.get("cells", []))
    if "100_000" not in cell_text and "100000" not in cell_text:
        errors.append(f"{notebook.relative_to(ROOT)} does not show a bounded synthetic larger dataset")
    if re.search(r"/projects|10\.240\.|132\.252\.|password\s*=|token\s*=", cell_text, re.I):
        errors.append(f"{notebook.relative_to(ROOT)} contains forbidden infrastructure or credential-like content")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("interactive example validation: PASS")
