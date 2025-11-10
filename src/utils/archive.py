# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode

import zipfile
import logging

def create_zip_file(file_path, files):
    """Create a zip file"""
    with zipfile.ZipFile(file_path, "w") as zf:
        for file in files:
            zf.write(file)
    logging.info(f"Created {file_path}")

def extract_zip_file(file_path, destination_folder):
    """Extract a zip file"""
    with zipfile.ZipFile(file_path, "r") as zf:
        zf.extractall(destination_folder)
    logging.info(f"Extracted {file_path} to {destination_folder}")
