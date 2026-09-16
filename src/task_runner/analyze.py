"""Static analysis for Python scripts: unused functions, variables, orphaned files."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import List, Optional, Set, Tuple


def _py_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*.py") if ".venv" not in p.parts and "__pycache__" not in p.parts]


def unused_functions(root: str | Path) -> List[str]:
    """Functions defined but never called anywhere in the tree."""
    root_p = Path(root).expanduser().resolve()
    files = _py_files(root_p)

    defined: List[Tuple[str, Path]] = []
    called: Set[str] = set()
    for f in files:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="ignore"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defined.append((node.name, f))
            elif isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name):
                    called.add(fn.id)

    return [f"{name} :: {path}" for name, path in defined if name not in called]


def unused_variables(root: str | Path) -> List[str]:
    """Variables assigned within a function but never referenced."""
    root_p = Path(root).expanduser().resolve()
    results: List[str] = []
    for f in _py_files(root_p):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="ignore"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            assigned: Set[str] = set()
            referenced: Set[str] = set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign):
                    for t in sub.targets:
                        if isinstance(t, ast.Name):
                            assigned.add(t.id)
                elif isinstance(sub, (ast.Name, ast.Attribute)):
                    if isinstance(sub, ast.Name):
                        referenced.add(sub.id)
                elif isinstance(sub, ast.Store) and hasattr(sub, "ctx"):  # pragma: no cover
                    pass
            for v in assigned:
                if v not in referenced:
                    results.append(f"{v} :: {f}")
    return results


def orphaned_scripts(root: str | Path) -> List[str]:
    """.py files whose basename is not referenced by any other file's content."""
    root_p = Path(root).expanduser().resolve()
    files = _py_files(root_p)
    contents: dict[Path, str] = {}
    for f in files:
        try:
            contents[f] = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

    orphans: List[str] = []
    for f in files:
        refs = [o for o, text in contents.items() if o != f and (f.stem in text or f.name in text)]
        if not refs:
            orphans.append(str(f))
    return orphans


def analyze_all(root: str | Path) -> dict:
    return {
        "unused_functions": unused_functions(root),
        "unused_variables": unused_variables(root),
        "orphaned_scripts": orphaned_scripts(root),
    }