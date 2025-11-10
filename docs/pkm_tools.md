# Module: `pkm_tools`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\tools\pkm_tools.py`
**Language:** Python

## Imports

- `from invoke import task`
- `from invoke import Collection`
- `from pathlib import Path`
- `import re`
- `from collections import defaultdict`

## Functions

### `generate_links(c, folder = '.')`

**Decorators:** @task

Generate links.md with all internal and external links.

#### Parameters

- **`c`**
- **`folder`** — defaults to `'.'`

### `generate_moc(c, folder = '.')`

**Decorators:** @task

Generate moc.md with wiki-style links to all notes.

#### Parameters

- **`c`**
- **`folder`** — defaults to `'.'`

### `generate_tags(c, folder = '.')`

**Decorators:** @task

Generate tags.md with tag glossary and linked notes.

#### Parameters

- **`c`**
- **`folder`** — defaults to `'.'`

### `get_markdown_files(folder)`

*No description available*

#### Parameters

- **`folder`**
