"""Create the folder layout for a new plan in `.agents/plans/<plan_name>/`.

Usage:
    uv run scaffold_plan.py <plan_name> --phases name_one,name_two [--repo PATH] [--add-exclude]

Exit codes:
    0  created
    2  `.agents/` is not git-ignored (nothing written)
    3  plan folder already exists (nothing written)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Templates live next to this script, in ../assets.
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def repo_root(start: Path) -> Path:
    """Return the git repo root that contains `start`."""
    # Ask git for the top-level folder of the repo.
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def is_ignored(root: Path, rel_path: str) -> bool:
    """Return True if git ignores `rel_path` in the repo at `root`."""
    # `git check-ignore` exits 0 when the path is ignored.
    result = subprocess.run(
        ["git", "check-ignore", "-q", rel_path], cwd=root, check=False
    )
    return result.returncode == 0


def add_exclude(root: Path) -> None:
    """Add `.agents/` to the repo's local `.git/info/exclude` file."""
    # This file is local to the clone and is never committed.
    exclude = root / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    text = exclude.read_text() if exclude.exists() else ""
    # Only add the line once.
    if ".agents/" not in text.splitlines():
        with exclude.open("a") as f:
            f.write(("" if text.endswith("\n") or not text else "\n") + ".agents/\n")


def render(template: str, **values: str) -> str:
    """Return the template text from `assets/` with `<key>` placeholders filled."""
    text = (ASSETS / template).read_text()
    for key, value in values.items():
        text = text.replace(f"<{key}>", value)
    return text


def main() -> int:
    """Parse arguments, run the safety checks, and write the plan files."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plan_name", help="short snake_case plan name")
    parser.add_argument(
        "--phases", default="", help="comma-separated snake_case phase names, in order"
    )
    parser.add_argument("--repo", default=".", help="any folder inside the repo")
    parser.add_argument(
        "--add-exclude",
        action="store_true",
        help="add .agents/ to .git/info/exclude first (only after the user agrees)",
    )
    args = parser.parse_args()

    # Plan and phase names become file names, so keep them simple.
    name_ok = re.compile(r"^[a-z0-9_]+$")
    phases = [p.strip() for p in args.phases.split(",") if p.strip()]
    for name in [args.plan_name, *phases]:
        if not name_ok.match(name):
            print(f"Bad name '{name}': use lowercase letters, digits, and _ only.")
            return 1

    root = repo_root(Path(args.repo))
    plan_dir = root / ".agents" / "plans" / args.plan_name

    # Add the local exclude only when asked.
    if args.add_exclude:
        add_exclude(root)

    # Stop if plan files would show up in git.
    if not is_ignored(root, f".agents/plans/{args.plan_name}/todo.md"):
        print(f"NOT-IGNORED: .agents/ is not git-ignored in {root}. Nothing written.")
        return 2

    # Never overwrite an existing plan.
    if plan_dir.exists():
        print(f"EXISTS: {plan_dir} already exists. Nothing written.")
        return 3

    plan_dir.mkdir(parents=True)
    written = []

    # Write the fixed files.
    for template, target in [
        ("todo.md", "todo.md"),
        ("overview.md", "00_overview.md"),
        ("lessons.md", "lessons.md"),
    ]:
        (plan_dir / target).write_text(render(template, plan_name=args.plan_name))
        written.append(target)

    # Write one guide file per phase, numbered from 01.
    for number, phase in enumerate(phases, start=1):
        target = f"{number:02d}_{phase}.md"
        title = phase.replace("_", " ").capitalize()
        text = render("phase.md", **{"Phase title": title}).replace(
            "# NN ", f"# {number:02d} ", 1
        )
        (plan_dir / target).write_text(text)
        written.append(target)

    print(f"CREATED: {plan_dir}")
    for target in written:
        print(f"  {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
