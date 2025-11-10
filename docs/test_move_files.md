# Module: `test_move_files`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\tests\test_move_files.py`
**Language:** Python

## Imports

- `import unittest`
- `from unittest.mock import patch`
- `from unittest.mock import MagicMock`
- `from unittest.mock import mock_open`
- `from unittest.mock import call`
- `import json`
- `import shutil`
- `import logging`
- `from invoke import Context`
- `from pathlib import Path`
- `from src.tools.move_files import organize_files`
- `from src.tools.move_files import create_patterns_sample`
- `from src.tools.move_files import clean_folder`
- `from src.tools.move_files import get_unique_filename`
- `from src.tools.move_files import move_files_to_directory`
- `from src.tools.move_files import ensure_directories_exist`
- `from src.tools.move_files import validate_paths`

## Classes

## Class: `TestMoveFiles` (inherits from: unittest.TestCase)

*No description available*

### Methods

### `test_clean_folder(self, mock_organize_files_body)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_organize_files_body`**

### `test_clean_folder_default_destination(self, mock_organize_files_body)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_organize_files_body`**

### `test_create_patterns_sample(self, mock_json_dump, mock_file_open, mock_print)`

**Decorators:** @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_json_dump`**
- **`mock_file_open`**
- **`mock_print`**

### `test_ensure_directories_exist(self, mock_mkdir)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_mkdir`**

### `test_get_unique_filename_no_duplicate(self, mock_exists)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_exists`**

### `test_get_unique_filename_no_extension(self, mock_exists)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_exists`**

### `test_get_unique_filename_with_duplicates(self, mock_exists)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_exists`**

### `test_move_files_to_directory(self, mock_error, mock_info, mock_print, mock_shutil_move, mock_get_unique_filename)`

**Decorators:** @patch, @patch, @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_error`**
- **`mock_info`**
- **`mock_print`**
- **`mock_shutil_move`**
- **`mock_get_unique_filename`**

### `test_organize_files(self, mock_print, mock_move_files_to_directory, mock_ensure_directories_exist, mock_validate_paths, mock_open, mock_json_load, mock_shutil_move, mock_setup_logging)`

**Decorators:** @patch, @patch, @patch, @patch, @patch, @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_print`**
- **`mock_move_files_to_directory`**
- **`mock_ensure_directories_exist`**
- **`mock_validate_paths`**
- **`mock_open`**
- **`mock_json_load`**
- **`mock_shutil_move`**
- **`mock_setup_logging`**

### `test_validate_paths_patterns_not_found(self, mock_print, mock_is_dir, mock_exists)`

**Decorators:** @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_print`**
- **`mock_is_dir`**
- **`mock_exists`**

### `test_validate_paths_source_not_directory(self, mock_print, mock_is_dir, mock_exists)`

**Decorators:** @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_print`**
- **`mock_is_dir`**
- **`mock_exists`**

### `test_validate_paths_source_not_found(self, mock_print, mock_exists)`

**Decorators:** @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_print`**
- **`mock_exists`**

### `test_validate_paths_success(self, mock_mkdir, mock_resolve, mock_is_dir, mock_exists)`

**Decorators:** @patch, @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_mkdir`**
- **`mock_resolve`**
- **`mock_is_dir`**
- **`mock_exists`**

---
