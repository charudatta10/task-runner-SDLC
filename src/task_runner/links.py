"""Symbolic/hard link and junction management (Windows-aware)."""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional


def create_link(path: str | Path, target: str | Path, link_type: str, force: bool = False) -> Path:
    """Create a symlink, hard link, or junction at *path* pointing to *target*."""
    p, t = Path(path).expanduser(), Path(target).expanduser()
    if p.exists() and not force:
        raise FileExistsError(f"Already exists: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)

    if link_type == "junction":
        _mklink_junction(p, t.absolute())
    elif link_type == "hard":
        if not t.exists():
            raise FileNotFoundError(f"Target not found: {t}")
        os.link(str(t), str(p))
    else:  # symlink
        os.symlink(str(t.absolute()), str(p))
    return p


def _mklink_junction(link: Path, target: Path) -> None:
    # mklink /J requires cmd.exe, but junctions work without admin rights.
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    else:
        os.symlink(str(target), str(link), target_is_directory=True)


def auto_link_type(target: Path) -> str:
    """Pick junction for dirs, hard link for files, symlink otherwise."""
    if target.exists() and target.is_dir():
        return "junction"
    if target.exists():
        return "hard"
    return "symlink"


def broken_links(root: str | Path, recurse: bool = False) -> List[Path]:
    """Return links whose target is missing."""
    root_p = Path(root).expanduser().resolve()
    candidates: Iterable[Path]
    if recurse:
        candidates = (p for p in root_p.rglob("*") if p.is_symlink() or _is_junction(p))
    else:
        candidates = (p for p in root_p.iterdir() if p.is_symlink() or _is_junction(p))

    broken: List[Path] = []
    for p in candidates:
        try:
            resolved = p.resolve(strict=True)
            if not resolved.exists():
                broken.append(p)
        except (OSError, RuntimeError):
            broken.append(p)
    return broken


def _is_junction(path: Path) -> bool:
    if not hasattr(path, "is_junction"):
        return False
    try:
        return bool(path.is_junction())
    except OSError:
        return False