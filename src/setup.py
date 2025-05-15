# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from pathlib import Path
import os
from .config import Config
from .utility import download_file


@task
def create_dirs(ctx):
    """Create project directories"""
    for directory in Config.PROJECT_DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")


@task
def create_files(ctx):
    """Create project files"""
    for file in Config.PROJECT_FILES:
        Path(file).touch()
        logging.info(f"Created file: {file}")


@task
def get_community_files(ctx):
    """Download community files"""
    for file in Config.COMMUNITY_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", file):
            logging.info(f"Downloaded community file: {file}")


@task
def init_uv(ctx):
    """Initialize the project uv environment"""
    ctx.run("uv init")


@task(
    create_dirs,
    create_files,
    get_community_files,
    init_uv,
)
def init_new(ctx):
    """Initialize the project new environment"""
    logging.info("Project initialized successfully.")


ns = Collection(create_files, create_dirs, get_community_files, init_uv, init_new)
