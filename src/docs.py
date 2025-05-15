# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import logging
from .config import Config
from .utility import download_file, generate_file
from pathlib import Path


def collect_items(prompt, formatter):
    items = []
    print(f"{prompt} (Type 'done' to finish):")
    while True:
        item = input("- ")
        if item.lower() == "done":
            break
        formatted_item = f"- {item}" if formatter == "list_features" else f"`{item}`"
        items.append(formatted_item)
    return "\n".join(items) if formatter == "list_features" else " ".join(items)


@task
def setup_docs(ctx):
    """Setup documentation"""
    data = collect_project_data()
    logging.info("README file input parsed successfully.")
    for file in Config.DOCS_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", f"docs/{file}"):
            logging.info(f"Downloaded docs file: {file}")
            generate_file(
                template_path=f"docs/{file}", config=data, output_path=f"docs/{file}"
            )


def collect_project_data():
    """Collect project data from user input."""
    return {
        "title": input("Enter title of project -> "),
        "description": input("Enter project description -> "),
        "features": collect_items("Enter project features -> ", "list_features"),
        "list_badges": collect_items(
            "Enter softwares used in the project -> ", "list_badges"
        ),
    }


@task
def generate_docs(ctx):
    """Generate documentation"""
    ctx.run(
        f"python {Path.home() / "Home" / "Github" / "ai-doc-gen" / "src" / "main.py"} ."
    )


ns = Collection(setup_docs, generate_docs)
