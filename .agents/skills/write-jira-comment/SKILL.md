---
name: write-jira-comment
description: Drafts a short Jira progress comment in the team format (Completed, Findings, Tested, Next) and posts it after the user approves. Use when the user wants a status update, progress note, standup summary, or done comment for a Jira story or sub-task.
---

# Write a Jira progress comment

Read the shared lessons `lessons/jira.md` and `lessons/general.md` first.

## Steps

1. **Read the ticket.** Get the issue and its latest comments, so the new
   comment does not repeat them. Read any plan Results log for this work
   (`.agents/plans/<plan_name>/`), and `git log` for the commits.

2. **Draft the comment** in this format:

   ```
   **<Topic in plain words>**

   **Completed**
   - <what was finished>

   **Findings**
   - <what we learned, with the reason>

   **Tested**
   - <what was run, and the result>

   **Next**
   - <the next step>
   ```

   - The title is the topic only. No "Update:" prefix.
   - Short bullets, one idea each, common words, no em dashes.
   - Explain any package or technical term in a few words.
   - Skip a section if it is empty.
   - Group commits by Jira sub-task key (for example "ABC-12 commits").
     Never use plan phase or task numbers.
   - State results faithfully. If a check failed or was skipped, say so.

3. **Show the draft.** Start the message with one line naming the audience
   (for example "Written for: the team following ABC-10"). Say which ticket it
   will go on. Wait for approval.

4. **Post it** only after approval, as a comment on that ticket. If the user
   would rather post it, give them the text to copy.

Comments may be public on some projects. If the posted comment comes back
marked public, tell the user.
