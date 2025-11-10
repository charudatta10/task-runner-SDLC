from invoke import task, Collection
from pathlib import Path
import re
from collections import defaultdict

TAG_PATTERN = re.compile(r"#(\w[\w-]*)")
LINK_PATTERN = re.compile(r"\[\[(.*?)\]\]|\[(.*?)\]\((.*?)\)")


def get_markdown_files(folder):
    return list(Path(folder).rglob("*.md"))


@task
def generate_tags(c, folder="."):
    """Generate tags.md with tag glossary and linked notes."""
    tag_map = defaultdict(list)
    for file in get_markdown_files(folder):
        content = file.read_text(encoding="utf-8")
        tags = TAG_PATTERN.findall(content)
        title = file.stem
        for tag in tags:
            tag_map[tag].append(f"- [[{title}]]")

    lines = ["# Tags Glossary\n"]
    for tag, links in sorted(tag_map.items()):
        lines.append(f"## #{tag}")
        lines.extend(links)
        lines.append("")

    Path(folder, "tags.md").write_text("\n".join(lines), encoding="utf-8")
    print("✅ tags.md generated.")


@task
def generate_moc(c, folder="."):
    """Generate moc.md with wiki-style links to all notes."""
    files = get_markdown_files(folder)
    lines = ["# Map of Content\n"]
    for file in files:
        title = file.stem
        lines.append(f"- [[{title}]]")
    Path(folder, "moc.md").write_text("\n".join(lines), encoding="utf-8")
    print("✅ moc.md generated.")


@task
def generate_links(c, folder="."):
    """Generate links.md with all internal and external links."""
    link_map = defaultdict(list)
    for file in get_markdown_files(folder):
        content = file.read_text(encoding="utf-8")
        title = file.stem
        matches = LINK_PATTERN.findall(content)
        for wikilink, text, url in matches:
            if wikilink:
                link_map["Internal"].append(f"- [[{wikilink}]] (from [[{title}]])")
            elif url:
                link_map["External"].append(f"- [{text}]({url}) (from [[{title}]])")

    lines = ["# Links Index\n"]
    for kind in ["Internal", "External"]:
        lines.append(f"## {kind} Links")
        lines.extend(link_map.get(kind, []))
        lines.append("")

    Path(folder, "links.md").write_text("\n".join(lines), encoding="utf-8")
    print("✅ links.md generated.")
