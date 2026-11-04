---
name: new-plan
description: >
  Turns an approved plan into the plan folder layout `.agents/plans/<plan_name>/`
  (todo.md checklist, 00_overview.md, one guide file per phase, lessons.md).
  Use right after the user approves a plan, including a plan written in plan mode,
  and whenever the user asks to start, set up, scaffold, or write down a new plan,
  project, or multi-phase task, even if they do not say "new-plan".
---

# New plan

Plans live in the repo so any agent (Claude Code, CoCo, others) can pick them up
in a later session. Plan mode only writes a draft to `~/.claude/plans/`; this
skill turns the approved draft into the working plan.

## Steps

1. **Pick the plan name.** Short, lowercase, snake_case (for example
   `deposit_trends`). Use the name the user gave. If none, propose one and
   confirm it. The name is used in every file of the plan.

2. **Find the source.** Use the approved plan from the conversation. If it was
   written in plan mode, read the plan file (its path is in the conversation, or
   is the newest file in `~/.claude/plans/`).

3. **Split into phases.** One phase is one unit of work with its own
   "Done when" check. Phase `00` is always the overview. List the other
   phases in the order they run, as short snake_case names.

4. **Create the files with the script.** Run from inside the repo:

   ```bash
   uv run ~/src/coastal/ai-dotfiles/.claude/skills/new-plan/scripts/scaffold_plan.py <plan_name> --phases <phase_one>,<phase_two>
   ```

   The script creates `todo.md`, `00_overview.md`, `lessons.md`, and one
   `NN_<phase>.md` per phase from the templates in `assets/`. It checks two
   things first and writes nothing if either fails:
   - Exit `2`, `NOT-IGNORED`: `.agents/` would show up in git. Client repos
     must never receive plan files. Tell the user and offer to add `.agents/`
     to `.git/info/exclude` (local only, never committed). If they agree, run
     again with `--add-exclude`. Do not edit `.gitignore`: it is a committed
     client file.
   - Exit `3`, `EXISTS`: the plan folder already exists. Ask the user whether
     to update it or pick another name.

5. **Fill in the files.** Replace the `<...>` placeholders with what the plan
   says. Where something is unknown, write
   `TBD: ask the user` instead of guessing. A wrong guess in a plan file gets
   followed later as if it were decided.

   Add a **Check-in gate** item under any phase that creates or changes objects
   (tables, views, grants, files in the client repo), and under any phase that
   must end with an open decision answered. The user wants to approve those
   before work goes on.

   Placeholders that a later phase fills (for example column names found in
   Phase 01) can stay. Mark them `TBD: filled in Phase NN`.

6. **Report.** List the files created in one short block. Ask the user to
   review them before Phase 01 starts.
