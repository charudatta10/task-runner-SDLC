from invoke import task, Collection
import logging

@task
def lint(ctx):
    """Run pylint checks"""
    ctx.run("pylint .")
    logging.info("✅ Linting complete")

@task
def format(ctx):
    """Format code with black"""
    ctx.run("black .")
    logging.info("✅ Code formatted")

# Create quality namespace
ns = Collection(lint, format)