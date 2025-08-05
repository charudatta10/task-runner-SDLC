# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

from invoke import task, Collection
import logging
from .utility import run_command

@task
def lint(ctx):
    """Run all linting and formatting checks"""
    run_command(ctx, "pylint .", "Pylint passed", "Pylint failed")
    run_command(ctx, "flake8 .", "Flake8 passed", "Flake8 failed")
    run_command(ctx, "black .", "Code formatted", "Formatting failed")

@task
def run_tests(ctx):
    """Run unit tests and measure coverage"""
    run_command(ctx, "pytest --cov=src --cov-report=term-missing", "Tests passed", "Tests failed")

@task
def security(ctx):
    """Run security checks"""
    run_command(ctx, "bandit -r .", "Security checks passed", "Security checks failed")

@task(lint, run_tests, security)
def quality_checks(ctx):
    """Run all quality checks"""
    logging.info("All quality checks completed.")

ns = Collection(lint, run_tests, security, quality_checks)
