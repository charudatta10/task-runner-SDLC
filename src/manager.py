# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
from .config import Config
from .utility import load_json_file, save_json_file, run_command


def add_task():
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


def list_tasks():
    """List all tasks"""
    tasks = load_json_file(Config.TASKS_FILE)
    for task in tasks:
        print(f"{task['id']}: {task['title']} - {task['status']}")


# Create manager namespace
