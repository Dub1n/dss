---
tags: [assistant_workflow, meta]
provides: [assistant_code_modification_workflow]
requires: [meta/roadmap.md, docs/api_reference.md, canvas/architecture.canvas, meta/update_links.py, meta/assistant_workflows/task_decomposition.md]
---

# Assistant Workflow: Code Modification

This document details the step-by-step process the AI assistant follows when adding or modifying code within the DSS repository.

When adding or modifying **code**...
1️. Locate matching doc stub.  
2️. Insert/update:
    - YAML front-matter (`provides`, `requires`).
    - Appropriate tags following [Tag Conventions](mdc:meta/guidelines/tag_conventions.md).
    - Short "Why/How" summary under `## Overview`.  
    - Links to any new types/functions in **Glossary.md**.
3️. If new public API:  
    - Append entry in `/docs/api_reference.md`.  
    - Add card + arrow in `/canvas/architecture.canvas` (JSON).  
4. Add / adjust node in `/canvas/architecture.canvas`.
4️. Update `/meta/roadmap.md` – move ticket from *Planned*→*In Progress* or tick box complete.  
5️. **Perform Maintenance Checks:** Consult the [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for detailed guidance on performing maintenance tasks relevant to code modification, including triggers, prioritization, and handling ambiguity.
6. Run `meta/update_links.py` script; fix dead links.  
7. Commit: `feat: <thing> | docs+meta auto-update`. 

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- Step 3 (Categorize Task Type) identifies code-focused tasks that should use this workflow
- Steps 5-8 are implemented through the detailed steps of this workflow

When a task reveals complexity beyond the scope of this workflow, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on transitioning to Task Decomposition. 