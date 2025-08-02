# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
from pathlib import Path
from invoke import task, Collection
import json
import shutil
import os
from .config import Config
import logging
from datetime import datetime

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
def move_files(
    ctx,
    directory=None,
    patterns_file=Config.PATTERN_FILE,
):
    """
    Move files from the Downloads directory to categorized directories based on file types.
    Handles duplicates by renaming with version numbers and logs all operations.
    
    Args:
        directory (str): The directory to scan for files. If None, uses the Downloads folder.
        patterns_file (str): Path to the JSON file containing file patterns.
    """

    def setup_logging():
        """Setup logging to both file and console"""
        log_dir = Path.home() / "Downloads" / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"file_move_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Create logger
        logger = logging.getLogger('file_mover')
        logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

    def get_unique_filename(destination_path, filename):
        """
        Generate a unique filename by appending version numbers if duplicates exist.
        
        Args:
            destination_path (Path): The destination directory
            filename (str): The original filename
            
        Returns:
            str: A unique filename
        """
        file_path = destination_path / filename
        
        if not file_path.exists():
            return filename
        
        # Extract name and extension
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) == 2:
            base_name, extension = name_parts
        else:
            base_name, extension = filename, ''
        
        version = 1
        while True:
            if extension:
                new_filename = f"{base_name}_v{version}.{extension}"
            else:
                new_filename = f"{base_name}_v{version}"
            
            new_file_path = destination_path / new_filename
            if not new_file_path.exists():
                return new_filename
            
            version += 1

    def move_files_to_directory(directory_path, file_patterns, destination, logger):
        """Move files with duplicate handling and logging"""
        moved_count = 0
        skipped_count = 0
        
        for file_pattern in file_patterns:
            for file in directory_path.glob(file_pattern):
                try:
                    # Get unique filename to handle duplicates
                    unique_filename = get_unique_filename(destination, file.name)
                    destination_file = destination / unique_filename
                    
                    # Move the file
                    shutil.move(str(file), str(destination_file))
                    
                    # Log the operation
                    if unique_filename != file.name:
                        logger.info(f"MOVED (renamed): {file.name} -> {destination_file} (renamed due to duplicate)")
                        print(f"✓ Moved and renamed: {file.name} -> {unique_filename}")
                    else:
                        logger.info(f"MOVED: {file.name} -> {destination_file}")
                        print(f"✓ Moved: {file.name} -> {destination.name}/")
                    
                    moved_count += 1
                    
                except Exception as e:
                    logger.error(f"FAILED to move {file.name}: {str(e)}")
                    print(f"✗ Failed to move {file.name}: {str(e)}")
                    skipped_count += 1
        
        return moved_count, skipped_count

    def ensure_directories_exist(*dirs):
        """Create directories if they don't exist"""
        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    logger = setup_logging()
    
    # Initialize paths
    home_folder = Path.home()
    downloads_folder = home_folder / "Downloads"
    categories = ["Pictures", "Documents", "Archives", "Code", "Music", "Videos"]
    directories = {cat: downloads_folder / cat for cat in categories}
    
    # Ensure all directories exist
    ensure_directories_exist(*directories.values())
    
    # Determine source directory
    root_directory = downloads_folder if directory is None else Path(directory)
    
    logger.info(f"Starting file organization from: {root_directory}")
    print(f"🚀 Starting file organization from: {root_directory}")
    
    try:
        # Load file patterns from JSON
        with open(patterns_file, "r", encoding="utf-8") as f:
            file_patterns = json.load(f)
        
        logger.info(f"Loaded file patterns from: {patterns_file}")
        print(f"📋 Loaded file patterns from: {patterns_file}")
        
        total_moved = 0
        total_skipped = 0
        
        # Process each category
        for category, patterns in file_patterns.items():
            if category in directories:
                logger.info(f"Processing category: {category}")
                print(f"\n📁 Processing {category}...")
                
                moved, skipped = move_files_to_directory(
                    root_directory, 
                    patterns, 
                    directories[category],
                    logger
                )
                
                total_moved += moved
                total_skipped += skipped
                
                if moved > 0 or skipped > 0:
                    logger.info(f"Category {category}: {moved} moved, {skipped} failed")
                    print(f"   {moved} files moved, {skipped} failed")
        
        # Summary
        logger.info(f"File organization completed. Total: {total_moved} moved, {total_skipped} failed")
        print(f"\n✅ File organization completed!")
        print(f"📊 Summary: {total_moved} files moved, {total_skipped} failed")
        
        if total_skipped > 0:
            print(f"⚠️  Check the log file for details on failed operations")
    
    except FileNotFoundError:
        error_msg = f"Patterns file not found: {patterns_file}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in patterns file: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")


@task
def generate_system_reports(ctx, destination_folder=Config.BACKUP_DIR):
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
    shutil.copy(Config.PROFILE_PATH, destination_folder)


ns = Collection(
    select_github_repo, clone_github_repos, move_files, generate_system_reports
)
