---
name: jira
description: Jira ticket standards for the Coastal Snowflake Team.
read_when: Writing or editing a Jira ticket (Acceptance Criteria, Testing tab, Deployment Notes, Release Notes).
---

# Jira lessons

Also follow the writing style in `general.md`.

- Do: write Acceptance Criteria (AC) as work the data engineer does and can check.
  Do not: add business owner sign-off or approvals to AC.
  Why: AC must be verifiable by the engineer. Approvals are tracked elsewhere.
- Do: when an AC is based on a sample or reference object, say so in the AC text.
- Do: put only SQL queries in the Testing tab (Steps to Test) for tickets
  that change data.
  Do not: add file checks, lint, or PR approval as test steps on those tickets.
  Why: those are checked visually. The Testing tab is for runnable SQL.
- Do: for CI/CD pipeline tickets, use local tool runs (for example actionlint
  and act) as test steps.
  Why: pipelines change no data, so SQL cannot test them.
- Do: in Design Notes, say what we use and why.
  Do not: name tools we chose not to use.
  Why: the user asked to remove a rejected option from the notes.
- Do: fill Deployment Notes and Release Notes only after the files exist.
  Why: the user adds them when the scripts and scope are final.
  Exception: deploy risks that do not depend on the final files (for example,
  what cannot be tested before merge) can go in Deployment Notes early.
- Do: write Jira progress comments in this format: a bold title line
  ("Update: <topic>"), then bold sections "Done today", "Findings",
  "Tested", and "Next". Short bullets, one idea each, plain words. Explain
  any package or term in a few words. Skip a section if it is empty.
  Do not: use plan phase or task numbers in the comment.
  Why: the user liked this format for subtask comments and standups at every client.

