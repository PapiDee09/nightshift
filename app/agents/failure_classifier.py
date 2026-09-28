from abc import ABC, abstractmethod

from app.mission.failure import FailureClassification


class FailureClassifier(ABC):
    @abstractmethod
    def classify(
        self,
        failure_output: str,
    ) -> FailureClassification:
        raise NotImplementedError
