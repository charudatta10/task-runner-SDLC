# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode


from .utility import run_command


def init_repo():
    """Initialize git repo"""
    run_command("git init", "Git repo initialized", "Git init failed")


def commit_changes(ctx, message="Deployment Commit"):
    """Stage, commit, and push changes"""
    run_command(ctx, "git pull origin main", "Pulled latest changes", "Pull failed")
    run_command(ctx, "git add .", "Changes staged", "Failed to stage changes")
    run_command(ctx, f'git commit -m "{message}"', "Changes committed", "Commit failed")
    run_command(ctx, "git push -u origin main", "Changes pushed", "Push failed")


