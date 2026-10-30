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
- Review lessons at session start for relevant project

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
`rlp_revenue_metrics`). Use that name in every file for the plan.

1. **Plan First**: Write the plan as two parts in `.agents/tasks/`:
   - `<plan_name>.todo.md`: the checklist. One checkable item per phase,
     plus a Review section at the end.
   - `<plan_name>/`: one guide file per phase (`00_overview.md`,
     `01_<phase>.md`, ...). Each file has: Description, Work, SQL or
     commands, Done when, and a Results log.
2. **Verify Plan**: Check in with the user before starting implementation,
   and before each phase that creates or changes any objects.
3. **Track Progress**: Mark items complete in `<plan_name>.todo.md`, and
   write results in the phase file's Results log.
4. **Explain Changes**: High-level summary at each step.
5. **Document Results**: Add a Review section to `<plan_name>.todo.md`.
6. **Capture Lessons**: After ANY correction from the user, write the lesson down:
   - If it applies to any work in this repo, add it to `.agents/tasks/lessons.md`.
   - If it applies only to one plan, add it to `.agents/tasks/<plan_name>.lessons.md`.
   - Write each lesson as a rule: "Do X" or "Do not do Y", plus one line on why.
   - If a plan lesson turns out to apply everywhere, move it to `lessons.md`.
   At session start, read `lessons.md`, and the `.lessons.md` file for the
   active plan.

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Use uv for Package Management**: Use uv for all package management; do not use pip.
