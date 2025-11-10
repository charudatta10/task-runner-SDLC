# Module: `file_system`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\utils\file_system.py`
**Language:** Python

## Imports

- `import logging`
- `import os`
- `import json`
- `import shutil`

## Functions

### `append_to_file(file_path, content)`

Append content to a file

#### Parameters

- **`file_path`**
- **`content`**

### `check_file_exists(file_path)`

Check if a file exists

#### Parameters

- **`file_path`**

### `check_folder_exists(folder_path)`

Check if a folder exists

#### Parameters

- **`folder_path`**

### `copy_file(source_path, destination_path)`

Copy a file from source to destination

#### Parameters

- **`source_path`**
- **`destination_path`**

### `create_folder(folder_path)`

Create a folder if it doesn't exist

#### Parameters

- **`folder_path`**

### `delete_file(file_path)`

Delete a file

#### Parameters

- **`file_path`**

### `generate_file(template_path, config, output_path)`

Generate a file from a template

#### Parameters

- **`template_path`**
- **`config`**
- **`output_path`**

### `get_file_created_time(file_path)`

Get the created time of a file

#### Parameters

- **`file_path`**

### `get_file_extension(file_path)`

Get the file extension

#### Parameters

- **`file_path`**

### `get_file_list(folder_path)`

Get a list of files in a folder

#### Parameters

- **`folder_path`**

### `get_file_modified_time(file_path)`

Get the last modified time of a file

#### Parameters

- **`file_path`**

### `get_file_name(file_path)`

Get the file name without extension

#### Parameters

- **`file_path`**

### `get_file_size(file_path)`

Get the size of a file in bytes

#### Parameters

- **`file_path`**

### `get_folder_name(folder_path)`

Get the folder name

#### Parameters

- **`folder_path`**

### `get_parent_folder(path)`

Get the parent folder

#### Parameters

- **`path`**

### `get_project_name()`

Get the project name from the current working directory

### `join_paths(*paths)`

Join multiple paths

#### Parameters

- **`*paths`**

### `load_json_file(file_path)`

Load JSON data from file

#### Parameters

- **`file_path`**

### `move_file(source_path, destination_path)`

Move a file from source to destination

#### Parameters

- **`source_path`**
- **`destination_path`**

### `read_file(file_path)`

Read content from a file

#### Parameters

- **`file_path`**

### `save_json_file(file_path, data)`

Save data to JSON file

#### Parameters

- **`file_path`**
- **`data`**

### `search_and_replace(file_path, search_term, replace_term)`

Search and replace in a file

#### Parameters

- **`file_path`**
- **`search_term`**
- **`replace_term`**

### `write_file(file_path, content)`

Write content to a file

#### Parameters

- **`file_path`**
- **`content`**
