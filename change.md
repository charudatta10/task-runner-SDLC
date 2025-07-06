# Proposed Changes for Improved Code Quality

This document outlines suggested changes to improve the project's structure and code quality, focusing on the principles of Don't Repeat Yourself (DRY), Keep It Simple, Stupid (KISS), and atomicity.

## 1. File Structure and Redundancy

### 1.1. Redundant Documentation Files

* **Issue:** The `docs` directory contains duplicates of several markdown files that also exist in the root directory (`CONTRIBUTING.md`, `LICENSE.md`, `README.md`). This violates the DRY principle, making maintenance harder. There is also a file that appears to be a backup, `_navbar copy.md`.
* **Suggestion:** Remove the following files from the `docs` directory and rely on the root-level versions:
  * `docs/CONTRIBUTING.md`
  * `docs/LICENSE.md`
  * `docs/README.md`
  * `docs/_navbar copy.md`

### 1.2. Duplicate Templates

* **Issue:** The `.github` directory and the `src/templates` directory contain similar templates for issue reporting and pull requests. This can lead to inconsistencies.
* **Suggestion:** Consolidate the templates. A good approach would be to keep the templates in the `.github` directory, as this is the standard location for them, and have the code in `src/setup.py` or a similar file copy or link to them when generating new documentation. This makes the project's GitHub integration the single source of truth.

### 1.3. Root Directory Clutter

* **Issue:** The root directory contains several Python scripts (`ai_docsGen.py`, `backup_tasks.py`, `main.py`, `tasks.py`). This clutters the root and mixes application code with project configuration files.
* **Suggestion:** Move these scripts into the `src` directory to create a cleaner separation of concerns. The `main.py` script could remain in the root if it's the primary entry point, but the others are likely better placed within the source directory.

## 2. Code Analysis

After reviewing the Python code in the `src` directory, the following areas for improvement have been identified:

### 2.1. Hardcoded Paths

* **Issue:** The `tools.py` and `docs.py` modules contain hardcoded paths (e.g., `C:/Users/korde/Home/Github`, `Path.home() / "OneDrive" / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"`). This makes the code less portable and difficult to run in different environments.
* **Suggestion:** Replace hardcoded paths with configurable options. For example, you could use environment variables or a configuration file to specify the base paths for repositories and user-specific directories.

    **Code Snippet from `tools.py`:**

    ```python
    @task
    def select_github_repo(ctx, base_path="C:/Users/korde/Home/Github"):
        ...
    ```

    **Code Snippet from `tools.py`:**

    ```python
    @task
    def generate_system_reports(
        ctx, destination_folder=Path("C:/Users/korde/Home/Github/backup-list/list")
    ):
        ...
        profile_path = (
            Path.home()
            / "OneDrive"
            / "Documents"
            / "PowerShell"
            / "Microsoft.PowerShell_profile.ps1"
        )
        shutil.copy(profile_path, destination_folder)
    ```

    **Code Snippet from `docs.py`:**

    ```python
    @task
    def generate_docs(ctx):
        """Generate documentation"""
        ctx.run(
            f"python {Path.home() / "Home" / "Github" / "ai-doc-gen" / "src" / "main.py"} ."
        )
    ```

### 2.2. Large, Monolithic Functions

* **Issue:** The `move_files` function in `tools.py` is a large, monolithic function that handles many file types. This makes it difficult to read, maintain, and test.
* **Suggestion:** Break down the `move_files` function into smaller, more specialized functions. For example, you could have a separate function for each file category (e.g., `move_images`, `move_documents`). You could also use a dictionary to map file extensions to their corresponding destination directories, which would make the code more data-driven and easier to extend.

    **Code Snippet from `tools.py`:**

    ```python
    @task
    def move_files(ctx, directory=None):
        """
        Move files from the Downloads directory to categorized directories based on file types.
        Args:
            directory (str): The directory to scan for files. If None, uses the Downloads folder.
        """
        # ... (function implementation)
    ```

### 2.3. Lack of Abstraction

* **Issue:** The `generate_system_reports` function in `tools.py` contains a series of hardcoded shell commands. This makes the function rigid and difficult to modify or test.
* **Suggestion:** Abstract the command execution. You could create a list of dictionaries, where each dictionary represents a command to be executed and contains the command string and the output file name. This would make it easier to add or remove commands without changing the core logic of the function.

    **Code Snippet from `tools.py`:**

    ```python
    @task
    def generate_system_reports(
        ctx, destination_folder=Path("C:/Users/korde/Home/Github/backup-list/list")
    ):
        """
        Generate system reports and copy PowerShell scripts from source to destination.

        Args:
            source_folder (str): The source folder containing PowerShell scripts.
            destination_folder (str): The destination folder for copying scripts.
        """
        os.chdir(destination_folder)
        ctx.run("scoop export > scoop.json")
        ctx.run("winget export -o winget.json")
        ctx.run("pipx list --json > pipx.json")
        ctx.run("choco list > choco.txt")
        ctx.run("conda env export --json > conda_base.json")
        ctx.run("conda env export --name s --json > conda_s.json")
        ctx.run("pip list --format=json > pip.json")
        ctx.run("npm -g list --json > npm.json")
        # ...
    ```

### 2.4. Potential for Code Duplication

* **Issue:** The `quality.py` module contains several tasks that run external tools (e.g., `pylint`, `flake8`, `black`). The `run_command` calls are very similar and could be consolidated.
* **Suggestion:** Create a helper function that takes the tool name and command as arguments and then runs the command. This would reduce code duplication and make it easier to add new quality checks in the future.

    **Code Snippet from `quality.py`:**

    ```python
    @task
    def tests(ctx):
        """Run unit tests"""
        run_command(
            ctx, "python -m unittest discover -s tests", "Tests passed", "Tests failed"
        )

    @task
    def security(ctx):
        """Run security checks"""
        run_command(ctx, "bandit -r .", "Security checks passed", "Security checks failed")

    @task
    def lint(ctx):
        """Run pylint checks"""
        run_command(ctx, "pylint .", "Linting passed", "Linting failed")

    @task
    def flake8(ctx):
        """Run flake8 checks"""
        run_command(ctx, "flake8 .", "Flake8 passed", "Flake8 failed")

    @task
    def lint_exec(ctx):
        """Format code with black"""
        run_command(ctx, "black .", "Code formatted", "Formatting failed")
    ```

### 2.5. Configuration in Code

* **Issue:** The `config.py` file contains a lot of configuration that is likely to change between different environments or users. Hardcoding this configuration makes it difficult to modify without changing the code.
* **Suggestion:** Move the configuration to a separate file (e.g., `config.ini`, `config.toml`, or `.env`). This would allow users to easily customize the aconfiguration without having to modify the source code.

    **Code Snippet from `config.py`:**

    ```python
    class Config:
        """Central configuration for all tasks"""

        REPO_DOCS = "https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates"
        LICENSE_HEADER = "© 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike."
        LICENSE_URL = f"{REPO_DOCS}/LICENSE"
        CODE_DIR = "src"
        TASKS_FILE = "tasks.json"
        # ... (and so on)
    ```

### 2.6. User Input in Core Logic

* **Issue:** The `docs.py` and `manager.py` modules mix user input (e.g., `input()`) with the core application logic. This makes the code harder to test and less reusable.
* **Suggestion:** Separate the user input from the core logic. For example, you could have a separate function that is responsible for gathering user input and then passes the input to the core functions as arguments. This would make the core functions more pure and easier to test in isolation.

    **Code Snippet from `docs.py`:**

    ```python
    def collect_items(prompt, formatter):
        items = []
        print(f"{prompt} (Type 'done' to finish):")
        while True:
            item = input("- ")
            if item.lower() == "done":
                break
            # ...
    ```

    **Code Snippet from `manager.py`:**

    ```python
    @task
    def add_task(ctx):
        """Add a new task"""
        tasks = load_json_file(Config.TASKS_FILE)
        task = {
            "id": len(tasks) + 1,
            "title": input("Title: "),
            "description": input("Description: "),
            "tags": input("Tags (comma-separated): ").split(","),
            "status": "todo",
        }
        # ...
    ```
