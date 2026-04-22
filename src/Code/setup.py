# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
from pathlib import Path
import os
from .config import Config
from .utils.web import download_file
import subprocess


def init_project():
    """Initialize the project: create dirs, files, download community files, and init uv env."""
    # Create directories
    for directory in Config.PROJECT_DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

    # Create files
    for file in Config.PROJECT_FILES:
        Path(file).touch()
        logging.info(f"Created file: {file}")

    # Download community files
    for file in Config.COMMUNITY_FILES:
        if download_file(f"{Config.REPO_DOCS}/{Path(file).name}", file):
            logging.info(f"Downloaded community file: {file}")

    # Initialize uv environment
    try:
        subprocess.run(["uv", "init"], check=True)
        logging.info("Initialized uv environment.")
    except subprocess.CalledProcessError as e:
        logging.error(f"uv init failed: {e}")
    logging.info("Project initialized successfully.")
