from pathlib import Path
from invoke import task


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
    # Run 'poe' to list tasks in the selected repository
    ctx.run(f"poe -C {Path(base_path) / selected_folder.name} --list")
    task = input("Enter the command to run: ")
    ctx.run(f"poe -C {Path(base_path) / selected_folder.name} {task}")
