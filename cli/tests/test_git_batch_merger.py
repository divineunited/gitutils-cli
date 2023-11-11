import unittest
from unittest.mock import call, patch

from cli import git_batch_merger


class TestGitBatchMerger(unittest.TestCase):
    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    def test_git_batch_merger__happy_path(self, mock_input, mock_run_command):
        """Tests the happy path and also shows the print output"""

        # GIVEN:
        # Mock the inputs for the function
        mock_input.side_effect = ["master", "branch1", "branch2", ""]

        # Mock the outputs for the _run_command function
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
                "Please enter the first branch name or press ENTER for default of `master`: "
            ),
            call("Please enter the next branch name or press ENTER to finish: "),
            call("Please enter the next branch name or press ENTER to finish: "),
            call("Please enter the next branch name or press ENTER to finish: "),
        ]

        assert mock_run_command.call_args_list == [
            call("git branch --show-current"),
            call("git branch -a"),
            call("git checkout master"),
            call("git pull origin master"),
            call("git checkout branch1"),
            call("git pull origin branch1"),
            call("git merge master"),
            call("git push origin branch1"),
            call("git checkout branch2"),
            call("git pull origin branch2"),
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
        mock_input.side_effect = ["", ""]
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
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nremotes/origin/foo\nremotes/origin/bar\n",
            ),  # output for the call to get all branches
        ]

        # WHEN:
        git_batch_merger.git_batch_merger()

        # THEN:
        user_branches_assertion = ["master", "foo", "bar", "foo"]
        mock_print.assert_any_call(
            f"All the branches you enter must be unique. You entered: {user_branches_assertion}"
        )


if __name__ == "__main__":
    unittest.main()
