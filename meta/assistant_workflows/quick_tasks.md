---
tags: [assistant_workflow, meta, efficiency]
provides: [assistant_quick_tasks_workflow]
requires: [meta/assistant_guidelines/maintenance_checklist.md, .cursor/rules/assistant.mdc, meta/assistant_workflows/code_modification.md, meta/assistant_workflows/docs_driven_development.md]
---

# Assistant Workflow: Lightweight Process for Quick Tasks

This document outlines a streamlined workflow for handling simple, atomic tasks that don't require the full complexity of other workflows. It's designed to improve efficiency while maintaining essential quality standards.

## Quick Task Criteria

A task can be considered "quick" and eligible for this lightweight workflow if it meets ALL of the following criteria:

1. **Scope**: The task is atomic and self-contained, requiring changes to at most 1-2 files
2. **Complexity**: The task can be completed in a single interaction with minimal cognitive load
3. **Risk**: The change has low potential for introducing errors or breaking existing functionality
4. **Dependencies**: The task has minimal or no dependencies on other pending changes
5. **Documentation Impact**: The change requires minimal updates to other documentation

Examples of quick tasks:
- Minor text corrections or formatting
- Adding simple tags or metadata
- Small self-contained code fixes (e.g., fixing a typo in a variable name)
- Adding a single TODO item
- Creating a simple file from an existing template

## Lightweight Workflow Steps

For tasks meeting the above criteria, follow this streamlined workflow:

1️. **Quick Assessment**:
   - Confirm the task meets all quick task criteria
   - If the task turns out to be more complex during execution, transition to the appropriate full workflow

2️. **Minimal Context Gathering**:
   - Read only the directly relevant files
   - Limit context gathering to immediate dependencies

3️. **Focused Execution**:
   - Implement the change with minimal tool calls
   - Focus only on the specific files that need modification

4️. **Essential Maintenance**:
   - Perform only these critical maintenance checks:
     - Ensure proper frontmatter is preserved/added if modifying markdown files
     - Add/update appropriate tags if applicable
     - Ensure links remain valid if modifying linked content
   - Skip lower-priority maintenance tasks that aren't directly affected

5️. **Verification**:
   - Quick check of the specific change for correctness
   - Verify that file format/structure remains consistent

## Abbreviated Maintenance Checklist

This abbreviated checklist replaces the full [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for quick tasks:

| Maintenance Task | When to Perform in Quick Tasks |
|------------------|--------------------------------|
| Update INDEX.md | Only if creating/deleting a file |
| Add Frontmatter | Always for new files |
| Preserve Existing Frontmatter | Always when editing files |
| Update Task Management | Only if the task was explicitly tracked |
| Check Links | Only if modifying linked content |
| Documentation Updates | Only for the directly modified files |

## Decision Tree: Full vs. Quick Workflow

Use this decision tree to determine whether to use this lightweight workflow or a more comprehensive one:

1. Does the task involve changes to more than 2 files?
   - Yes → Use [Code Modification](mdc:meta/assistant_workflows/code_modification.md) or [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
   - No → Continue

2. Does the task require complex reasoning or multiple steps?
   - Yes → Use [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
   - No → Continue

3. Does the task involve high-risk changes to core functionality?
   - Yes → Use [Code Modification](mdc:meta/assistant_workflows/code_modification.md)
   - No → Continue

4. Does the task require significant documentation updates?
   - Yes → Use [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
   - No → Use this Quick Tasks workflow

## Integration with Core Process

This lightweight workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc) by providing a streamlined path through the process:

- Step 3 (Categorize Task Type) identifies that the Quick Tasks workflow is appropriate
- Step 5 (Plan & Cross-Reference) is simplified to identifying that the Quick Tasks workflow applies
- Step 6 (Execute & Integrate) focuses only on the essential maintenance tasks listed above
- Step 7 (Review & Verify) is limited to a quick correctness check of the specific changes

When transitioning from this workflow to a more comprehensive one, return to the Core Process Checklist and resume from step 3 with task recategorization. Refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on how to handle these transitions. 