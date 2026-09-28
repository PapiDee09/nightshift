from pathlib import Path

from app.agents.model_repair import ModelRepairAgent
from app.models.fake import FakeRepairModel


def test_model_repair_agent_returns_structured_patch(
    tmp_path: Path,
):
    target = tmp_path / "calculator.py"

    target.write_text(
        "def add(a, b):\n"
        "    return a - b\n"
    )

    agent = ModelRepairAgent(
        model=FakeRepairModel()
    )

    patched_source, summary = agent.propose_patch(
        repo_path=tmp_path,
        target_file=Path("calculator.py"),
        failure_output="assert -1 == 5",
    )

    assert "return a + b" in patched_source
    assert summary
