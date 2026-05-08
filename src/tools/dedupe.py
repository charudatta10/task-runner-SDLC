"""
dedupe.py
---------
Find (and optionally remove) duplicate files inside a directory tree using
a two-stage hash: size match → BLAKE2b digest. Pure stdlib.

CLI:
    python -m tools.dedupe <root> [--delete] [--keep first|shortest|newest]
                                  [--report PATH]

Programmatic:
    from tools.dedupe import find_duplicates, dedupe
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional


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
    """Return ``{digest: [paths…]}`` for every file with at least one duplicate."""
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
            entry = {"hash": digest, "keeper": str(keeper), "duplicate": str(r), "bytes": size}
            report.append(entry)
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


def _cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Find/remove duplicate files.")
    p.add_argument("root")
    p.add_argument("--delete", action="store_true")
    p.add_argument("--keep", choices=["first", "shortest", "newest"], default="first")
    p.add_argument("--report", default=None, help="Write JSON report to PATH")
    args = p.parse_args(argv)
    summary = dedupe(args.root, delete=args.delete, keep=args.keep, report_path=args.report)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
