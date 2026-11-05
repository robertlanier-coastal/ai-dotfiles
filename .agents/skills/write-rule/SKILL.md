---
name: write-rule
description: >
  Writes a rule at the right level: this plan, this repo, or the shared rules in
  ai-dotfiles (.agents/rules/). Use when the user asks to create, add,
  or write a rule; after ANY correction from the user, to turn the lesson learned
  into a rule ("no, do it this way", "don't do that", "I told you"); when the user
  says "remember this", "add a lesson", or "don't do that again"; and when a rule
  should move up a level. Use this instead of Claude Code auto memory.
---

# Write a rule

Rules are how agents stop repeating mistakes across sessions, tools, and
clients. Every lesson learned becomes a rule. A rule only works if it is clear
and lives where the next agent will read it.

## Steps

1. **Write the rule.** One idea per rule, in this format:

   ```markdown
   - **Do:** <what to do>.
     **Do not:** <what to avoid>.   (only if it adds something)
     **Why:** <one line: the reason or what went wrong>.
   ```

   For a correction, base it on what the user actually said. Do not widen it
   beyond the correction. For a new rule the user asks for, ask until the rule
   is clear.

2. **Pick the level.** Use the narrowest level that fits:

   | Level | File | When |
   |---|---|---|
   | Plan | `.agents/plans/<plan_name>/rules.md` | Decisions and scope that only matter for this plan |
   | Repo | `.agents/rules.md` | This client's conventions and people, and facts about its source systems (code values, what a table or column means). Other plans at this client need these too |
   | Shared | `<ai-dotfiles>/.agents/rules/<topic>.md` | Would help at a different client |

   Test: "Would this help at another client?" If yes, shared. If unsure, ask
   the user. `<ai-dotfiles>` is the folder where the `ai-dotfiles` repo is
   cloned (this skill lives in `<ai-dotfiles>/.agents/skills/write-rule/`).

3. **For shared rules, remove client details.** The `ai-dotfiles` repo is
   pushed to GitHub and used at every client. Remove client and company names,
   people, ticket and PR numbers, object, table, and column names, data values,
   and internal URLs. Rewrite the Why line in general terms.

4. **Pick the shared file.** Run
   `uv run scripts/rule_files.py list` from this skill's folder
   and match on `description`, `read_when`, and `paths`.
   If `uv` is not available, run the same script with `python3` (it uses only
   the standard library). If Python is not available either, read the
   frontmatter of each `<ai-dotfiles>/.agents/rules/*.md` file, and copy
   `assets/topic-file.md` by hand for a new file. Use a tool file
   (`snowflake.md`, `python.md`, `jira.md`, ...) for tool-specific rules,
   `data-modeling.md` for tool-neutral modeling, and `general.md` for how to
   work with the user. If a new topic has no file, create it with
   `uv run scripts/rule_files.py new <tool> --read-when "<when to read it>" [--paths "<glob>" ...]`.

5. **Decide how it loads.** Shared rule files have two loaders:
   - `read_when` (required): any agent reads the file when the task matches.
   - `paths:` (optional): Claude Code loads the file only when it reads a
     matching file. Use it for file-type rules (`"**/*.py"`, `"**/*.sql"`).
     A file with no `paths:` loads in every Claude Code session, so keep those
     files short and generic.
   Pattern examples: `"**/*.py"` (all Python), `"src/**/*"` (everything under
   `src/`), `"src/**/*.{ts,tsx}"` (brace expansion).

6. **Check for duplicates and conflicts.** Read the target file. If a rule
   already covers this, sharpen it instead of adding a near-copy. If it
   contradicts another rule file, ask the user which one wins.

7. **Insert under the matching heading.** Add a new `## Heading` only if no
   existing one fits. In a file without headings, add the rule after the last
   rule. Keep scope notes (such as "does not apply to dbt") at the top, so a new
   rule never reads as an exception to one.

8. **Moving a rule up a level.** Add the rewritten rule at the new level, then
   delete it from the lower level, so it lives in one place only.

9. **Report in one line:** the rule and the file path. For shared rules, say
   the change is not committed, and ask the user before committing and pushing
   `ai-dotfiles`.

## Writing good rules

- One topic per file. Keep each file under 200 lines.
- Be specific enough to check: "Run `ruff check scripts/` before pushing", not
  "lint your code".
- Use numbered lists for steps in order, bullets for independent facts.
- Do not save rules to Claude Code auto memory. Rule files are the source of
  truth, and other agents (such as CoCo) cannot read auto memory.
