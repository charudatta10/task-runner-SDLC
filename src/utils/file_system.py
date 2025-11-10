# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
import os
import json
import shutil

def load_json_file(file_path):
    """Load JSON data from file"""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_json_file(file_path, data):
    """Save data to JSON file"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def generate_file(template_path, config, output_path):
    """Generate a file from a template"""
    with open(template_path, "r") as f:
        content = f.read()
        for key, value in config.items():
            placeholder = "{" + key + "}"
            content = content.replace(placeholder, value)
        with open(output_path, "w") as f:
            f.write(content)
    logging.info(f"Generated {output_path} from {template_path}")

def create_folder(folder_path):
    """Create a folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logging.info(f"Created folder: {folder_path}")

def move_file(source_path, destination_path):
    """Move a file from source to destination"""
    try:
        shutil.move(source_path, destination_path)
        logging.info(f"Moved {source_path} to {destination_path}")
    except Exception as e:
        logging.error(f"Error moving {source_path}: {e}")

def copy_file(source_path, destination_path):
    """Copy a file from source to destination"""
    try:
        shutil.copy(source_path, destination_path)
        logging.info(f"Copied {source_path} to {destination_path}")
    except Exception as e:
        logging.error(f"Error copying {source_path}: {e}")

def delete_file(file_path):
    """Delete a file"""
    try:
        os.remove(file_path)
        logging.info(f"Deleted {file_path}")
    except Exception as e:
        logging.error(f"Error deleting {file_path}: {e}")

def get_file_list(folder_path):
    """Get a list of files in a folder"""
    return os.listdir(folder_path)

def read_file(file_path):
    """Read content from a file"""
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file"""
    with open(file_path, "w") as f:
        f.write(content)

def append_to_file(file_path, content):
    """Append content to a file"""
    with open(file_path, "a") as f:
        f.write(content)

def search_and_replace(file_path, search_term, replace_term):
    """Search and replace in a file"""
    content = read_file(file_path)
    content = content.replace(search_term, replace_term)
    write_file(file_path, content)

def get_project_name():
    """Get the project name from the current working directory"""
    return os.path.basename(os.getcwd())

def get_file_extension(file_path):
    """Get the file extension"""
    return os.path.splitext(file_path)[1]

def get_file_name(file_path):
    """Get the file name without extension"""
    return os.path.splitext(os.path.basename(file_path))[0]

def get_folder_name(folder_path):
    """Get the folder name"""
    return os.path.basename(folder_path)

def get_parent_folder(path):
    """Get the parent folder"""
    return os.path.dirname(path)

def join_paths(*paths):
    """Join multiple paths"""
    return os.path.join(*paths)

def check_file_exists(file_path):
    """Check if a file exists"""
    return os.path.exists(file_path)

def check_folder_exists(folder_path):
    """Check if a folder exists"""
    return os.path.exists(folder_path)

def get_file_size(file_path):
    """Get the size of a file in bytes"""
    return os.path.getsize(file_path)

def get_file_modified_time(file_path):
    """Get the last modified time of a file"""
    return os.path.getmtime(file_path)

def get_file_created_time(file_path):
    """Get the created time of a file"""
    return os.path.getctime(file_path)
