from invoke import task, Collection
import logging
from pathlib import Path
import os 

class Config:
    pass

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return False

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
def setup_docs(ctx):
    """Setup documentation"""
    for file in Config.DOCS_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", f"docs/{file}"):
            logging.info(f"Downloaded docs file: {file}")

@task
def get_community_files(ctx):
    """Download community files"""
    for file in Config.COMMUNITY_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", file):
            logging.info(f"Downloaded community file: {file}")

ns = Collection(create_files, create_dirs, get_community_files)