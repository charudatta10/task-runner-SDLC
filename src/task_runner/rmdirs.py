"""Remove empty directories (bottom-up)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional


def remove_empty_dirs(root: str | Path, recurse: bool = False) -> List[Path]:
    """Return and remove empty directories under *root* (bottom-up when recursing)."""
    root_p = Path(root).expanduser().resolve()
    removed: List[Path] = []
    if not recurse:
        if not any(root_p.iterdir()):
            try:
                root_p.rmdir()
                removed.append(root_p)
            except OSError:
                pass
        return removed

    # deepest-first so newly-emptied parents are found too
    dirs = sorted(
        (p for p in root_p.rglob("*") if p.is_dir()),
        key=lambda p: len(p.parts), reverse=True,
    )
    dirs.append(root_p)
    for d in dirs:
        try:
            st = d.stat()
        except OSError:
            continue
        if not st.st_size and not any(d.iterdir()):
            try:
                d.rmdir()
                removed.append(d)
            except OSError:
                continue
    return removed