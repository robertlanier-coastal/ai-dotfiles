# AI Dotfiles

Personal, portable instructions, rules, and skills for AI coding assistants.

One repo travels with the engineer. It works on their own Mac, on a client
machine that has its own AI settings, and on a client VDI with a different AI
tool. Nothing here changes a client's settings.

## What lives where

| Content | Where | Loaded on |
|---|---|---|
| Workflow, code, git, and documentation rules | `.agents/AGENTS.md` | Every machine |
| Shared rules, one file per topic | `.agents/rules/` | Every machine |
| Skills (Agent Skills format) | `.agents/skills/` | Every machine |
| Personal voice and Mac setup (shell, Podman, 1Password) | `.claude/CLAUDE.md` | The engineer's Mac |
| Plans | `.agents/plans/` (ignored by git) | Local only |

Project content (a client repo's own plans and rules) lives in that repo's
`.agents/` folder, which is excluded from git there with `.git/info/exclude`.

## Supported tools

| Tool | Instructions | Rules | Skills | Status |
|---|---|---|---|---|
| Claude Code (own Mac) | `~/.claude/CLAUDE.md` link | `~/.claude/rules` link (auto-loaded) | `~/.claude/skills/<name>` links | Active |
| Claude Code (client machine) | `CLAUDE.local.md` import in the repo | Read by Session Start steps | Read `SKILL.md` by hand | Active |
| Any other agent (for example Snowflake Cortex Code) | Session-start prompt | Read by Session Start steps | Read `SKILL.md` by hand | Active (manual) |
| Copilot, Cursor, Codex, Gemini CLI | Their global instructions file | Read by Session Start steps | `~/.agents/skills` link | Planned |

Skills follow the open Agent Skills format (`SKILL.md`), which most AI coding
tools can read. Check each tool's docs before adding its links.

## Repository structure

```text
ai-dotfiles/
├── .claude/
│   ├── CLAUDE.md                 # personal voice and Mac setup, loads AGENTS.md
│   ├── rules -> ../.agents/rules
│   └── skills -> ../.agents/skills
├── .agents/
│   ├── AGENTS.md                 # rules for any agent on any machine
│   ├── rules/                    # shared rules, one file per topic or tool
│   ├── skills/                   # create-jira-story, new-plan, write-jira-comment, write-rule
│   └── plans/                    # local plans, ignored by git
├── .github/
│   └── README.md
└── .gitignore
```

In the docs, `<ai-dotfiles>` means the folder where this repo is cloned. The
suggested place is `~/src/coastal/ai-dotfiles`. Scripts find the repo from
their own location, so any folder works.

## Setup

Clone the repo on every machine you work on:

```bash
mkdir -p ~/src/coastal
git clone git@github.com:YOUR_USERNAME/ai-dotfiles.git ~/src/coastal/ai-dotfiles
```

Then follow the section for that machine.

### 1. Your own Mac (Claude Code)

Back up any existing files in `~/.claude/` first.

```bash
mkdir -p ~/.claude/skills
ln -s ~/src/coastal/ai-dotfiles/.claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/src/coastal/ai-dotfiles/.claude/rules ~/.claude/rules
for s in ~/src/coastal/ai-dotfiles/.agents/skills/*/; do
  ln -s "${s%/}" ~/.claude/skills/"$(basename "$s")"
done
```

Check:

```bash
ls -l ~/.claude/CLAUDE.md ~/.claude/rules ~/.claude/skills/
```

In a new Claude Code session, run `/context`. `general.md` and `jira.md` should
be listed. `python.md`, `snowflake.md`, and `data-modeling.md` load only when
matching files are read.

### 2. Client machine with its own Claude Code setup

Do not change the client's `~/.claude/`. Load your instructions per repo
instead. In the client repo root:

```bash
echo "@<ai-dotfiles>/.agents/AGENTS.md" > CLAUDE.local.md
echo "CLAUDE.local.md" >> .git/info/exclude
```

Replace `<ai-dotfiles>` with the clone path. If the client repo uses an
`AGENTS.md`, run `/config` and set **Project instructions** to
`claude-md-and-agents-md`, so Claude Code reads both files.

### 3. Client VDI with another AI tool

Start each session with:

> Read `<ai-dotfiles>/.agents/AGENTS.md` and follow it.

The agent then reads the shared rules (Session Start steps) and any skill's
`SKILL.md` when needed.

## Without uv

The skill scripts use only the Python standard library. If `uv` is missing,
run them with `python3`. Each skill also says how to do its steps by hand.

## Keeping it up to date

```bash
cd <ai-dotfiles>
git pull
```

Personal repo rules for committing are in the Git section of `.agents/AGENTS.md`.

## Security

Do not commit:

- API keys, credentials, or authentication tokens.
- Session histories and conversation transcripts.
- Cached data, logs, or temporary files.
- Client names, ticket keys, table names, or other client details in shared rules and skills.

## Design principles

- **Single source of truth:** each rule lives in one file.
- **Portable:** works on any machine, from any clone path, with or without uv.
- **Client-safe:** never changes a client's AI settings.
- **Tool-neutral:** standard files (`AGENTS.md`, `SKILL.md`), linked into each tool.
- **Simple:** plain files and symbolic links, no install tooling.
