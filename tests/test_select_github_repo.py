import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from pathlib import Path
import os
from src.tools.select_github_repo import select_github_repo


class TestSelectGithubRepo(unittest.TestCase):
    @patch("pathlib.Path.iterdir")
    @patch("builtins.input", side_effect=["1", "my_task"])
    @patch("builtins.print")
    def test_select_github_repo(self, mock_print, mock_input, mock_iterdir):
        # Mocking Path objects for iterdir
        mock_dir1 = MagicMock()
        mock_dir1.name = "repo1"
        mock_dir1.is_dir.return_value = True
        mock_dir2 = MagicMock()
        mock_dir2.name = "repo2"
        mock_dir2.is_dir.return_value = True
        mock_iterdir.return_value = [mock_dir1, mock_dir2]

        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()

        base_path = "/test/path"
        selected_repo_path = os.path.normpath(os.path.join(base_path, "repo1"))

        select_github_repo.body(ctx, base_path=base_path)

        mock_print.assert_has_calls(
            [
                call("Select a GitHub Repository:"),
                call("1. repo1"),
                call("2. repo2"),
            ]
        )
        ctx.run.assert_has_calls(
            [
                call(f"poe -C {selected_repo_path} --list"),
                call(f"poe -C {selected_repo_path} my_task"),
            ]
        )


if __name__ == "__main__":
    unittest.main()
