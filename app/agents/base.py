from abc import ABC, abstractmethod
from pathlib import Path


class RepairAgent(ABC):
    @abstractmethod
    def propose_patch(
        self,
        repo_path: Path,
        target_file: Path,
        failure_output: str,
    ) -> tuple[str, str]:
        """
        Returns:
            patched_source: full replacement file contents
            summary: human-readable explanation of the repair
        """
        raise NotImplementedError
