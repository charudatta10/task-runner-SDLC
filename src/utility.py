# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import logging
import os
import urllib.request
import json


def run_command(ctx, command, success_msg, error_msg):
    """DRY helper to run commands with consistent logging"""
    try:
        ctx.run(command)
        logging.info(success_msg)
        return True
    except Exception as e:
        logging.error(f"{error_msg}: {e}")
        return False


def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return False


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
