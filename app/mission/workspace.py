import shutil
import tempfile
from pathlib import Path


class TemporaryWorkspace:
    def __init__(self, source_repo: Path) -> None:
        self.source_repo = source_repo.resolve()
        self._temp_dir: tempfile.TemporaryDirectory[str] | None = None
        self.path: Path | None = None

    def __enter__(self) -> Path:
        self._temp_dir = tempfile.TemporaryDirectory(
            prefix="nightshift-workspace-"
        )

        destination = Path(self._temp_dir.name) / "repo"

        shutil.copytree(
            self.source_repo,
            destination,
            ignore=shutil.ignore_patterns(
                ".git",
                ".venv",
                "__pycache__",
                ".pytest_cache",
                "node_modules",
            ),
        )

        self.path = destination
        return destination

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        if self._temp_dir is not None:
            self._temp_dir.cleanup()

    def commit_file(
        self,
        workspace_path: Path,
        relative_file: Path,
    ) -> None:
        source = workspace_path / relative_file
        destination = self.source_repo / relative_file

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            destination,
        )
