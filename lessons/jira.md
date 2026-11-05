---
name: jira
description: Jira ticket standards for the Coastal Snowflake Team.
read_when: Writing or editing a Jira ticket (Acceptance Criteria, Testing tab, Deployment Notes, Release Notes).
---

# Jira lessons

Also follow the writing style in `general.md`.

- Do: before editing any Jira field, read its current value, then change only
  the lines that need to change. Keep the user's sections, order and format.
  Do not: rewrite a field from my own earlier copy.
  Why: I overwrote a Why section and a Tasks section the user had added.
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
  (the topic, no "Update:" prefix), then bold sections "Completed", "Findings",
  "Tested", and "Next". Short bullets, one idea each, plain words. Explain
  any package or term in a few words. Skip a section if it is empty.
  Do not: use plan phase or task numbers in the comment.
  Why: the user liked this format for subtask comments and standups at every client.
- Do: in every dev ticket (story and sub-task), add a "Why" section. Say the
  problem, and how the work helps the client. Keep it to 1 to 3 plain bullets.
  Sub-tasks: at the top of the Description, above "What". Stories have no
  Description (Key details has the tabs Field, Notes, Testing, Waves): put the
  Why at the top of Design Notes on the Notes tab.
  Do: in the closing comment, say what the finished result is and what the
  work took (number of commits, files, checks run), so it can feed a demo or
  a client update.
  Why: the user wants to explain why the work was done, how much work it
  took, and what was delivered, not only what was changed.
- Do: write sub-task descriptions as: What (bullets), Why (bullets), Tasks
  (Jira checkbox list). Put the checks that prove the result at the end of
  Tasks. No "Done When" section and no task numbers. Stories use their own
  format. The user ticks the boxes; never change checkbox state.
  Why: the user set this format to avoid a separate, overlapping Done list.
- Do: write checkboxes as an ADF `taskList` (contentFormat "adf").
  Do not: send `- [ ]` with contentFormat "markdown"; it becomes plain text
  and removes existing checkboxes.
  Why: a markdown edit turned real checkboxes into escaped text.

