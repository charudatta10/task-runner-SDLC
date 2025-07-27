from pathlib import Path

class Config:
    """Central configuration for all tasks"""

    REPO_DOCS = Path(__file__).parent / "templates"
    LICENSE_HEADER = "© 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode"
    LICENSE_URL = f"{REPO_DOCS}/LICENSE"
    PROFILE_PATH = (
        Path.home()
        / "OneDrive"
        / "Documents"
        / "PowerShell"
        / "Microsoft.PowerShell_profile.ps1"
    )
    BACKUP_DIR = Path.home() / "Github" / "backup-list" / "list"
    PATTERN_FILE = Path(__file__).parent / "file_patterns.json"
    DOC_GEN_FILE = Path.home() / "Github" / "ai-doc-gen" / "src" / "main.py"
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
        "LICENSE.md",
        "SECURITY.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/pull_request_template.md",
    ]
