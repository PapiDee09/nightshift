from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from app.agents.model_repair import ModelRepairAgent
from app.mission.controller import execute_mission
from app.mission.models import Mission
from app.models.codex_cli import CodexCLIModel


console = Console()


def main() -> None:
    repo = Path(
        "sandbox/fixtures/broken-python-app"
    ).resolve()

    mission = Mission(
        repo_path=repo,
        test_command=["pytest", "-q"],
        target_file=Path("calculator.py"),
    )

    repair_agent = ModelRepairAgent(
        model=CodexCLIModel()
    )

    evidence = execute_mission(
        mission=mission,
        repair_agent=repair_agent,
    )

    console.print(
        Panel.fit(
            f"""
[bold]NightShift Mission #002[/bold]

Provider: Codex CLI

Before exit code: {evidence.before_exit_code}
Patch: {evidence.patch_summary}
After exit code: {evidence.after_exit_code}
Rollback: {"YES" if evidence.rolled_back else "NO"}
Changed files: {", ".join(evidence.changed_files)}

Verified: {"YES" if evidence.verified else "NO"}
""",
            title="Live Evidence Report",
        )
    )


if __name__ == "__main__":
    main()
