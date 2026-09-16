"""task-runner CLI entry point."""

from __future__ import annotations

import json
import pathlib

import click

from task_runner import __version__
from task_runner import analyze as analyze_mod
from task_runner import scaffold as scaffold_mod
from task_runner import summarize as summarize_mod
from task_runner.dups import dedupe
from task_runner.index import build_index, filter_index
from task_runner.links import auto_link_type, broken_links, create_link
from task_runner.organize import auto_organize
from task_runner.packages import list_managers
from task_runner.rmdirs import remove_empty_dirs
from task_runner.summarize import print_summary


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Personal CLI toolbox."""


# --- file organization ----------------------------------------------------


@main.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--dest", type=click.Path(resolve_path=True), help="Destination root (default: <source>/_organized)")
@click.option("--rules", type=click.Path(exists=True, dir_okay=False), help="Path to label_rules.json")
@click.option("--dry-run", is_flag=True, help="Print plan without moving")
@click.option("--copy", is_flag=True, help="Copy instead of move")
@click.option("--no-stamp", is_flag=True, help="Do not prefix YYYYMMDD on filenames")
@click.option("--no-peek", is_flag=True, help="Filename-only matching (skip text peek)")
@click.option("--recursive", is_flag=True, help="Recurse into subdirectories")
def organize(source, dest, rules, dry_run, copy, no_stamp, no_peek, recursive) -> None:
    """Auto-organize files into <Institute>/<Topic>/<YYYY-MM>/ hierarchy."""
    summary = auto_organize(
        source=source,
        dest=dest,
        rules_file=rules,
        dry_run=dry_run,
        copy=copy,
        stamp=not no_stamp,
        peek=not no_peek,
        recursive=recursive,
    )
    click.echo(json.dumps(summary, indent=2))


@main.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--delete", is_flag=True, help="Actually delete duplicates")
@click.option("--keep", type=click.Choice(["first", "shortest", "newest"]), default="first", help="Which copy to keep")
@click.option("--report", type=click.Path(dir_okay=False), help="Write JSON report to PATH")
def dups(root, delete, keep, report) -> None:
    """Find (and optionally delete) duplicate files in ROOT."""
    summary = dedupe(root, delete=delete, keep=keep, report_path=report)
    click.echo(json.dumps(summary, indent=2))


@main.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--rules", type=click.Path(exists=True, dir_okay=False), help="Path to label_rules.json")
@click.option("--out", type=click.Path(dir_okay=False), help="Write JSON to PATH (default: stdout)")
@click.option("--query", help="Substring filter on name/path")
@click.option("--institute", help="Filter by institute label")
@click.option("--topic", help="Filter by topic label")
@click.option("--since", help="Only files dated on/after YYYY-MM-DD")
def index(root, rules, out, query, institute, topic, since) -> None:
    """Build a labeled JSON index of files in ROOT."""
    idx = build_index(root, rules_file=rules)
    idx = filter_index(idx, query=query, institute=institute, topic=topic, since=since)
    blob = json.dumps(idx, indent=2)
    if out:
        pathlib.Path(out).write_text(blob)
        click.echo(f"Wrote {len(idx)} entries to {out}")
    else:
        click.echo(blob)


@main.command(name="summarize")
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--rules", type=click.Path(exists=True, dir_okay=False), help="Path to label_rules.json")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def summarize_cmd(root, rules, as_json) -> None:
    """Print per-category counts and sizes for ROOT."""
    print_summary(summarize_mod.summarize(root, rules_file=rules), as_json=as_json)


# --- links, dirs -----------------------------------------------------------


@main.group()
def links() -> None:
    """Create and repair file links."""


@links.command()
@click.argument("path", type=click.Path(resolve_path=True))
@click.argument("target", type=click.Path(resolve_path=True))
@click.option("--type", "link_type", type=click.Choice(["symlink", "hard", "junction", "auto"]), default="auto", help="Link kind (auto: junction for dirs, hard for files)")
@click.option("--force", is_flag=True, help="Overwrite existing link")
def create(path, target, link_type, force) -> None:
    """Create a symlink, hard link, or junction."""
    if link_type == "auto":
        link_type = auto_link_type(pathlib.Path(target))
    try:
        p = create_link(path, target, link_type, force=force)
        click.echo(f"{link_type}: {p} -> {target}")
    except (FileExistsError, FileNotFoundError, RuntimeError, OSError) as e:
        raise click.ClickException(str(e))


@links.command(name="broken")
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--recurse", is_flag=True, help="Scan subdirectories")
@click.option("--remove", is_flag=True, help="Remove broken links found")
def broken(root, recurse, remove) -> None:
    """Find (and optionally remove) broken links."""
    found = broken_links(root, recurse=recurse)
    if not found:
        click.echo("No broken links found.")
        return
    for p in found:
        if remove:
            try:
                p.unlink()
                click.echo(f"removed: {p}")
            except OSError as e:
                click.echo(f"FAILED  {p}: {e}")
        else:
            click.echo(f"broken: {p}")


@main.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--recurse", is_flag=True, help="Remove empty dirs bottom-up within tree")
def rmdirs(root, recurse) -> None:
    """Remove empty directories."""
    removed = remove_empty_dirs(root, recurse=recurse)
    for d in removed:
        click.echo(f"removed: {d}")
    click.echo(f"Removed {len(removed)} empty director(ies).")


# --- analysis --------------------------------------------------------------


@main.command()
@click.argument("root", type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option("--type", "which", type=click.Choice(["functions", "variables", "orphaned", "all"]), default="all")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def analyze(root, which, as_json) -> None:
    """Static analysis of Python scripts (unused code, orphans)."""
    if as_json:
        if which == "all":
            result = analyze_mod.analyze_all(root)
        else:
            result = {"unused_functions": [], "unused_variables": [], "orphaned_scripts": []}
            result[f"{'functions' if which == 'functions' else 'variables' if which == 'variables' else 'orphaned_scripts'}"] = {
                "functions": lambda: analyze_mod.unused_functions(root),
                "variables": lambda: analyze_mod.unused_variables(root),
                "orphaned": lambda: analyze_mod.orphaned_scripts(root),
            }[which]()
        click.echo(json.dumps(result, indent=2))
        return

    if which in ("functions", "all"):
        r = analyze_mod.unused_functions(root)
        click.echo(f"\n--- Unused Functions ({len(r)}) ---")
        for x in r:
            click.echo(f"  {x}")
    if which in ("variables", "all"):
        r = analyze_mod.unused_variables(root)
        click.echo(f"\n--- Unused Variables ({len(r)}) ---")
        for x in r:
            click.echo(f"  {x}")
    if which in ("orphaned", "all"):
        r = analyze_mod.orphaned_scripts(root)
        click.echo(f"\n--- Orphaned Scripts ({len(r)}) ---")
        for x in r:
            click.echo(f"  {x}")


# --- packages --------------------------------------------------------------


@main.command()
@click.option("--export", type=click.Path(dir_okay=False), help="Write inventory JSON to PATH")
def packages(export) -> None:
    """List installed packages across package managers."""
    results = list_managers()
    for r in results:
        status = "installed" if r["installed"] else "MISSING"
        click.echo(f"[{status}] {r['name']}: {r['error'] or ''}")
        pkgs = r["packages"]
        if pkgs:
            for p in (pkgs[:10] if isinstance(pkgs, list) else pkgs.splitlines()[:10]):
                click.echo(f"    {p}")
            if isinstance(pkgs, list) and len(pkgs) > 10:
                click.echo(f"    ... {len(pkgs) - 10} more")
    if export:
        pathlib.Path(export).write_text(json.dumps(results, indent=2), encoding="utf-8")
        click.echo(f"Wrote inventory to {export}")


# --- scaffolding -----------------------------------------------------------


@main.command()
@click.argument("path", type=click.Path(resolve_path=True))
@click.option("--type", "ptype", type=click.Choice(["generic", "python", "powershell"]), default="generic")
def scaffold(path, ptype) -> None:
    """Scaffold a project folder structure."""
    root = scaffold_mod.project(path, ptype=ptype)
    click.echo(f"Project scaffolded in {root}")


@main.command()
@click.option("--path", "dest", type=click.Path(resolve_path=True), default="notes", help="Root path for notes")
@click.option("--topic", help="Optional topic sub-folder")
def notes(dest, topic) -> None:
    """Initialize a date-based notes folder structure."""
    root = scaffold_mod.notes(dest, topic=topic)
    click.echo(f"Notes folder initialized in {root}")


@main.command()
@click.option("--path", "dest", type=click.Path(resolve_path=True), default="tasks")
def tasks(dest) -> None:
    """Initialize a task/sprint folder structure."""
    root = scaffold_mod.tasks(dest)
    click.echo(f"Task folder initialized in {root}")


if __name__ == "__main__":
    main()