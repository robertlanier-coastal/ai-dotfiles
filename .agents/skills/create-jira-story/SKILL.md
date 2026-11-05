---
name: create-jira-story
description: Drafts a Coastal Jira story and its sub-tasks in the team format, reviews the draft with the user, then creates them in Jira. Use when the user wants to create, write, or set up a Jira story, ticket, or sub-tasks for dev work, or when new-plan offers it after a plan is written.
---

# Create a Jira story

Every story and sub-task follows the format in `references/format.md`. Read it
first. Also read the shared lessons `lessons/jira.md` and `lessons/general.md`.

Nothing is created in Jira until the user approves the full draft.

## Steps

1. **Find the plan.** Look in `.agents/plans/` in the current repo. If the user
   named a plan, use it. If there is none, suggest running `new-plan` first,
   because a plan fills most of the ticket. If the user declines, go through
   each step below with them and ask whenever something is unclear.

2. **Look things up in parallel.** These do not depend on each other, so run
   them as parallel tool calls in one message:
   - Read the plan files (`00_overview.md`, `todo.md`).
   - Get the cloud ID, then the field metadata for the Story and Sub-task issue
     types in the project (`getJiraIssueTypeMetaWithFields` with
     `requiredFieldsOnly: false`). Match fields by their names: "As a...",
     "I want...", "So that...", "Acceptance Criteria", "Design Notes",
     "Deployment Notes", "Steps to Test". Never hard-code field IDs.
   - List open epics in the project (JQL `issuetype = Epic AND statusCategory != Done`).
   - Look up the assignee's account ID, if a name is known.

3. **Ask only what is not clear.** Fill what the plan answers. Ask the rest, in
   one message, using these exact questions:
   1. What Parent Epic will the new Story be a child of?
   2. Who to assign the Story to?
   3. What role to enter for "As a..." field?
   4. What are you wanting to do for the "I want..." field?
   5. What are you accomplishing with this story for the "So that..." field?
   6. What is the priority of the Story?
   7. What is the Acceptance Criteria?

4. **Notes tab.** Tell the user what you recommend for Design Notes (Why first)
   and Deployment Notes, ask any clarifying questions, then use the answers.
   Leave Release Notes empty.

5. **Testing tab.** Tell the user what you recommend for Steps to Test, ask any
   clarifying questions, then use the answers. Leave Assigned tester empty.

6. **Sub-tasks.** Split the work into the most simple, logical sub-tasks.
   Titles start with a verb. In each, split Tasks into small steps that are one
   commit each and easy to roll back. Put the proving checks last. Reuse the
   plan's phases and tasks when there is a plan.

7. **Show the full draft.** Story fields, Notes, Testing, and every sub-task.
   Start the message with one line naming the audience. Wait for approval.

8. **Create in Jira.**
   1. Create the story with its fields (markdown is fine for story fields).
   2. For each sub-task, write its JSON (see `references/format.md`), run
      `uv run scripts/build_adf.py <file>`, and create it with the parent key
      and `contentFormat: "adf"`.
   3. Read one sub-task back and confirm the Tasks are checkboxes.
   4. Report the new keys and links.

## Rules

- Before editing any existing Jira field, read it, then change only the lines
  that must change.
- Use a subagent only for heavy research, for example reading many repo files
  to draft Design Notes when there is no plan. Tell the user the token cost
  first (about 130k tokens per subagent). Never use a subagent for a step that
  needs the user's answers.
- If the plan exists, offer to add the new ticket keys to its `00_overview.md`.
