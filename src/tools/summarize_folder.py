"""
summarize_folder.py
-------------------
Walk a directory and print a per-category summary (counts, total size, last
modified). Categories come from label_rules.json's "extensions" map; when the
directory was produced by ``auto_organize`` the institute/topic layout is also
summarized.

CLI:
    python -m tools.summarize_folder <root> [--rules FILE] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from tools.auto_organize import load_rules  # type: ignore  # noqa: E402


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

        # institute/topic inferred from path under root (auto_organize layout)
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


def _cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Summarize folder contents.")
    p.add_argument("root")
    p.add_argument("--rules", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    s = summarize(args.root, rules_file=args.rules)
    if args.json:
        print(json.dumps(s, indent=2))
        return 0
    print(f"Root  : {s['root']}")
    print(f"Total : {s['total']['count']} files  ({s['total']['human']})")
    _print_table("By kind", s["by_kind"])
    _print_table("By institute", s["by_institute"])
    _print_table("By topic", s["by_topic"])
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
