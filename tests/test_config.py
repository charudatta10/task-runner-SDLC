import unittest
from pathlib import Path
from src.config import Config

class TestConfig(unittest.TestCase):
    def test_repo_docs(self):
        expected_path = Path(__file__).parent.parent / "src" / "templates"
        self.assertEqual(Config.REPO_DOCS, expected_path)

    def test_license_header(self):
        expected_header = "© 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode"
        self.assertEqual(Config.LICENSE_HEADER, expected_header)

    def test_tasks_file(self):
        self.assertEqual(Config.TASKS_FILE, "tasks.json")

    def test_file_types(self):
        expected_file_types = {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*", ".sh": "#"}
        self.assertEqual(Config.FILE_TYPES, expected_file_types)

    def test_project_dirs(self):
        expected_project_dirs = [
            "src",
            "docs",
            "tests",
            ".github",
            ".github/workflows",
            ".github/ISSUE_TEMPLATE",
        ]
        self.assertEqual(Config.PROJECT_DIRS, expected_project_dirs)

    def test_project_files(self):
        expected_project_files = [
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
        self.assertEqual(Config.PROJECT_FILES, expected_project_files)

    def test_docs_files(self):
        expected_docs_files = [
            "_coverpage.md",
            "_homepage.md",
            "_navbar.md",
            ".nojekyll",
            "index.html",
            "README.md",
        ]
        self.assertEqual(Config.DOCS_FILES, expected_docs_files)

    def test_community_files(self):
        expected_community_files = [
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "LICENSE.md",
            "SECURITY.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
            ".github/pull_request_template.md",
        ]
        self.assertEqual(Config.COMMUNITY_FILES, expected_community_files)

if __name__ == "__main__":
    unittest.main()
