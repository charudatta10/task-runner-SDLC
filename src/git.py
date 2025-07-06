from invoke import task, Collection
from .utility import run_command

@task
def init_repo(ctx):
    """Initialize git repo"""
    run_command(ctx, "git init", "Git repo initialized", "Git init failed")

@task
def commit_changes(ctx, message="Deployment Commit"):
    """Stage, commit, and push changes"""
    run_command(ctx, "git add .", "Changes staged", "Failed to stage changes")
    run_command(ctx, f'git commit -m "{message}"', "Changes committed", "Commit failed")
    run_command(ctx, "git push -u origin main", "Changes pushed", "Push failed")

ns = Collection(init_repo, commit_changes)
