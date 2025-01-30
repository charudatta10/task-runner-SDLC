# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt

# tasks.py

from invoke import task, Collection
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@task
def pull_latest_changes(ctx):
    """Pull the latest changes from the main branch."""
    ctx.run("git pull origin main --force")


@task
def run_unit_tests(ctx):
    """Run unit tests."""
    ctx.run("python -m unittest discover -s tests")


@task
def run_security_checks(ctx):
    """Run security checks with Bandit."""
    ctx.run("bandit -r .")


@task
def run_pylint(ctx):
    """Run Pylint."""
    ctx.run("pylint .")


@task
def run_flake8(ctx):
    """Run Flake8."""
    ctx.run("flake8 .")


@task
def run_black(ctx):
    """Run Black."""
    ctx.run("black .")


@task
def add_changes(ctx):
    """Add changes to Git."""
    ctx.run("git add .")


@task
def commit_changes(ctx, message="Deployment Commit"):
    """Commit changes to Git."""
    ctx.run(f'git commit -m "{message}"')


@task
def push_changes(ctx):
    """Push changes to the main branch."""
    ctx.run("git push -u origin main")


@task(
    pre=[
        pull_latest_changes,
        run_unit_tests,
        run_security_checks,
        run_pylint,
        run_flake8,
        run_black,
        add_changes,
        commit_changes,
        push_changes,
    ]
)
def deploy(ctx, message="Deployment Commit"):
    """
    Perform deployment checks and commit changes.

    Args:
        message (str): The commit message for the deployment.
    """
    logging.info("Deployment checks completed.")


# Create a collection of tasks
ns = Collection(
    pull_latest_changes,
    run_unit_tests,
    run_security_checks,
    run_pylint,
    run_flake8,
    run_black,
    add_changes,
    commit_changes,
    push_changes,
    deploy,
    default=deploy,
)
ns.name = "deploy_checks"

if __name__ == "__main__":
    default(Context())
