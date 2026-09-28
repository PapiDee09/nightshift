from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from app.agents.deterministic import DeterministicRepairAgent
from app.mission.controller import execute_mission
from app.mission.models import Mission


console = Console()


def main() -> None:
    repo = Path("sandbox/fixtures/broken-python-app").resolve()

    mission = Mission(
        repo_path=repo,
        test_command=["pytest", "-q"],
        target_file=Path("calculator.py"),
    )

    evidence = execute_mission(
        mission=mission,
        repair_agent=DeterministicRepairAgent(),
    )

    console.print(
        Panel.fit(
            f"""
[bold]NightShift Mission #001[/bold]

Before exit code: {evidence.before_exit_code}
Patch: {evidence.patch_summary}
After exit code: {evidence.after_exit_code}
Rollback: {"YES" if evidence.rolled_back else "NO"}
Changed files: {", ".join(evidence.changed_files)}

Verified: {"YES" if evidence.verified else "NO"}
""",
            title="Evidence Report",
        )
    )


if __name__ == "__main__":
    main()
