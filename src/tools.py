from pathlib import Path
from invoke import task, Collection
import json
import shutil
import os


@task
def select_github_repo(ctx, base_path="C:/Users/korde/Home/Github"):
    """
    Select a GitHub repository from the specified base path and change the working directory to the selected repository.

    Args:
        base_path (str): The base path where the GitHub repositories are located.
    """
    folders = [
        d for d in Path(base_path).iterdir() if d.is_dir()
    ]  # Get all folders in the directory
    # Display a menu to select a folder
    print("Select a GitHub Repository:")
    for idx, folder in enumerate(folders, start=1):
        print(f"{idx}. {folder.name}")
    choice = int(input("Enter the number of the folder you want to select: "))
    selected_folder = folders[choice - 1]
    # Run 'invoke default' command
    ctx.run(f"invoke -r {Path(base_path) / selected_folder.name} --list")
    task = input("Enter the command to run: ")
    ctx.run(f"invoke -r {Path(base_path) / selected_folder.name} {task}")


@task
def clone_github_repos(ctx, source_user="charudatta10"):
    """
    Clone all repositories from a specified GitHub user.

    Args:
        source_user (str): The GitHub username to clone repositories from.
    """
    result = ctx.run(f"gh repo list --source {source_user} --json nameWithOwner")
    repos = json.loads(result.stdout)
    for repo in repos:
        repo_name = repo["nameWithOwner"]
        ctx.run(f"gh repo clone {repo_name}")
        print(f"Cloned repository: {repo_name}")
    print(f"Cloned all repositories from GitHub user: {source_user}.")


@task
def move_files(ctx, directory=None):
    """
    Move files from the Downloads directory to categorized directories based on file types.
    Args:
        directory (str): The directory to scan for files. If None, uses the Downloads folder.
    """
    # Get the home folder path dynamically
    def move_files_to_directory(directory_path, file_patterns, destination):
        for file_pattern in file_patterns:
            for file in directory_path.glob(file_pattern):
                shutil.move(str(file), destination / file.name)

    def ensure_directories_exist(*dirs):
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)

    home_folder = Path.home()
    # Set the default directory based on the environment
    downloads_folder = home_folder / "Downloads"
    directories = {
        "images": downloads_folder / "Pictures",
        "documents": downloads_folder / "Documents",
        "archives": downloads_folder / "Archives",
        "code": downloads_folder / "Code",
        "music": downloads_folder / "Music",
        "videos": downloads_folder / "Videos",
    }
    ensure_directories_exist(*directories.values())
    # Use the provided directory or the default directory
    root_directory = downloads_folder if directory is None else Path(directory)
    # Define file patterns for each type
    file_patterns = {
        "images": [
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.gif",
            "*.bmp",
            "*.tiff",
            "*.webp",
            "*.svg",
            "*.ico",
            "*.eps",
            "*.raw",
            "*.drawio",
            "*.avif",
        ],
        "documents": [
            "*.pdf",
            "*.doc",
            "*.docx",
            "*.xls",
            "*.xlsx",
            "*.ppt",
            "*.pptx",
            "*.txt",
            "*.rtf",
            "*.csv",
            "*.xml",
            "*.json",
            "*.md",
            "*.tex",
            "*.odt",
            "*.ods",
            "*.odp",
            "*.epub",
            "*.mobi",
            "*.azw3",
            "*.fb2",
        ],
        "archives": ["*.zip", "*.rar", "*.7z", "*.tar", "*.gz", "*.bz2", "*.xz"],
        "code": [
            "*.py",
            "*.c",
            "*.cpp",
            "*.java",
            "*.js",
            "*.ts",
            "*.html",
            "*.css",
            "*.scss",
            "*.sass",
            "*.less",
            "*.exe",
            "*.msi",
            "*.app",
            "*.iso",
            "*.img",
            "*.deb",
            "*.rpm",
            "*.jar",
            "*.war",
            "*.ear",
            "*.dll",
            "*.so",
            "*.pkg",
            "*.run",
            "*.sh",
            "*.bat",
            "*.cmd",
            "*.vbs",
            "*.ps1",
            "*.psm1",
            "*.psd1",
            "*.ps1xml",
            "*.reg",
        ],
        "music": ["*.mp3", "*.wav"],
        "videos": ["*.mp4", "*.m4a", "*.mov"],
    }
    # Move files based on patterns
    for category, patterns in file_patterns.items():
        move_files_to_directory(root_directory, patterns, directories[category])


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
    profile_path = (
        Path.home()
        / "OneDrive"
        / "Documents"
        / "PowerShell"
        / "Microsoft.PowerShell_profile.ps1"
    )
    shutil.copy(profile_path, destination_folder)


ns = Collection(
    select_github_repo, clone_github_repos, move_files, generate_system_reports
)
