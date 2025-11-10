import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from src.tools.clone_github_repos import clone_github_repos


class TestCloneGithubRepos(unittest.TestCase):
    @patch("json.loads")
    @patch("builtins.print")
    def test_clone_github_repos(self, mock_print, mock_json_loads):
        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()
        ctx.run.return_value.stdout = "mocked json output"

        mock_json_loads.return_value = [
            {"nameWithOwner": "user/repo1"},
            {"nameWithOwner": "user/repo2"},
        ]

        clone_github_repos.body(ctx, source_user="test_user")

        ctx.run.assert_has_calls(
            [
                call("gh repo list --source test_user --json nameWithOwner"),
                call("gh repo clone user/repo1"),
                call("gh repo clone user/repo2"),
            ]
        )
        mock_print.assert_has_calls(
            [
                call("Cloned repository: user/repo1"),
                call("Cloned repository: user/repo2"),
                call("Cloned all repositories from GitHub user: test_user."),
            ]
        )


if __name__ == "__main__":
    unittest.main()
