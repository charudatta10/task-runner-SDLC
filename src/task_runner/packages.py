"""List installed packages across common package managers."""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Dict, List, Optional


MANAGERS: Dict[str, Dict[str, str]] = {
    "winget":  {"cmd": "winget list", "version": "winget --version"},
    "scoop":   {"cmd": "scoop list",  "version": "scoop --version"},
    "choco":   {"cmd": "choco list --local-only", "version": "choco --version"},
    "pip":     {"cmd": "pip list --format=json",   "version": "pip --version"},
    "uv":      {"cmd": "uv pip list --format=json", "version": "uv --version"},
    "npm":     {"cmd": "npm list -g --depth=0 --json", "version": "npm --version"},
    "bun":     {"cmd": "bun pm ls -g", "version": "bun --version"},
    "cargo":   {"cmd": "cargo install --list", "version": "cargo --version"},
    "gem":     {"cmd": "gem list --local", "version": "gem --version"},
    "dotnet":  {"cmd": "dotnet tool list --global", "version": "dotnet --version"},
}


def list_managers(include_missing: bool = False) -> List[Dict[str, object]]:
    """Return list of dicts with name, installed (bool), output, error."""
    results: List[Dict[str, object]] = []
    for name, info in MANAGERS.items():
        if not shutil.which(name.split()[0]):
            if include_missing:
                results.append({"name": name, "installed": False, "packages": [], "error": "not found"})
            continue
        try:
            proc = subprocess.run(info["cmd"], shell=True, capture_output=True, text=True, timeout=30)
            out = proc.stdout.strip()
            pkgs = _try_json(out) or out
            results.append({"name": name, "installed": True, "packages": pkgs, "error": None})
        except subprocess.TimeoutExpired:
            results.append({"name": name, "installed": True, "packages": [], "error": "timeout"})
        except Exception as e:
            results.append({"name": name, "installed": True, "packages": [], "error": str(e)})
    return results


def _try_json(raw: str) -> Optional[list]:
    try:
        d = json.loads(raw)
        if isinstance(d, dict) and "dependencies" in d:  # npm
            return list(d.get("dependencies", {}).keys())
        if isinstance(d, list):
            return [x.get("name", str(x)) if isinstance(x, dict) else str(x) for x in d]
    except (json.JSONDecodeError, TypeError):
        return None
    return None