import unittest
from unittest.mock import patch, MagicMock, call
from invoke import Context
from src.quality import lint, run_tests, security, quality_checks


class TestQuality(unittest.TestCase):
    @patch("src.quality.run_command")
    def test_lint(self, mock_run_command):
        ctx = MagicMock(spec=Context)
        lint.body(ctx)
        calls = [
            call(ctx, "pylint .", "Pylint passed", "Pylint failed"),
            call(ctx, "flake8 .", "Flake8 passed", "Flake8 failed"),
            call(ctx, "black .", "Code formatted", "Formatting failed"),
        ]
        mock_run_command.assert_has_calls(calls)

    @patch("src.quality.run_command")
    def test_run_tests(self, mock_run_command):
        ctx = MagicMock(spec=Context)
        run_tests.body(ctx)
        mock_run_command.assert_called_once_with(
            ctx,
            "pytest --cov=src --cov-report=term-missing",
            "Tests passed",
            "Tests failed",
        )

    @patch("src.quality.run_command")
    def test_security(self, mock_run_command):
        ctx = MagicMock(spec=Context)
        security.body(ctx)
        mock_run_command.assert_called_once_with(
            ctx, "bandit -r .", "Security checks passed", "Security checks failed"
        )


if __name__ == "__main__":
    unittest.main()
