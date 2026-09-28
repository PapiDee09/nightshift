import json

from app.models.base import ModelClient


class FakeRepairModel(ModelClient):
    def generate(self, prompt: str) -> str:
        return json.dumps(
            {
                "patched_source": (
                    "def add(a, b):\n"
                    "    return a + b\n"
                ),
                "summary": (
                    "Corrected add() to perform addition."
                ),
            }
        )
