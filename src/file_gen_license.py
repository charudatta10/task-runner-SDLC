import os
import urllib.request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the license information
from dataclasses import dataclass, field

@dataclass
class LicenseConfig:
    LICENSE_TYPE: str = "Apache-2.0"
    COPYRIGHT_HOLDER: str = "CHARUDATTA KORDE LLC"
    COPYRIGHT_YEAR: int = 2076
    LICENSE_URL: str = field(init=False)
    HEADER_TEXT: str = field(init=False)
    CODE_DIR: str = "."
    FILE_TYPES: dict = field(default_factory=lambda: {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*", ".sh": "#"})
    
    # Logging configuration
    LOGGING_CONFIG: dict = field(default_factory=lambda: {
        "log_filename": "app.log",
        "log_level": "DEBUG",
        "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    })

    def __post_init__(self):
        self.LICENSE_URL = f"https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/{self.LICENSE_TYPE.lower()}.txt"
        self.HEADER_TEXT = f"Copyright {self.COPYRIGHT_YEAR} {self.COPYRIGHT_HOLDER} - {self.LICENSE_TYPE} License"

config = LicenseConfig()

def fetch_license_text():
    try:
        with urllib.request.urlopen(config.LICENSE_URL) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
            else:
                logging.error(f"Failed to fetch the license text. HTTP Status Code: {response.status}")
    except urllib.error.URLError as e:
        logging.error(f"Failed to fetch the license text. Error: {e}")

def create_license_file():
    license_text = fetch_license_text()
    if license_text:
        with open("LICENSE", "w") as license_file:
            license_file.write(license_text)
        logging.info("LICENSE file created.")

def get_license_header(comment_symbol):
    """Generate license header with appropriate comment symbol"""
    return f"{comment_symbol} {config.HEADER_TEXT} \n{comment_symbol}\n{comment_symbol} {config.LICENSE_URL}\n\n"

def get_logging_header():
    """Generate Python logging configuration header"""
    log_config = config.LOGGING_CONFIG
    return f"""import logging
logging.basicConfig(filename="{log_config['log_filename']}", level=logging.{log_config['log_level']}, format="{log_config['log_format']}")

"""

def modify_file_header(file_path, header_type, action="add"):
    """Add or remove headers (license or logging) to/from a file"""
    file_ext = os.path.splitext(file_path)[1]
    comment_symbol = config.FILE_TYPES.get(file_ext, "#")
    
    # Only process Python files for logging headers
    if header_type == "logging" and file_ext != ".py":
        return
    
    with open(file_path, "r+") as file:
        content = file.read()
        license_header = get_license_header(comment_symbol) if header_type in ["license", "both"] else ""
        logging_header = get_logging_header() if header_type in ["logging", "both"] and file_ext == ".py" else ""
        
        if action == "add":
            # Add headers as needed
            modified = False
            if license_header and config.HEADER_TEXT not in content:
                content = license_header + content
                modified = True
                
            if logging_header and "import logging\nlogging.basicConfig" not in content:
                content = content.replace(license_header, license_header + logging_header) if license_header in content else logging_header + content
                modified = True
                
            if modified:
                file.seek(0, 0)
                file.truncate()
                file.write(content)
                logging.info(f"Added {header_type} header(s) to {file_path}")
            else:
                logging.warning(f"{header_type.capitalize()} header(s) already exist in {file_path}")
                
        elif action == "remove":
            modified = False
            
            # Remove license header if present
            if license_header and header_type in ["license", "both"] and config.HEADER_TEXT in content:
                content = content.replace(license_header, "")
                modified = True
                
            # Remove logging header if present
            if header_type in ["logging", "both"] and file_ext == ".py":
                logging_import = "import logging\nlogging.basicConfig"
                if logging_import in content:
                    lines = content.split("\n")
                    new_lines = []
                    skip = False
                    for i, line in enumerate(lines):
                        if logging_import in line:
                            skip = True
                        elif skip and (i+1 < len(lines) and not lines[i+1].strip()) or not line.strip():
                            skip = False
                        elif not skip:
                            new_lines.append(line)
                    content = "\n".join(new_lines)
                    modified = True
            
            if modified:
                file.seek(0, 0)
                file.truncate()
                file.write(content)
                logging.info(f"Removed {header_type} header(s) from {file_path}")
            else:
                logging.warning(f"No {header_type} header(s) found in {file_path}")

def process_file_headers(header_type, action):
    """Process all files in the directory based on header type and action"""
    if action == "add" and header_type in ["license", "both"]:
        create_license_file()
        
    for root, _, files in os.walk(config.CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in config.FILE_TYPES:
                file_path = os.path.join(root, file)
                modify_file_header(file_path, header_type, action)

def main():
    print("\nHeader Management Utility")
    print("========================")
    print("1. Add/remove license headers")
    print("2. Add/remove logging configuration")
    print("3. Add/remove both license and logging headers")
    
    try:
        header_choice = int(input("\nChoose header type (1-3): ").strip())
        if header_choice not in [1, 2, 3]:
            raise ValueError("Invalid choice")
            
        header_types = {1: "license", 2: "logging", 3: "both"}
        header_type = header_types[header_choice]
        
        action = input("Enter 'add' to add headers or 'remove' to remove them: ").strip().lower()
        if action not in ["add", "remove"]:
            raise ValueError("Invalid action")
            
        process_file_headers(header_type, action)
        
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()