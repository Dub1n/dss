---
tags: [assistant_workflow, meta, task_management, decomposition]
provides: [assistant_task_decomposition_workflow]
requires: [docs/task_decomposition.md, meta/assistant_guidelines/maintenance_checklist.md, meta/TODO.md, meta/guidelines/tag_conventions.md, .cursor/rules/assistant.mdc]
---

# Assistant Workflow: Task Decomposition

This document outlines the workflow the AI assistant follows when decomposing complex tasks into manageable, atomic subtasks using the Hierarchical Atomic Decomposition (HAD) method defined in the [Task Decomposition Guide](mdc:docs/task_decomposition.md).

## When to Use Task Decomposition

A task should use this workflow if it meets MOST of the following criteria:

1. **Complexity**: The task is multi-step and cannot be completed in a single reasoning cycle
2. **Coordination**: Changes span multiple files, systems, or workflow types requiring coordination
3. **Planning Benefit**: The task would benefit from explicit tracking of dependencies and outputs
4. **Duration**: Work may span multiple assistant interactions or require phased implementation
5. **Uncertainty**: Task requirements or scope are unclear and need structured exploration

Examples of task decomposition tasks:
- Complex feature implementations requiring both code and documentation
- Large-scale refactoring projects affecting multiple system components
- Multi-phase project rollouts with dependencies between phases
- Integration projects requiring coordination across different tools or platforms
- Research and planning tasks that inform subsequent implementation work

## Task Decomposition Steps

For tasks meeting the above criteria, follow this workflow:

1️⃣ **Identify Top-Level Task:**
   - Define the primary goal as a clear, verb-driven statement
   - Clarify the expected final output and success criteria with the user if necessary
   - Establish the scope and boundaries of what will and won't be included

2️⃣ **Break Down into Major Phases:**
   - Segment the task into 3-5 logical phases or major components
   - Follow a natural workflow progression (e.g., Research → Plan → Implement → Test → Document)
   - Ensure each phase has clear deliverables and can be evaluated independently

3️⃣ **Decompose to Atomic Subtasks:**
   - Iterate through each phase, breaking it down into specific, atomic actions
   - Ensure each subtask is achievable in a single reasoning step (1-5 minutes of focused work)
   - Use the hierarchical ID system (e.g., 1.1, 1.2, 2.1) to maintain clear parent-child relationships

4️⃣ **Annotate Each Subtask:**
   - Use the standardized template from the [Task Decomposition Guide](mdc:docs/task_decomposition.md):
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
   - Include appropriate status indicators for tracking progress

5️⃣ **Add Tags, Links and References:**
   - Add inline tags using the `#tag` format to categorize tasks and subtasks (see [Tag Conventions](mdc:meta/guidelines/tag_conventions.md))
   - Link directly to related files using MDC links (`mdc:path/to/file`)
   - Add cross-references to other tasks or sections within the document using anchor links
   - Include "Related" section at the top of each major task with key related resources

6️⃣ **Create Status Summary Table:**
   - Add a status summary table at the end of each major section or task breakdown
   - Include columns for task name, status, and completion percentage
   - Calculate overall project completion status for tracking progress
   - Follow the status tracking guidelines for consistency

7️⃣ **Document the Task Breakdown:**
   - For significant projects, create a dedicated task file in `meta/tasks/` directory
   - For smaller tasks, document the breakdown directly in conversation or relevant documentation
   - Add a reference to `meta/TODO.md` linking to the comprehensive task breakdown

8️⃣ **Execute and Track Progress:**
   - Begin execution following the hierarchical order, respecting dependencies
   - Update task status after completing each subtask
   - Document outputs as specified in the task breakdown
   - Update the status summary table as progress is made

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** If the task involved creating new files or significant directory restructuring, update [INDEX.md](mdc:INDEX.md) to reflect the current project structure. See [How to Update Index](mdc:docs/how_to_update_index.md).
   - **Validate Frontmatter:** Ensure proper YAML frontmatter follows [DSS Config](mdc:meta/dss_config.yml) standards for all created files.
   - **Check Links:** Verify all MDC links remain valid throughout the decomposition process.
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance on integrating task management with broader DSS workflows.

## Reference Materials

### Status Indicators
- `[NOT STARTED]` - Work has not yet begun
- `[IN PROGRESS]` - Work has started but is not complete
- `[BLOCKED]` - Cannot proceed due to dependencies or obstacles
- `[COMPLETED]` - Task has been finished and verified
- `[DEFERRED]` - Intentionally postponed to a later time

### Example Task Breakdown Document Structure

```markdown
# Task: {Task Name}

## Overview
Brief description of the overall task and goal.

## Task Status Legend
{Status indicator definitions}

## Task Breakdown

### 1. {Phase 1 Name} `[STATUS]` #{category_tag} #{priority_tag}
*Related: [Link to related resource](mdc:path/to/resource)*

#### 1.1. {Subtask Title} `[STATUS]` #{specific_tag}
- **Inputs**: {List of required inputs with links where applicable}
- **Outputs**: {List of expected outputs}
- **Dependencies**: {IDs of prerequisite subtasks}
- **Estimate**: {Time or complexity score}
- **Status**: {Brief status description}

## Task Status Summary
| Phase | Status | Completion |
|-------|--------|------------|
| 1. Phase 1 Name | STATUS | X% |
| **OVERALL** | **STATUS** | **X%** |
```

## Decision Points

If during execution you discover that:
- **Individual subtasks are primarily documentation-focused** → Apply [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md) workflow to those subtasks
- **Individual subtasks are primarily code-focused** → Apply [Code Modification](mdc:meta/assistant_workflows/code_modification.md) workflow to those subtasks
- **Subtasks are simple and self-contained** → Apply [Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md) workflow to those subtasks
- **Task scope is smaller than initially assessed** → Consider consolidating into a simpler workflow

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- **Step 3 (Categorize Task Type)**: Identifies complex, multi-step tasks through complexity and coordination criteria
- **Steps 5-8**: Implemented through the hierarchical breakdown process with special attention to structured decomposition and dependency management

## Integration with Other Workflows

### Related Workflows
- **[Code Modification](mdc:meta/assistant_workflows/code_modification.md)**: Apply to subtasks involving code changes
- **[Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)**: Apply to subtasks involving documentation creation
- **[Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)**: Apply to simple, atomic subtasks
- **[Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)**: Apply to subtasks involving coordinated documentation updates

### Transition Protocol
This workflow serves as a coordination layer for other workflows at the subtask level. When executing individual subtasks, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on applying the appropriate workflow for each subtask while maintaining overall task coherence.