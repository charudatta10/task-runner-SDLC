# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

"""Task management module for handling task operations."""

import logging
from pathlib import Path
from typing import List, Dict, Any

from .config import Config
from .utils.file_system import load_json_file, save_json_file


class TaskManager:
    """Manages task operations including creation, retrieval, and updates."""

    def __init__(self, tasks_file: str = None):
        """Initialize TaskManager with specified tasks file.
        
        Args:
            tasks_file: Path to tasks JSON file. Defaults to Config.TASKS_FILE.
        """
        self.tasks_file = tasks_file or Config.TASKS_FILE
        self.logger = logging.getLogger(__name__)

    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file."""
        return load_json_file(self.tasks_file)

    def _save_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Save tasks to JSON file."""
        save_json_file(self.tasks_file, tasks)

    def _get_next_id(self, tasks: List[Dict[str, Any]]) -> int:
        """Generate next available task ID."""
        return max((task.get("id", 0) for task in tasks), default=0) + 1

    def add_task(
        self, title: str, description: str = "", tags: List[str] = None, status: str = "todo"
    ) -> Dict[str, Any]:
        """Add a new task.
        
        Args:
            title: Task title (required)
            description: Task description
            tags: List of task tags
            status: Task status (default: 'todo')
            
        Returns:
            The newly created task dictionary
        """
        tasks = self._load_tasks()
        task = {
            "id": self._get_next_id(tasks),
            "title": title.strip(),
            "description": description.strip(),
            "tags": [tag.strip() for tag in (tags or [])],
            "status": status,
        }
        tasks.append(task)
        self._save_tasks(tasks)
        self.logger.info(f"Task added: {task['title']}")
        return task

    def list_tasks(self, status_filter: str = None) -> List[Dict[str, Any]]:
        """List all tasks, optionally filtered by status.
        
        Args:
            status_filter: Optional status to filter tasks by
            
        Returns:
            List of task dictionaries
        """
        tasks = self._load_tasks()
        if status_filter:
            tasks = [t for t in tasks if t.get("status") == status_filter]
        return tasks

    def get_task(self, task_id: int) -> Dict[str, Any]:
        """Get a specific task by ID.
        
        Args:
            task_id: The task ID to retrieve
            
        Returns:
            Task dictionary or None if not found
        """
        tasks = self._load_tasks()
        return next((t for t in tasks if t.get("id") == task_id), None)

    def update_task(self, task_id: int, **updates) -> bool:
        """Update task fields.
        
        Args:
            task_id: The task ID to update
            **updates: Field names and values to update
            
        Returns:
            True if task was updated, False if not found
        """
        tasks = self._load_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                task.update(updates)
                self._save_tasks(tasks)
                self.logger.info(f"Task updated: {task_id}")
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            task_id: The task ID to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        tasks = self._load_tasks()
        initial_length = len(tasks)
        tasks = [t for t in tasks if t.get("id") != task_id]
        if len(tasks) < initial_length:
            self._save_tasks(tasks)
            self.logger.info(f"Task deleted: {task_id}")
            return True
        return False


# Legacy function wrappers for backward compatibility
_manager = TaskManager()


def add_task():
    """Add a new task (legacy interactive function)."""
    title = input("Title: ")
    description = input("Description: ")
    tags = input("Tags (comma-separated): ").split(",")
    return _manager.add_task(title, description, tags)


def list_tasks():
    """List all tasks (legacy print function)."""
    tasks = _manager.list_tasks()
    for task in tasks:
        print(f"{task['id']}: {task['title']} - {task['status']}")
