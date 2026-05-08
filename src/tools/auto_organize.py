"""
auto_organize.py
----------------
Auto-organize a folder of files into a labeled hierarchy:

    <destination>/<Institute>/<Topic>/<YYYY-MM>/<original-or-stamped-name>

Labels are derived from (in order):
  1. Filename keywords           (matched against label_rules.json)
  2. Lightweight text peek       (first ~8 KB of .txt/.md/.csv/.html, PDF page 1
                                  if pypdf is available — completely optional)
  3. File mtime                  (used as the date bucket and an optional
                                  YYYYMMDD prefix on the moved filename)
  4. Extension                   (fallback "kind" used only when no topic hits)

Pure-stdlib by default. Works in --dry-run mode for safe preview.

CLI:
    python -m tools.auto_organize <source> [--dest DIR] [--rules FILE]
                                  [--dry-run] [--no-stamp] [--copy]

Programmatic:
    from tools.auto_organize import auto_organize
    auto_organize(source="~/Downloads", dry_run=True)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Logger (reuse project logger if present, else stdlib)
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
try:
    from utils.logger import setup_logging  # type: ignore
except Exception:  # pragma: no cover
    import logging

    def setup_logging(log_dir):  # type: ignore
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger("auto_organize")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(
                Path(log_dir)
                / f"auto_organize_{datetime.now():%Y%m%d_%H%M%S}.log"
            )
            fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(fh)
            logger.addHandler(ch)
        return logger


# ---------------------------------------------------------------------------
# Rule loading
# ---------------------------------------------------------------------------
DEFAULT_RULES_FILE = Path(__file__).with_name("label_rules.json")


def load_rules(rules_path: Optional[str | Path] = None) -> dict:
    p = Path(rules_path) if rules_path else DEFAULT_RULES_FILE
    if not p.exists():
        raise FileNotFoundError(f"Label rules not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Date / text helpers
# ---------------------------------------------------------------------------
DATE_RE = re.compile(
    r"(?P<y>20\d{2}|19\d{2})[-_./]?(?P<m>0[1-9]|1[0-2])[-_./]?(?P<d>0[1-9]|[12]\d|3[01])"
)


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
    suffix = path.suffix.lower()
    text_like = {".txt", ".md", ".csv", ".tsv", ".html", ".htm", ".log", ".json", ".xml"}
    try:
        if suffix in text_like:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(limit)
        if suffix == ".pdf":
            try:
                from pypdf import PdfReader  # optional dep

                reader = PdfReader(str(path))
                if reader.pages:
                    return (reader.pages[0].extract_text() or "")[:limit]
            except Exception:
                return ""
    except Exception:
        return ""
    return ""


# ---------------------------------------------------------------------------
# Labeling
# ---------------------------------------------------------------------------
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


_SEP_RE = re.compile(r"[._\-/\\]+")


def _normalize(s: str) -> str:
    """Lowercase and collapse common separators (._-/\\) to single spaces.

    Lets a rule like ``"nit goa"`` match filenames like ``NIT_Goa`` or
    ``nit-goa`` without listing every variant.
    """
    return _SEP_RE.sub(" ", s.lower())


def _match_any(haystack: str, needles: Iterable[str]) -> bool:
    return any(_normalize(n) in haystack for n in needles if n)


def classify(path: Path, rules: dict, peek: bool = True) -> Label:
    name = _normalize(path.name)
    text = _normalize(_peek_text(path)) if peek else ""
    blob = f"{name} {text}"

    # institute (first hit wins; "_unsorted" is the fallback bucket and not matched)
    institute = "_unsorted"
    for inst, kws in rules.get("institutes", {}).items():
        if inst.startswith("_"):
            continue
        if _match_any(blob, kws):
            institute = inst
            break

    # topics (collect every hit, ordered by rule definition)
    topics: List[str] = []
    for topic, kws in rules.get("topics", {}).items():
        if _match_any(blob, kws):
            topics.append(topic)

    # extension → kind
    ext = path.suffix.lower()
    kind = "Other"
    for k, exts in rules.get("extensions", {}).items():
        if ext in exts:
            kind = k
            break

    # date: prefer a date in the filename, else mtime
    dt = _date_from_name(path.name)
    if dt is None:
        try:
            dt = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            dt = None

    return Label(institute=institute, topics=topics, kind=kind, date=dt)


# ---------------------------------------------------------------------------
# Move / copy
# ---------------------------------------------------------------------------
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
    """Prefix YYYYMMDD if not already present at the start."""
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
        # don't re-organize files already inside the destination tree
        try:
            f.resolve().relative_to(dest.resolve())
            continue
        except ValueError:
            pass

        label = classify(f, rules, peek=peek)
        topic = label.primary_topic
        target_dir = dest / label.institute / topic / label.date_bucket
        target_name = _stamped_name(f, label) if stamp else f.name
        plans.append(Plan(src=f, dst=target_dir / target_name, label=label))
    return plans


def apply_plan(
    plans: List[Plan],
    *,
    copy: bool = False,
    dry_run: bool = False,
    logger=None,
) -> Tuple[int, int]:
    moved = failed = 0
    for plan in plans:
        try:
            if not dry_run:
                plan.dst.parent.mkdir(parents=True, exist_ok=True)
                final = _unique(plan.dst.parent, plan.dst.name)
                if copy:
                    shutil.copy2(str(plan.src), str(final))
                else:
                    shutil.move(str(plan.src), str(final))
                action = "COPIED" if copy else "MOVED"
            else:
                action = "WOULD-MOVE"
                final = plan.dst
            tags = ",".join(plan.label.topics) or plan.label.kind
            msg = (
                f"{action} [{plan.label.institute} | {tags} | {plan.label.date_bucket}] "
                f"{plan.src.name} -> {final}"
            )
            if logger:
                logger.info(msg)
            else:
                print(msg)
            moved += 1
        except Exception as e:
            failed += 1
            err = f"FAILED {plan.src}: {e}"
            if logger:
                logger.error(err)
            else:
                print(err)
    return moved, failed


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
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
    """Organize files in *source* into *dest* labeled by institute/topic/date.

    Returns a dict summary: ``{"planned": N, "moved": N, "failed": N, "dest": path}``.
    """
    source_p = Path(source).expanduser().resolve()
    if not source_p.is_dir():
        raise NotADirectoryError(f"Not a directory: {source_p}")
    dest_p = Path(dest).expanduser().resolve() if dest else source_p / "_organized"
    dest_p.mkdir(parents=True, exist_ok=True)

    rules = load_rules(rules_file)
    logger = setup_logging(dest_p / "Logs")
    logger.info(f"auto_organize start  src={source_p}  dst={dest_p}  dry_run={dry_run}")

    plans = build_plan(
        source_p, dest_p, rules,
        stamp=stamp, peek=peek, recursive=recursive,
    )
    if not plans:
        logger.info("Nothing to organize.")
        return {"planned": 0, "moved": 0, "failed": 0, "dest": str(dest_p)}

    moved, failed = apply_plan(plans, copy=copy, dry_run=dry_run, logger=logger)
    logger.info(f"auto_organize done   planned={len(plans)} moved={moved} failed={failed}")
    return {"planned": len(plans), "moved": moved, "failed": failed, "dest": str(dest_p)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Auto-organize files by institute/topic/date.")
    p.add_argument("source", help="Source directory")
    p.add_argument("--dest", default=None, help="Destination root (default: <source>/_organized)")
    p.add_argument("--rules", default=None, help="Path to label_rules.json")
    p.add_argument("--dry-run", action="store_true", help="Print plan without moving")
    p.add_argument("--copy", action="store_true", help="Copy instead of move")
    p.add_argument("--no-stamp", action="store_true", help="Do not prefix YYYYMMDD on filenames")
    p.add_argument("--no-peek", action="store_true", help="Skip text peek (faster, filename-only matching)")
    p.add_argument("--recursive", action="store_true", help="Recurse into subdirectories of source")
    args = p.parse_args(argv)

    summary = auto_organize(
        source=args.source,
        dest=args.dest,
        rules_file=args.rules,
        dry_run=args.dry_run,
        copy=args.copy,
        stamp=not args.no_stamp,
        peek=not args.no_peek,
        recursive=args.recursive,
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
