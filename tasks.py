from invoke import task, Collection
import sys
import os
import importlib.util

from pathlib import Path
import sys


BASE_DIR = Path(__file__).parent
SRC_PATH = BASE_DIR / "src"

sys.path.insert(0, str(SRC_PATH))

from Code import config

import tools.pkm_tools
import tools.clone_github_repos
import tools.generate_system_reports
import tools.select_github_repo
import tools.move_files
import tools.ai_file_renamer
import tools.ai_docsGen


@task
def init_repo(c):
    """Initialize a new git repository."""
    c.run("git init")


@task
def ai_doc_gen_task(c, repo_path=".", template_file="prompt_docgen.json", output_dir="docs"):
    """Generate documentation using AI."""
    tools.ai_docsGen.ai_doc_gen(repo_path=repo_path, template_file=template_file, output_dir=output_dir)


@task
def file_renamer(c, directory=".", dry_run=False):
    """Rename files using AI based on content."""
    renamer = tools.ai_file_renamer.AIFileRenamer()
    renamer.rename_directory(directory, dry_run=dry_run)


@task
def commit_changes(c, message):
    """Commit and push changes to main branch."""
    c.run("git pull origin main")
    c.run("git add .")
    c.run(f'git commit -m "{message}"')
    c.run("git push -u origin main")


@task
def lint(c, target="."):
    """Run ruff linter and formatter."""
    c.run(f"ruff check {target}")
    c.run(f"ruff format {target}")


@task
def run_tests(c):
    """Run pytest with coverage."""
    c.run("pytest --cov=src --cov-report=term-missing")


@task
def security_check(c):
    """Run security check with bandit."""
    c.run("bandit -r .")


@task
def move_files(c, folder=".", patterns=None, destination=None):
    """Move files to organized directories based on patterns."""
    if patterns is None:
        patterns = "file_patterns.json"
    if destination is None:
        destination = folder
    tools.move_files.clean_folder(folder=folder, patterns=patterns, destination=destination)


@task
def create_patterns(c, output_file="file_patterns.json"):
    """Create a sample file patterns JSON file."""
    tools.move_files.create_patterns_sample(output_file=output_file)


generate_tags = tools.pkm_tools.generate_tags
generate_moc = tools.pkm_tools.generate_moc
generate_links = tools.pkm_tools.generate_links
clone_repos = tools.clone_github_repos.clone_github_repos
generate_report = tools.generate_system_reports.generate_system_reports
list_system_tools = tools.generate_system_reports.list_system_tools
quick_backup = tools.generate_system_reports.quick_backup
select_repo = tools.select_github_repo.select_github_repo


ns = Collection(
    init_repo,
    ai_doc_gen_task,
    file_renamer,
    commit_changes,
    lint,
    run_tests,
    security_check,
    move_files,
    create_patterns,
    generate_tags,
    generate_moc,
    generate_links,
    clone_repos,
    generate_report,
    list_system_tools,
    quick_backup,
    select_repo,
)
