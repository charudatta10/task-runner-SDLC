"""Build a labeled JSON index of every file in a tree."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from task_runner.organize import classify, load_rules


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