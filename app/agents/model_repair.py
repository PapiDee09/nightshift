import json
from pathlib import Path

from app.agents.base import RepairAgent
from app.models.base import ModelClient


class ModelRepairAgent(RepairAgent):
    def __init__(self, model: ModelClient) -> None:
        self.model = model

    def propose_patch(
        self,
        repo_path: Path,
        target_file: Path,
        failure_output: str,
    ) -> tuple[str, str]:
        target_path = repo_path / target_file
        source = target_path.read_text()

        prompt = f"""
You are NightShift's software repair agent.

Repair the failing source file using the test evidence.

Rules:
- Make the smallest possible correct change.
- Do not modify tests.
- Do not introduce unrelated refactors.
- Return JSON only.
- Include the entire replacement source file.

Target:
{target_file}

Current source:
{source}

Failure evidence:
{failure_output}

Return:
{{
  "patched_source": "...",
  "summary": "..."
}}
""".strip()

        response = self.model.generate(prompt)

        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Model returned invalid JSON."
            ) from exc

        patched_source = data.get("patched_source")
        summary = data.get("summary")

        if not isinstance(patched_source, str) or not patched_source:
            raise RuntimeError(
                "Model response missing patched_source."
            )

        if not isinstance(summary, str) or not summary:
            raise RuntimeError(
                "Model response missing summary."
            )

        return patched_source, summary
