from invoke import task
import os
import shutil
from ..config import Config

@task
def generate_system_reports(ctx, destination_folder=Config.BACKUP_DIR):
    """
    Generate system reports and copy PowerShell scripts from source to destination.

    Args:
        source_folder (str): The source folder containing PowerShell scripts.
        destination_folder (str): The destination folder for copying scripts.
    """
    os.chdir(destination_folder)
    ctx.run("scoop export > scoop.json")
    ctx.run("winget export -o winget.json")
    ctx.run("pipx list --json > pipx.json")
    ctx.run("choco list > choco.txt")
    ctx.run("conda env export --json > conda_base.json")
    ctx.run("conda env export --name s --json > conda_s.json")
    ctx.run("pip list --format=json > pip.json")
    ctx.run("npm -g list --json > npm.json")
    shutil.copy(Config.PROFILE_PATH, destination_folder)
