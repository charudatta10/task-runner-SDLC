# Module: `generate_system_reports`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\tools\generate_system_reports.py`
**Language:** Python

## Imports

- `from invoke import task`
- `import os`
- `import shutil`
- `import json`
- `import platform`
- `import subprocess`
- `from pathlib import Path`
- `from datetime import datetime`
- `import logging`
- `from config import Config`
- `from utils.logger import setup_logging`

## Functions

### `check_tool_availability(tool_name)`

Check if a tool is available in the system PATH

#### Parameters

- **`tool_name`**

### `copy_file_safe(source, destination, description = '')`

Safely copy a file with error handling

#### Parameters

- **`source`**
- **`destination`**
- **`description`** — defaults to `''`

### `generate_system_reports(ctx, destination_folder = None, include_optional = False)`

**Decorators:** @task

Generate comprehensive system reports and copy configuration files.

Args:
destination_folder (str): Destination folder for reports (default: Config.BACKUP_DIR)
include_optional (bool): Include optional/experimental package managers

#### Parameters

- **`ctx`**
- **`destination_folder`** — defaults to `None`
- **`include_optional`** — defaults to `False`

### `list_system_tools(ctx)`

**Decorators:** @task

List available system package managers and tools.

#### Parameters

- **`ctx`**

### `quick_backup(ctx, destination_folder = None)`

**Decorators:** @task

Quick backup of essential system configurations.
Only backs up core package managers and essential config files.

#### Parameters

- **`ctx`**
- **`destination_folder`** — defaults to `None`

### `run_command_safe(ctx, command, output_file = None, description = '')`

Safely run a command with error handling and logging

Args:
ctx: Invoke context
command (str): Command to run
output_file (str): Optional output file for command result
description (str): Description for logging

Returns:
tuple: (success: bool, result: str)

#### Parameters

- **`ctx`**
- **`command`**
- **`output_file`** — defaults to `None`
- **`description`** — defaults to `''`
