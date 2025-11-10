# © 2025 Charudatta Korde · Licensed under CC BY-NC-SA 4.0 · View License @ https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode


from pathlib import Path
from .config import Config


def get_files(directory):
    for path in Path(directory).rglob("*"):
        if path.suffix in Config.FILE_TYPES:
            yield path


def license_text(ext):
    comment = Config.FILE_TYPES[ext]
    text = f"{comment} {Config.LICENSE_HEADER}\n"
    return f"{text} -->\n" if comment == "<!--" else text


def add_header(action="add"):
    """Add or remove license headers. Usage: inv license.add-header --action=remove"""
    for file_path in get_files("src"):
        text = license_text(file_path.suffix)
        content = file_path.read_text(encoding="utf-8")
        if action == "add" and Config.LICENSE_HEADER not in content:
            file_path.write_text(text + content, encoding="utf-8")
        elif action == "remove" and Config.LICENSE_HEADER in content:
            file_path.write_text(content.replace(text, ""), encoding="utf-8")
