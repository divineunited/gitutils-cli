"""Safely keep all your branches up to date with Remote"""

import os
import subprocess


def is_git_directory(path: str) -> bool:
    """Check if the path is a git repository."""
    try:
        subprocess.check_output(["git", "-C", path, "status"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_branch(path: str) -> str:
    """Get the current branch name of a git repository."""
    try:
        branch = (
            subprocess.check_output(
                ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.STDOUT,
            )
            .strip()
            .decode("utf-8")
        )
        return branch
    except subprocess.CalledProcessError:
        return None


def git_pull(path):
    """Perform a git pull in the given directory."""
    try:
        # Execute git pull and capture output
        output = subprocess.check_output(
            ["git", "-C", path, "pull"], stderr=subprocess.STDOUT
        )
        print(f"✅ Successfully pulled latest changes in {path}")
        print(f"Output for {path}:\n{output.decode('utf-8')}")
    except subprocess.CalledProcessError as e:
        print(f"🤔 Failed to pull latest changes in {path}: {e}\n")


def git_batch_puller():
    """Main entrypoint to the git batch puller"""

    # Display helper text and ask for confirmation
    print("This script will update all git repositories in the current directory.")
    print("\nIt will only check directories one level down")
    print("and assumes there are no git repositories nested within sub-directories.")
    print("\nPress 'Y' or 'Enter' to continue, or any other key to exit.")
    confirmation = input().strip().lower()
    if confirmation != "" and confirmation != "y":
        print("Exiting script.")
        exit()

    # Iterate through subdirectories
    items = os.listdir(".")
    for item in items:
        full_path = os.path.join(".", item)

        # Check if it's a directory
        if os.path.isdir(full_path):
            # Check if it's a git repository
            if is_git_directory(full_path):
                branch = get_current_branch(full_path)
                if branch in ["main", "master"]:
                    git_pull(full_path)
                else:
                    print(f"🤔 Skipping {full_path}: Not on main or master branch.\n")
            else:
                print(f"🤔 Skipping {full_path}: Not a git repository.\n")

    print("🚀 git batch pull completed.")


if __name__ == "__main__":
    git_batch_puller()
