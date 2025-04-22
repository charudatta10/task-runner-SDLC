from invoke import task, Collection
import os
import logging
from pathlib import Path

class Config:
    LICENSE_HEADER = "© 2025 Charudatta Korde. Some Rights Reserved."
    FILE_TYPES = {".py": "#", ".js": "//", ".html": "<!--", ".css": "/*"}

@task
def add_header(ctx, action="add"):
    """Add/remove license headers. Usage: `inv license.add-header --action=remove`"""
    for root, _, files in os.walk("src"):
        for file in files:
            ext = Path(file).suffix
            if ext in Config.FILE_TYPES:
                file_path = Path(root) / file
                comment = Config.FILE_TYPES[ext]
                license_text = f"{comment} {Config.LICENSE_HEADER}\n"

                with open(file_path, "r+", encoding="utf-8") as f:
                    content = f.read()
                    
                    if action == "add" and Config.LICENSE_HEADER not in content:
                        f.seek(0)
                        f.write(license_text + content)
                        logging.info(f"✅ Added header to {file}")
                    
                    elif action == "remove" and Config.LICENSE_HEADER in content:
                        updated = content.replace(license_text, "")
                        f.seek(0)
                        f.truncate()
                        f.write(updated)
                        logging.info(f"❌ Removed header from {file}")

# Create license namespace
ns = Collection(add_header)