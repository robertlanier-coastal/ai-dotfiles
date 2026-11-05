## Workflow Orchestration

### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes wrong, STOP and re-plan immediately - do not keep pushing
- Use plan mode for verification steps, not just development
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use parallel tool calls for independent lookups and reads
- Use subagents for heavy research or large reads, to keep the main context clean
- Tell the user the token cost before starting subagents (about 130k tokens each)
- Never use a subagent for a step that needs the user's answers
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user, turn the lesson learned into a rule with the `write-rule` skill (see Task Management, step 6)
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these rules until mistake rate drops
- Follow Session Start.

### 4. Verification Before Done

- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

## Task Management

Plans are for the agent to follow. Each plan has a short name (for example
`deposit_trends`). Use that name in every file for the plan.

The active plan is the one the user names. If none is named, list
`.agents/plans/` and ask.

1. **Plan First**: After the user approves a plan (including a plan-mode
   draft), use the `new-plan` skill. It creates `.agents/plans/<plan_name>/`
   with `todo.md` and one guide file per phase. Optional: a `reference/`
   folder for source notes and samples.
2. **Verify Plan**: Check in with the user before starting implementation,
   and before each phase that creates or changes any objects.
3. **Track Progress**: Mark items complete in `todo.md`, and write results in
   the phase file's Results log.
4. **Explain Changes**: Say what changed and why.
5. **Document Results**: Add a Review section to `todo.md`.
6. **Write Rules**: After ANY correction from the user, turn the lesson
   learned into a rule with the `write-rule` skill. Use it too when the user
   asks for a new rule. It writes the rule at the narrowest level that fits:
   this plan, this repo, or the shared rules in
   `<ai-dotfiles>/.agents/rules/`. Rule files are the source of
   truth. Do not save workflow rules to Claude Code auto memory.

For Jira stories, sub-tasks and progress comments, use the `create-jira-story`
and `write-jira-comment` skills.

If skills are not available (for example in CoCo), read the skill's `SKILL.md`
in `<ai-dotfiles>/.agents/skills/<skill>/` and follow it.

## Session Start

`<ai-dotfiles>` is the folder where this repo is cloned. On the user's Mac it
is `~/src/coastal/ai-dotfiles`. On other machines, ask the user if unsure.

1. Read `<ai-dotfiles>/.agents/rules/general.md`. Skip this step only if
   the rules are already loaded (Claude Code on the user's Mac loads them
   from `~/.claude/rules`).
2. Run `uv run <ai-dotfiles>/.agents/skills/write-rule/scripts/rule_files.py list`
   (without uv: read the frontmatter of `<ai-dotfiles>/.agents/rules/*.md`).
   Read each file whose `read_when` matches the task (Claude Code: only files
   it has not loaded already).
3. Read `.agents/rules.md` in the current repo, if it exists.
4. Read `.agents/plans/<plan_name>/rules.md` for the active plan, if it exists.

## Git

- **Default branch:** `main`.
- **Branch naming:** `<type>/<Jira ticket>-<description>`.
- **Commit messages:** Conventional Commits.
- **Pull strategy:** rebase.
- **Client or project repos:** Never commit or push to `main`. Always commit
  to a feature or fix branch and open a pull request.
- **Client or project repos, review first:** Make each task's change and leave
  it uncommitted. Show the diff, wait for the user's go-ahead, then commit.
  Push when a phase or sub-task is done.
- **Personal repos (for example `ai-dotfiles`):** Always ask
  first. Users differ, so offer the choice: review each diff first, or commit
  and push to `main` directly. Ask clarifying questions until the request is clear.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Python**: Use `uv` for projects and package management, not pip. Lint with Ruff.

## Code

- Add simple docstrings to functions and classes.
- Add simple comments above lines of code.
- Do not add abstractions beyond what the task needs.
- Do not add error handling for things that cannot happen.
- Shell scripts are ShellCheck-clean.

## Documentation

- Use `|---|---|` separators in Markdown tables.
- No time estimates in documentation: they deter engineers from reading.
