# Module: `ai_docsGen`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\tools\ai_docsGen.py`
**Language:** Python

## Imports

- `import json`
- `from pathlib import Path`
- `from config import Config`
- `from  import load_json_file`
- `from  import download_file`
- `import urllib.request`

## Functions

### `ai_doc_gen(repo_path = '.', template_file = 'prompt_docgen.json', output_dir = 'docs')`

Invoke Task to Generate Documentation

#### Parameters

- **`repo_path`** — defaults to `'.'`
- **`template_file`** — defaults to `'prompt_docgen.json'`
- **`output_dir`** — defaults to `'docs'`

## Classes

## Class: `DocumentationGenerator`

*No description available*

### Methods

### `__init__(self, repo_path: str, template_file: str, output_dir: str = 'docs')`

*No description available*

#### Parameters

- **`self`**
- **`repo_path`** *(str)*
- **`template_file`** *(str)*
- **`output_dir`** *(str)* — defaults to `'docs'`

### `generate_all_docs(self)`

*No description available*

#### Parameters

- **`self`**

### `generate_with_ollama(self, prompt: str, context: str = '', model: str = 'granite3.2:8b') -> str`

*No description available*

#### Parameters

- **`self`**
- **`prompt`** *(str)*
- **`context`** *(str)* — defaults to `''`
- **`model`** *(str)* — defaults to `'granite3.2:8b'`

#### Returns

- `str`

---
