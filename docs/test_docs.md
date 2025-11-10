# Module: `test_docs`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\tests\test_docs.py`
**Language:** Python

## Imports

- `import unittest`
- `from unittest.mock import patch`
- `from unittest.mock import MagicMock`
- `from unittest.mock import call`
- `from invoke import Context`
- `from src.docs import collect_items`
- `from src.docs import collect_project_data`
- `from src.docs import setup_docs`
- `from src.docs import generate_docs`
- `from src.config import Config`

## Classes

## Class: `TestDocs` (inherits from: unittest.TestCase)

*No description available*

### Methods

### `test_collect_items_list_badges(self, mock_input)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_input`**

### `test_collect_items_list_features(self, mock_input)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_input`**

### `test_collect_project_data(self, mock_input)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_input`**

### `test_generate_docs(self)`

*No description available*

#### Parameters

- **`self`**

### `test_setup_docs(self, mock_collect_project_data, mock_generate_file, mock_download_file)`

**Decorators:** @patch, @patch, @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_collect_project_data`**
- **`mock_generate_file`**
- **`mock_download_file`**

---
