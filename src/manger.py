# tasks.py

import json
import os
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(
    title,
    description="",
    tags="",
    subtasks="",
    deadline="",
    priority="",
    repeat="",
    status="Todo",
):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "tags": tags.split(","),
        "subtasks": subtasks.split(","),
        "deadline": deadline,
        "priority": priority,
        "repeat": repeat,
        "status": status,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added successfully")


def update_task(
    task_id,
    title=None,
    description=None,
    tags=None,
    subtasks=None,
    deadline=None,
    priority=None,
    repeat=None,
    status=None,
):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == int(task_id):
            if title:
                task["title"] = title
            if description:
                task["description"] = description
            if tags:
                task["tags"] = tags.split(",")
            if subtasks:
                task["subtasks"] = subtasks.split(",")
            if deadline:
                task["deadline"] = deadline
            if priority:
                task["priority"] = priority
            if repeat:
                task["repeat"] = repeat
            if status:
                task["status"] = status
            save_tasks(tasks)
            print(f"Task '{task_id}' updated successfully")
            return
    print(f"Task '{task_id}' not found")


def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != int(task_id)]
    save_tasks(tasks)
    print(f"Task '{task_id}' deleted successfully")


def search_tasks(query):
    tasks = load_tasks()
    results = [
        task
        for task in tasks
        if query.lower() in task["title"].lower()
        or query.lower() in task["description"].lower()
    ]
    if results:
        for task in results:
            print(task)
    else:
        print("No tasks found")


def list_tasks():
    tasks = load_tasks()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("No tasks available")


def schedule_tasks():
    tasks = load_tasks()
    now = datetime.now()
    for task in tasks:
        if task["repeat"]:
            repeat_days = int(task["repeat"])
            deadline_date = datetime.strptime(task["deadline"], "%Y-%m-%d")
            while deadline_date < now:
                deadline_date += timedelta(days=repeat_days)
            task["deadline"] = deadline_date.strftime("%Y-%m-%d")
    save_tasks(tasks)
    print("Tasks scheduled successfully")


# Command mapping
commands = {
    "add": add_task,
    "update": update_task,
    "delete": delete_task,
    "search": search_tasks,
    "list": list_tasks,
    "schedule": schedule_tasks,
}


# Display available commands
def display_commands():
    print("Available commands:")
    for index, name in enumerate(commands.keys()):
        print(f"{index}: {name}")


def main():
    display_commands()

    user_input = input("Enter the command name to run: ").strip()

    if user_input in commands:
        command = commands[user_input]

        if user_input == "add":
            title = input("Title: ")
            description = input("Description: ")
            tags = input("Tags (comma-separated): ")
            subtasks = input("Subtasks (comma-separated): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            priority = input("Priority: ")
            repeat = input("Repeat (days): ")
            status = input("Status: ")
            command(
                title, description, tags, subtasks, deadline, priority, repeat, status
            )

        elif user_input == "update":
            task_id = input("Task ID: ")
            title = input("Title: ")
            description = input("Description: ")
            tags = input("Tags (comma-separated): ")
            subtasks = input("Subtasks (comma-separated): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            priority = input("Priority: ")
            repeat = input("Repeat (days): ")
            status = input("Status: ")
            command(
                task_id,
                title,
                description,
                tags,
                subtasks,
                deadline,
                priority,
                repeat,
                status,
            )

        elif user_input == "delete":
            task_id = input("Task ID: ")
            command(task_id)

        elif user_input == "search":
            query = input("Search query: ")
            command(query)

        else:
            command()
    else:
        print(f"Invalid command: {user_input}")


if __name__ == "__main__":
    main()
