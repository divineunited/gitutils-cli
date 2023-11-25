"""Safely batch cherry-pick commits to different branches and push to remote."""

from cli_utils import utils

INTRO_TEXT__GIT_BATCH_CHERRY_PICK = """
This command cherry picks a commit to a batch of branches and pushes that change to each branches remote.

It is helpful when:
- you have a commit on your branch and you want to apply it to some shared branches.
"""


def git_batch_cherry_picker():
    """Entrypoint Cherry Picker"""
    print(INTRO_TEXT__GIT_BATCH_CHERRY_PICK + "\n")

    # Setup
    current_branch = utils.get_current_branch()
    conflict_branches = []
    branches = []
    remote_branches = utils.get_all_remote_branches_set()

    # Accept Input
    commit = utils.get_input_commit_from_user()
    if not commit:
        return
    branches = utils.get_input_branches_from_user(
        remote_branches=remote_branches,
        allow_only_one_input_branch=True,
    )
    if not branches:
        return

    if ("master" in branches) or ("main" in branches):
        print("You cannot cherry-pick into `master` or `main` branches. Exiting.")
        return

    pull_choice = utils.get_input_pull_config_from_user()

    # Do the work:
    for branch in branches:
        branch = branch.strip()
        utils.checkout_and_pull_branch(branch, pull_choice)

        print(f"Cherry-picking commit into branch: {branch}")
        return_code, _ = utils.run_git_command(f"git cherry-pick {commit}")
        if return_code != 0:
            print(f"Conflict detected, skipping {branch}")
            conflict_branches.append(branch)
            utils.run_git_command("git cherry-pick --abort")
            continue
        print(f"...Cherry-picked {commit:} to {branch:}")

        utils.push_branch_to_remote(branch)

    # Clean up
    utils.perform_clean_up(
        original_branch=current_branch, conflict_branches=conflict_branches
    )


if __name__ == "__main__":
    git_batch_cherry_picker()
