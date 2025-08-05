import unittest
from unittest.mock import MagicMock, call
from invoke import Context
from src.git import init_repo, commit_changes

class TestGit(unittest.TestCase):
    def test_init_repo(self):
        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()
        init_repo(ctx)
        ctx.run.assert_called_once_with("git init")

    def test_commit_changes(self):
        ctx = MagicMock(spec=Context)
        ctx.run = MagicMock()
        message = "Test Commit"
        commit_changes(ctx, message=message)
        calls = [
            call("git pull origin main"),
            call("git add ."),
            call(f'git commit -m "{message}"'),
            call("git push -u origin main"),
        ]
        ctx.run.assert_has_calls(calls)

if __name__ == "__main__":
    unittest.main()