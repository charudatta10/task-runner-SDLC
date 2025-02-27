# main.py

from deploy import main as deploy
from file_gen_readme import main as generate_readme
from file_gen_license import create_license_file, add_license_headers, remove_license_headers
from initialize import main as init
from maintain import package, build_mkdocs, serve_mkdocs
from manger import main as manage

# Define available commands and their corresponding functions
commands = [
    ("deploy", deploy),
    ("generate_readme", generate_readme),
    ("create_license_file", create_license_file),
    ("add_license_headers", add_license_headers),
    ("remove_license_headers", remove_license_headers),
    ("init", init),
    ("package", package),
    ("build_mkdocs", build_mkdocs),
    ("serve_mkdocs", serve_mkdocs),
    ("manage", manage),
]

def display_commands():
    """Display available commands."""
    print("Available commands:")
    for index, (name, _) in enumerate(commands):
        print(f"{index}: {name}")

def main():
    display_commands()

    user_input = input("Enter the command index to run: ").strip()

    try:
        command_index = int(user_input)
        if command_index in range(len(commands)):
            _, command = commands[command_index]
            command()
        else:
            print(f"Invalid command index: {command_index}")
    except ValueError:
        print("Invalid input. Please enter a valid command index.")

if __name__ == "__main__":
    main()
