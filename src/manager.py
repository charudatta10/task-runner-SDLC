from invoke import task, Collection
import logging
from .config import Config
from .utility import load_json_file, save_json_file, run_command


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
ns = Collection(add_task, list_tasks, main)
