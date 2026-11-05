---
name: general
description: How to work with the user on any project. Sources, writing style, and process.
read_when: Always. Read at the start of every session.
---

# General lessons

## Writing style

- Do: write for a neurodivergent audience. Short sentences, one idea each.
  Common words. Define technical terms on first use. Prefer lists to long
  paragraphs. No idioms. No em dashes.
  Why: applies to tickets, docs, PR descriptions, and messages for every client.

## Sources and claims

- Do: say where every recommendation comes from (user message, repo file,
  query result, or my own suggestion).
  Do not: imply a pattern came from the repo when I have not read the files.
  Why: the user asked if a design was based on a repo folder I had not read.
- Do: read a referenced repo folder before calling it a model to follow.
- Do: recount lists before quoting a count (for example, column counts).
  Why: a wrong column count was quoted for many turns.

## Design

- Do not: copy a folder structure only to match an existing folder.
  Do: add structure only when the work needs it (for example, logic used in
  two or more places).

## Process

- Do: write commit messages that are simple, clear, and direct. One short
  subject line. Add a body only if it is really needed.
  Why: the user asked for this.
- Do: use one pull request per story. Split each phase (or sub-task) into
  small, simple, logical tasks. Each task is one commit. Write a draft
  Conventional Commits message for each task in the plan's `todo.md`.
  Do not: plan one commit per phase or per sub-task.
  Why: small commits let reviewers read the pull request one commit at a
  time, and let any one change be rolled back.
- Do: make each task's change and leave it uncommitted. Show the diff and
  wait for the user's go-ahead. Then commit. Push only when a whole phase is done.
  Do not: commit before the user has reviewed the change.
  Why: the user wants to review every change before it is committed.
- Do: in personal repos (such as `ai-dotfiles`), ask, then commit and push to
  `main`. In client or project repos, never commit or push to `main`: use a
  branch and a pull request.
  Why: the user set this rule. The global CLAUDE.md has the same rule.
- Do: in PRs, comments and tickets, group commits by their Jira sub-task key
  (for example "CCFIN4-143 commits").
  Do not: call them "Phase 1 commits". Plan phases are internal.
  Why: the user asked for this.
- Do: before writing a phase's file, check in with the user. List the design
  choices (filters, columns kept or dropped, optimizations). Then write it.
  Do not: add optimizations (for example, removing zero rows) without asking.
  Why: design choices were made without a check-in, which breaks "Verify Plan".
- Do: ask before creating files when the location or structure is not decided.
- Do not: create, move (`git mv`), or edit repo files when the user says they
  will make the changes.
  Do: give step-by-step instructions one file at a time. Review each file after
  the user saves it.
  Why: the user wanted to copy their own work and follow a reviewer's steps.
- Do: when a review points to another open PR, ask how to use it before
  branching off it.
  Why: the user chose to copy one block from the other PR, not to branch from it.
- Do: check `.gitignore` before suggesting where local files go.
- Do: write any script an agent or skill runs in Python. Run it with `uv run`.
  Do not: write agent scripts in shell.
  Why: the user asked for this.
- Do: tell the user the token cost before starting test subagents.
  Each fresh subagent costs about 130k tokens, mostly its base context, even
  for a few tool calls.
  Why: skill tests used four subagents at about 130k tokens each.
- Do: name skills with a verb first that says what they do (for example
  `create-jira-story`, not `jira-story`).
  Why: the user asked for this.

