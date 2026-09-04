from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ACK = "Computational resources and services were provided by the Research Compute Cluster (RCC) at University Hospital Essen."


def test_publication_credit_page_is_navigable_and_review_bounded() -> None:
    page = (ROOT / "docs/reference/publications-and-rcc-credit.md").read_text(encoding="utf-8")
    nav = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))

    assert ACK in page
    assert "DOI or PMID" in page
    assert "RCC project name" in page
    assert "candidates only" in page
    assert "accepted record" in page
    assert "unpublished manuscript" in page
    assert "publication-submission form exists" in page
    assert "32 Folker Meyer scholarly outputs from 2020 through 2026" in page
    assert "Thirty entries are published" in page
    assert "labelled **accepted** until final publication" in page
    assert "https://rcc.ikim.uk-essen.de/#rcc-publications" in page
    assert "not a rule that every paper by an RCC user automatically belongs" in page

    reference = next(section["Reference"] for section in nav["nav"] if "Reference" in section)
    assert {"Publications and acknowledging RCC": "reference/publications-and-rcc-credit.md"} in reference
