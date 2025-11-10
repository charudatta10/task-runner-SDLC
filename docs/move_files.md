# Module: `move_files`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\tools\move_files.py`
**Language:** Python

## Imports

- `from pathlib import Path`
- `import json`
- `import shutil`
- `from utils.logger import setup_logging`

## Functions

### `clean_folder(folder = '.', patterns = None, destination = None)`

Clean a folder by organizing files into categories.
Simplified interface for common use case.

Args:
folder (str): Folder to clean (default: current directory)
patterns (str): Patterns file (default: file_patterns.json)
destination (str): Where to create organized folders (default: same as folder)

#### Parameters

- **`folder`** — defaults to `'.'`
- **`patterns`** — defaults to `None`
- **`destination`** — defaults to `None`

### `create_patterns_sample(output_file = 'file_patterns.json')`

Create a sample patterns JSON file.

Args:
output_file (str): Path where to create the sample file

#### Parameters

- **`output_file`** — defaults to `'file_patterns.json'`

### `ensure_directories_exist(*dirs)`

Create directories if they don't exist

#### Parameters

- **`*dirs`**

### `get_unique_filename(destination_path, filename)`

Generate a unique filename by appending version numbers if duplicates exist.

Args:
destination_path (Path): The destination directory
filename (str): The original filename

Returns:
str: A unique filename

#### Parameters

- **`destination_path`**
- **`filename`**

### `move_files_to_directory(source_path, file_patterns, destination, logger)`

Move files with duplicate handling and logging

#### Parameters

- **`source_path`**
- **`file_patterns`**
- **`destination`**
- **`logger`**

### `organize_files(source_directory, destination_directory, patterns_file, log_directory = None)`

Organize files from a source directory to categorized directories based on file patterns.
Handles duplicates by renaming with version numbers and logs all operations.

Args:
source_directory (str): The directory to scan and clean files from.
destination_directory (str): The root directory where categorized folders will be created.
patterns_file (str): Path to the JSON file containing file patterns.
log_directory (str, optional): Directory to store log files. If None, uses destination_directory/logs.

#### Parameters

- **`source_directory`**
- **`destination_directory`**
- **`patterns_file`**
- **`log_directory`** — defaults to `None`

### `validate_paths(source, destination, patterns)`

Validate that all required paths exist and are accessible

#### Parameters

- **`source`**
- **`destination`**
- **`patterns`**
