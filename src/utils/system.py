# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import os
import tempfile
import platform
import sys

def get_environment_variable(variable_name):
    """Get an environment variable"""
    return os.environ.get(variable_name)

def set_environment_variable(variable_name, value):
    """Set an environment variable"""
    os.environ[variable_name] = value

def get_user_home_directory():
    """Get the user's home directory"""
    return os.path.expanduser("~")

def get_temp_directory():
    """Get the temporary directory"""
    return tempfile.gettempdir()

def create_temp_file():
    """Create a temporary file"""
    return tempfile.NamedTemporaryFile(delete=False)

def create_temp_directory():
    """Create a temporary directory"""
    return tempfile.mkdtemp()

def get_platform():
    """Get the operating system platform"""
    return platform.system()

def get_python_version():
    """Get the Python version"""
    return sys.version
