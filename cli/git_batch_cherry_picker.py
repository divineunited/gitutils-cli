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
    branches = utils.get_input_branches_from_user(remote_branches)
    if not branches:
        return

    # Do the work:
    for branch in branches:
        branch = branch.strip()
        utils.checkout_and_pull_branch(branch)

        print(f"Cherry-picking commit into branch: {branch}")
        return_code = utils.run_git_command(f"git cherry-pick {commit}")
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
