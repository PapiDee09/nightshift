from app.agents.base import RepairAgent
from app.agents.failure_classifier import FailureClassifier
from app.mission.execution import CommandRunner
from app.mission.models import Evidence, Mission
from app.mission.runner import LocalRunner
from app.mission.workspace import TemporaryWorkspace


def execute_mission(
    mission: Mission,
    repair_agent: RepairAgent,
    failure_classifier: FailureClassifier | None = None,
    runner: CommandRunner | None = None,
) -> Evidence:
    command_runner = runner or LocalRunner()

    workspace_manager = TemporaryWorkspace(
        mission.repo_path
    )

    with workspace_manager as workspace:
        before_code, before_output = command_runner.run(
            mission.test_command,
            workspace,
        )

        if before_code == 0:
            raise RuntimeError(
                "Mission target is not currently failing."
            )

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

        target_path = workspace / mission.target_file

        if not target_path.exists():
            raise RuntimeError(
                "Target file does not exist: "
                f"{mission.target_file}"
            )

        original_source = target_path.read_text()

        patched_source, patch_summary = (
            repair_agent.propose_patch(
                repo_path=workspace,
                target_file=mission.target_file,
                failure_output=before_output,
            )
        )

        if patched_source == original_source:
            raise RuntimeError(
                "Repair agent returned an unchanged file."
            )

        target_path.write_text(
            patched_source
        )

        after_code, after_output = command_runner.run(
            mission.test_command,
            workspace,
        )

        if after_code != 0:
            return Evidence(
                before_exit_code=before_code,
                before_output=before_output,
                patch_summary=patch_summary,
                after_exit_code=after_code,
                after_output=after_output,
                rolled_back=True,
                changed_files=[
                    str(mission.target_file)
                ],
            )

        workspace_manager.commit_file(
            workspace,
            mission.target_file,
        )

        return Evidence(
            before_exit_code=before_code,
            before_output=before_output,
            patch_summary=patch_summary,
            after_exit_code=after_code,
            after_output=after_output,
            rolled_back=False,
            changed_files=[
                str(mission.target_file)
            ],
        )
