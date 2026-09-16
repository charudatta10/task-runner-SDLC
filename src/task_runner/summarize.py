"""Print per-category counts and sizes for a directory tree."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from task_runner.organize import load_rules


def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def _kind_for(ext: str, ext_map: Dict[str, List[str]]) -> str:
    for k, exts in ext_map.items():
        if ext in exts:
            return k
    return "Other"


def summarize(root: str | Path, rules_file: Optional[str | Path] = None) -> dict:
    root_p = Path(root).expanduser().resolve()
    rules = load_rules(rules_file)
    ext_map = rules.get("extensions", {})

    by_kind: Dict[str, dict] = defaultdict(lambda: {"count": 0, "bytes": 0})
    by_institute: Dict[str, dict] = defaultdict(lambda: {"count": 0, "bytes": 0})
    by_topic: Dict[str, dict] = defaultdict(lambda: {"count": 0, "bytes": 0})

    institutes = set(k for k in rules.get("institutes", {}).keys() if not k.startswith("_"))
    institutes.add("_unsorted")

    total_count = total_bytes = 0
    for f in root_p.rglob("*"):
        if not f.is_file():
            continue
        try:
            size = f.stat().st_size
        except OSError:
            continue
        total_count += 1
        total_bytes += size

        kind = _kind_for(f.suffix.lower(), ext_map)
        by_kind[kind]["count"] += 1
        by_kind[kind]["bytes"] += size

        try:
            rel_parts = f.relative_to(root_p).parts
        except ValueError:
            rel_parts = ()
        if rel_parts and rel_parts[0] in institutes:
            by_institute[rel_parts[0]]["count"] += 1
            by_institute[rel_parts[0]]["bytes"] += size
            if len(rel_parts) >= 2:
                by_topic[rel_parts[1]]["count"] += 1
                by_topic[rel_parts[1]]["bytes"] += size

    return {
        "root": str(root_p),
        "total": {"count": total_count, "bytes": total_bytes, "human": _human(total_bytes)},
        "by_kind": dict(by_kind),
        "by_institute": dict(by_institute),
        "by_topic": dict(by_topic),
    }


def _print_table(title: str, rows: Dict[str, dict]) -> None:
    if not rows:
        return
    print(f"\n{title}")
    print("-" * len(title))
    width = max((len(k) for k in rows), default=10)
    for k, v in sorted(rows.items(), key=lambda kv: -kv[1]["bytes"]):
        print(f"  {k.ljust(width)}  {v['count']:>6}  {_human(v['bytes']):>10}")


def print_summary(s: dict, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(s, indent=2))
        return
    print(f"Root  : {s['root']}")
    print(f"Total : {s['total']['count']} files  ({s['total']['human']})")
    _print_table("By kind", s["by_kind"])
    _print_table("By institute", s["by_institute"])
    _print_table("By topic", s["by_topic"])