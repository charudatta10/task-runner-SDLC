"""Find (and optionally remove) duplicate files using size + BLAKE2b hash."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional


def _hash(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.blake2b(digest_size=16)
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def find_duplicates(root: str | Path) -> Dict[str, List[Path]]:
    """Return ``{digest: [paths...]}`` for every file with at least one duplicate."""
    root_p = Path(root).expanduser().resolve()
    by_size: Dict[int, List[Path]] = defaultdict(list)
    for f in root_p.rglob("*"):
        if f.is_file():
            try:
                by_size[f.stat().st_size].append(f)
            except OSError:
                continue

    dup: Dict[str, List[Path]] = defaultdict(list)
    for size, paths in by_size.items():
        if len(paths) < 2 or size == 0:
            continue
        for p in paths:
            try:
                dup[_hash(p)].append(p)
            except OSError:
                continue
    return {h: ps for h, ps in dup.items() if len(ps) > 1}


def _pick_keeper(paths: List[Path], strategy: str) -> Path:
    if strategy == "shortest":
        return min(paths, key=lambda p: len(str(p)))
    if strategy == "newest":
        return max(paths, key=lambda p: p.stat().st_mtime)
    return paths[0]  # "first"


def dedupe(
    root: str | Path,
    *,
    delete: bool = False,
    keep: str = "first",
    report_path: Optional[str | Path] = None,
) -> dict:
    groups = find_duplicates(root)
    summary = {"groups": len(groups), "redundant": 0, "freed_bytes": 0, "deleted": []}
    report: List[dict] = []

    for digest, paths in groups.items():
        keeper = _pick_keeper(paths, keep)
        redundants = [p for p in paths if p != keeper]
        summary["redundant"] += len(redundants)
        for r in redundants:
            try:
                size = r.stat().st_size
            except OSError:
                size = 0
            summary["freed_bytes"] += size
            report.append({"hash": digest, "keeper": str(keeper), "duplicate": str(r), "bytes": size})
            if delete:
                try:
                    r.unlink()
                    summary["deleted"].append(str(r))
                    print(f"DELETED {r}")
                except OSError as e:
                    print(f"FAILED  {r}: {e}", file=sys.stderr)
            else:
                print(f"DUP     keep={keeper}  drop={r}")

    if report_path:
        Path(report_path).write_text(json.dumps(report, indent=2))
    return summary