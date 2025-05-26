---
tags: [assistant_workflow, meta, integration]
provides: [assistant_workflow_transitions]
requires: [meta/assistant_workflows/code_modification.md, meta/assistant_workflows/docs_driven_development.md, meta/assistant_workflows/task_decomposition.md, meta/assistant_workflows/quick_tasks.md, meta/assistant_workflows/documentation_refactoring.md, meta/assistant_guidelines/status_tracking.md]
---

# Assistant Workflow: Cross-Workflow Transition Protocol

This document outlines how to smoothly transition between different assistant workflows while preserving context and maintaining consistency. It provides guidelines for determining when to transition, how to preserve context during transitions, and how to ensure continuity in the assistant's operations.

## Workflow Relationship Map

The DSS Assistant operates with the following core workflows that frequently interact:

```
┌───────────────────────┐       ┌───────────────────────┐
│                       │       │                       │
│  Task Decomposition   │◄─────►│  Code Modification    │
│                       │       │                       │
└───────────┬───────────┘       └───────────┬───────────┘
            │                               │
            │                               │
            ▼                               ▼
┌───────────────────────┐       ┌───────────────────────┐
│                       │       │                       │
│  Docs-Driven          │◄─────►│  Quick Tasks          │
│  Development          │       │                       │
│                       │       │                       │
└───────────┬───────────┘       └───────────────────────┘
            │
            │
            ▼
┌───────────────────────┐
│                       │
│  Documentation        │
│  Refactoring          │
│                       │
└───────────────────────┘
```

### Primary Transition Scenarios

1. **Task Decomposition → Specific Workflow**: When a complex task is broken down into atomic subtasks, each subtask may require a different workflow.

2. **Quick Tasks → Full Workflow**: When a task initially thought to be simple turns out to be more complex than anticipated.

3. **Code Modification ↔ Docs-Driven Development**: When code changes reveal the need for documentation updates or vice versa.

4. **Any Workflow → Task Decomposition**: When any task reveals itself to be more complex than initially thought and requires structured breakdown.

## Context Preservation Protocol

When transitioning between workflows, follow these steps to preserve context:

### 1. Document Current State

Before transitioning:
- Document the current state of the task, including [status indicators](mdc:meta/assistant_guidelines/status_tracking.md)
- Summarize progress made and decisions taken
- Note any outstanding questions or ambiguities

### 2. Carry Forward Essential Context

The following context must be carried forward during any transition:

| Context Element | How to Preserve |
|-----------------|-----------------|
| Task Goals | Explicitly restate the overall goal at the beginning of the new workflow |
| User Requirements | Summarize key requirements that must be satisfied |
| Progress Status | Use consistent [status tracking](mdc:meta/assistant_guidelines/status_tracking.md) across workflows |
| Key Decisions | Note important decisions made that affect the current work |
| Related Files | Maintain awareness of all files involved in the task |
| Dependencies | Track dependencies between tasks across workflow boundaries |

### 3. Update References

When transitioning:
- Update any task tracking documents to reflect the workflow change
- Add references to relevant documentation from the new workflow
- Maintain links between related tasks in different workflows

## Transition Decision Trees

Use these decision trees to determine when to transition between workflows.

### From Quick Tasks Workflow

```
Is the task more complex than initially thought?
├── YES → Does it require changes to multiple files or systems?
│         ├── YES → Transition to Code Modification Workflow
│         └── NO → Does it require significant documentation?
│                  ├── YES → Transition to Docs-Driven Development
│                  └── NO → Does it need to be broken into subtasks?
│                           ├── YES → Transition to Task Decomposition
│                           └── NO → Continue with Quick Tasks but allow more time
└── NO → Continue with Quick Tasks Workflow
```

### From Code Modification Workflow

```
Is the code change revealing larger complexity?
├── YES → Transition to Task Decomposition Workflow
└── NO → Is significant documentation needed?
         ├── YES → Transition to Docs-Driven Development
         └── NO → Continue with Code Modification Workflow
```

### From Docs-Driven Development

```
Does the documentation reveal the need for significant code changes?
├── YES → Is the implementation complex?
│         ├── YES → Transition to Task Decomposition, then Code Modification
│         └── NO → Transition directly to Code Modification
└── NO → Continue with Docs-Driven Development
```

### From Task Decomposition

```
For each atomic subtask:
├── Is it primarily a documentation task?
│   ├── YES → Apply Docs-Driven Development Workflow
│   └── NO → Continue
├── Is it primarily a code change?
│   ├── YES → Apply Code Modification Workflow
│   └── NO → Continue
└── Is it simple and self-contained?
    ├── YES → Apply Quick Tasks Workflow
    └── NO → Further decompose using Task Decomposition
```

### From Documentation Refactoring

```
Are code changes needed in addition to documentation updates?
├── YES → Is the implementation complex?
│         ├── YES → Transition to Task Decomposition
│         └── NO → Transition to Code Modification Workflow
└── NO → Is the documentation scope expanding significantly?
         ├── YES → Does it need to be broken into phases?
         │         ├── YES → Transition to Task Decomposition
         │         └── NO → Transition to Docs-Driven Development
         └── NO → Continue with Documentation Refactoring
```

## Practical Transition Examples

### Example 1: Quick Task → Code Modification

**Initial Task**: Fix a typo in a function name in `src/utils.py`

**Transition Trigger**: While examining the file, you discover the function is used in multiple places and fixing it requires coordinated changes across several files.

**Transition Actions**:
1. Document the current state: "Initial assessment as quick task was incorrect. Function is used in multiple places."
2. Transition to Code Modification workflow:
   ```
   I'm transitioning to the Code Modification workflow as this task affects multiple files.
   
   Current Status: [IN PROGRESS: 2024-08-17]
   Files affected:
   - src/utils.py (primary function definition)
   - src/services/data_processor.py (imports and uses the function)
   - tests/test_utils.py (tests the function)
   ```
3. Follow Code Modification workflow steps, preserving the original task goal

### Example 2: Docs-Driven Development → Task Decomposition

**Initial Task**: Create documentation for the authentication system

**Transition Trigger**: During documentation, you realize the authentication system is only partially implemented and requires significant development work.

**Transition Actions**:
1. Document findings: "Authentication system documentation reveals incomplete implementation."
2. Transition to Task Decomposition:
   ```
   This task requires breaking down into both documentation and implementation components.
   
   Current Status: [IN PROGRESS: 2024-08-17]
   Completed work:
   - Initial authentication flow documentation
   
   Remaining work requires decomposition into:
   - Complete documentation of existing features
   - Identify missing implementation components
   - Implement missing components
   - Update documentation to reflect final implementation
   ```
3. Apply Task Decomposition workflow to create a structured breakdown
4. For implementation subtasks, apply Code Modification workflow

### Example 3: Documentation Refactoring → Code Modification

**Initial Task**: Update terminology across documentation files to reflect new feature naming

**Transition Trigger**: While updating the documentation, you discover that the code itself still uses the old terminology and needs to be updated for consistency.

**Transition Actions**:
1. Document the current state: "Documentation updates are partially complete, but code needs corresponding changes."
2. Transition to Code Modification workflow:
   ```
   I'm transitioning to the Code Modification workflow as terminology changes must be reflected in code.
   
   Current Status: [IN PROGRESS: 2024-08-17]
   Completed work:
   - Updated terminology in 5 documentation files
   
   Remaining work:
   - Update terminology in src/core/models.py
   - Update terminology in src/utils/constants.py
   - Update unit tests to reflect new terminology
   - Complete remaining documentation updates
   ```
3. Follow Code Modification workflow steps, preserving the progress made in documentation updates

## Implementation Guidelines

1. **Be Explicit**: Always explicitly announce a workflow transition to maintain clarity
2. **Document Transitions**: Record workflow transitions in task documentation
3. **Preserve Progress**: Ensure no progress or context is lost during transitions
4. **Avoid Churn**: Don't transition unnecessarily - only when the current workflow is clearly insufficient
5. **Complete Cycles**: When possible, complete the current workflow cycle before transitioning

## Integration with Status Tracking

Workflow transitions should be recorded as part of the task's status history:

```markdown
**Status Update [2024-08-17]**: Transitioning from Quick Tasks to Code Modification workflow due to increased scope. Task status: [IN PROGRESS]
```

For complex tasks using the Task Decomposition workflow, record transitions at the subtask level in the status summary table:

```markdown
| Task | Status | Workflow | Started | Completed | Progress |
|------|--------|----------|---------|-----------|----------|
| 1.1. Subtask | COMPLETED | Quick Tasks | 2024-08-17 | 2024-08-17 | 100% |
| 1.2. Subtask | IN PROGRESS | Code Modification | 2024-08-17 | - | 50% |
| 1.3. Subtask | NOT STARTED | Docs-Driven | - | - | 0% |
```

## Integration with Core Process

The transition protocol integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc) in the following ways:

- It extends step 3 (**Categorize Task Type**) by providing detailed guidance on selecting the appropriate workflow
- It supplements step 5 (**Plan & Cross-Reference**) by offering a structured approach to transitions when multiple workflows are needed
- It informs step 6 (**Execute & Integrate**) by ensuring context is preserved during workflow changes 