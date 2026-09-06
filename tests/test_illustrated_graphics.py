from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"


def _svg(name: str) -> tuple[str, ET.Element]:
    path = ASSETS / name
    text = path.read_text(encoding="utf-8")
    return text, ET.fromstring(text)


def test_lab_network_flow_keeps_public_safe_state_labels() -> None:
    text, root = _svg("lab-network-flow.svg")
    assert root.tag.endswith("svg")
    assert "ARDIA · NOT RELEASED" in text
    assert "PROJECT MEMBERS ONLY" in text
    assert "Mass spectrometers" in text
    assert "DNA sequencers" in text
    assert "Microscopes" in text
    assert "10.240." not in text
    assert "is2-" not in text


def test_slurm_flow_teaches_resource_requests_not_node_selection() -> None:
    text, root = _svg("slurm-execution-flow.svg")
    assert root.tag.endswith("svg")
    for phrase in (
        "Request resources",
        "not a physical node",
        "cpu_short",
        "cpu_nodes",
        "gpu_nodes",
        "PROJECT-SCOPED STORAGE",
    ):
        assert phrase in text
    assert "srun" in text and "sbatch" in text
    assert "c001" not in text
    assert "d01" not in text
    assert "g1-" not in text
