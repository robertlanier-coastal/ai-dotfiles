# Coastal Jira story and sub-task format

Writing style: short sentences, one idea each, common words, no em dashes.
Define technical terms on first use. No client details in examples.

## Story

Stories have no Description field. Key details has 4 tabs: Field, Notes,
Testing, Waves. Leave Waves alone.

### Field tab

| Field | What to write |
|---|---|
| As a... | The role, for example "Data Engineer". |
| I want... | What the work does, in plain words. |
| So that... | The one-line outcome. |
| Acceptance Criteria | Bullets that describe the end state. Each one is work the engineer does and can check. No sign-offs or approvals. |

Also set: Parent (the Epic), Assignee, Priority.

### Notes tab

- **Design Notes:** start with a **Why** section (the problem, and how the work
  helps the client, 1 to 3 bullets with sub-bullets). Then the design facts:
  what changes, what is out of date or broken, decisions, open decisions.
  Say what we use and why. Do not name options we chose not to use.
- **Deployment Notes:** steps that happen outside the merge, and deploy risks
  (for example, what cannot be tested before merge).
- **Release Notes:** leave empty.

### Testing tab

- **Steps to Test:** numbered, runnable checks that match what was built:
  SQL for data changes, Python or shell commands for scripts, local tool runs
  for CI/CD. No file checks, lint-only steps, or PR approval.
- **Assigned tester:** leave empty.

## Sub-task

- **Title:** starts with a verb, short and plain. Example: "Upgrade the build tool".
- **Description:** 3 sections, each after a horizontal rule, with a bold heading.
  1. **What:** bullets of what changes.
  2. **Why:** bullets of why it matters, sub-bullets for detail.
  3. **Tasks:** a Jira checkbox list (ADF `taskList`). Small, logical tasks,
     each one commit that can be rolled back alone. Put the checks that prove
     the result last. No task numbers. No "Done When" section.
- Build the description with `scripts/build_adf.py`. Never send `- [ ]` as
  markdown: Jira turns it into plain text.
- The user ticks the boxes. Never change checkbox state.

### Example sub-task input for build_adf.py

```json
{"what": ["Upgrade the build tool from 1.0 to 2.0"],
 "why": ["Version 1.0 is end of life.", ["No security fixes.", ["It gets no updates."]]],
 "tasks": ["Pin the build tool to 2.0", "Update the setup docs", "Run the local checks", "Pull request checks pass"]}
```

### ADF shape, for writing by hand

A sub-task description is one `doc` with: `rule`, bold `paragraph` "What",
`bulletList`, `rule`, bold "Why", `bulletList`, `rule`, bold "Tasks", then a
`taskList` of `taskItem`s:

```json
{"type": "taskList", "attrs": {"localId": "any-unique-id"},
 "content": [
   {"type": "taskItem", "attrs": {"localId": "another-unique-id", "state": "TODO"},
    "content": [{"type": "text", "text": "Pin the build tool to 2.0"}]}
 ]}
```

Inline code is a text node with `"marks": [{"type": "code"}]`.

