# Module: `select_github_repo`

**File:** `C:\Users\korde\Home\Github\task-runner-SDLC\src\tools\select_github_repo.py`
**Language:** Python

## Imports

- `from pathlib import Path`
- `from invoke import task`

## Functions

### `select_github_repo(ctx, base_path = 'C:/Users/korde/Home/Github')`

**Decorators:** @task

Select a GitHub repository from the specified base path and change the working directory to the selected repository.

Args:
base_path (str): The base path where the GitHub repositories are located.

#### Parameters

- **`ctx`**
- **`base_path`** — defaults to `'C:/Users/korde/Home/Github'`
