# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from pathlib import Path
import os 
from .config import Config
from .utility import download_file, generate_file

def generate_files():
    """Generate a README file based on user input and a template."""
    # Step 1: Collect data
    data = {
        "title": input("Enter title of project -> "),
        "description": input("Enter project description -> "),
    }
    logging.info("README file input parsed successfully.")
    # Step 2: Format and write the README file
    print(data)
    generate_file(template_path="docs/_coverpage.md", config=data, output_path="docs/_coverpage.md")
    logging.info("README file generated successfully.")

@task
def setup_docs(ctx):
    """Setup documentation"""
    for file in Config.DOCS_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", f"docs/{file}"):
            logging.info(f"Downloaded docs file: {file}")
    generate_files()






ns = Collection(setup_docs)