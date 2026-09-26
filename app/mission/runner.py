import subprocess
from pathlib import Path


def run_command(command: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )

    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output
