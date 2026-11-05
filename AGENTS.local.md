## Workflow Orchestration

### 1. Plan Mode Default

- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes wrong, STOP and re-plan immediately - do not keep pushing
- Use plan mode for verification steps, not just development
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy

- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, use more compute for subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop

- After ANY correction from the user: capture the lesson (see Task Management, step 6)
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
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
4. **Explain Changes**: One or two lines on what changed and why. Lead with
   the point. No recap of steps.
5. **Document Results**: Add a Review section to `todo.md`.
6. **Capture Lessons**: After ANY correction from the user, use the
   `capture-lesson` skill. It writes the lesson at the narrowest level that
   fits: this plan, this repo, or the shared lessons in
   `~/src/coastal/ai-dotfiles/lessons/`. Lesson files are the source of
   truth. Do not save workflow lessons to Claude Code auto memory.

If skills are not available (for example in CoCo), read the skill's `SKILL.md`
in `~/src/coastal/ai-dotfiles/.claude/skills/<skill>/` and follow it.

## Session Start

`~` is the user's home folder.

1. Read `~/src/coastal/ai-dotfiles/lessons/general.md`. Skip this step if it
   is already loaded (Claude Code imports it through `CLAUDE.md`).
2. Run `uv run ~/src/coastal/ai-dotfiles/.claude/skills/capture-lesson/scripts/lesson_files.py list`.
   Read each file whose `read_when` matches the task.
3. Read `.agents/lessons.md` in the current repo, if it exists.
4. Read `.agents/plans/<plan_name>/lessons.md` for the active plan, if it exists.

## Git

- **Client or project repos:** Never commit or push to `main`. Always commit
  to a feature or fix branch and open a pull request.
- **Personal repos (for example `~/src/coastal/ai-dotfiles`):** Ask the user,
  then commit and push to `main`.
- **Review first:** Make each task's change and leave it uncommitted. Show the
  diff, wait for the user's go-ahead, then commit. Push when a phase is done.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Use uv for Package Management**: Use uv for all package management; do not use pip.
