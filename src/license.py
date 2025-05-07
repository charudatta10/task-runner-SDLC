# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
import os
import logging
from pathlib import Path
from .config import Config
from .utility import download_file


@task
def add_header(ctx, action="add"):
    """Add/remove license headers. Usage: `inv license.add-header --action=remove`"""
    for file_path in _get_files_with_supported_extensions("src"):
        license_text = _generate_license_text(file_path.suffix)
        
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            
            if action == "add" and Config.LICENSE_HEADER not in content:
                f.seek(0)
                f.write(license_text + content)
                logging.info(f"✅ Added header to {file_path}")
            
            elif action == "remove" and Config.LICENSE_HEADER in content:
                updated = content.replace(license_text, "")
                f.seek(0)
                f.truncate()
                f.write(updated)
                logging.info(f"❌ Removed header from {file_path}")


def _get_files_with_supported_extensions(directory):
    """Yield file paths with supported extensions in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            ext = Path(file).suffix
            if ext in Config.FILE_TYPES:
                yield Path(root) / file


def _generate_license_text(extension):
    """Generate the license text based on the file extension."""
    comment = Config.FILE_TYPES[extension]
    license_text = f"{comment} {Config.LICENSE_HEADER}\n{comment} {Config.LICENSE_URL}\n"
    if comment == "<!--":
        license_text = f"{license_text} -->\n"
    return license_text

# Create license namespace
ns = Collection(add_header)