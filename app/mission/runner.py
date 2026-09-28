import os
import subprocess
import tempfile
from pathlib import Path

from app.mission.execution import CommandRunner


class LocalRunner(CommandRunner):
    def run(
        self,
        command: list[str],
        repo_path: Path,
    ) -> tuple[int, str]:
        with tempfile.TemporaryDirectory(
            prefix="nightshift-pycache-"
        ) as pycache_dir:
            env = os.environ.copy()
            env["PYTHONPYCACHEPREFIX"] = pycache_dir
            env["PYTHONDONTWRITEBYTECODE"] = "1"

            result = subprocess.run(
                command,
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )

        output = (
            result.stdout
            + ("\n" if result.stdout and result.stderr else "")
            + result.stderr
        )

        return result.returncode, output
