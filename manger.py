# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt

from invoke import task, Collection
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


@task
def add(
    c,
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


@task
def update(
    c,
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


@task
def delete(c, task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != int(task_id)]
    save_tasks(tasks)
    print(f"Task '{task_id}' deleted successfully")


@task
def search(c, query):
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


@task
def list_tasks(c):
    tasks = load_tasks()
    if tasks:
        for task in tasks:
            print(task)
    else:
        print("No tasks available")


@task
def schedule(c):
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


ns = Collection(add, update, delete, search, list_tasks, schedule, default=add)
ns.name = "manager"

if __name__ == "__main__":
    default(context())
