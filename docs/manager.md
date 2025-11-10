# Module: `manager`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\manager.py`
**Language:** Python

## Description

Task management module for handling task operations.

## Imports

- `import logging`
- `from pathlib import Path`
- `from typing import List`
- `from typing import Dict`
- `from typing import Any`
- `from config import Config`
- `from utils.file_system import load_json_file`
- `from utils.file_system import save_json_file`

## Functions

### `add_task()`

Add a new task (legacy interactive function).

### `list_tasks()`

List all tasks (legacy print function).

## Classes

## Class: `TaskManager`

Manages task operations including creation, retrieval, and updates.

### Methods

### `__init__(self, tasks_file: str = None)`

Initialize TaskManager with specified tasks file.

Args:
tasks_file: Path to tasks JSON file. Defaults to Config.TASKS_FILE.

#### Parameters

- **`self`**
- **`tasks_file`** *(str)* — defaults to `None`

### `_get_next_id(self, tasks: List[Dict[(str, Any)]]) -> int`

Generate next available task ID.

#### Parameters

- **`self`**
- **`tasks`** *(List[Dict[(str, Any)]])*

#### Returns

- `int`

### `_load_tasks(self) -> List[Dict[(str, Any)]]`

Load tasks from JSON file.

#### Parameters

- **`self`**

#### Returns

- `List[Dict[(str, Any)]]`

### `_save_tasks(self, tasks: List[Dict[(str, Any)]]) -> None`

Save tasks to JSON file.

#### Parameters

- **`self`**
- **`tasks`** *(List[Dict[(str, Any)]])*

#### Returns

- `None`

### `add_task(self, title: str, description: str = '', tags: List[str] = None, status: str = 'todo') -> Dict[(str, Any)]`

Add a new task.

Args:
title: Task title (required)
description: Task description
tags: List of task tags
status: Task status (default: 'todo')

Returns:
The newly created task dictionary

#### Parameters

- **`self`**
- **`title`** *(str)*
- **`description`** *(str)* — defaults to `''`
- **`tags`** *(List[str])* — defaults to `None`
- **`status`** *(str)* — defaults to `'todo'`

#### Returns

- `Dict[(str, Any)]`

### `delete_task(self, task_id: int) -> bool`

Delete a task by ID.

Args:
task_id: The task ID to delete

Returns:
True if task was deleted, False if not found

#### Parameters

- **`self`**
- **`task_id`** *(int)*

#### Returns

- `bool`

### `get_task(self, task_id: int) -> Dict[(str, Any)]`

Get a specific task by ID.

Args:
task_id: The task ID to retrieve

Returns:
Task dictionary or None if not found

#### Parameters

- **`self`**
- **`task_id`** *(int)*

#### Returns

- `Dict[(str, Any)]`

### `list_tasks(self, status_filter: str = None) -> List[Dict[(str, Any)]]`

List all tasks, optionally filtered by status.

Args:
status_filter: Optional status to filter tasks by

Returns:
List of task dictionaries

#### Parameters

- **`self`**
- **`status_filter`** *(str)* — defaults to `None`

#### Returns

- `List[Dict[(str, Any)]]`

### `update_task(self, task_id: int, **updates) -> bool`

Update task fields.

Args:
task_id: The task ID to update
**updates: Field names and values to update

Returns:
True if task was updated, False if not found

#### Parameters

- **`self`**
- **`task_id`** *(int)*
- **`**updates`**

#### Returns

- `bool`

---
