from invoke import Collection
from .select_github_repo import select_github_repo
from .clone_github_repos import clone_github_repos
from .move_files import move_files
from .generate_system_reports import generate_system_reports

ns = Collection(
    select_github_repo,
    clone_github_repos,
    move_files,
    generate_system_reports,
)
