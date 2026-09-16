# task-runner

Lean personal CLI toolbox. One command, zero bloat.

## Install

```bash
uv tool install .           # global: task-runner on PATH
# or editable dev mode
uv pip install -e .
```

## Commands

```
task-runner organize <source> [--dest DIR] [--rules FILE] [--dry-run] [--copy] [--recursive]
task-runner dups <root> [--delete] [--keep first|shortest|newest] [--report PATH]
task-runner index <root> [--out PATH] [--query TEXT] [--institute NAME] [--topic NAME]
task-runner summarize <root> [--json]
task-runner links create <path> <target> [--type auto|symlink|hard|junction]
task-runner links broken <root> [--remove]
task-runner rmdirs <root> [--recurse]
task-runner analyze <root> [--type functions|variables|orphaned|all] [--json]
task-runner packages [--export PATH]
task-runner scaffold <path> --type generic|python|powershell
task-runner notes [--path DIR] [--topic NAME]
task-runner tasks [--path DIR]
```

### organize

Move files into `<dest>/<Institute>/<Topic>/<YYYY-MM>/` hierarchy driven by
keyword rules in `src/task_runner/data/label_rules.json`.

### dups

Two-stage duplicate detection: size match → BLAKE2b digest. `--delete` removes
non-kept copies. `--keep newest` preserves the most recent file.

### index / summarize

`index` builds a JSON list of every file with its classify labels (institute,
topics, kind, date). `summarize` prints a per-category stats table.

### links / rmdirs

Links: create symlink/hard/junction (`--type auto` picks the best kind) and
find/fix broken ones with `--remove`. rmdirs: prune empty directories bottom-up.

### analyze

AST-based static analysis on Python files: unused functions, unused variables,
and orphaned scripts. `--json` for machine-readable output.

### packages

Reports installed packages across winget, scoop, choco, pip, uv, npm, bun,
cargo, gem, and dotnet. `--export` writes JSON.

### scaffold / notes / tasks

`scaffold <dir> --type python` creates src/tests/docs/pyproject.toml etc.
`notes` and `tasks` set up dated template structures for project management.

## Config

`label_rules.json` drives `organize`/`index`/`summarize`. Keywords are matched
case-insensitively after normalizing separators (`-`, `_`, `.`, spaces).
Override with `--rules path/to/other_rules.json`.
