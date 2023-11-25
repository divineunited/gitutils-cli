"""Safely batch merge branches together and push them to remote"""

from cli_utils import utils

INTRO_TEXT__GIT_BATCH_MERGER = """
This command safely batch merges changes from one branch to the next in order of input.
It also pushes each branch to remote.

It is helpful when:
- you have a chain of PRs where you need to need to consolidate the changes across all the branches
e.g. `master -> my-working-branch-p1 -> my-working-branch-p2 -> my-working-branch-p3`

- or simply you just want to merge from your personal branch to a shared branch and have it push
e.g. `master -> my-working-branch -> deployment-qa`
"""


def git_batch_merger():
    """
    Main entrypoint for this function.
    """
    print(INTRO_TEXT__GIT_BATCH_MERGER + "\n")

    # Setup
    current_branch = utils.get_current_branch()
    conflict_branches = []
    branches = []
    remote_branches = utils.get_all_remote_branches_set()

    # Accept Input
    branches = utils.get_input_branches_from_user(remote_branches)
    if not branches:
        return

    if ("main" in branches[1:]) or ("master" in branches[1:]):
        print(
            "You cannot merge any branches into main or master. Main or Master can only be merged into other branches."
        )
        return

    pull_choice = utils.get_input_pull_config_from_user()

    # Do the work:
    for i, branch in enumerate(branches):
        branch = branch.strip()
        utils.checkout_and_pull_branch(branch, pull_choice)

        if i == 0:
            # There is nothing to merge into the first branch
            continue

        prior_branch = branches[i - 1]
        print(f"Merging branch: {prior_branch} into branch: {branch}")
        return_code, _ = utils.run_git_command(f"git merge {prior_branch}")
        if return_code != 0:
            decision = utils.handle_conflicts(
                prior_branch=prior_branch,
                current_branch=branch,
                conflict_branches=conflict_branches,
            )
            if decision == utils.ConflictHandleScenario.Abort:
                continue
        print(f"...Merged branch: {prior_branch} into branch: {branch}")

        utils.push_branch_to_remote(branch)

    # Clean up
    utils.perform_clean_up(
        original_branch=current_branch, conflict_branches=conflict_branches
    )


if __name__ == "__main__":
    git_batch_merger()
