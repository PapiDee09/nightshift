from enum import Enum

from pydantic import BaseModel


class FailureKind(str, Enum):
    APPLICATION = "application"
    TEST = "test"
    DEPENDENCY = "dependency"
    INFRASTRUCTURE = "infrastructure"
    FLAKY = "flaky"
    UNKNOWN = "unknown"


class FailureClassification(BaseModel):
    kind: FailureKind
    reason: str
    confidence: float
    repair_allowed: bool
