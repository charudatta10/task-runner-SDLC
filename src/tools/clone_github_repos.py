from invoke import task
import json

@task
def clone_github_repos(ctx, source_user="charudatta10"):
    """
    Clone all repositories from a specified GitHub user.

    Args:
        source_user (str): The GitHub username to clone repositories from.
    """
    result = ctx.run(f"gh repo list --source {source_user} --json nameWithOwner")
    repos = json.loads(result.stdout)
    for repo in repos:
        repo_name = repo["nameWithOwner"]
        ctx.run(f"gh repo clone {repo_name}")
        print(f"Cloned repository: {repo_name}")
    print(f"Cloned all repositories from GitHub user: {source_user}.")
