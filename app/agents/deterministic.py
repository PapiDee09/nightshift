from pathlib import Path

from app.agents.base import RepairAgent


class DeterministicRepairAgent(RepairAgent):
    def propose_patch(
        self,
        repo_path: Path,
        target_file: Path,
        failure_output: str,
    ) -> tuple[str, str]:
        path = repo_path / target_file
        source = path.read_text()

        broken = "return a - b"
        fixed = "return a + b"

        if broken not in source:
            raise RuntimeError("Expected broken implementation was not found.")

        patched = source.replace(broken, fixed)

        return patched, "Changed add() from subtraction to addition."
