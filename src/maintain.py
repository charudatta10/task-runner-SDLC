# Copyright 2076 CHARUDATTA KORDE LLC - Apache-2.0 License
#
# https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/apache-2.0.txt
####################################################
# create generalized gitignore, logging function
# folders = [f"Archives_{project_name}", f"Home_{project_name}", f"Favorites_{project_name}"
#####################################################
# tasks.py

from invoke import task, Collection

from invoke import task
import zipfile
from pathlib import Path


@task
def package(ctx):
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


@task
def build_mkdocs(ctx):
    """build MkDocs using specified Conda environment."""
    with ctx.run(f"conda activate s", shell=True):
        ctx.run(f"python -m mkdocs build")


@task
def serve_mkdocs(ctx):
    """build MkDocs using specified Conda environment."""
    with ctx.run(f"conda activate s", shell=True):
        ctx.run(f"python -m mkdocs serve")


# Create a collection of tasks
ns = Collection(
    build_mkdocs,
    serve_mkdocs,
    package,
)
ns.name = "maintain"

if __name__ == "__main__":
    default(context())
