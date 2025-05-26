---
tags: [assistant_workflow, meta, documentation]
provides: [assistant_documentation_refactoring_workflow]
requires: [meta/assistant_guidelines/maintenance_checklist.md, .cursor/rules/assistant.mdc, meta/assistant_workflows/workflow_transitions.md]
---

# Assistant Workflow: Documentation Refactoring

This document outlines a specialized workflow for systematically updating, improving, or restructuring existing documentation across multiple files. It's designed for tasks that require coordinated changes to documentation that don't involve creating new documentation from scratch or significant code modifications.

## Documentation Refactoring Criteria

A task can be considered "documentation refactoring" if it meets MOST of the following criteria:

1. **Focus**: The task primarily involves updating existing markdown or documentation files
2. **Scope**: Changes span multiple related files (typically more than 2)
3. **Consistency**: Changes need to be coordinated and consistent across files
4. **Structure**: The existing documentation structure is preserved while content is updated
5. **Code Impact**: Minimal or no code changes are required

Examples of documentation refactoring tasks:
- Updating terminology consistently across multiple documentation files
- Adding new sections to a set of related documentation files
- Improving cross-referencing between existing documentation
- Restructuring the organization of content within documentation
- Updating links, references, or file paths across multiple files

## Documentation Refactoring Workflow Steps

For tasks meeting the above criteria, follow this workflow:

1️. **Analyze Documentation Structure**:
   - Identify all affected documentation files
   - Understand the relationships between the files
   - Determine how changes to one file will affect others

2️. **Plan Coordinated Changes**:
   - Create a clear plan for what changes are needed across all files
   - Establish patterns or templates for consistent changes
   - Identify any potential conflicts or dependencies

3️. **Apply Changes Systematically**:
   - Make changes to one file at a time, following a logical order
   - Ensure consistent formatting, terminology, and structure
   - Preserve existing YAML frontmatter (`tags`, `provides`, `requires`)
   - Update frontmatter as needed to reflect new content relationships

4️. **Update Cross-References**:
   - Ensure all internal links between documents remain valid
   - Update any cross-references to reflect the new content
   - Check external references for consistency

5️. **Perform Documentation Maintenance**:
   - Check for and fix any broken links
   - Ensure consistent formatting across all updated files
   - Update the INDEX.md if documentation structure has changed
   - Verify all files have appropriate frontmatter

6️. **Review for Consistency**:
   - Verify that changes are applied consistently across all files
   - Check that terminology, formatting, and structure are uniform
   - Ensure the overall documentation coherence is maintained

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- Step 3 (Categorize Task Type) identifies documentation refactoring tasks that involve coordinated changes across multiple files
- Steps 5-8 are implemented through the detailed steps of this workflow

When a task also requires significant code changes or creation of entirely new documentation, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on transitioning to Code Modification or Docs-Driven Development workflows.

## Relationship to Other Workflows

This workflow complements other existing workflows:

- **Quick Tasks**: For simple documentation changes to 1-2 files, use the Quick Tasks workflow instead
- **Docs-Driven Development**: For creating new documentation from scratch, use the Docs-Driven Development workflow
- **Code Modification**: When documentation changes must be accompanied by significant code changes
- **Task Decomposition**: For large-scale documentation restructuring that requires breaking down into multiple phases

## Decision Points

If during execution you discover that:
- The task requires creating entirely new documentation → Transition to Docs-Driven Development
- The task requires significant code changes → Transition to Code Modification
- The task is much larger than anticipated → Transition to Task Decomposition
- The task affects only 1-2 files → Consider switching to Quick Tasks 