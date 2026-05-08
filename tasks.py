from invoke import task, Collection
import sys
import os
import importlib.util

from pathlib import Path
import sys


BASE_DIR = Path(__file__).parent
SRC_PATH = BASE_DIR / "src"

sys.path.insert(0, str(SRC_PATH))

from Code import config

import tools.pkm_tools
import tools.clone_github_repos
import tools.generate_system_reports
import tools.select_github_repo
import tools.move_files
import tools.ai_file_renamer
import tools.ai_docsGen
import tools.auto_organize
import tools.dedupe
import tools.summarize_folder
import tools.tag_index


@task
def init_repo(c):
    """Initialize a new git repository."""
    c.run("git init")


@task
def ai_doc_gen_task(c, repo_path=".", template_file="prompt_docgen.json", output_dir="docs"):
    """Generate documentation using AI."""
    tools.ai_docsGen.ai_doc_gen(repo_path=repo_path, template_file=template_file, output_dir=output_dir)


@task
def file_renamer(c, directory=".", dry_run=False):
    """Rename files using AI based on content."""
    renamer = tools.ai_file_renamer.AIFileRenamer()
    renamer.rename_directory(directory, dry_run=dry_run)


@task
def commit_changes(c, message):
    """Commit and push changes to main branch."""
    c.run("git pull origin main")
    c.run("git add .")
    c.run(f'git commit -m "{message}"')
    c.run("git push -u origin main")


@task
def lint(c, target="."):
    """Run ruff linter and formatter."""
    c.run(f"ruff check {target}")
    c.run(f"ruff format {target}")


@task
def run_tests(c):
    """Run pytest with coverage."""
    c.run("pytest --cov=src --cov-report=term-missing")


@task
def security_check(c):
    """Run security check with bandit."""
    c.run("bandit -r .")


@task
def move_files(c, folder=".", patterns=None, destination=None):
    """Move files to organized directories based on patterns."""
    if patterns is None:
        patterns = "file_patterns.json"
    if destination is None:
        destination = folder
    tools.move_files.clean_folder(folder=folder, patterns=patterns, destination=destination)


@task
def create_patterns(c, output_file="file_patterns.json"):
    """Create a sample file patterns JSON file."""
    tools.move_files.create_patterns_sample(output_file=output_file)


@task
def auto_organize(
    c,
    source=".",
    dest=None,
    rules=None,
    dry_run=False,
    copy=False,
    no_stamp=False,
    no_peek=False,
    recursive=False,
):
    """Auto-organize files into <Institute>/<Topic>/<YYYY-MM>/ folders.

    Labels: NIT_Goa, NFSUG, NFSUD (configurable in src/tools/label_rules.json).
    """
    summary = tools.auto_organize.auto_organize(
        source=source,
        dest=dest,
        rules_file=rules,
        dry_run=dry_run,
        copy=copy,
        stamp=not no_stamp,
        peek=not no_peek,
        recursive=recursive,
    )
    print(summary)


@task
def dedupe(c, root=".", delete=False, keep="first", report=None):
    """Find (and optionally delete) duplicate files in ROOT."""
    tools.dedupe.dedupe(root=root, delete=delete, keep=keep, report_path=report)


@task
def summarize(c, root=".", rules=None, json_out=False):
    """Print per-category counts and sizes for ROOT."""
    s = tools.summarize_folder.summarize(root, rules_file=rules)
    if json_out:
        import json as _json
        print(_json.dumps(s, indent=2))
    else:
        print(f"Root  : {s['root']}")
        print(f"Total : {s['total']['count']} files  ({s['total']['human']})")
        for label, rows in (("By kind", s["by_kind"]),
                            ("By institute", s["by_institute"]),
                            ("By topic", s["by_topic"])):
            if not rows:
                continue
            print(f"\n{label}")
            for k, v in sorted(rows.items(), key=lambda kv: -kv[1]["bytes"]):
                print(f"  {k:<20} {v['count']:>5}  {v['bytes']} B")


@task
def tag_index(c, root=".", rules=None, out=None, query=None,
              institute=None, topic=None, since=None):
    """Build/query a labeled JSON index of files in ROOT."""
    idx = tools.tag_index.build_index(root, rules_file=rules)
    idx = tools.tag_index.filter_index(
        idx, query=query, institute=institute, topic=topic, since=since
    )
    import json as _json
    blob = _json.dumps(idx, indent=2)
    if out:
        from pathlib import Path as _P
        _P(out).write_text(blob)
        print(f"Wrote {len(idx)} entries to {out}")
    else:
        print(blob)


generate_tags = tools.pkm_tools.generate_tags
generate_moc = tools.pkm_tools.generate_moc
generate_links = tools.pkm_tools.generate_links
clone_repos = tools.clone_github_repos.clone_github_repos
generate_report = tools.generate_system_reports.generate_system_reports
list_system_tools = tools.generate_system_reports.list_system_tools
quick_backup = tools.generate_system_reports.quick_backup
select_repo = tools.select_github_repo.select_github_repo


ns = Collection(
    init_repo,
    ai_doc_gen_task,
    file_renamer,
    commit_changes,
    lint,
    run_tests,
    security_check,
    move_files,
    create_patterns,
    auto_organize,
    dedupe,
    summarize,
    tag_index,
    generate_tags,
    generate_moc,
    generate_links,
    clone_repos,
    generate_report,
    list_system_tools,
    quick_backup,
    select_repo,
)
