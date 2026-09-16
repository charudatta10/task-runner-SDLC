"""Auto-organize files into <Institute>/<Topic>/<YYYY-MM>/ hierarchy."""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

DEFAULT_RULES_FILE = Path(__file__).parent / "data" / "label_rules.json"

DATE_RE = re.compile(
    r"(?P<y>20\d{2}|19\d{2})[-_./]?(?P<m>0[1-9]|1[0-2])[-_./]?(?P<d>0[1-9]|[12]\d|3[01])"
)
_SEP_RE = re.compile(r"[._\-/\\]+")


def load_rules(rules_path: Optional[str | Path] = None) -> dict:
    p = Path(rules_path) if rules_path else DEFAULT_RULES_FILE
    if not p.exists():
        raise FileNotFoundError(f"Label rules not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _date_from_name(name: str) -> Optional[datetime]:
    m = DATE_RE.search(name)
    if not m:
        return None
    try:
        return datetime(int(m["y"]), int(m["m"]), int(m["d"]))
    except ValueError:
        return None


def _peek_text(path: Path, limit: int = 8192) -> str:
    """Best-effort read of the first few KB as text. Empty string on failure."""
    text_like = {".txt", ".md", ".csv", ".tsv", ".html", ".htm", ".log", ".json", ".xml"}
    try:
        if path.suffix.lower() in text_like:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(limit)
    except Exception:
        pass
    return ""


@dataclass
class Label:
    institute: str = "_unsorted"
    topics: List[str] = field(default_factory=list)
    kind: str = "Other"
    date: Optional[datetime] = None

    @property
    def primary_topic(self) -> str:
        return self.topics[0] if self.topics else self.kind

    @property
    def date_bucket(self) -> str:
        return self.date.strftime("%Y-%m") if self.date else "undated"

    @property
    def date_stamp(self) -> str:
        return self.date.strftime("%Y%m%d") if self.date else ""


def _normalize(s: str) -> str:
    return _SEP_RE.sub(" ", s.lower())


def _match_any(haystack: str, needles: Iterable[str]) -> bool:
    return any(_normalize(n) in haystack for n in needles if n)


def classify(path: Path, rules: dict, peek: bool = True) -> Label:
    name = _normalize(path.name)
    text = _normalize(_peek_text(path)) if peek else ""
    blob = f"{name} {text}"

    institute = "_unsorted"
    for inst, kws in rules.get("institutes", {}).items():
        if inst.startswith("_"):
            continue
        if _match_any(blob, kws):
            institute = inst
            break

    topics: List[str] = []
    for topic, kws in rules.get("topics", {}).items():
        if _match_any(blob, kws):
            topics.append(topic)

    ext = path.suffix.lower()
    kind = "Other"
    for k, exts in rules.get("extensions", {}).items():
        if ext in exts:
            kind = k
            break

    dt = _date_from_name(path.name)
    if dt is None:
        try:
            dt = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            dt = None

    return Label(institute=institute, topics=topics, kind=kind, date=dt)


def _unique(dest_dir: Path, name: str) -> Path:
    p = dest_dir / name
    if not p.exists():
        return p
    stem, suf = os.path.splitext(name)
    i = 1
    while True:
        cand = dest_dir / f"{stem}_v{i}{suf}"
        if not cand.exists():
            return cand
        i += 1


def _stamped_name(path: Path, label: Label) -> str:
    if not label.date_stamp:
        return path.name
    if path.name.startswith(label.date_stamp):
        return path.name
    return f"{label.date_stamp}_{path.name}"


@dataclass
class Plan:
    src: Path
    dst: Path
    label: Label


def build_plan(
    source: Path,
    dest: Path,
    rules: dict,
    *,
    stamp: bool = True,
    peek: bool = True,
    recursive: bool = False,
) -> List[Plan]:
    plans: List[Plan] = []
    iterator = source.rglob("*") if recursive else source.glob("*")
    for f in iterator:
        if not f.is_file():
            continue
        try:
            f.resolve().relative_to(dest.resolve())
            continue
        except ValueError:
            pass
        label = classify(f, rules, peek=peek)
        target_dir = dest / label.institute / label.primary_topic / label.date_bucket
        target_name = _stamped_name(f, label) if stamp else f.name
        plans.append(Plan(src=f, dst=target_dir / target_name, label=label))
    return plans


def apply_plan(plans: List[Plan], *, copy: bool = False, dry_run: bool = False) -> Tuple[int, int]:
    moved = failed = 0
    for plan in plans:
        try:
            if not dry_run:
                plan.dst.parent.mkdir(parents=True, exist_ok=True)
                final = _unique(plan.dst.parent, plan.dst.name)
                if copy:
                    shutil.copy2(plan.src, final)
                else:
                    shutil.move(str(plan.src), str(final))
                action = "COPIED" if copy else "MOVED"
            else:
                action = "WOULD-MOVE"
                final = plan.dst
            tags = ",".join(plan.label.topics) or plan.label.kind
            print(
                f"{action} [{plan.label.institute} | {tags} | {plan.label.date_bucket}] "
                f"{plan.src.name} -> {final}"
            )
            moved += 1
        except Exception as e:
            failed += 1
            print(f"FAILED {plan.src}: {e}")
    return moved, failed


def auto_organize(
    source: str | Path,
    dest: Optional[str | Path] = None,
    rules_file: Optional[str | Path] = None,
    *,
    dry_run: bool = False,
    copy: bool = False,
    stamp: bool = True,
    peek: bool = True,
    recursive: bool = False,
) -> dict:
    """Organize files in *source* into *dest* labeled by institute/topic/date."""
    source_p = Path(source).expanduser().resolve()
    if not source_p.is_dir():
        raise NotADirectoryError(f"Not a directory: {source_p}")
    dest_p = Path(dest).expanduser().resolve() if dest else source_p / "_organized"
    dest_p.mkdir(parents=True, exist_ok=True)

    rules = load_rules(rules_file)
    plans = build_plan(
        source_p, dest_p, rules,
        stamp=stamp, peek=peek, recursive=recursive,
    )
    if not plans:
        print("Nothing to organize.")
        return {"planned": 0, "moved": 0, "failed": 0, "dest": str(dest_p)}

    moved, failed = apply_plan(plans, copy=copy, dry_run=dry_run)
    print(f"Done. planned={len(plans)} moved={moved} failed={failed} dest={dest_p}")
    return {"planned": len(plans), "moved": moved, "failed": failed, "dest": str(dest_p)}