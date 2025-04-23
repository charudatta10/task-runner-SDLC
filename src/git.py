# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from .config import Config
from .utility import run_command


@task
def pull(ctx):
    """Pull latest changes"""
    run_command(ctx, "git pull origin main --force", "Pulled latest changes", "Pull failed")

@task
def add(ctx):
    """Stage all changes"""
    run_command(ctx, "git add .", "Changes staged", "Failed to stage changes")

@task
def commit(ctx, message="Deployment Commit"):
    """Commit changes"""
    run_command(ctx, f'git commit -m "{message}"', "Changes committed", "Commit failed")

@task
def push(ctx):
    """Push changes"""
    run_command(ctx, "git push -u origin main", "Changes pushed", "Push failed")

@task
def init(ctx):
    """Initialize git repo"""
    run_command(ctx, "git init", "Git repo initialized", "Git init failed")

# Create git namespace
ns = Collection(pull, push, add, commit, init)