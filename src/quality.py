# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from .config import Config
from .utility import run_command

@task
def tests(ctx):
    """Run unit tests"""
    run_command(ctx, "python -m unittest discover -s tests", "Tests passed", "Tests failed")

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
def format(ctx):
    """Format code with black"""
    run_command(ctx, "black .", "Code formatted", "Formatting failed")

# Create quality namespace
ns = Collection(lint, flake8, format, tests, security)
