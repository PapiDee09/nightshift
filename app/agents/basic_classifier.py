from app.agents.failure_classifier import FailureClassifier
from app.mission.failure import (
    FailureClassification,
    FailureKind,
)


class BasicFailureClassifier(FailureClassifier):
    def classify(
        self,
        failure_output: str,
    ) -> FailureClassification:
        output = failure_output.lower()

        dependency_signals = [
            "modulenotfounderror",
            "no module named",
            "cannot find module",
            "eresolve",
            "dependency conflict",
        ]

        infrastructure_signals = [
            "cannot connect to the docker daemon",
            "connection refused",
            "no space left on device",
            "service unavailable",
            "failed to start server",
        ]

        for signal in dependency_signals:
            if signal in output:
                return FailureClassification(
                    kind=FailureKind.DEPENDENCY,
                    reason=(
                        f"Detected dependency-related signal: {signal}"
                    ),
                    confidence=0.90,
                    repair_allowed=False,
                )

        for signal in infrastructure_signals:
            if signal in output:
                return FailureClassification(
                    kind=FailureKind.INFRASTRUCTURE,
                    reason=(
                        f"Detected infrastructure signal: {signal}"
                    ),
                    confidence=0.90,
                    repair_allowed=False,
                )

        if "assert" in output and "failed" in output:
            return FailureClassification(
                kind=FailureKind.APPLICATION,
                reason=(
                    "A deterministic test assertion failed."
                ),
                confidence=0.70,
                repair_allowed=True,
            )

        return FailureClassification(
            kind=FailureKind.UNKNOWN,
            reason="Failure type could not be safely classified.",
            confidence=0.20,
            repair_allowed=False,
        )
