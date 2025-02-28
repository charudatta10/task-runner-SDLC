import logging

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt
####################################################
# create generalized gitignore, logging function
# folders = [f"Archives_{project_name}", f"Home_{project_name}", f"Favorites_{project_name}"
#####################################################
# tasks.py

import zipfile
from pathlib import Path
import subprocess


def package():
    project_dir = Path("src/")
    output_filename = project_dir / "ypp.zip"

    # Create __main__.py
    main_script = project_dir / "__main__.py"
    if not main_script.exists():
        main_script.write_text("print('hello world')\n")

    # Package project into a zip file
    with zipfile.ZipFile(output_filename, "w") as zipf:
        for file_path in project_dir.rglob("*"):
            if not file_path.is_dir() and not file_path.name.endswith(".zip"):
                arcname = file_path.relative_to(project_dir)
                zipf.write(file_path, arcname)

    print(f"Packaged project into {output_filename}")


def build_mkdocs():
    """build MkDocs using specified Conda environment."""
    subprocess.run(["python", "-m", "mkdocs", "build"], check=True)


def serve_mkdocs():
    """build MkDocs using specified Conda environment."""
    subprocess.run(["python", "-m", "mkdocs", "serve"], check=True)


if __name__ == "__main__":
    ...
