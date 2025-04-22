from invoke import task, Collection
import logging

@task
def pull(ctx):
    """Pull latest changes"""
    ctx.run("git pull origin main --force")
    logging.info("✅ Git pull successful")

@task
def push(ctx):
    """Push changes"""
    ctx.run("git push -u origin main")
    logging.info("✅ Git push successful")

# Create git namespace
ns = Collection(pull, push)