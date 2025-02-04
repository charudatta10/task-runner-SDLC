# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt
####################################################
# create generalized gitignore, logging function
# folders = [f"Archives_{project_name}", f"Home_{project_name}", f"Favorites_{project_name}"
#####################################################
# tasks.py

from invoke import task, Collection
import subprocess
import os
import logging
from pathlib import Path
import urllib.request

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@task
def initialize_git(ctx):
    """Initialize Git repository."""
    ctx.run("git init")


@task
def create_files(ctx):
    """Create specified files."""
    files = [
        ".env",
        ".gitattributes",
        "requirements.txt",
        "tasks.py",
        "__main__.py",
    ]
    for file_name in files:
        Path(file_name).touch()


@task
def create_directories(ctx):
    """Create specified directories."""
    directories = ["docs", "src", "tests"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


GITHUB_GITIGNORE_BASE_URL = "https://raw.githubusercontent.com/github/gitignore/main/"


@task
def create_gitignore(ctx, language="Python"):
    """Create a .gitignore file with the specified language's template from GitHub.
    Args:
        ctx (invoke.Context): The context instance (passed automatically).
        language (str): The programming language for which to create the .gitignore file. Default is "Python".
    Returns:
        None
    Example:
        $ invoke create_gitignore --language=Python
    """
    url = f"{GITHUB_GITIGNORE_BASE_URL}{language}.gitignore"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                with open(".gitignore", "w") as file:
                    file.write(response.read().decode("utf-8"))
                    print(f".gitignore file created for {language}.")
            else:
                print(
                    f"Failed to fetch .gitignore template for {language} from GitHub."
                )
    except urllib.error.URLError as e:
        print(f"Failed to fetch the license text. Error: {e}")


@task
def setup_logging(ctx, log_file="app.log"):
    """Set up logging in Python files within the src folder to write to a specified file.
    Args:
        ctx (invoke.Context): The context instance (passed automatically).
        log_file (str): The name of the log file. Default is "app.log".
    Returns:
        None
    Example:
        $ invoke setup_logging --log-file=app.log
    """
    # Setup logging in all Python files within src folder
    src_folder = "src"
    if not os.path.exists(src_folder):
        os.makedirs(src_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r+") as f:
                    content = f.read()
                    if "import logging" not in content:
                        f.seek(0, 0)
                        f.write("import logging\n")
                    if f"logging.basicConfig(filename='{log_file}'," not in content:
                        f.write(
                            f"\nlogging.basicConfig(filename='{log_file}', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n"
                        )
                print(f"Added logging setup in {file_path}")


@task
def create_archive(ctx):
    """Create an archive using 7z."""
    ctx.run("zip archive.zip __main__.py")


@task
def initialize_mkdocs(ctx):
    """Initialize MkDocs using specified Conda environment."""
    with ctx.prefix("pwsh -command 'conda activate s'"):
        ctx.run("mkdocs new docs")


@task(
    pre=[
        initialize_git,
        create_files,
        create_directories,
        create_gitignore,
        setup_logging,
        create_archive,
        initialize_mkdocs,
    ]
)
def initialize_project(ctx, project_name="NewProject"):
    """
    Initialize the project with the provided settings.

    Args:
        project_name (str): The name of the project.
    """
    logging.info("Project initialization completed.")


# Create a collection of tasks
ns = Collection(
    create_gitignore,
    setup_logging,
    create_archive,
    initialize_mkdocs,
    initialize_project,
    default=initialize_project,
)
ns.name = "initialize"

if __name__ == "__main__":
    default(context())
