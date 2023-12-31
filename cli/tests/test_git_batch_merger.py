import unittest
from unittest.mock import call, patch

from cli import git_batch_merger


class TestGitBatchMerger(unittest.TestCase):
    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    def test_git_batch_merger__happy_path(self, mock_input, mock_run_command):
        """Tests the happy path and also shows the print output"""

        # GIVEN:
        # Mock the inputs
        mock_input.side_effect = ["master", "branch1", "branch2", "", "1"]
        # Mock the outputs
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
            (0, ""),  # output for the call to checkout to master
            (0, ""),  # output for the call to pull master
            (0, ""),  # output for the call to checkout to branch1
            (0, ""),  # output for the call to pull branch1
            (0, ""),  # output for the call to merge master into branch1
            (0, ""),  # output for the call to push branch1
            (0, ""),  # output for the call to checkout to branch2
            (0, ""),  # output for the call to pull branch2
            (0, ""),  # output for the call to merge branch1 into branch2
            (0, ""),  # output for the call to push branch2
            (0, ""),  # output for the call to checkout to the original branch
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        # Assert that the mock functions were called with the correct arguments
        assert mock_input.call_args_list == [
            call(
                "Please enter the first branch name or press ENTER for default of current branch: "
            ),
            call("Please enter the next branch name or press ENTER to finish: "),
            call("Please enter the next branch name or press ENTER to finish: "),
            call("Please enter the next branch name or press ENTER to finish: "),
            call(
                "\nChoose how you want to pull other branches onto your local: \n1. [Default] Rebase local changes onto remote before applying changes. Press ENTER or Input 1 to choose this. \n2. Reset to remote before applying changes. Input 2 to choose this. \n3. Input h or help to learn more about these commands.\n"
            ),
        ]

        assert mock_run_command.call_args_list == [
            call("git branch --show-current"),
            call("git branch -a"),
            call("git checkout master"),
            call("git pull --rebase origin master"),
            call("git checkout branch1"),
            call("git pull --rebase origin branch1"),
            call("git merge master"),
            call("git push origin branch1"),
            call("git checkout branch2"),
            call("git pull --rebase origin branch2"),
            call("git merge branch1"),
            call("git push origin branch2"),
            call("git checkout master"),
        ]

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__first_branch_does_not_exist(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["foo"]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        mock_print.assert_any_call("Branch foo does not exist. Stopping program.")

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__less_than_2_branches_exits(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["master", ""]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        mock_print.assert_any_call("You must enter at least 2 branches.")

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__duplicate_branches_to_merge(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["", "foo", "bar", "foo", ""]
        mock_run_command.side_effect = [
            (0, "current_branch"),
            (
                0,
                "master\nremotes/origin/foo\nremotes/origin/bar\n",
            ),  # output for the call to get all branches
            (0, "current_branch"),  # empty input, so calls to get current branch
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        user_branches_assertion = ["current_branch", "foo", "bar", "foo"]
        mock_print.assert_any_call(
            f"All the branches you enter must be unique. You entered: {user_branches_assertion}"
        )

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__handles_conflicts__abort_merge(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["master", "branch1", "branch2", "", "2", "No"]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
            (0, ""),  # output for the call to checkout to master
            (0, ""),  # output for the call to fetch origin
            (0, ""),  # output for the call to reset to master
            (0, ""),  # output for the call to checkout to branch1
            (0, ""),  # output for the call to fetch origin
            (0, ""),  # output for the call to reset to branch1
            (0, ""),  # output for the call to merge master into branch1
            (0, ""),  # output for the call to push branch1
            (0, ""),  # output for the call to checkout to branch2
            (0, ""),  # output for the call to fetch origin
            (0, ""),  # output for the call to reset to branch2
            (1, ""),  # output for the CONFLICT call to merge branch1 into branch2
            (0, ""),  # output for the call to git merge --abort for conflict
            (0, ""),  # output for the call to checkout to the original branch
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        assert mock_run_command.call_args_list == [
            call("git branch --show-current"),
            call("git branch -a"),
            call("git checkout master"),
            call("git fetch origin"),
            call("git reset --hard origin/master"),
            call("git checkout branch1"),
            call("git fetch origin"),
            call("git reset --hard origin/branch1"),
            call("git merge master"),
            call("git push origin branch1"),
            call("git checkout branch2"),
            call("git fetch origin"),
            call("git reset --hard origin/branch2"),
            call("git merge branch1"),
            call("git merge --abort"),
            call("git checkout master"),
        ]
        mock_print.assert_any_call(
            "There were conflicts with the following branches. Please manually resolve:"
        )
        mock_print.assert_any_call("branch2")

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__handles_conflicts__merge_override_theirs(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["master", "branch1", "branch2", "", "1", "yes"]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
            (0, ""),  # output for the call to checkout to master
            (0, ""),  # output for the call to pull master
            (0, ""),  # output for the call to checkout to branch1
            (0, ""),  # output for the call to pull branch1
            (0, ""),  # output for the call to merge master into branch1
            (0, ""),  # output for the call to push branch1
            (0, ""),  # output for the call to checkout to branch2
            (0, ""),  # output for the call to pull branch2
            (1, ""),  # output for the CONFLICT call to merge branch1 into branch2
            (0, ""),  # output for the call to git checkout --theirs
            (0, ""),  # output for the call to git add .
            (0, ""),  # output for the call to git commit -m 'resolve conflicts'
            (0, ""),  # output for the call to push branch2
            (0, ""),  # output for the call to checkout to the original branch
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        assert mock_run_command.call_args_list == [
            call("git branch --show-current"),
            call("git branch -a"),
            call("git checkout master"),
            call("git pull --rebase origin master"),
            call("git checkout branch1"),
            call("git pull --rebase origin branch1"),
            call("git merge master"),
            call("git push origin branch1"),
            call("git checkout branch2"),
            call("git pull --rebase origin branch2"),
            call("git merge branch1"),
            call("git checkout --theirs ."),
            call("git add ."),
            call(
                "git commit -m 'Resolved merge conflicts by accepting all changes from branch1'"
            ),
            call("git push origin branch2"),
            call("git checkout master"),
        ]
        mock_print.assert_any_call("Performed command with no conflicts.")

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__protects_from_merging_into_master(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["branch1", "master", ""]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        mock_print.assert_any_call(
            "You cannot merge any branches into main or master. Main or Master can only be merged into other branches."
        )


if __name__ == "__main__":
    unittest.main()
