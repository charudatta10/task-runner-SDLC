# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from .utility import run_command


@task
def tests(ctx):
    """Run unit tests"""
    run_command(
        ctx, "python -m unittest discover -s tests", "Tests passed", "Tests failed"
    )


@task
def security(ctx):
    """Run security checks"""
    run_command(ctx, "bandit -r .", "Security checks passed", "Security checks failed")


@task
def lint(ctx):
    """Run pylint checks"""
    run_command(ctx, "pylint .", "Linting passed", "Linting failed")


@task
def flake8(ctx):
    """Run flake8 checks"""
    run_command(ctx, "flake8 .", "Flake8 passed", "Flake8 failed")


@task
def lint_exec(ctx):
    """Format code with black"""
    run_command(ctx, "black .", "Code formatted", "Formatting failed")


@task(
    lint,
    flake8,
    lint_exec,
    tests,
    security,
)
def quality_checks(ctx):
    """Run all quality checks"""
    logging.info("All quality checks completed.")


# Create quality namespace
ns = Collection(lint, flake8, lint_exec, tests, security, quality_checks)
