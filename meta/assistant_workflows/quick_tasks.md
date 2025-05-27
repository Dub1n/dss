---
tags: [assistant_workflow, meta, efficiency, quick_tasks]
provides: [assistant_quick_tasks_workflow]
requires: [meta/assistant_guidelines/maintenance_checklist.md, .cursor/rules/assistant.mdc, meta/assistant_workflows/code_modification.md, meta/assistant_workflows/docs_driven_development.md, meta/assistant_workflows/workflow_transitions.md]
---

# Assistant Workflow: Quick Tasks

This document outlines a streamlined workflow for handling simple, atomic tasks that don't require the full complexity of other workflows. It's designed to improve efficiency while maintaining essential quality standards.

## When to Use Quick Tasks

A task can be considered "quick" and eligible for this lightweight workflow if it meets ALL of the following criteria:

1. **Scope**: The task is atomic and self-contained, requiring changes to at most 1-2 files
2. **Complexity**: The task can be completed in a single interaction with minimal cognitive load
3. **Risk**: The change has low potential for introducing errors or breaking existing functionality
4. **Dependencies**: The task has minimal or no dependencies on other pending changes
5. **Documentation Impact**: The change requires minimal updates to other documentation

Examples of quick tasks:
- Minor text corrections or formatting fixes
- Adding simple tags or metadata to existing files
- Small self-contained code fixes (e.g., fixing a typo in a variable name)
- Adding a single TODO item to tracking documents
- Creating a simple file from an existing template

## Quick Tasks Steps

For tasks meeting the above criteria, follow this streamlined workflow:

1️⃣ **Quick Assessment:**
   - Confirm the task meets all quick task criteria above
   - If the task turns out to be more complex during execution, transition to the appropriate full workflow

2️⃣ **Minimal Context Gathering:**
   - Read only the directly relevant files needed for the task
   - Limit context gathering to immediate dependencies and directly affected components

3️⃣ **Focused Execution:**
   - Implement the change with minimal tool calls and focused scope
   - Make changes only to the specific files that need modification
   - Avoid scope creep or additional "while I'm here" improvements

4️⃣ **Essential Maintenance:**
   - Perform only critical maintenance checks that are directly affected by the change
   - Ensure proper frontmatter is preserved/added if modifying markdown files
   - Add/update appropriate tags if applicable using [Tag Conventions](mdc:meta/guidelines/tag_conventions.md)
   - Ensure links remain valid if modifying linked content
   - **Prettify markdown tables:** If the file contains tables that were edited, run `meta/scripts/prettify_md.ps1 filename.md` to ensure consistent table formatting

5️⃣ **Quick Verification:**
   - Perform a quick check of the specific change for correctness
   - Verify that file format and structure remain consistent
   - Confirm the change achieves the intended outcome

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** Only if creating or deleting a file
   - **Validate Frontmatter:** When creating new files or substantially modifying frontmatter
   - **Check Links:** Only if modifying content that contains or is referenced by links
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance when uncertain

## Reference Materials

### Abbreviated Maintenance Checklist

This abbreviated checklist replaces the full [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for quick tasks:

| Maintenance Task | When to Perform in Quick Tasks |
|------------------|--------------------------------|
| Update INDEX.md | Only if creating/deleting a file |
| Add Frontmatter | Always for new files |
| Preserve Existing Frontmatter | Always when editing files |
| Validate Frontmatter | When creating new files or substantially modifying frontmatter |
| Update Task Management | Only if the task was explicitly tracked |
| Check Links | Only if modifying linked content |
| Documentation Updates | Only for the directly modified files |
| Git Operations | Commit after completion; push when appropriate |

### Git Operations for Quick Tasks

**Commit Changes:**
- Use concise but descriptive commit messages
- For tiny changes: `fix: correct typo in filename.md`
- For small features: `feat: add quick validation to script.py`

**When to Push:**
- Push immediately for urgent fixes explicitly requested by the user
- For routine changes, ask the user if they want to push now or later
- Always respect explicit user instructions about pushing

### Decision Tree: Full vs. Quick Workflow

Use this decision tree to determine whether to continue with Quick Tasks or transition:

1. **Does the task involve changes to more than 2 files?**
   - Yes → Transition to [Code Modification](mdc:meta/assistant_workflows/code_modification.md) or [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
   - No → Continue

2. **Does the task require complex reasoning or multiple steps?**
   - Yes → Transition to [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
   - No → Continue

3. **Does the task involve high-risk changes to core functionality?**
   - Yes → Transition to [Code Modification](mdc:meta/assistant_workflows/code_modification.md)
   - No → Continue

4. **Does the task require significant documentation updates?**
   - Yes → Transition to [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
   - No → Continue with Quick Tasks workflow

## Decision Points

If during execution you discover that:
- **Task affects more files than initially assessed** → Transition to [Code Modification](mdc:meta/assistant_workflows/code_modification.md) or [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
- **Task requires breaking down into subtasks** → Transition to [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
- **Task involves coordinated changes across multiple related files** → Transition to [Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)
- **Complexity is higher than initially thought** → Continue with Quick Tasks but allow more time and thorough verification

## Integration with Core Process

This lightweight workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc) by providing a streamlined path through the process:

- **Step 3 (Categorize Task Type)**: Uses strict ALL criteria to identify genuinely simple tasks
- **Step 5 (Plan & Cross-Reference)**: Simplified to confirming Quick Tasks workflow applies and identifying specific maintenance needs
- **Step 6 (Execute & Integrate)**: Focuses only on essential maintenance tasks directly affected by the change
- **Step 7 (Review & Verify)**: Limited to quick correctness check of the specific changes made

## Integration with Other Workflows

### Related Workflows
- **[Code Modification](mdc:meta/assistant_workflows/code_modification.md)**: Natural escalation for tasks affecting multiple files or requiring comprehensive changes
- **[Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)**: Use when documentation creation is needed
- **[Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)**: Use when complexity requires structured breakdown

### Transition Protocol
When transitioning from this workflow to a more comprehensive one, return to the Core Process Checklist and resume from step 3 with task recategorization. Refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on handling these transitions while preserving completed work. 