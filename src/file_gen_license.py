import os
import urllib.request
import logging
from dataclasses import dataclass, field

# Constants
LICENSE_HEADER = "© 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike."
LICENSE_URL = "https://github.com/charudatta10/task-runner-SDLC/tree/main/src/template/LICENSE"
LOG_FILENAME = "app.log"
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
CODE_DIR = "src"

FILE_TYPES = {
    ".py": "#",
    ".js": "//",
    ".html": "<!--",
    ".css": "/*",
    ".sh": "#",
}

# Configure logging
logging.basicConfig(
    filename=LOG_FILENAME, 
    level=getattr(logging, LOG_LEVEL), 
    format=LOG_FORMAT
)

def fetch_license_text():
    """Fetch license text from URL."""
    try:
        with urllib.request.urlopen(LICENSE_URL) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
            logging.error(f"Failed to fetch license text. HTTP Status Code: {response.status}")
    except urllib.error.URLError as e:
        logging.error(f"Failed to fetch license text. Error: {e}")
    return None

def write_to_file(file_path, content):
    """Write content to a file."""
    with open(file_path, "w") as file:
        file.write(content)

def create_license_file():
    """Create LICENSE file with fetched text."""
    license_text = fetch_license_text()
    if license_text:
        write_to_file("LICENSE", license_text)
        logging.info("LICENSE file created.")

def generate_header(header_type, comment_symbol=None):
    """Generate headers based on type."""
    if header_type == "license":
        return f"{comment_symbol} {LICENSE_HEADER}\n{comment_symbol}\n{comment_symbol} {LICENSE_URL}\n\n"
    elif header_type == "logging":
        return f"""import logging
logging.basicConfig(filename="{LOG_FILENAME}", level=logging.{LOG_LEVEL}, format="{LOG_FORMAT}")\n"""
    return ""

def modify_content(content, header, action):
    """Add or remove headers from content."""
    if action == "add" and header not in content:
        return header + content
    elif action == "remove" and header in content:
        return content.replace(header, "")
    return content

def process_file(file_path, header_type, action):
    """Process a single file for header modification."""
    file_ext = os.path.splitext(file_path)[1]
    comment_symbol = FILE_TYPES.get(file_ext, "#")
    header = generate_header(header_type, comment_symbol)
    
    with open(file_path, "r+") as file:
        content = file.read()
        content = modify_content(content, header, action)
        file.seek(0)
        file.truncate()
        file.write(content)
        logging.info(f"{action.capitalize()}ed {header_type} header for {file_path}")

def process_directory(header_type, action):
    """Process all files in the directory for header modification."""
    if action == "add" and header_type == "license":
        create_license_file()
    
    for root, _, files in os.walk(CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in FILE_TYPES:
                process_file(os.path.join(root, file), header_type, action)

def main():
    options = {"1": "license", "2": "logging", "3": "both"}
    print("\nHeader Management Utility\n=========================")
    for key, value in options.items():
        print(f"{key}. Add/remove {value} headers")
    
    try:
        choice = input("\nChoose header type (1-3): ").strip()
        header_type = options[choice]
        action = input("Enter 'add' to add headers or 'remove' to remove them: ").strip().lower()
        process_directory(header_type, action)
    except KeyError:
        logging.error("Invalid choice")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()