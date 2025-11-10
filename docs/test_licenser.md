# Module: `test_licenser`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\tests\test_licenser.py`
**Language:** Python

## Imports

- `import unittest`
- `from unittest.mock import patch`
- `from unittest.mock import MagicMock`
- `from pathlib import Path`
- `from src.licenser import get_files`
- `from src.licenser import license_text`
- `from src.licenser import add_header`
- `from src.config import Config`

## Classes

## Class: `TestLicenser` (inherits from: unittest.TestCase)

*No description available*

### Methods

### `test_add_header_add(self, mock_get_files)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_get_files`**

### `test_add_header_remove(self, mock_get_files)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_get_files`**

### `test_get_files(self, mock_rglob)`

**Decorators:** @patch

*No description available*

#### Parameters

- **`self`**
- **`mock_rglob`**

### `test_license_text_html(self)`

*No description available*

#### Parameters

- **`self`**

### `test_license_text_py(self)`

*No description available*

#### Parameters

- **`self`**

---
