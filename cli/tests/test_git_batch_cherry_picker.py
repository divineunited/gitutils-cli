import unittest
from unittest.mock import call, patch

from cli import git_batch_cherry_picker


class TestGitBatchCherryPicker(unittest.TestCase):
    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    def test_git_batch_cherry_picker__happy_path(self, mock_input, mock_run_command):
        """Tests the happy path and also shows the print output"""

        # GIVEN:
        # Mock the inputs for the function
        mock_input.side_effect = ["foo_commit", "branch0", "branch1", ""]

        # Mock the outputs for the _run_command function
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "branch0\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
            (0, ""),  # output for the call to git rev-parse the commit
            (0, ""),  # output for the call to checkout to branch0
            (0, ""),  # output for the call to pull branch0
            (0, ""),  # output for the call to cherry-pick to branch0
            (0, ""),  # output for the call to push branch0
            (0, ""),  # output for the call to checkout to branch1
            (0, ""),  # output for the call to pull branch1
            (0, ""),  # output for the call to cherry-pick to branch1
            (0, ""),  # output for the call to push branch1
            (0, ""),  # output for the call to checkout to the original branch
        ]

        # WHEN:
        git_batch_cherry_picker.git_batch_cherry_picker()

        # THEN:
        # Assert that the mock functions were called with the correct arguments
        assert mock_input.call_args_list == [
            call("Please enter the commit id you would like to batch cherry-pick: "),
            call(
                "Please enter the first branch name or press ENTER for default of current branch: "
            ),
            call("Please enter the next branch name or press ENTER to finish: "),
            call("Please enter the next branch name or press ENTER to finish: "),
        ]

        assert mock_run_command.call_args_list == [
            call("git branch --show-current"),
            call("git branch -a"),
            call("git rev-parse foo_commit"),
            call("git checkout branch0"),
            call("git pull origin branch0"),
            call("git cherry-pick foo_commit"),
            call("git push origin branch0"),
            call("git checkout branch1"),
            call("git pull origin branch1"),
            call("git cherry-pick foo_commit"),
            call("git push origin branch1"),
            call("git checkout master"),
        ]

    @patch("cli_utils.utils.run_git_command")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_git_batch_merger__protects_from_cherry_picking_to_master(
        self, mock_print, mock_input, mock_run_command
    ):
        # GIVEN:
        mock_input.side_effect = ["foo_commit", "branch1", "master", ""]
        mock_run_command.side_effect = [
            (0, "master"),  # output for the first call to get the current branch
            (
                0,
                "master\nbranch1\nbranch2\n",
            ),  # output for the call to get all branches
            (0, ""),  # output for the call to git rev-parse the commit
        ]

        # WHEN:
        git_batch_cherry_picker.git_batch_cherry_picker()

        # THEN:
        mock_print.assert_any_call(
            "You cannot cherry-pick into `master` or `main` branches. Exiting."
        )


if __name__ == "__main__":
    unittest.main()
