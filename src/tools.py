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
def move_files(ctx, directory=None, patterns_file=r"C:/Users/korde/Home/Github/task-runner-SDLC/src/file_patterns.json"):
    """
    Move files from the Downloads directory to categorized directories based on file types.
    Args:
        directory (str): The directory to scan for files. If None, uses the Downloads folder.
        patterns_file (str): Path to the JSON file containing file patterns.
    """
    def move_files_to_directory(directory_path, file_patterns, destination):
        for file_pattern in file_patterns:
            for file in directory_path.glob(file_pattern):
                shutil.move(str(file), destination / file.name)

    def ensure_directories_exist(*dirs):
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)

    home_folder = Path.home()
    downloads_folder = home_folder / "Downloads"
    categories = ["Pictures", "Documents", "Archives", "Code", "Music", "Videos"]
    directories = {cat: downloads_folder / cat for cat in categories}
    ensure_directories_exist(*directories.values())
    root_directory = downloads_folder if directory is None else Path(directory)

    # Load file patterns from JSON
    with open(patterns_file, "r", encoding="utf-8") as f:
        file_patterns = json.load(f)

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
