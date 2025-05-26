---
tags: [assistant_guidelines, meta]
provides: [assistant_documentation_task_management]
requires: [INDEX.md, docs/how_to_update_index.md, meta/TODO.md, docs/automated_formatting, docs/task_decomposition.md, meta/assistant_workflows/task_decomposition.md]
---

# Assistant Guidelines: Documentation & Task Management

This document outlines the AI assistant's guidelines and responsibilities related to managing project documentation and tracking tasks.

Ignore any content under docs/🔒archive/. Only summarise and document files that reflect the current design state unless asked otherwise.

For detailed instructions on updating the project index (`INDEX.md`), refer to [docs/how_to_update_index.md](mdc:docs/how_to_update_index.md).

Whenever a potential task or improvement is identified, add it to the 'Tasks' section of `meta/TODO.md`. If completed within the same interaction, mark it as [x]. **Note:** Until an automated sorting script is implemented, completed tasks will remain in the 'Tasks' section marked with [x] and will not be manually moved to the 'Completed Tasks' section by the assistant.

**For complex tasks**, utilize the Hierarchical Atomic Decomposition (HAD) method outlined in [docs/task_decomposition.md](mdc:docs/task_decomposition.md) and follow the workflow in [meta/assistant_workflows/task_decomposition.md](mdc:meta/assistant_workflows/task_decomposition.md) to break down the task into manageable, atomic subtasks with clear dependencies and outputs. Apply appropriate tags to tasks and subtasks following the [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) to facilitate organization and filtering.

**Task Management Commitment:** I will actively track major tasks discussed and completed within our interaction by adding them to the 'Completed Tasks' section of `meta/TODO.md` upon completion. For ongoing work, I will add tasks to the 'Tasks' section at the outset and mark them [x] upon finishing.

When adding a task to `meta/TODO.md` that relates to a specific code location, also add a comment in the code referencing `meta/TODO.md` and the task.

Whenever a plan or useful information that would be helpful later is identified or discussed, I will automatically add it to the relevant project documentation file(s) (e.g., `meta/TODO.md`, `docs/automated_formatting`) instead of solely keeping it in the chat, without waiting for explicit confirmation unless the appropriate location or content is ambiguous.

Verify the outcome of file edits, paying close attention to formatting. 