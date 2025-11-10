# Module: `test_manager`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\tests\test_manager.py`
**Language:** Python

## Imports

- `import unittest`
- `from unittest.mock import patch`
- `from unittest.mock import MagicMock`
- `from unittest.mock import call`
- `from invoke import Context`
- `from src.manager import add_task`
- `from src.manager import list_tasks`
- `from src.manager import main`
- `from src.config import Config`

## Classes

## Class: `TestManager` (inherits from: unittest.TestCase)

*No description available*

### Methods

### `test_add_task(self, mock_logging_info, mock_input, mock_save_json_file, mock_load_json_file)`

**Decorators:** @patch, @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_logging_info`**
- **`mock_input`**
- **`mock_save_json_file`**
- **`mock_load_json_file`**

### `test_list_tasks(self, mock_print, mock_load_json_file)`

**Decorators:** @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_print`**
- **`mock_load_json_file`**

### `test_main_task(self, mock_run_command)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_run_command`**

---
