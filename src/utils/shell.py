# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
import subprocess
import os

def run_command(command):
    """Run a shell command"""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {command}\n{e}")

def get_current_working_directory():
    """Get the current working directory"""
    return os.getcwd()

def change_directory(path):
    """Change the current working directory"""
    os.chdir(path)

