---
name: capture-lesson
description: >
  Writes a lesson as a short rule at the right level: this plan, this repo,
  or the shared lessons in ~/src/coastal/ai-dotfiles/lessons/. Use after ANY
  correction from the user ("no, do it this way", "don't do that", "I told you"),
  when the user says "remember this", "add a lesson", or "don't do that again",
  and when a lesson turns out to apply more widely and should be moved up a level.
  Use this instead of Claude Code auto memory for workflow lessons.
---

# Capture lesson

Lessons are how agents stop repeating mistakes across sessions, tools, and
clients. They only work if each one is a clear rule and lives where the next
agent will read it.

## Steps

1. **Write the rule.** One idea per lesson, in this format:

   ```markdown
   - Do: <what to do>.
     Do not: <what to avoid>.   (only if it adds something)
     Why: <one line: the reason or what went wrong>.
   ```

   Base it on what the user actually said. Do not widen it beyond the correction.

2. **Pick the level.** Use the narrowest level that fits:

   | Level | File | When |
   |---|---|---|
   | Plan | `.agents/plans/<plan_name>/lessons.md` | Decisions and scope that only matter for this plan |
   | Repo | `.agents/lessons.md` | This client's conventions and people, and facts about its source systems (code values, what a table or column means). Other plans at this client need these too |
   | Shared | `~/src/coastal/ai-dotfiles/lessons/<topic>.md` | Would help at a different client |

   Test: "Would this help at another client?" If yes, shared. If unsure, ask
   the user. `~` is the user's home folder.

3. **For shared lessons, remove client details.** The `ai-dotfiles` repo is
   pushed to GitHub and used at every client. Remove client and company names,
   people, ticket and PR numbers, object, table, and column names, data values,
   and internal URLs. Rewrite the Why line in general terms.

4. **Pick the shared file.** Run
   `uv run ~/src/coastal/ai-dotfiles/.claude/skills/capture-lesson/scripts/lesson_files.py list` and match on
   `description` and `read_when`. Use a tool file (`snowflake.md`, `python.md`,
   `jira.md`, ...) for tool-specific lessons, `data-modeling.md` for
   tool-neutral modeling, and `general.md` for how to work with the user.
   If a new tool has no file, create it with
   `uv run ~/src/coastal/ai-dotfiles/.claude/skills/capture-lesson/scripts/lesson_files.py new <tool> --read-when "<when to read it>"`.

5. **Check for duplicates.** Read the target file. If a lesson already covers
   this, sharpen that lesson instead of adding a near-copy.

6. **Insert under the matching heading.** Add a new `## Heading` only if no
   existing one fits. In a file without headings, add the lesson after the
   last lesson. Keep scope notes (such as "does not apply to dbt") at the top,
   so a new lesson never reads as an exception to one.

7. **Moving a lesson up a level.** Add the rewritten lesson at the new level,
   then delete it from the lower level, so it lives in one place only.

8. **Report in one line:** the rule and the file path. For shared lessons, add
   that the change is not committed; committing and pushing `ai-dotfiles` is the
   user's call.

Do not save workflow lessons to Claude Code auto memory. Lesson files are the
source of truth, and other agents (such as CoCo) cannot read auto memory.
