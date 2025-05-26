---
tags: [assistant_workflow, meta, task_management]
provides: [assistant_task_decomposition_workflow]
requires: [docs/task_decomposition.md, meta/assistant_guidelines/maintenance_checklist.md, meta/TODO.md, meta/guidelines/tag_conventions.md]
---

# Assistant Workflow: Task Decomposition

This document outlines the workflow the AI assistant follows when decomposing complex tasks into manageable, atomic subtasks using the Hierarchical Atomic Decomposition (HAD) method defined in the [Task Decomposition Guide](mdc:docs/task_decomposition.md).

## When to Use Task Decomposition

- For complex, multi-step user requests
- When planning implementation of roadmap items
- For tasks that would benefit from explicit tracking of dependencies and outputs
- When working on tasks that may span multiple assistant interactions

## Task Decomposition Workflow

1️. **Identify Top-Level Task:**
   - Define the primary goal as a verb-driven statement.
   - Clarify the expected final output with the user if necessary.

2️. **Break Down into Major Phases:**
   - Segment the task into 3-5 logical phases or components.
   - Follow a natural workflow progression (e.g., Research → Plan → Implement → Test → Document).

3️. **Decompose to Atomic Subtasks:**
   - Iterate through each phase, breaking it down into specific, atomic actions.
   - Ensure each subtask is achievable in a single reasoning step (1-5 minutes of work).
   - Use the hierarchical ID system (e.g., 1.1, 1.2, 2.1) to maintain parent-child relationships.

4️. **Annotate Each Subtask:**
   - Use the template from the [Task Decomposition Guide](mdc:docs/task_decomposition.md):
     ```markdown
     ### {ID}. {Title} `[STATUS]` #{tag1} #{tag2}
     *Related: [Link to related file/resource](mdc:path/to/file), [Another resource](mdc:path/to/another/file)*

     - **Inputs**: {List of required inputs with links where applicable}
     - **Outputs**: {List of expected outputs}
     - **Dependencies**: {IDs of prerequisite subtasks}
     - **Estimate**: {Time or complexity score}
     - **Status**: {Brief status description}
     - **References**: {Optional links to relevant documentation or resources}
     ```
   - Include status indicators for each task and subtask:
     - `[NOT STARTED]` - Work has not yet begun
     - `[IN PROGRESS]` - Work has started but is not complete
     - `[BLOCKED]` - Cannot proceed due to dependencies or obstacles
     - `[COMPLETED]` - Task has been finished and verified
     - `[DEFERRED]` - Intentionally postponed to a later time

5️. **Add Tags, Links and References:**
   - Add inline tags using the `#tag` format to categorize tasks and subtasks (see [Tag Conventions](mdc:meta/guidelines/tag_conventions.md)).
   - Link directly to related files using MDC links (`mdc:path/to/file`).
   - Add cross-references to other tasks or sections within the document using anchor links (`#section-id`).
   - Include "Related" section at the top of each major task with key related resources.
   - Link inputs directly to source files where applicable.
   - Add optional "References" field to subtasks when additional context would be helpful.

6️. **Create Status Summary Table:**
   - Add a status summary table at the end of each major section or task breakdown.
   - Include columns for task name, status, and completion percentage.
   - Calculate overall project completion status.
   - Follow the status tracking guidelines in [Status Tracking System](mdc:meta/assistant_guidelines/status_tracking.md).

7️. **Document the Task Breakdown:**
   - For significant projects, create a dedicated task file in the appropriate directory.
   - For smaller tasks, document the breakdown directly in conversation or in the relevant documentation.
   - Add a reference to `meta/TODO.md` linking to the task breakdown.

8️. **Execute and Track Progress:**
   - Begin execution following the hierarchical order, respecting dependencies.
   - Update task status after completing each subtask.
   - Document outputs as specified in the task breakdown.
   - Update the status summary table as progress is made.

9️. **Perform Maintenance Checks:**
   - Consult the [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for guidance on integrating task management with the broader DSS maintenance workflow.
   - Ensure that completed tasks are properly recorded in `meta/TODO.md`.

## Integration with Other Workflows

- **Code Modification:** When a subtask involves code changes, follow the [Code Modification Workflow](mdc:meta/assistant_workflows/code_modification.md) for that specific subtask.
- **Documentation:** When a subtask involves creating or updating documentation, follow the [Docs-Driven Development Workflow](mdc:meta/assistant_workflows/docs_driven_development.md) for that specific subtask.

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- Step 3 (Categorize Task Type) identifies complex, multi-step tasks that should use this workflow
- Steps 5-8 are implemented through the detailed steps of this workflow, with special attention to breaking down the task hierarchically

This workflow may transition to other workflows at the subtask level. When executing individual subtasks, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on using the appropriate workflow for each subtask.

## Example Task Breakdown Document Structure

```markdown
# Task: {Task Name}

## Overview
Brief description of the overall task and goal.

## Task Status Legend

Each task and subtask is marked with a status indicator:
- `[NOT STARTED]` - Work has not yet begun
- `[IN PROGRESS]` - Work has started but is not complete
- `[BLOCKED]` - Cannot proceed due to dependencies or obstacles
- `[COMPLETED]` - Task has been finished and verified
- `[DEFERRED]` - Intentionally postponed to a later time

For more detailed status tracking, including timestamps and additional status types, refer to the [Status Tracking System](mdc:meta/assistant_guidelines/status_tracking.md).

## Task Breakdown

### 1. {Phase 1 Name} `[STATUS]` #{category_tag} #{priority_tag}
*Related: [Link to related resource](mdc:path/to/resource)*

#### 1.1. {Subtask Title} `[STATUS]` #{specific_tag}
- **Inputs**: {List of required inputs with links where applicable}
- **Outputs**: {List of expected outputs}
- **Dependencies**: {IDs of prerequisite subtasks}
- **Estimate**: {Time or complexity score}
- **Status**: {Brief status description}
- **References**: {Optional links to relevant documentation or resources}

#### 1.2. {Subtask Title} `[STATUS]`
...

### 2. {Phase 2 Name} `[STATUS]`
...

## Task Status Summary

| Phase | Status | Completion |
|-------|--------|------------|
| 1. Phase 1 Name | STATUS | X% |
| 2. Phase 2 Name | STATUS | X% |
| **OVERALL** | **STATUS** | **X%** |

## Integration Strategy
Describe the optimal sequence for implementation.

## Related Documentation
- [Resource 1](mdc:path/to/resource1) - Brief description
- [Resource 2](mdc:path/to/resource2) - Brief description
- [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) - Guidelines for using tags throughout the project
```

This structure can be adapted based on the specific needs and complexity of the task at hand.