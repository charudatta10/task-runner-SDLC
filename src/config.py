class Config:
    """Central configuration for all tasks"""

    REPO_DOCS = "https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates"
    LICENSE_HEADER = "© 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike."
    LICENSE_URL = f"{REPO_DOCS}/LICENSE"
    CODE_DIR = "src"
    TASKS_FILE = "tasks.json"
    FILE_TYPES = {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*", ".sh": "#"}
    PROJECT_DIRS = [
        "src",
        "docs",
        "tests",
        ".github",
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
    ]
    PROJECT_FILES = [
        ".env",
        ".gitattributes",
        ".gitignore",
        ".pre-commit-config.yaml",
        "Dockerfile",
        "README.md",
        "requirements.txt",
        "tasks.py",
        "src/__main__.py",
        "src/__init__.py",
        "tests/__init__.py",
        "tests/test_main.py",
        ".log",
    ]
    DOCS_FILES = [
        "_coverpage.md",
        "_homepage.md",
        "_navbar.md",
        ".nojekyll",
        "index.html",
        "README.md",
    ]
    COMMUNITY_FILES = [
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "LICENSE.md",,
        "SECURITY.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    ]
