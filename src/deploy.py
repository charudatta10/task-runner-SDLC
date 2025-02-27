# tasks.py

import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define commands in a dictionary
commands = {
    0: ("pull latest changes", "git pull origin main --force"),
    1: ("unit tests", "python -m unittest discover -s tests"),
    2: ("security checks", "bandit -r ."),
    3: ("pylint", "pylint ."),
    4: ("flake8", "flake8 ."),
    5: ("black", "black ."),
    6: ("add changes", "git add ."),
    7: ("commit changes", 'git commit -m "Deployment Commit"'),
    8: ("push changes", "git push -u origin main"),
}

# Default command index
DEFAULT_COMMAND_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def run_command(command):
    """Run a given command."""
    logging.info(f"Running {command}...")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command '{command}': {e}")


def display_commands():
    """Display available commands."""
    print("Available commands:")
    for index, (name, _) in commands.items():
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
            else DEFAULT_COMMAND_INDEX
        )
    except ValueError:
        print("Invalid input. Using default command.")
        command_indices = DEFAULT_COMMAND_INDEX

    for index in command_indices:
        if index in commands:
            description, command = commands[index]
            run_command(command)
        else:
            print(f"Invalid command index: {index}")


if __name__ == "__main__":
    main()
