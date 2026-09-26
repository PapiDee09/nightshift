from app.agents.base import RepairAgent
from app.mission.models import Evidence, Mission
from app.mission.runner import run_command


def execute_mission(
    mission: Mission,
    repair_agent: RepairAgent,
) -> Evidence:
    before_code, before_output = run_command(
        mission.test_command,
        mission.repo_path,
    )

    if before_code == 0:
        raise RuntimeError("Mission target is not currently failing.")

    target_path = mission.repo_path / mission.target_file

    patched_source, patch_summary = repair_agent.propose_patch(
        repo_path=mission.repo_path,
        target_file=mission.target_file,
        failure_output=before_output,
    )

    target_path.write_text(patched_source)

    after_code, after_output = run_command(
        mission.test_command,
        mission.repo_path,
    )

    return Evidence(
        before_exit_code=before_code,
        before_output=before_output,
        patch_summary=patch_summary,
        after_exit_code=after_code,
        after_output=after_output,
    )
