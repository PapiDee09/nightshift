from pathlib import Path

from app.agents.base import RepairAgent
from app.mission.controller import execute_mission
from app.mission.models import Mission


BROKEN = """def add(a, b):
    return a - b
"""


class GoodRepairAgent(RepairAgent):
    def propose_patch(
        self,
        repo_path: Path,
        target_file: Path,
        failure_output: str,
    ) -> tuple[str, str]:
        source = (repo_path / target_file).read_text()
        return (
            source.replace("return a - b", "return a + b"),
            "Correct repair",
        )


class BadRepairAgent(RepairAgent):
    def propose_patch(
        self,
        repo_path: Path,
        target_file: Path,
        failure_output: str,
    ) -> tuple[str, str]:
        source = (repo_path / target_file).read_text()
        return (
            source.replace("return a - b", "return a * b"),
            "Incorrect repair",
        )


def create_repo(tmp_path: Path) -> Mission:
    (tmp_path / "calculator.py").write_text(BROKEN)

    (tmp_path / "test_calculator.py").write_text(
        """from calculator import add

def test_add():
    assert add(2, 3) == 5
"""
    )

    return Mission(
        repo_path=tmp_path,
        test_command=["pytest", "-q"],
        target_file=Path("calculator.py"),
    )


def test_successful_repair_is_kept(tmp_path: Path):
    mission = create_repo(tmp_path)

    evidence = execute_mission(
        mission=mission,
        repair_agent=GoodRepairAgent(),
    )

    assert evidence.verified is True
    assert evidence.rolled_back is False
    assert "return a + b" in (
        tmp_path / "calculator.py"
    ).read_text()


def test_failed_repair_is_rolled_back(tmp_path: Path):
    mission = create_repo(tmp_path)

    evidence = execute_mission(
        mission=mission,
        repair_agent=BadRepairAgent(),
    )

    assert evidence.verified is False
    assert evidence.rolled_back is True
    assert (
        tmp_path / "calculator.py"
    ).read_text() == BROKEN


class BlockingClassifier:
    def classify(self, failure_output: str):
        from app.mission.failure import (
            FailureClassification,
            FailureKind,
        )

        return FailureClassification(
            kind=FailureKind.INFRASTRUCTURE,
            reason="Synthetic infrastructure failure.",
            confidence=1.0,
            repair_allowed=False,
        )


def test_blocked_failure_never_repairs(tmp_path: Path):
    mission = create_repo(tmp_path)

    try:
        execute_mission(
            mission=mission,
            repair_agent=GoodRepairAgent(),
            failure_classifier=BlockingClassifier(),
        )
    except RuntimeError as exc:
        assert "Repair blocked by failure classification" in str(exc)
    else:
        raise AssertionError(
            "Expected repair to be blocked."
        )

    assert (
        tmp_path / "calculator.py"
    ).read_text() == BROKEN
