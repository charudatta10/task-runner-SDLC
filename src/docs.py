from invoke import task, Collection
import logging
from pathlib import Path
import os 

@task
def setup_docs(ctx):
    """Setup documentation"""
    for file in Config.DOCS_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", f"docs/{file}"):
            logging.info(f"Downloaded docs file: {file}")

ns = Collection(setup_docs)