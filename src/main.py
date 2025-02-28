import logging

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt

# main.py

from deploy import main as deploy
from file_gen_readme import main as generate_readme
from file_gen_license import main as process_file_headers
from initialize import main as init
from maintain import package, build_mkdocs, serve_mkdocs
from manger import main as manage

# Define available commands and their corresponding functions
commands = [
    ("init", init),
    ("generate readme", generate_readme),
    ("process file headers", process_file_headers),
    ("deploy", deploy),
    ("package", package),
    ("build mkdocs", build_mkdocs),
    ("serve mkdocs", serve_mkdocs),
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
