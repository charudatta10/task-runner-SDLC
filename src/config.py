from invoke import task
import logging
import os
from pathlib import Path
import urllib.request
import json
from datetime import datetime, timedelta
import zipfile


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
        "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE.md", "CHANGELOG.md",
        "SECURITY.md", "bug_report.md", "feature_request.md",
        "issue_template.md", "pull_request_template.md"     
    ]