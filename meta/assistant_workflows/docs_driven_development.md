---
tags: [assistant_workflow, meta]
provides: [assistant_docs_driven_workflow]
requires: [INDEX.md, meta/assistant_guidelines/maintenance_checklist.md, meta/dss_config.yml, meta/assistant_workflows/task_decomposition.md]
---

# Assistant Workflow: Docs-Driven Development

This document outlines the workflow the AI assistant follows when starting the development process by creating documentation first.

When you create **docs** first (docs-driven)...

1️. **Create New Documentation File:** Create the new `.md` file (or other appropriate documentation format) in the relevant directory (e.g., `/docs/`, `/meta/`).
2️. **Add Initial Structure & Frontmatter:** Add the basic section structure, initial content, and the required YAML frontmatter stub (`tags`, `provides`, `requires`) based on `meta/dss_config.yml`. Follow the [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) when selecting appropriate tags.
3️. **Perform Maintenance Checks:** Consult the [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for detailed guidance on performing maintenance tasks relevant to creating new documentation, including triggers, prioritization, and handling ambiguity.
4️. **Develop Content:** Flesh out the detailed content of the documentation, including explanations, examples, and linking to other relevant documents or code.
5️. **Generate Code Stubs (Optional):** If applicable, generate initial code stubs in the `/src/` directory based on the documentation.
6️. **Refine and Integrate:** Continue refining both documentation and code, potentially following the [Code Modification Workflow](mdc:meta/assistant_workflows/code_modification.md) for subsequent code changes.
7️. **Commit:** Commit the changes with a descriptive message. 

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- Step 3 (Categorize Task Type) identifies documentation-first tasks that should use this workflow
- Steps 5-8 are implemented through the detailed steps of this workflow

When a task requires significant code implementation beyond the scope of documentation, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on transitioning to Code Modification or Task Decomposition workflows. 