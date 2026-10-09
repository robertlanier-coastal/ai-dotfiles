---
name: creating-rules
description: >
  Creates or updates .claude/rules/ files that give Claude persistent, scoped instructions
  for a project. Use when a user asks to create a rule, add a rule file, write a rules file,
  or scope instructions to specific file types or directories. Also use when instructions
  in CLAUDE.md are growing too large and should be extracted into path-scoped rule files.
---

# Creating Rules Files

Rules files live in `.claude/rules/` and give Claude persistent instructions scoped to
specific file paths or loaded globally for every session.

## Rules vs Skills

Use a rule when the instruction should be in context automatically — coding standards,
conventions, constraints that apply whenever Claude touches a file. Use a skill when the
instruction is a workflow that only matters when explicitly invoked.

## File naming

One topic per file. Use a descriptive kebab-case name that reflects the content — not
`general.md` but `secrets.md`, `skill-usage.md`, `api-design.md`. A reader should know
what the file covers from the name alone.

## Global rules (no frontmatter)

A rule without `paths:` frontmatter loads at launch for every session, unconditionally.
Use this for instructions that apply regardless of what files are being edited.

```markdown
# Skill Usage

- Use `phr-beta:creating-feature-branch` when starting new work.
- Use `phr:committing-changes` for all commits.
```

## Path-scoped rules (with frontmatter)

A rule with `paths:` frontmatter loads only when Claude reads files matching those patterns.
This keeps unrelated instructions out of context and reduces token use.

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/api/**/*.js"
---

# API Rules

- All endpoints must include input validation.
- Use the standard error response format defined in src/api/errors.ts.
```

### Path pattern reference

| Pattern | Matches |
|---|---|
| `**/*.py` | All Python files in any directory |
| `src/**/*` | All files under src/ |
| `*.md` | Markdown files at project root only |
| `plugins/*/.claude-plugin/**` | Files in any plugin's .claude-plugin directory |

Multiple patterns and brace expansion are supported:

```yaml
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
```

## Load behavior

- Global rules (no `paths:`): loaded at launch every session
- Path-scoped rules: loaded when Claude reads a matching file
- After `/compact`: global rules reload from disk; path-scoped rules reload the next time a matching file is read

## Writing effective instructions

- One topic per file — if a file covers two unrelated concerns, split it
- Be specific enough to verify: "Run `ruff check scripts/` before pushing" not "lint your code"
- Use imperative voice: "Verify X", "Flag Y", "Do not Z"
- Avoid contradicting other rule files — Claude may pick one arbitrarily
- Target under 200 lines per file; longer files consume context and reduce adherence

### Numbered lists vs bullets

Use **numbered lists** for sequential steps or ranked checks where order matters — workflows,
validation checklists, things that must happen in sequence.

Use **bullets** for reference lists where items are independent and unordered — field
definitions, option catalogs, feature descriptions. Bullets signal "these are options or
facts" not "do these in order."

## Workflow

1. Determine scope: should this load globally or only for specific file types?
2. Choose a descriptive filename that reflects the topic.
3. Write the rule file — global rules need no frontmatter; scoped rules need `paths:`.
4. Place the file in `.claude/rules/` (project-level) or `~/.claude/rules/` (user-level, applies to all projects).
5. Update any references to rule files in `CLAUDE.md` so the index stays accurate.
6. Verify the file loads with `/context` in a new session.
