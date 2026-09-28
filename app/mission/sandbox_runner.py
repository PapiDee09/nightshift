import subprocess
from pathlib import Path

from app.mission.execution import CommandRunner


class DockerSandboxRunner(CommandRunner):
    def __init__(
        self,
        image: str = "nightshift-python-sandbox:local",
    ) -> None:
        self.image = image

    def run(
        self,
        command: list[str],
        repo_path: Path,
    ) -> tuple[int, str]:
        docker_command = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--cpus",
            "1",
            "--memory",
            "512m",
            "--pids-limit",
            "128",
            "-e",
            "PYTHONPYCACHEPREFIX=/tmp/nightshift-pycache",
            "-e",
            "PYTHONDONTWRITEBYTECODE=1",
            "-v",
            f"{repo_path.resolve()}:/workspace",
            "-w",
            "/workspace",
            self.image,
            *command,
        ]

        result = subprocess.run(
            docker_command,
            capture_output=True,
            text=True,
            check=False,
        )

        output = (
            result.stdout
            + ("\n" if result.stdout and result.stderr else "")
            + result.stderr
        )

        return result.returncode, output
