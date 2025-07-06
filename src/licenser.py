# © 2025 Charudatta Korde. Some Rights Reserved. Attribution Required. Non-Commercial Use & Share-Alike.
# https://raw.githubusercontent.com/charudatta10/task-runner-SDLC/refs/heads/main/src/templates/LICENSE
from invoke import task, Collection
from pathlib import Path
from .config import Config

def get_files(directory):
    for path in Path(directory).rglob("*"):
        if path.suffix in Config.FILE_TYPES:
            yield path

def license_text(ext):
    comment = Config.FILE_TYPES[ext]
    text = f"{comment} {Config.LICENSE_HEADER}\n{comment} {Config.LICENSE_URL}\n"
    return f"{text} -->\n" if comment == "<!--" else text

@task
def add_header(ctx, action="add"):
    """Add or remove license headers. Usage: inv license.add-header --action=remove"""
    for file_path in get_files("src"):
        text = license_text(file_path.suffix)
        content = file_path.read_text(encoding="utf-8")
        if action == "add" and Config.LICENSE_HEADER not in content:
            file_path.write_text(text + content, encoding="utf-8")
        elif action == "remove" and Config.LICENSE_HEADER in content:
            file_path.write_text(content.replace(text, ""), encoding="utf-8")

ns = Collection(add_header)
