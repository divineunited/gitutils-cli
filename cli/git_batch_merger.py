"""Safely batch merge branches together and push them to remote"""

import subprocess


def _run_command(cmd) -> tuple[int, str]:
    """Run a subprocess command in a users terminal"""
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # result.stderr.decode("utf-8"),
    return (result.returncode, result.stdout.decode("utf-8"))


def git_batch_merger():
    """
    Main entrypoint for this function.
    """

    help_text = """
    This command safely batch merges changes from one branch to the next in order of input.
    It also pushes each branch to remote.

    It is helpful when:
    - you have a chain of PRs where you need to need to consolidate the changes across all the branches
    e.g. `master -> my-working-branch-p1 -> my-working-branch-p2 -> my-working-branch-p3`

    - or simply you just want to merge from your personal branch to a shared branch and have it push
    e.g. `master -> my-working-branch -> deployment-qa`
    """
    print(help_text + "\n")

    # Setup
    current_branch = _run_command("git branch --show-current")[1].strip()
    conflict_branches = []
    branches = []
    all_branches = set(_run_command("git branch -a")[1].split("\n"))
    all_branches_raw = _run_command("git branch -a")[1].split("\n")
    all_branches = [
        branch.replace("remotes/origin/", "").strip() for branch in all_branches_raw
    ]
    all_branches_set = set(all_branches)

    # Accept Input
    first_branch = input(
        "Please enter the first branch name or press ENTER for default of `master`: "
    ).strip()
    if not first_branch:
        print("Using the default branch of `master` as the first branch.")
        first_branch = "master"
    if first_branch not in all_branches_set:
        print(f"Branch {first_branch} does not exist. Stopping program.")
        return
    branches.append(first_branch)

    while True:
        branch = input(
            "Please enter the next branch name or press ENTER to finish: "
        ).strip()

        if not branch:
            break

        if branch not in all_branches_set:
            print(f"Branch {branch} does not exist. Skipping...")
            continue

        branches.append(branch)

    if len(branches) < 2:
        print("You must enter at least 2 branches.")
        return

    if len(branches) != len(set(branches)):
        print(f"All the branches you enter must be unique. You entered: {branches}")
        return

    # Do the work:
    for i, branch in enumerate(branches):
        branch = branch.strip()
        print(f"\nChecking out branch: {branch}...")
        _run_command(f"git checkout {branch}")
        print(f"\n...Checked out {branch}")

        print(f"\nPulling branch: {branch}...")
        _run_command(f"git pull origin {branch}")
        print(f"\n...Pulled {branch}")

        if i == 0:
            # There is nothing to merge into the first branch
            continue

        prior_branch = branches[i - 1]
        print(f"\nMerging branch: {prior_branch} into branch: {branch}")
        return_code, _ = _run_command(f"git merge {prior_branch}")
        if return_code != 0:
            print(f"Conflict detected, skipping {branch}")
            conflict_branches.append(branch)
            _run_command("git merge --abort")
            continue
        print(f"\n...Merged branch: {prior_branch} into branch: {branch}")

        print(f"\nPushing branch to remote: {branch}...")
        _run_command(f"git push origin {branch}")
        print(f"\n...Pushed to remote: {branch}")

    # Clean up
    _run_command(f"git checkout {current_branch}")
    print(f"\nBack to original branch: {current_branch}")

    if conflict_branches:
        print(
            "\nThere were conflicts with the following branches. Please manually resolve:"
        )
        for branch in conflict_branches:
            print(branch)
    else:
        print("\nPerformed merging with no conflicts.")


if __name__ == "__main__":
    git_batch_merger()
