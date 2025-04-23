# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import os
import logging
from .config import Config
from .utility import download_file

@task
def generate_readme(ctx):
    """Generate a README file based on user input and a template."""
    download_file(Config.REPO_DOCS + "/template.md", "README.md")
    logging.info("README file downloaded successfully.")
    with open("README.md", "r", encoding="utf-8") as file:
        template_content = file.read()
    logging.info("README file opened successfully.")
    # Step 2: Helper functions to collect user input
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
    # Step 3: Collect data
    data = {
        "title": input("Enter title of project -> "),
        "description": input("Enter project description -> "),
        "features": collect_items("Enter project features -> ", "list_features"),
        "list_badges": collect_items("Enter softwares used in the project -> ", "list_badges"),
    }
    logging.info("README file input parsed successfully.")
    # Step 4: Format and write the README file
    readme_content = template_content.format(
        title=data.get("title", "Untitled Project"),
        description=data.get("description", "No description provided."),
        features=data.get("features", ""),
        list_badges=data.get("list_badges", "")
    )
    logging.info("README file text generated successfully.")
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)
    
    logging.info("README file generated successfully.")

@task
def ppt_gen(ctx):
    """Generate a presentation file based on README content."""
    # Read the content of the README file
    if not os.path.exists("README.md"):
        logging.error("README.md file not found. Please generate it first.")
        return

    with open("README.md", "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    # Prepare the presentation content
    file_content = f"""---
marp: true
headingDivider: 6
theme: gaia
---

{readme_content}"""

    # Write the content to a new presentation file
    with open("readmex.md", "w+", encoding="utf-8") as presentation_file:
        presentation_file.write(file_content)

    logging.info("Presentation file 'readmex.md' generated successfully.")


# Create license namespace
ns = Collection(generate_readme, ppt_gen)