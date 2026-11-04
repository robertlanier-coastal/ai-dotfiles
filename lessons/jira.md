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
- Do: put only SQL queries in the Testing tab (Steps to Test).
  Do not: add file checks, lint, or PR approval as test steps.
  Why: those are checked visually. The Testing tab is for runnable SQL.
- Do: fill Deployment Notes and Release Notes only after the files exist.
  Why: the user adds them when the scripts and scope are final.
