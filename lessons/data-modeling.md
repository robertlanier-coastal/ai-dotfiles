---
name: data-modeling
description: Tool-neutral data modeling and data engineering practices.
read_when: Designing tables, views, or build-step objects in any warehouse or tool.
---

# Data modeling lessons

- Do: query sample or reference objects before designing from them.
- Do: verify formulas against sample data before calling them the definition.
- Do: in build-step objects, keep source columns that help trace or reuse a
  row (natural keys, codes, file audit columns), unless the user says otherwise.
- Do: explain build-step objects that have no sample (why they exist, who uses them).
