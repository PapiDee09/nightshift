from abc import ABC, abstractmethod
from pathlib import Path


class CommandRunner(ABC):
    @abstractmethod
    def run(
        self,
        command: list[str],
        repo_path: Path,
    ) -> tuple[int, str]:
        raise NotImplementedError
