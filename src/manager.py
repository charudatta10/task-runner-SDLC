from invoke import task, Collection
import os
import logging
from .config import Config
from .utility import load_json_file, save_json_file, run_command
from pathlib import Path
import zipfile


@task
def package(ctx):
    """Package the project"""
    project_dir = Path(Config.CODE_DIR)
    output_file = project_dir / "ypp.zip"

    # Ensure main script exists
    main_script = project_dir / "__main__.py"
    if not main_script.exists():
        main_script.write_text("print('hello world')\n")

    # Create zip archive
    with zipfile.ZipFile(output_file, "w") as zipf:
        for file_path in project_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(".zip"):
                zipf.write(file_path, file_path.relative_to(project_dir))

    logging.info(f"Package created: {output_file}")


# ========== Task Management ==========
@task
def add_task(ctx):
    """Add a new task"""
    tasks = load_json_file(Config.TASKS_FILE)
    task = {
        "id": len(tasks) + 1,
        "title": input("Title: "),
        "description": input("Description: "),
        "tags": input("Tags (comma-separated): ").split(","),
        "status": "todo",
    }
    tasks.append(task)
    save_json_file(Config.TASKS_FILE, tasks)
    logging.info(f"Task added: {task['title']}")


@task
def list_tasks(ctx):
    """List all tasks"""
    tasks = load_json_file(Config.TASKS_FILE)
    for task in tasks:
        print(f"{task['id']}: {task['title']} - {task['status']}")


@task(default=True)
def main(ctx):
    """List all tasks"""
    run_command(
        ctx, "inv --list", "To select command type invoke again and cmd", "fail"
    )


# Create manager namespace
ns = Collection(package, add_task, list_tasks, main)
