"""Build a Jira sub-task description in ADF with real task-list checkboxes.

Usage: uv run build_adf.py <input.json>

Input JSON:
  {"what": ["line", ...],
   "why": ["line", ["line with sub-bullets", ["sub", ...]], ...],
   "files": ["`path/to/file`", ...],
   "tasks": ["task", {"text": "task", "done": true}, ...]}

A task is a string (unticked), or an object with "done" to keep an existing
tick when rewriting a ticket. New tickets start with every task unticked.

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


def tasks(items: list) -> dict:
    """Task list. Strings are unticked; {"text", "done"} keeps an existing tick."""
    content = []
    for item in items:
        # A plain string is a new, unticked task.
        text, done = (item, False) if isinstance(item, str) else (item["text"], item.get("done", False))
        state = "DONE" if done else "TODO"
        content.append({"type": "taskItem", "attrs": {"localId": str(uuid.uuid4()), "state": state}, "content": inline(text)})
    return {"type": "taskList", "attrs": {"localId": str(uuid.uuid4())}, "content": content}


def build(spec: dict) -> dict:
    """Build the full sub-task description: What, Why, Files, Tasks."""
    rule = {"type": "rule"}
    return {
        "type": "doc",
        "version": 1,
        "content": [
            rule, heading("What"), bullets(spec["what"]),
            rule, heading("Why"), bullets(spec["why"]),
            rule, heading("Files"), bullets(spec["files"]),
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
