"""Scaffold project, notes, and task folder structures."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Dict, List


def project(root: str | Path, ptype: str = "generic") -> Path:
    """Create a project folder structure: generic, python, or powershell."""
    root_p = Path(root).expanduser().resolve()
    name = root_p.name

    dirs: List[str] = []
    files: Dict[str, str] = {
        ".gitignore": "# OS\nThumbs.db\n.DS_Store\n# IDE\n.vscode/\n.idea/\n# Build\ndist/\nbuild/\n*.log\n",
        "README.md": f"# {name}\n\nProject description.\n",
    }

    if ptype == "python":
        dirs = ["src", "tests", "docs", "data", "notebooks"]
        pkg = name.replace("-", "_")
        files.update({
            "pyproject.toml": (
                "[build-system]\nrequires = [\"hatchling\"]\n"
                'build-backend = "hatchling.build"\n\n'
                "[project]\n"
                f'name = "{pkg}"\nversion = "0.1.0"\n'
                'description = ""\nrequires-python = ">=3.10"\n'
            ),
        })
    elif ptype == "powershell":
        dirs = ["Public", "Private", "Tests", "Docs"]
        files.update({
            f"{name}.psd1": (
                "@{\n"
                f"    RootModule        = '{name}.psm1'\n"
                "    ModuleVersion     = '0.1.0'\n"
                f"    GUID              = '{_guid()}'\n"
                "    Author            = ''\n"
                "    Description       = ''\n"
                "    PowerShellVersion = '7.0'\n"
                "    FunctionsToExport = @()\n"
                "}\n"
            ),
            f"{name}.psm1": f"#Requires -Version 7.0\n# {name}\n",
        })
    else:  # generic
        dirs = ["src", "tests", "docs"]

    for d in dirs:
        (root_p / d).mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        target = root_p / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(content, encoding="utf-8")

    return root_p


def _guid() -> str:
    import uuid
    return str(uuid.uuid4())


def notes(root: str | Path, topic: str | None = None) -> Path:
    """Initialize a date-based notes structure with templates and today's entry."""
    root_p = Path(root).expanduser().resolve()
    root_p = root_p / topic if topic else root_p
    root_p.mkdir(parents=True, exist_ok=True)

    templates = {
        "daily.md": "# Daily Notes — {date}\n\n## Highlights\n\n-\n\n## Tasks\n\n- [ ]\n\n## Notes\n\n## Tomorrow\n\n-\n",
        "meeting.md": (
            "# Meeting — {date}\n\n**Topic:**\n**Attendees:**\n**Duration:**\n\n## Agenda\n\n1.\n\n"
            "## Notes\n\n## Action Items\n\n- [ ]\n"
        ),
        "idea.md": "# Idea — {date}\n\n**Concept:**\n\n## Context\n\n## Implementation Sketch\n\n## References\n\n",
    }
    tpl_dir = root_p / "_templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    for fname, content in templates.items():
        t = tpl_dir / fname
        if not t.exists():
            t.write_text(content.replace("{date}", today), encoding="utf-8")

    entry_dir = root_p / str(date.today().year)
    entry_dir.mkdir(parents=True, exist_ok=True)
    entry = entry_dir / f"{date.today():%m-%d}-notes.md"
    if not entry.exists():
        entry.write_text(f"# Notes — {today}\n\n## \n", encoding="utf-8")

    (root_p / "_archive").mkdir(parents=True, exist_ok=True)
    return root_p


def tasks(root: str | Path) -> Path:
    """Initialize a task/sprint folder structure with templates."""
    root_p = Path(root).expanduser().resolve()
    root_p.mkdir(parents=True, exist_ok=True)

    for d in ["backlog", "sprint-current", "sprint-next", "completed", "archive", "templates"]:
        (root_p / d).mkdir(parents=True, exist_ok=True)

    now = datetime.now().isoformat(timespec="seconds")
    templates = {
        "task.md": (
            "# Task: {title}\n\n**Status:** Backlog\n**Priority:** Medium\n"
            f"**Created:** {now}\n**Estimated:** \n\n## Description\n\n## Acceptance Criteria\n\n- [ ]\n\n## Notes\n\n"
        ),
        "sprint.md": "# Sprint {number}\n\n**Dates:** {start} → {end}\n**Goal:**\n\n## Tasks\n\n- [ ]\n\n## Retrospective\n\n### Went Well\n\n### To Improve\n\n### Actions\n\n",
    }
    tpl_dir = root_p / "templates"
    for fname, content in templates.items():
        t = tpl_dir / fname
        if not t.exists():
            t.write_text(content, encoding="utf-8")

    sprint_readme = root_p / "sprint-current" / "README.md"
    if not sprint_readme.exists():
        sprint_readme.write_text("# Current Sprint\n\nSee [templates/sprint.md](templates/sprint.md).\n", encoding="utf-8")

    return root_p