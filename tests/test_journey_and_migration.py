from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _read(path: str) -> str:
    return (DOCS / path).read_text(encoding="utf-8")


def test_home_exposes_journey_and_migration_assistant() -> None:
    text = _read("index.md")
    assert "RCC Journey" in text
    assert "Journey Light or Playful" in text
    assert "Migration Assistant" in text
    assert "getting-started/migration-assistant.md" in text


def test_journey_has_two_modes_and_shared_process_grammar() -> None:
    text = _read("rcc-journey.md")
    for phrase in (
        "Journey Light",
        "Playful Journey",
        "One RCC trust model · two ways to explore it",
        "●",
        "○",
        "×",
        "!",
        "Why RCC asks",
        "RCC can help",
        "without turning every researcher into a systems, workflow, or container engineer",
        "Snakemake or Nextflow",
        "slurm-execution-flow.svg",
        "No scoring. No leaderboard.",
    ):
        assert phrase in text
    # Guard the old competitive prototype rather than rejecting the explicit
    # statement that Journey has no score/leaderboard.
    assert "WEEKLY CHALLENGE" not in text
    assert "0 / 90" not in text
    assert "register this practice score" not in text.lower()


def test_migration_assistant_translates_old_habits_without_destructive_shortcuts() -> None:
    text = _read("getting-started/migration-assistant.md")
    for phrase in (
        "Old habit → current RCC practice",
        "I still start with SSH",
        "I still mount/browse storage",
        "I still run scripts by hand",
        "I still request nodes/resources the old way",
        "Conda environment + lock",
        "Snakemake / Nextflow",
        "do not erase the entire SSH trust database",
        "do not recursively change permissions",
        "What changed from the old cluster?",
    ):
        assert phrase in text


def test_ng_branch_name_is_not_present_in_new_surfaces() -> None:
    combined = _read("index.md") + _read("rcc-journey.md") + _read("getting-started/migration-assistant.md")
    assert "clusterdocs-ng" not in combined
