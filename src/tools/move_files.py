from pathlib import Path
from invoke import task
import json
import shutil
from ..utils.logger import setup_logging

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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path

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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path

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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path

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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path

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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path


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

def move_files_to_directory(source_path, file_patterns, destination, logger):
    """Move files with duplicate handling and logging"""
    moved_count = 0
    skipped_count = 0
    
    for file_pattern in file_patterns:
        for file in source_path.glob(file_pattern):
            # Skip if it's a directory
            if file.is_dir():
                continue
                
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
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)

def validate_paths(source, destination, patterns):
    """Validate that all required paths exist and are accessible"""
    source_path = Path(source).resolve()  # Convert to absolute path
    destination_path = Path(destination).resolve()  # Convert to absolute path
    patterns_path = Path(patterns).resolve()  # Convert to absolute path
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path is not a directory: {source}")
            
    if not patterns_path.exists():
        raise FileNotFoundError(f"Patterns file does not exist: {patterns}")
    
    # Create destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    
    return source_path, destination_path, patterns_path

@task
def organize_files(
    c,
    source_directory,
    destination_directory,
    patterns_file,
    log_directory=None,
):
    """
    Organize files from a source directory to categorized directories based on file patterns.
    Handles duplicates by renaming with version numbers and logs all operations.
    
    Args:
        source_directory (str): The directory to scan and clean files from.
        destination_directory (str): The root directory where categorized folders will be created.
        patterns_file (str): Path to the JSON file containing file patterns.
        log_directory (str, optional): Directory to store log files. If None, uses destination_directory/logs.
    """
    # Validate input paths
    try:
        source_path, dest_path, patterns_path = validate_paths(
            source_directory, destination_directory, patterns_file
        )
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Path validation error: {str(e)}")
        return

    # Setup logging
    log_dir = Path(log_directory) if log_directory else dest_path / "logs"
    logger = setup_logging(log_dir)
    
    logger.info(f"Starting file organization from: {source_path} to: {dest_path}")
    print(f"🚀 Starting file organization")
    print(f"📂 Source: {source_path}")
    print(f"📁 Destination: {dest_path}")
    
    try:
        # Load file patterns from JSON
        with open(patterns_path, "r", encoding="utf-8") as f:
            file_patterns = json.load(f)
        
        logger.info(f"Loaded file patterns from: {patterns_path}")
        print(f"📋 Loaded file patterns from: {patterns_path}")
        
        # Create category directories based on patterns
        category_dirs = {}
        for category in file_patterns.keys():
            category_path = dest_path / category
            category_dirs[category] = category_path
        
        # Ensure all directories exist
        ensure_directories_exist(*category_dirs.values())
        logger.info(f"Created/verified {len(category_dirs)} category directories")
        print(f"📁 Created/verified {len(category_dirs)} category directories")
        
        total_moved = 0
        total_skipped = 0
        
        # Process each category
        for category, patterns in file_patterns.items():
            logger.info(f"Processing category: {category}")
            print(f"\n📁 Processing {category}...")
            
            moved, skipped = move_files_to_directory(
                source_path, 
                patterns, 
                category_dirs[category],
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
            print(f"⚠️  Check the log file in {log_dir} for details on failed operations")
    
    except FileNotFoundError as e:
        error_msg = f"File not found: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in patterns file: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        
    except PermissionError as e:
        error_msg = f"Permission denied: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")


@task
def create_patterns_sample(c, output_file="file_patterns.json"):
    """
    Create a sample patterns JSON file.
    
    Args:
        output_file (str): Path where to create the sample file
    """
    sample_patterns = {
        "Images": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.svg", "*.webp"],
        "Documents": ["*.pdf", "*.doc", "*.docx", "*.txt", "*.rtf", "*.odt"],
        "Spreadsheets": ["*.xls", "*.xlsx", "*.csv", "*.ods"],
        "Presentations": ["*.ppt", "*.pptx", "*.odp"],
        "Archives": ["*.zip", "*.rar", "*.7z", "*.tar", "*.gz", "*.bz2"],
        "Code": ["*.py", "*.js", "*.html", "*.css", "*.cpp", "*.java", "*.php"],
        "Audio": ["*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg", "*.m4a"],
        "Video": ["*.mp4", "*.avi", "*.mkv", "*.mov", "*.wmv", "*.flv", "*.webm"],
        "Executables": ["*.exe", "*.msi", "*.deb", "*.rpm", "*.dmg", "*.pkg"]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_patterns, f, indent=2)
    
    print(f"✅ Sample patterns file created at: {output_file}")


# Alternative task with cleaner interface
@task
def clean_folder(c, folder=".", patterns="file_patterns.json", destination=None):
    """
    Clean a folder by organizing files into categories.
    Simplified interface for common use case.
    
    Args:
        folder (str): Folder to clean (default: current directory)
        patterns (str): Patterns file (default: file_patterns.json)
        destination (str): Where to create organized folders (default: same as folder)
    """
    if destination is None:
        destination = folder
    
    organize_files(c, folder, destination, patterns)