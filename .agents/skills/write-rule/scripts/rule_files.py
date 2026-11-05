"""List the shared rule files, or create a new tool file.

Usage:
    uv run rule_files.py list
    uv run rule_files.py new <tool> --read-when "Writing or reviewing <tool> code." [--paths "**/*.ext" ...]

Exit codes:
    0  done
    3  the tool file already exists (nothing written)
"""

import argparse
import re
import sys
from pathlib import Path

# Shared rules live in the same ai-dotfiles repo as this script:
# <ai-dotfiles>/.agents/skills/write-rule/scripts/rule_files.py -> <ai-dotfiles>/.agents/rules
RULES = Path(__file__).resolve().parents[3] / "rules"

# Template for a new tool file, next to this script in ../assets.
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "topic-file.md"


def frontmatter(path: Path) -> dict[str, str]:
    """Return the frontmatter fields. List values are joined with ', '."""
    lines = path.read_text().splitlines()
    # Frontmatter is the block between the first two `---` lines.
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    key = ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        # A "  - value" line belongs to the list under the last key.
        if line.lstrip().startswith("- ") and key:
            item = line.strip()[2:].strip().strip('"')
            fields[key] = f"{fields[key]}, {item}" if fields[key] else item
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        fields[key] = value.strip()
    return fields


def list_files() -> int:
    """Print each rule file with its description, read_when, and paths."""
    for path in sorted(RULES.glob("*.md")):
        fields = frontmatter(path)
        print(f"{path.name}")
        print(f"  description: {fields.get('description', '(missing)')}")
        print(f"  read_when:   {fields.get('read_when', '(missing)')}")
        print(f"  paths:       {fields.get('paths') or '(none: loads every session)'}")
    return 0


def new_file(tool: str, read_when: str, paths: list[str]) -> int:
    """Create `<tool>.md` from the template."""
    # File names stay simple: lowercase letters, digits, and -.
    if not re.match(r"^[a-z0-9-]+$", tool):
        print(f"Bad tool name '{tool}': use lowercase letters, digits, and - only.")
        return 1
    target = RULES / f"{tool}.md"
    # Never overwrite an existing rule file.
    if target.exists():
        print(f"EXISTS: {target}. Add the rule to it instead.")
        return 3
    title = tool.replace("-", " ").title()
    text = TEMPLATE.read_text().replace("<tool>", tool).replace("<Tool>", title)
    # Replace the whole read_when placeholder line.
    text = re.sub(r"^read_when: .*$", f"read_when: {read_when}", text, flags=re.MULTILINE)
    # Add paths: so Claude Code loads the file only for matching files.
    if paths:
        block = "paths:\n" + "\n".join(f'  - "{p}"' for p in paths) + "\n"
        head, sep, rest = text.partition("\n---\n")
        text = head + "\n" + block.rstrip("\n") + sep + rest
    target.write_text(text)
    print(f"CREATED: {target}")
    return 0


def main() -> int:
    """Parse arguments and run the chosen command."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list rule files, when to read them, and their paths")
    new = sub.add_parser("new", help="create a new tool rule file")
    new.add_argument("tool", help="tool name, for example dbt or airflow")
    new.add_argument("--read-when", required=True, help="when an agent should read it")
    new.add_argument("--paths", nargs="*", default=[], help="file globs that load it in Claude Code")
    args = parser.parse_args()
    if args.command == "list":
        return list_files()
    return new_file(args.tool, args.read_when, args.paths)


if __name__ == "__main__":
    sys.exit(main())
