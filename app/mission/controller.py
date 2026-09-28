from app.agents.base import RepairAgent
from app.agents.failure_classifier import FailureClassifier
from app.mission.models import Evidence, Mission
from app.mission.runner import run_command


def execute_mission(
    mission: Mission,
    repair_agent: RepairAgent,
    failure_classifier: FailureClassifier | None = None,
) -> Evidence:
    before_code, before_output = run_command(
        mission.test_command,
        mission.repo_path,
    )

    if before_code == 0:
        raise RuntimeError("Mission target is not currently failing.")

    if failure_classifier is not None:
        classification = failure_classifier.classify(
            before_output
        )

        if not classification.repair_allowed:
            raise RuntimeError(
                "Repair blocked by failure classification: "
                f"{classification.kind.value} — "
                f"{classification.reason}"
            )

    target_path = mission.repo_path / mission.target_file

    if not target_path.exists():
        raise RuntimeError(
            f"Target file does not exist: {mission.target_file}"
        )

    original_source = target_path.read_text()

    patched_source, patch_summary = repair_agent.propose_patch(
        repo_path=mission.repo_path,
        target_file=mission.target_file,
        failure_output=before_output,
    )

    if patched_source == original_source:
        raise RuntimeError(
            "Repair agent returned an unchanged file."
        )

    target_path.write_text(patched_source)

    after_code, after_output = run_command(
        mission.test_command,
        mission.repo_path,
    )

    rolled_back = False

    if after_code != 0:
        target_path.write_text(original_source)
        rolled_back = True

    return Evidence(
        before_exit_code=before_code,
        before_output=before_output,
        patch_summary=patch_summary,
        after_exit_code=after_code,
        after_output=after_output,
        rolled_back=rolled_back,
        changed_files=[str(mission.target_file)],
    )
