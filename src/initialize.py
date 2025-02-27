# tasks.py

import logging
import subprocess
import os
from pathlib import Path
import urllib.request

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define commands in a dictionary
commands = {
    "initialize_git": "git init",
    "create_files": [
        "touch .env",
        "touch .gitattributes",
        "touch requirements.txt",
        "touch tasks.py",
        "touch __main__.py",
    ],
    "create_directories": ["mkdir -p docs", "mkdir -p src", "mkdir -p tests"],
    "create_gitignore": "curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore",
    "setup_logging": 'echo \'import logging\nlogging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")\' >> src/*.py',
    "create_archive": "zip archive.zip __main__.py",
    "initialize_mkdocs": "mkdocs new docs",
}


# Run a given command or a list of commands
def run_command(command):
    """Run a given command or a list of commands."""
    if isinstance(command, list):
        for cmd in command:
            logging.info(f"Running {cmd}...")
            subprocess.run(cmd, shell=True, check=True)
    else:
        logging.info(f"Running {command}...")
        subprocess.run(command, shell=True, check=True)


# Display available commands
def display_commands():
    """Display available commands."""
    print("Available commands:")
    for index, name in enumerate(commands.keys()):
        print(f"{index}: {name}")


def main():
    display_commands()

    user_input = input(
        "Enter the command indices to run (comma-separated, default: all): "
    )

    try:
        command_indices = (
            list(map(int, user_input.split(",")))
            if user_input.strip()
            else list(range(len(commands)))
        )
    except ValueError:
        print("Invalid input. Using default command.")
        command_indices = list(range(len(commands)))

    for index in command_indices:
        if index in range(len(commands)):
            command_name = list(commands.keys())[index]
            command = commands[command_name]
            run_command(command)
        else:
            print(f"Invalid command index: {index}")


if __name__ == "__main__":
    main()
