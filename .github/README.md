# AI Dotfiles

Personal configuration repository for AI coding assistants and agents.

This repository provides a version-controlled, portable source of truth for global instructions, rules, skills, and other AI tool configurations.

Configuration files are managed through symbolic links, allowing tools to use their expected configuration locations while keeping reusable configurations centralized.

## Supported Tools

| Tool | Configuration Directory | Status |
|---|---|---|
| Claude Code | `~/.claude/` | Active |
| OpenAI Codex | `~/.codex/` | Planned |

Additional tools may be added as needed.

## Repository Structure

```text
ai-dotfiles/
├── .claude/
│   ├── CLAUDE.md
│   ├── rules/
│   ├── settings.json
│   ├── skills/
│   └── agents/
├── .gitignore
└── README.md
```

Only configuration files intentionally managed by this repository are tracked.

## Installation

### 1. Clone the repository

```bash
mkdir -p ~/src
git clone git@github.com:YOUR_USERNAME/ai-dotfiles.git ~/src/ai-dotfiles
```

### 2. Create configuration directories

```bash
mkdir -p ~/.claude
```

### 3. Create symbolic links

Back up any existing configuration files before creating symbolic links.

```bash
ln -s ~/src/ai-dotfiles/.claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/src/ai-dotfiles/.claude/rules ~/.claude/rules
```

Link additional configuration files or directories as they are added to the repository.

### 4. Verify installation

```bash
ls -l ~/.claude/CLAUDE.md ~/.claude/rules
```

The symbolic links should point to files within `~/src/ai-dotfiles/`.

## Configuration Management

The repository serves as the source of truth for managed configurations.

Changes made through the symbolic links are reflected directly in the repository.

To commit and publish changes:

```bash
cd ~/src/ai-dotfiles
git add .
git commit -m "Update AI configuration"
git push
```

To synchronize changes on another machine:

```bash
cd ~/src/ai-dotfiles
git pull
```

## Security

This repository intentionally excludes sensitive information and machine-specific runtime data.

Do not commit:

- API keys, credentials, or authentication tokens.
- Session histories and conversation transcripts.
- Cached data, logs, or temporary files.
- Machine-specific secrets or local environment files.

Review configuration files before committing, particularly settings containing environment variables, permissions, hooks, or external integrations.

## Design Principles

- **Single source of truth:** Maintain reusable configurations in one repository.
- **Portability:** Reproduce configurations across development environments.
- **Separation of concerns:** Keep agent instructions separate from runtime state.
- **Modularity:** Organize configurations by tool and purpose.
- **Simplicity:** Prefer native configuration files and symbolic links over unnecessary tooling.
- **Version control:** Track configuration changes through Git.
