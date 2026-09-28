from pathlib import Path

from pydantic import BaseModel


class Mission(BaseModel):
    repo_path: Path
    test_command: list[str]
    target_file: Path


class Evidence(BaseModel):
    before_exit_code: int
    before_output: str

    patch_summary: str

    after_exit_code: int
    after_output: str

    rolled_back: bool = False
    changed_files: list[str] = []

    @property
    def verified(self) -> bool:
        return (
            self.before_exit_code != 0
            and self.after_exit_code == 0
            and not self.rolled_back
        )
