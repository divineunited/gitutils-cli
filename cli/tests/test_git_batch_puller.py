import io
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from cli import git_batch_puller


class TestGitFunctions(unittest.TestCase):

    @patch("subprocess.check_output")
    def test_is_git_directory_true(self, mock_check_output):
        # Setup mock to simulate success
        mock_check_output.return_value = b"Success"

        # Call the function under test
        result = git_batch_puller.is_git_directory("/fake/path")

        # Assert the expected outcome
        self.assertTrue(result)
        mock_check_output.assert_called_with(
            ["git", "-C", "/fake/path", "status"], stderr=subprocess.STDOUT
        )

    @patch("subprocess.check_output")
    def test_is_git_directory_false(self, mock_check_output):
        # Setup mock to simulate failure
        mock_check_output.side_effect = subprocess.CalledProcessError(128, "cmd")

        # Call the function under test
        result = git_batch_puller.is_git_directory("/fake/path")

        # Assert the expected outcome
        self.assertFalse(result)
        mock_check_output.assert_called_with(
            ["git", "-C", "/fake/path", "status"], stderr=subprocess.STDOUT
        )

    @patch("subprocess.check_output")
    def test_get_current_branch(self, mock_check_output):
        # Setup mock to simulate success
        mock_check_output.return_value = b"main\n"

        # Call the function under test
        result = git_batch_puller.get_current_branch("/fake/path")

        # Assert the expected outcome
        self.assertEqual(result, "main")
        mock_check_output.assert_called_with(
            ["git", "-C", "/fake/path", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.STDOUT,
        )

    @patch("subprocess.check_output")
    def test_git_pull_success(self, mock_check_output):
        # Setup mock to simulate success
        mock_check_output.return_value = b"Successful pull\n"

        # Call the function under test
        git_batch_puller.git_pull("/fake/path")

        # Assert the expected outcome
        mock_check_output.assert_called_with(
            ["git", "-C", "/fake/path", "pull"], stderr=subprocess.STDOUT
        )

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("cli.git_batch_puller.is_git_directory")
    @patch("cli.git_batch_puller.get_current_branch")
    @patch("cli.git_batch_puller.git_pull")
    def test_git_batch_puller(
        self,
        mock_git_pull,
        mock_get_current_branch,
        mock_is_git_directory,
        mock_isdir,
        mock_listdir,
    ):
        # Setup mocks
        mock_listdir.return_value = ["repo1", "not_a_repo"]
        mock_isdir.side_effect = [True, False]
        mock_is_git_directory.return_value = True
        mock_get_current_branch.return_value = "main"

        # Redirect stdin to simulate user input using StringIO
        with io.StringIO("\n") as inputs:
            sys.stdin = inputs

            # Call the function under test
            git_batch_puller.git_batch_puller()

        # Assert the expected outcomes
        mock_is_git_directory.assert_called_with(os.path.join(".", "repo1"))
        mock_get_current_branch.assert_called_with(os.path.join(".", "repo1"))
        mock_git_pull.assert_called_once_with(os.path.join(".", "repo1"))


if __name__ == "__main__":
    unittest.main()
