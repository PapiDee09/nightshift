import subprocess
import tempfile
from pathlib import Path

from app.models.base import ModelClient


class CodexCLIModel(ModelClient):
    def __init__(self) -> None:
        self.schema_path = (
            Path(__file__).parent
            / "schemas"
            / "repair.schema.json"
        )

    def generate(self, prompt: str) -> str:
        with tempfile.NamedTemporaryFile(
            suffix=".json",
            delete=False,
        ) as output_file:
            output_path = Path(output_file.name)

        command = [
            "codex",
            "exec",
            prompt,
            "--output-schema",
            str(self.schema_path),
            "-o",
            str(output_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Codex CLI failed:\n"
                f"{result.stderr.strip()}"
            )

        if not output_path.exists():
            raise RuntimeError(
                "Codex CLI did not produce an output file."
            )

        response = output_path.read_text().strip()

        output_path.unlink(missing_ok=True)

        if not response:
            raise RuntimeError(
                "Codex CLI returned an empty response."
            )

        return response
