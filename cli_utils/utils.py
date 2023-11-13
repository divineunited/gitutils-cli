"""Utility functions"""

import subprocess


class ConflictHandleScenario:
    Abort = "Abort"
    Theirs = "Theirs"


def run_git_command(cmd: str) -> tuple[int, str]:
    """Run a GIT subprocess command in a users terminal"""
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # result.stderr.decode("utf-8"),
    return (result.returncode, result.stdout.decode("utf-8"))


def get_current_branch() -> str:
    return run_git_command("git branch --show-current")[1].strip()


def get_all_remote_branches_set() -> set[str]:
    """Return a set of all remote branches that are available in this repo"""
    all_branches_raw = run_git_command("git branch -a")[1].split("\n")
    # The raw branches look like: remotes/origin/actual-branch-name
    all_branches = [
        branch.replace("remotes/origin/", "").strip() for branch in all_branches_raw
    ]
    return set(all_branches)


def get_input_commit_from_user() -> str | None:
    """Gets a commit from a user and verifies it"""
    commit = input("Please enter the commit id you would like to batch cherry-pick: ")
    return_code, _ = run_git_command(f"git rev-parse {commit}")
    if return_code != 0:
        print(f"Commit {commit} does not exist. Stopping program.")
        return None
    return commit


def get_input_branches_from_user(
    remote_branches: set[str],
    allow_only_one_input_branch: bool = False,
) -> list[str] | None:
    """Gets branches from user and checks that those branches are legit."""
    branches = []
    first_branch = input(
        "Please enter the first branch name or press ENTER for default of current branch: "
    ).strip()
    if not first_branch:
        first_branch = get_current_branch()
        print(f"Using the current branch as the first branch: {first_branch}")
    elif first_branch not in remote_branches:
        print(f"Branch {first_branch} does not exist. Stopping program.")
        return None
    branches.append(first_branch)

    while True:
        branch = input(
            "Please enter the next branch name or press ENTER to finish: "
        ).strip()

        if not branch:
            break

        if branch not in remote_branches:
            print(f"Branch {branch} does not exist. Skipping...")
            continue

        branches.append(branch)

    if len(branches) < 2 and not allow_only_one_input_branch:
        print("You must enter at least 2 branches.")
        return None

    if len(branches) != len(set(branches)):
        print(f"All the branches you enter must be unique. You entered: {branches}")
        return None

    return branches


def checkout_and_pull_branch(branch: str) -> None:
    """Git checkout and pull branch from remote"""
    print(f"Checking out branch: {branch}...")
    run_git_command(f"git checkout {branch}")
    print(f"...Checked out {branch}")

    print(f"Pulling branch: {branch}...")
    run_git_command(f"git pull origin {branch}")
    print(f"...Pulled {branch}")


def push_branch_to_remote(branch: str) -> None:
    """Git push branch to remote"""
    print(f"Pushing branch to remote: {branch}...")
    run_git_command(f"git push origin {branch}")
    print(f"...Pushed to remote: {branch}")


def handle_conflicts(
    prior_branch: str, current_branch: str, conflict_branches: list[str]
) -> ConflictHandleScenario:
    """
    Git conflict handler. Mutates a list of conflict_branches
    and returns ConflictHandleScenario decision
    """
    print(f"Conflict detected: {current_branch}")

    decision = input(
        f"Do you want to override changes from the current branch: {current_branch} with changes from prior branch {prior_branch}? \nType 'yes' if you are sure. \nENTER to safely ignore this conflict. \nor CTRL+C to stop program: "
    )

    conflict_decision = None

    if decision.strip().lower() == "yes":
        print("...Handling conflicts using the --theirs strategy.")
        run_git_command("git checkout --theirs .")
        print("...adding prior branch changes.")
        run_git_command("git add .")
        print(
            "...commiting changes. This might take a while if you have pre-commit running."
        )
        run_git_command(
            f"git commit -m 'Resolved merge conflicts by accepting all changes from {prior_branch}'"
        )
        print("...changes commited!")
        conflict_decision = ConflictHandleScenario.Theirs
    else:
        conflict_branches.append(current_branch)
        run_git_command("git merge --abort")
        conflict_decision = ConflictHandleScenario.Abort

    assert conflict_decision
    return conflict_decision


def perform_clean_up(original_branch: str, conflict_branches: list[str]) -> None:
    """Checks out the original branch and prints any conflicting branches to user"""
    run_git_command(f"git checkout {original_branch}")
    print(f"Back to original branch: {original_branch}")

    if conflict_branches:
        print(
            "There were conflicts with the following branches. Please manually resolve:"
        )
        for branch in conflict_branches:
            print(branch)
    else:
        print("Performed command with no conflicts.")
