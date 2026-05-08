"""
tag_index.py
------------
Build a JSON index of every file in a tree along with the labels that
``auto_organize`` would assign (institute, topics, kind, date). The index is
useful for searching / filtering without moving anything.

CLI:
    python -m tools.tag_index <root> [--rules FILE] [--out PATH]
                              [--query "<text>"] [--institute NAME]
                              [--topic NAME] [--since YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from tools.auto_organize import classify, load_rules  # type: ignore  # noqa: E402


def build_index(root: str | Path, rules_file: Optional[str | Path] = None) -> List[dict]:
    root_p = Path(root).expanduser().resolve()
    rules = load_rules(rules_file)
    out: List[dict] = []
    for f in root_p.rglob("*"):
        if not f.is_file():
            continue
        try:
            label = classify(f, rules)
            stat = f.stat()
        except OSError:
            continue
        out.append(
            {
                "path": str(f),
                "name": f.name,
                "size": stat.st_size,
                "institute": label.institute,
                "topics": label.topics,
                "kind": label.kind,
                "date": label.date.isoformat() if label.date else None,
            }
        )
    return out


def filter_index(
    index: List[dict],
    *,
    query: Optional[str] = None,
    institute: Optional[str] = None,
    topic: Optional[str] = None,
    since: Optional[str] = None,
) -> List[dict]:
    q = query.lower() if query else None
    since_dt = datetime.fromisoformat(since) if since else None
    result = []
    for entry in index:
        if institute and entry["institute"] != institute:
            continue
        if topic and topic not in entry["topics"]:
            continue
        if q and q not in entry["name"].lower() and q not in entry["path"].lower():
            continue
        if since_dt and (not entry["date"] or datetime.fromisoformat(entry["date"]) < since_dt):
            continue
        result.append(entry)
    return result


def _cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Build a labeled file index.")
    p.add_argument("root")
    p.add_argument("--rules", default=None)
    p.add_argument("--out", default=None, help="Write JSON to PATH (default: stdout)")
    p.add_argument("--query", default=None)
    p.add_argument("--institute", default=None)
    p.add_argument("--topic", default=None)
    p.add_argument("--since", default=None, help="Only files dated on/after YYYY-MM-DD")
    args = p.parse_args(argv)

    idx = build_index(args.root, rules_file=args.rules)
    idx = filter_index(idx, query=args.query, institute=args.institute, topic=args.topic, since=args.since)

    blob = json.dumps(idx, indent=2)
    if args.out:
        Path(args.out).write_text(blob)
        print(f"Wrote {len(idx)} entries to {args.out}")
    else:
        print(blob)
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
