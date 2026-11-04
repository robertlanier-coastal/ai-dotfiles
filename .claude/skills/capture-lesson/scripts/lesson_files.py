"""List the shared lesson files, or create a new tool file.

Usage:
    uv run lesson_files.py list
    uv run lesson_files.py new <tool> --read-when "Writing or reviewing <tool> code."

Exit codes:
    0  done
    3  the tool file already exists (nothing written)
"""

import argparse
import re
import sys
from pathlib import Path

# Shared lessons live in the ai-dotfiles repo.
LESSONS = Path.home() / "src" / "coastal" / "ai-dotfiles" / "lessons"

# Template for a new tool file, next to this script in ../assets.
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "topic-file.md"


def frontmatter(path: Path) -> dict[str, str]:
    """Return the `key: value` pairs from a file's frontmatter."""
    lines = path.read_text().splitlines()
    # Frontmatter is the block between the first two `---` lines.
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def list_files() -> int:
    """Print each lesson file with its description and read_when."""
    for path in sorted(LESSONS.glob("*.md")):
        fields = frontmatter(path)
        print(f"{path.name}")
        print(f"  description: {fields.get('description', '(missing)')}")
        print(f"  read_when:   {fields.get('read_when', '(missing)')}")
    return 0


def new_file(tool: str, read_when: str) -> int:
    """Create `<tool>.md` from the template."""
    # File names stay simple: lowercase letters, digits, and -.
    if not re.match(r"^[a-z0-9-]+$", tool):
        print(f"Bad tool name '{tool}': use lowercase letters, digits, and - only.")
        return 1
    target = LESSONS / f"{tool}.md"
    # Never overwrite an existing lesson file.
    if target.exists():
        print(f"EXISTS: {target}. Add the lesson to it instead.")
        return 3
    title = tool.replace("-", " ").title()
    text = TEMPLATE.read_text().replace("<tool>", tool).replace("<Tool>", title)
    # Replace the whole read_when placeholder line.
    text = re.sub(
        r"^read_when: .*$", f"read_when: {read_when}", text, flags=re.MULTILINE
    )
    target.write_text(text)
    print(f"CREATED: {target}")
    return 0


def main() -> int:
    """Parse arguments and run the chosen command."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list lesson files and when to read them")
    new = sub.add_parser("new", help="create a new tool lesson file")
    new.add_argument("tool", help="tool name, for example dbt or airflow")
    new.add_argument("--read-when", required=True, help="when an agent should read it")
    args = parser.parse_args()
    if args.command == "list":
        return list_files()
    return new_file(args.tool, args.read_when)


if __name__ == "__main__":
    sys.exit(main())
