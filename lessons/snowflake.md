---
name: snowflake
description: Lessons for hand-written Snowflake SQL.
read_when: Writing or reviewing Snowflake SQL outside dbt models.
---

# Snowflake lessons

These rules do not apply to dbt models.

- Do: follow Snowflake SQL standards and best practices when writing SQL.
- Do: reuse logic by building objects that read from each other.
  Do not: copy the same logic into several scripts.
  Why: plain SQL scripts cannot include other files. A folder does not stop repetition.
