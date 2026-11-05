"""Build a Jira sub-task description in ADF with real task-list checkboxes.

Usage: uv run build_adf.py <input.json>

Input JSON:
  {"what": ["line", ...],
   "why": ["line", ["line with sub-bullets", ["sub", ...]], ...],
   "tasks": ["task", ...]}

Lines may use `code` spans and [label](url) links. Prints the ADF document.
"""

import json
import re
import sys
import uuid
from pathlib import Path

# Split a line into plain text, `code` spans, and [label](url) links.
TOKEN = re.compile(r"(`[^`]+`|\[[^\]]+\]\([^)]+\))")


def inline(text: str) -> list[dict]:
    """Convert one line into ADF text nodes."""
    nodes = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("`"):
            # Inline code span.
            nodes.append({"type": "text", "text": part[1:-1], "marks": [{"type": "code"}]})
        elif part.startswith("["):
            # Markdown-style link.
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part).groups()
            nodes.append({"type": "text", "text": label, "marks": [{"type": "link", "attrs": {"href": url}}]})
        else:
            nodes.append({"type": "text", "text": part})
    return nodes


def heading(text: str) -> dict:
    """Bold paragraph used as a section heading."""
    return {"type": "paragraph", "content": [{"type": "text", "text": text, "marks": [{"type": "strong"}]}]}


def bullets(items: list) -> dict:
    """Bullet list. An item is a string, or [string, [sub strings]]."""
    out = []
    for item in items:
        text, subs = (item, []) if isinstance(item, str) else item
        content = [{"type": "paragraph", "content": inline(text)}]
        if subs:
            content.append(bullets(subs))
        out.append({"type": "listItem", "content": content})
    return {"type": "bulletList", "content": out}


def tasks(items: list[str]) -> dict:
    """Task list with every item unticked. The user ticks the boxes."""
    return {
        "type": "taskList",
        "attrs": {"localId": str(uuid.uuid4())},
        "content": [
            {"type": "taskItem", "attrs": {"localId": str(uuid.uuid4()), "state": "TODO"}, "content": inline(t)}
            for t in items
        ],
    }


def build(spec: dict) -> dict:
    """Build the full sub-task description: What, Why, Tasks."""
    rule = {"type": "rule"}
    return {
        "type": "doc",
        "version": 1,
        "content": [
            rule, heading("What"), bullets(spec["what"]),
            rule, heading("Why"), bullets(spec["why"]),
            rule, heading("Tasks"), tasks(spec["tasks"]),
        ],
    }


def main() -> int:
    """Read the input file and print the ADF document."""
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    spec = json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps(build(spec)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
