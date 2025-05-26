---
tags: [assistant_guidelines, meta, status_tracking, transparency]
provides: [assistant_status_tracking_system]
requires: [meta/assistant_workflows/task_decomposition.md, meta/assistant_workflows/quick_tasks.md]
---

# Assistant Guidelines: Standardized Status Tracking System

This document outlines a consistent system for tracking the status of tasks, subtasks, and processes across all assistant workflows. It provides clear definitions, visualization methods, and timestamp protocols to improve transparency and progress tracking.

## Universal Status Indicators

The following standardized status indicators should be used consistently across all workflows and documentation:

| Status | Symbol | Definition | When to Use |
|--------|--------|------------|-------------|
| **Not Started** | `[NOT STARTED]` | Work has not yet begun | For tasks that have been identified but no work has been initiated |
| **In Progress** | `[IN PROGRESS]` | Work has started but is not complete | For tasks where active work is underway |
| **Blocked** | `[BLOCKED: reason]` | Cannot proceed due to dependencies or obstacles | For tasks that cannot move forward; always include a brief reason |
| **Completed** | `[COMPLETED]` | Task has been finished and verified | For tasks that are fully completed with no further work needed |
| **Deferred** | `[DEFERRED: date]` | Intentionally postponed to a later time | For tasks that have been deliberately delayed; include target date when known |
| **Needs Review** | `[NEEDS REVIEW]` | Work is done but requires verification | For tasks that are provisionally complete but need validation |
| **Failed** | `[FAILED: reason]` | Attempted but unsuccessful | For tasks that were attempted but could not be completed; include reason |

## Timestamp Protocol

To improve tracking and provide better context on progress, timestamps should be included at key status transition points:

1. **Format**: Use ISO 8601 format (YYYY-MM-DD) for all timestamps
2. **Required Timestamps**:
   - When a task transitions to `[IN PROGRESS]`: `[IN PROGRESS: 2024-08-15]`
   - When a task is `[COMPLETED]`: `[COMPLETED: 2024-08-15]`
   - When a task is `[DEFERRED]`: `[DEFERRED: 2024-08-15 → 2024-09-01]` (including target date when known)
   - When a task is `[BLOCKED]`: `[BLOCKED: 2024-08-15: dependency X not ready]`

3. **Omitted Timestamps**: 
   - For `[NOT STARTED]` tasks, timestamps are not required

## Status Visualization Methods

### Progress Tables

For complex tasks with multiple subtasks, include a status summary table:

```markdown
| Task | Status | Started | Completed | Progress |
|------|--------|---------|-----------|----------|
| 1. Task Name | IN PROGRESS | 2024-08-15 | - | 60% |
| 1.1. Subtask | COMPLETED | 2024-08-15 | 2024-08-15 | 100% |
| 1.2. Subtask | IN PROGRESS | 2024-08-15 | - | 50% |
| 1.3. Subtask | NOT STARTED | - | - | 0% |
| **OVERALL** | **IN PROGRESS** | **2024-08-15** | **-** | **40%** |
```

Calculate progress percentages as follows:
- For atomic tasks: 0% (Not Started), 50% (In Progress), 100% (Completed)
- For complex tasks: Average of subtask percentages
- For blocked tasks: Use the current percentage and note the blocked state

### Inline Status Updates

For inline status updates within documentation or comments:

```markdown
**Status Update [2024-08-15]**: Task is [IN PROGRESS] with subtasks 1 and 2 [COMPLETED] 
and subtask 3 [BLOCKED: waiting for external API documentation].
```

## Integration with Workflows

### Task Decomposition Workflow

When using the [Task Decomposition Workflow](mdc:meta/assistant_workflows/task_decomposition.md):
- Apply status indicators to both main tasks and all subtasks
- Include the status summary table at the end of each major task section
- Update status indicators and timestamps whenever a task's status changes

### Quick Tasks Workflow

When using the [Quick Tasks Workflow](mdc:meta/assistant_workflows/quick_tasks.md):
- Simplified tracking is appropriate
- At minimum, indicate whether the quick task is [COMPLETED] or [FAILED]
- For tasks that ended up being more complex than expected, transition to the full status tracking system

### Other Workflows

For all other workflows:
- Apply status indicators to any task lists or steps that span multiple interactions
- Use inline status updates for progress reporting
- Ensure timestamps are included for key transitions

## Implementation Guidelines

1. **Consistency**: Always use the exact format of status indicators specified in this document
2. **Visibility**: Place status indicators prominently in headings or at the beginning of task descriptions
3. **Updating**: Update status indicators as soon as a status change occurs
4. **Documentation**: Include status summary tables in any document with multiple tasks or subtasks
5. **Transitions**: When transitioning between workflows, maintain consistent status tracking

## Examples

### Example: Task with Subtasks

```markdown
### 1. Implement Authentication System `[IN PROGRESS: 2024-08-15]` #feature #security
*Related: [Security Requirements](mdc:docs/security_requirements.md)*

#### 1.1. Design Authentication Flow `[COMPLETED: 2024-08-15]`
- **Inputs**: Security requirements, user stories
- **Outputs**: Authentication flow diagram
- **Dependencies**: None
- **Status**: Completed on 2024-08-15

#### 1.2. Implement Login API `[IN PROGRESS: 2024-08-16]`
- **Inputs**: Authentication flow from 1.1
- **Outputs**: Login API endpoints
- **Dependencies**: 1.1
- **Status**: Backend implementation complete, frontend integration in progress

#### 1.3. Implement User Registration `[BLOCKED: 2024-08-16: waiting for email service]`
- **Inputs**: Authentication flow from 1.1
- **Outputs**: User registration functionality
- **Dependencies**: 1.1
- **Status**: Blocked by email service availability

#### Status Summary

| Task | Status | Started | Completed | Progress |
|------|--------|---------|-----------|----------|
| 1.1. Design Authentication Flow | COMPLETED | 2024-08-15 | 2024-08-15 | 100% |
| 1.2. Implement Login API | IN PROGRESS | 2024-08-16 | - | 50% |
| 1.3. Implement User Registration | BLOCKED | - | - | 0% |
| **Overall Authentication System** | **IN PROGRESS** | **2024-08-15** | **-** | **50%** |
```

### Example: Status Update Comment

```markdown
<!-- 
Status Update [2024-08-16]: 
- Authentication System: [IN PROGRESS] (50%)
- User Management: [NOT STARTED]
- Permission System: [DEFERRED: 2024-08-16 → 2024-09-01] (waiting for authentication completion)
-->
``` 