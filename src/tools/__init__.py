from invoke import Collection
from .select_github_repo import select_github_repo
from .clone_github_repos import clone_github_repos
from .move_files import organize_files, create_patterns_sample
from .generate_system_reports import generate_system_reports

ns = Collection(
    select_github_repo,
    clone_github_repos,
    organize_files,
    create_patterns_sample,
    generate_system_reports,
)
