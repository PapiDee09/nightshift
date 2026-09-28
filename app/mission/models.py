from pathlib import Path

from pydantic import BaseModel, Field


class Mission(BaseModel):
    repo_path: Path
    test_command: list[str]
    target_file: Path
    apply_verified_patch: bool = False


class Evidence(BaseModel):
    before_exit_code: int
    before_output: str

    patch_summary: str

    after_exit_code: int
    after_output: str

    rolled_back: bool = False
    changed_files: list[str] = Field(default_factory=list)
    applied: bool = False

    @property
    def verified(self) -> bool:
        return (
            self.before_exit_code != 0
            and self.after_exit_code == 0
            and not self.rolled_back
        )
