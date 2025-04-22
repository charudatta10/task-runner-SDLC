from invoke import task
import logging
import os
from pathlib import Path
import urllib.request
import json
from datetime import datetime, timedelta
import zipfile

# ========== Configuration ==========
class Config:
    """Central configuration for all tasks"""
    REPO_DOCS = "https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates"
    LICENSE_HEADER = "© 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike."
    LICENSE_URL = f"{REPO_DOCS}/LICENSE"
    CODE_DIR = "src"
    TASKS_FILE = "tasks.json"
    FILE_TYPES = {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*", ".sh": "#"}
    PROJECT_DIRS = ["src", "docs", "tests"]
    PROJECT_FILES = [
        ".env", ".gitattributes", ".gitignore", ".pre-commit-config.yaml",
        "Dockerfile", "README.md", "requirements.txt", "tasks.py",
        "src/__main__.py", "src/__init__.py", "tests/__init__.py", "tests/test_main.py"
    ]
    DOCS_FILES = [
        "_coverpage.md", "_homepage.md", "_navbar.md",
        ".nojekyll", "index.html", "README.md"
    ]
    COMMUNITY_FILES = [
        "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE", "CHANGELOG.md",
        "SECURITY.md", "bug_report.md", "feature_request.md",
        "issue_template.md", "pull_request_template.md"     
    ]

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ========== Helper Functions ==========
def run_command(ctx, command, success_msg, error_msg):
    """DRY helper to run commands with consistent logging"""
    try:
        ctx.run(command)
        logging.info(success_msg)
        return True
    except Exception as e:
        logging.error(f"{error_msg}: {e}")
        return False

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return False

def load_json_file(file_path):
    """Load JSON data from file"""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_json_file(file_path, data):
    """Save data to JSON file"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ========== Git Tasks ==========
@task
def git_pull(ctx):
    """Pull latest changes"""
    run_command(ctx, "git pull origin main --force", "Pulled latest changes", "Pull failed")

@task
def git_add(ctx):
    """Stage all changes"""
    run_command(ctx, "git add .", "Changes staged", "Failed to stage changes")

@task
def git_commit(ctx, message="Deployment Commit"):
    """Commit changes"""
    run_command(ctx, f'git commit -m "{message}"', "Changes committed", "Commit failed")

@task
def git_push(ctx):
    """Push changes"""
    run_command(ctx, "git push -u origin main", "Changes pushed", "Push failed")

@task
def git_init(ctx):
    """Initialize git repo"""
    run_command(ctx, "git init", "Git repo initialized", "Git init failed")

# ========== Code Quality Tasks ==========
@task
def run_tests(ctx):
    """Run unit tests"""
    run_command(ctx, "python -m unittest discover -s tests", "Tests passed", "Tests failed")

@task
def run_security(ctx):
    """Run security checks"""
    run_command(ctx, "bandit -r .", "Security checks passed", "Security checks failed")

@task
def run_lint(ctx):
    """Run pylint checks"""
    run_command(ctx, "pylint .", "Linting passed", "Linting failed")

@task
def run_flake8(ctx):
    """Run flake8 checks"""
    run_command(ctx, "flake8 .", "Flake8 passed", "Flake8 failed")

@task
def run_format(ctx):
    """Format code with black"""
    run_command(ctx, "black .", "Code formatted", "Formatting failed")

# ========== Project Setup Tasks ==========
@task
def create_dirs(ctx):
    """Create project directories"""
    for directory in Config.PROJECT_DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

@task
def create_files(ctx):
    """Create project files"""
    for file in Config.PROJECT_FILES:
        Path(file).touch()
        logging.info(f"Created file: {file}")

@task
def setup_docs(ctx):
    """Setup documentation"""
    for file in Config.DOCS_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", f"docs/{file}"):
            logging.info(f"Downloaded docs file: {file}")

@task
def get_community_files(ctx):
    """Download community files"""
    for file in Config.COMMUNITY_FILES:
        if download_file(f"{Config.REPO_DOCS}/{file}", file):
            logging.info(f"Downloaded community file: {file}")



@task
def add_license_header(ctx, action="add"):
    """Add or remove license header to/from files.
    
    Use `--action=add` to add headers and `--action=remove` to remove them.
    """
    for root, _, files in os.walk(Config.CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in Config.FILE_TYPES.keys():
                license_text = f"{Config.FILE_TYPES[file_ext]} {Config.LICENSE_HEADER}\n{Config.FILE_TYPES[file_ext]} {Config.LICENSE_URL}"
                file_path = os.path.join(root, file)
                print(f"LICENSE_HEADER: {Config.LICENSE_HEADER}")
                print(f"Action: {action}")

                with open(file_path, "r+", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    print(f"Content: {content}")
                    
                    if action == "add" and Config.LICENSE_HEADER not in content:
                        f.seek(0)
                        f.write(license_text + "\n" + content)
                        logging.info(f"Added license header to {file}")
                    
                    elif action == "remove" and Config.LICENSE_HEADER in content:
                        updated_content = content.replace(license_text + "\n", "")
                        f.seek(0)
                        f.truncate()
                        f.write(updated_content)
                        logging.info(f"Removed license header from {file}")


@task(pre=[git_init, create_dirs, create_files, setup_docs, get_community_files])
def setup_project(ctx):
    """Initialize new project"""
    logging.info("Project setup complete")


# ========== Deployment Tasks ==========
@task(pre=[git_pull, run_tests, run_security, run_lint, run_flake8, run_format, git_add, git_commit, git_push])
def deploy(ctx):
    """Full deployment pipeline"""
    logging.info("Deployment complete")

# ========== Package Management ==========
@task
def package(ctx):
    """Package the project"""
    project_dir = Path(Config.CODE_DIR)
    output_file = project_dir / "ypp.zip"
    
    # Ensure main script exists
    main_script = project_dir / "__main__.py"
    if not main_script.exists():
        main_script.write_text("print('hello world')\n")
    
    # Create zip archive
    with zipfile.ZipFile(output_file, "w") as zipf:
        for file_path in project_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(".zip"):
                zipf.write(file_path, file_path.relative_to(project_dir))
    
    logging.info(f"Package created: {output_file}")

# ========== Task Management ==========
@task
def add_task(ctx):
    """Add a new task"""
    tasks = load_json_file(Config.TASKS_FILE)
    task = {
        "id": len(tasks) + 1,
        "title": input("Title: "),
        "description": input("Description: "),
        "tags": input("Tags (comma-separated): ").split(","),
        "status": "todo"
    }
    tasks.append(task)
    save_json_file(Config.TASKS_FILE, tasks)
    logging.info(f"Task added: {task['title']}")

@task
def list_tasks(ctx):
    """List all tasks"""
    tasks = load_json_file(Config.TASKS_FILE)
    for task in tasks:
        print(f"{task['id']}: {task['title']} - {task['status']}")

@task(default=True)
def main(ctx):
    """List all tasks"""
    run_command(ctx, "inv --list","To select command type invoke again and cmd", "fail")

#============ README Generation ==========
@task
def generate_readme(ctx):
    """Generate a README file based on user input and a template."""
    download_file(Config.REPO_DOCS + "/template.md", "README.md")
    logging.info("README file downloaded successfully.")
    with open("README.md", "r", encoding="utf-8") as file:
        template_content = file.read()
    logging.info("README file opened successfully.")
    # Step 2: Helper functions to collect user input
    def collect_items(prompt, formatter):
        items = []
        print(f"{prompt} (Type 'done' to finish):")
        while True:
            item = input("- ")
            if item.lower() == "done":
                break
            formatted_item = f"- {item}" if formatter == "list_features" else f"`{item}`"
            items.append(formatted_item)
        return "\n".join(items) if formatter == "list_features" else " ".join(items)
    # Step 3: Collect data
    data = {
        "title": input("Enter title of project -> "),
        "description": input("Enter project description -> "),
        "features": collect_items("Enter project features -> ", "list_features"),
        "list_badges": collect_items("Enter softwares used in the project -> ", "list_badges"),
    }
    logging.info("README file input parsed successfully.")
    # Step 4: Format and write the README file
    readme_content = template_content.format(
        title=data.get("title", "Untitled Project"),
        description=data.get("description", "No description provided."),
        features=data.get("features", ""),
        list_badges=data.get("list_badges", "")
    )
    logging.info("README file text generated successfully.")
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)
    
    logging.info("README file generated successfully.")

@task
def ppt_gen(ctx):
    """Generate a presentation file based on README content."""
    # Read the content of the README file
    if not os.path.exists("README.md"):
        logging.error("README.md file not found. Please generate it first.")
        return

    with open("README.md", "r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    # Prepare the presentation content
    file_content = f"""---
marp: true
headingDivider: 6
theme: gaia
---

{readme_content}"""

    # Write the content to a new presentation file
    with open("readmex.md", "w+", encoding="utf-8") as presentation_file:
        presentation_file.write(file_content)

    logging.info("Presentation file 'readmex.md' generated successfully.")
