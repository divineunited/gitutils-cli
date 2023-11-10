"""
This command cherry picks a commit to a bunch of branches and pushes that change to remote.

It is helpful when:
- you have a chain of PRs where you need to make a change and apply it to the rest of the chain
- you have some changes on your branch and you want to apply it to some shared branches
"""

import subprocess


def _run_command(cmd) -> tuple[int, str]:
    result = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # result.stderr.decode("utf-8"),
    return (result.returncode, result.stdout.decode("utf-8"))


def git_batch_cherry_picker():
    commit = input("Please enter the commit id you would like to batch cherry-pick: ")
    branches = input(
        "Please enter branch names you would like to apply that commit to, in order & separated by commas: "
    ).split(",")
    current_branch = _run_command("git branch --show-current")[1].strip()
    conflict_branches = []

    for branch in branches:
        branch = branch.strip()
        print(f"\nApplying commit to {branch}...")

        _run_command(f"git checkout {branch}")
        print(f"\n...Checked out {branch}")

        _run_command(f"git pull origin {branch}")
        print(f"\n...Pulled {branch}")

        return_code = _run_command(f"git cherry-pick {commit}")
        if return_code != 0:
            print(f"Conflict detected, skipping {branch}")
            conflict_branches.append(branch)
            _run_command("git cherry-pick --abort")
            continue
        print(f"\n...Cherry-picked {commit:} to {branch:}")

        _run_command(f"git push origin {branch}")
        print(f"\n...Pushed to remote: {branch}")

    _run_command(f"git checkout {current_branch}")
    print(f"\nBack to original branch: {current_branch}")

    if conflict_branches:
        print(
            "\nThere were conflicts with the following branches. Please manually resolve:"
        )
        for branch in conflict_branches:
            print(branch)
    else:
        print(f"\nPerformed cherry-picking with no conflicts.")


if __name__ == "__main__":
    git_batch_cherry_picker()
