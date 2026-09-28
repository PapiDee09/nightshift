from app.agents.basic_classifier import BasicFailureClassifier
from app.mission.failure import FailureKind


def test_assertion_failure_allows_repair():
    classifier = BasicFailureClassifier()

    result = classifier.classify(
        """
        FAILED test_calculator.py::test_add
        E assert -1 == 5
        """
    )

    assert result.kind == FailureKind.APPLICATION
    assert result.repair_allowed is True


def test_dependency_failure_blocks_repair():
    classifier = BasicFailureClassifier()

    result = classifier.classify(
        "ModuleNotFoundError: No module named 'requests'"
    )

    assert result.kind == FailureKind.DEPENDENCY
    assert result.repair_allowed is False


def test_infrastructure_failure_blocks_repair():
    classifier = BasicFailureClassifier()

    result = classifier.classify(
        "Cannot connect to the Docker daemon"
    )

    assert result.kind == FailureKind.INFRASTRUCTURE
    assert result.repair_allowed is False


def test_unknown_failure_blocks_repair():
    classifier = BasicFailureClassifier()

    result = classifier.classify(
        "Something strange happened"
    )

    assert result.kind == FailureKind.UNKNOWN
    assert result.repair_allowed is False
