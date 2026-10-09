# Claude Code — Global Preferences

## Who I am

- **Data Platform Engineer**
- **Primary work:** Snowflake Data Warehouse, dbt (Data Build Tool)

## Communication style

- **Lead with the point:** Keep responses short and direct, use complete sentences for explanations, put key finding or action first, no trailing summaries of what you just did.
- **Flag complexity before starting:** If a task is complex with multi-steps, say so upfront so I can decide whether to proceed.
- **Break multi-step work into explicit easily to consume tasks:** Make it clear what's done and what's next.
- **No more than two or three recommendations:** Too many options causes decision paralysis, give a 2 or 3 sentence recommendation with the main tradeoff, don't implement until I confirm.
- **Keep uncertainty bounded:** If you don't know something, say you do not know, then ask simple clarifying questions.
- **No emojis unless requested**
- **No em dashes**

## Environment

- **Shell:** Zsh with Starship prompt, zoxide, fzf
- **No Admin Access:** User Tools installed locally or within `~/.local/bin`
- **Containers:** Podman Not Docker — use `podman` in commands, not `docker`.
- **Config standard:** XDG Base Directory Spec. Configs go in `~/.config/`, not bare `~/`.
- **Git Repos:** Live under `~/src/project`

## Tools and Systems

- **Credential Management:** 1Password via `Coastal` vault.
- **1Password CLI access:** `op`
- **Version control:** Git and GitHub
- **Slack**
- **Ticketing:** Jira

## Code preferences

- **Editor:**  VS Code (primary) used as git editor only. Learning to use Neovim as an alternative to VS Code.
- **Always add simple docstrings:** To functions and classes.
- **Always add simple comments:** Above line of code
- **Do not introduce abstractions beyond what the task requires.**
- **Do not add error handling for scenarios that can't happen.**
- **Python:** Use `uv` for project management and Ruff for linting
- **Shell:** ShellCheck-clean.
- **GitHub CLI access** `gh`
- **Default branch:** `main`.
- **Never make changes directly on `main`** Always create a feature or fix branch first
- **Git Branch naming:** `<type>/<Jira ticket>-<description>`
- **Always Use Conventional Commits format.**
- **Pull strategy:** rebase.

## Skill workflow preferences

- **Code Simplifier(`code-simplifier:code-simplifier`):** Always report findings first with numbered items before applying any changes. Prompt with: "Apply all fixes, select by number (e.g. 1,3), or provide your own answer?" Wait for a response before touching files.

## Documentation preferences

- Use `|---|---|` separator style for Markdown tables (compact, MD060 disabled).
- No time estimates in documentation: they deter engineers from reading.
- Do not use the em-dash character (`—`) in any document, post, README, CONTRIBUTING file, or written communication. Restructure the sentence to use a comma, colon, or semicolon instead.
