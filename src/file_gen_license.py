# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt

import os
import urllib.request
import logging
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class LicenseConfig:
    LICENSE_TYPE: str = "Apache-2.0"
    COPYRIGHT_HOLDER: str = "CHARUDATTA KORDE LLC"
    COPYRIGHT_YEAR: int = 2076
    CODE_DIR: str = "."
    LICENSE_URL: str = field(init=False)
    HEADER_TEXT: str = field(init=False)
    FILE_TYPES: dict = field(
        default_factory=lambda: {
            ".py": "#",
            ".js": "//",
            ".html": "<!--",
            ".css": "/*",
            ".sh": "#",
        }
    )
    LOGGING_CONFIG: dict = field(
        default_factory=lambda: {
            "log_filename": "app.log",
            "log_level": "DEBUG",
            "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    )

    def __post_init__(self):
        self.LICENSE_URL = f"https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/{self.LICENSE_TYPE.lower()}.txt"
        self.HEADER_TEXT = f"Copyright {self.COPYRIGHT_YEAR} {self.COPYRIGHT_HOLDER} - {self.LICENSE_TYPE} License"


config = LicenseConfig()


def fetch_license_text():
    try:
        with urllib.request.urlopen(config.LICENSE_URL) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
            logging.error(
                f"Failed to fetch the license text. HTTP Status Code: {response.status}"
            )
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
logging.basicConfig(filename="{log_config['log_filename']}", level=logging.{log_config['log_level']}, format="{log_config['log_format']}")\n"""


def add_license_header(content, comment_symbol):
    """Add license header to content if not present"""
    license_header = get_license_header(comment_symbol)
    if config.HEADER_TEXT not in content:
        content = license_header + content
    return content


def add_logging_header(content):
    """Add logging header to content if not present"""
    logging_header = get_logging_header()
    if "import logging\nlogging.basicConfig" not in content:
        content = logging_header + content
    return content


def remove_license_header(content, comment_symbol):
    """Remove license header from content if present"""
    license_header = get_license_header(comment_symbol)
    if config.HEADER_TEXT in content:
        content = content.replace(license_header, "")
    return content


def remove_logging_header(content):
    """Remove logging header from content if present"""
    lines = content.split("\n")
    content = "\n".join(
        line
        for line in lines
        if not line.startswith("import logging")
        and not line.startswith("logging.basicConfig")
    )
    return content


def modify_file_header(file_path, header_type, action="add"):
    """Add or remove headers (license or logging) to/from a file"""
    file_ext = os.path.splitext(file_path)[1]
    comment_symbol = config.FILE_TYPES.get(file_ext, "#")

    # Only process Python files for logging headers
    if header_type == "logging" and file_ext != ".py":
        return

    with open(file_path, "r+") as file:
        content = file.read()

        if action == "add":
            if header_type in ["license", "both"]:
                content = add_license_header(content, comment_symbol)
            if header_type in ["logging", "both"] and file_ext == ".py":
                content = add_logging_header(content)
        elif action == "remove":
            if header_type in ["license", "both"]:
                content = remove_license_header(content, comment_symbol)
            if header_type in ["logging", "both"] and file_ext == ".py":
                content = remove_logging_header(content)

        file.seek(0, 0)
        file.truncate()
        file.write(content)
        logging.info(f"{action.capitalize()}ed {header_type} header(s) to {file_path}")


def process_file_headers(header_type, action):
    """Process all files in the directory based on header type and action"""
    if action == "add" and header_type in ["license", "both"]:
        create_license_file()
    for root, _, files in os.walk(config.CODE_DIR):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in config.FILE_TYPES:
                modify_file_header(os.path.join(root, file), header_type, action)


def main():
    print("\nHeader Management Utility")
    print("========================")
    print("1. Add/remove license headers")
    print("2. Add/remove logging configuration")
    print("3. Add/remove both license and logging headers")

    try:
        header_choice = int(input("\nChoose header type (1-3): ").strip())
        header_types = {1: "license", 2: "logging", 3: "both"}
        header_type = header_types[header_choice]
        action = (
            input("Enter 'add' to add headers or 'remove' to remove them: ")
            .strip()
            .lower()
        )
        process_file_headers(header_type, action)
    except (ValueError, KeyError):
        logging.error("Invalid input")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
