---
tags: [assistant_workflow, meta, integration, transitions]
provides: [assistant_workflow_transitions]
requires: [meta/assistant_workflows/code_modification.md, meta/assistant_workflows/docs_driven_development.md, meta/assistant_workflows/task_decomposition.md, meta/assistant_workflows/quick_tasks.md, meta/assistant_workflows/documentation_refactoring.md, meta/assistant_guidelines/status_tracking.md, .cursor/rules/assistant.mdc]
---

# Assistant Workflow: Cross-Workflow Transition Protocol

This document outlines how to smoothly transition between different assistant workflows while preserving context and maintaining consistency. It provides guidelines for determining when to transition, how to preserve context during transitions, and how to ensure continuity in the assistant's operations.

## When to Use Cross-Workflow Transitions

This transition protocol should be used when ANY of the following criteria are met:

1. **Workflow Mismatch**: Current task no longer fits the criteria of the workflow being used
2. **Scope Change**: Task scope expands or contracts beyond the current workflow's intended range
3. **Complexity Evolution**: Task reveals itself to be more or less complex than initially assessed
4. **Multi-Workflow Requirements**: Task requires coordinated application of multiple different workflows
5. **Error Recovery**: Need to correct an initial workflow selection that proved inappropriate

Examples of transition scenarios:
- Quick task revealing complexity requiring code modification workflow
- Documentation task requiring significant code implementation
- Simple task expanding into multi-phase project needing decomposition
- Complex task breaking down into simpler atomic subtasks
- Error correction when wrong workflow was initially selected

## Cross-Workflow Transition Steps

When transitioning between workflows, follow this protocol:

1️⃣ **Document Current State:**
   - Record the current state of the task, including status indicators and progress made
   - Summarize decisions taken and any outstanding questions or ambiguities
   - Note specific work products or outputs already created

2️⃣ **Assess Transition Need:**
   - Clearly identify why the current workflow is no longer appropriate
   - Determine which target workflow better fits the evolved task requirements
   - Evaluate whether transition preserves or enhances overall efficiency

3️⃣ **Preserve Essential Context:**
   - Carry forward all essential context elements using the preservation guidelines
   - Ensure task goals, user requirements, and key decisions remain clear
   - Maintain awareness of all files and dependencies involved in the task

4️⃣ **Execute Transition:**
   - Explicitly announce the workflow transition with clear rationale
   - Begin following the target workflow from its appropriate entry point
   - Apply target workflow criteria to confirm the transition is appropriate

5️⃣ **Update Documentation:**
   - Update any task tracking documents to reflect the workflow change
   - Add references to relevant documentation from the new workflow
   - Maintain links between related tasks across workflow boundaries

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** If the transition involves creating new files or changing the project structure, update [INDEX.md](mdc:INDEX.md) to reflect any changes. See [How to Update Index](mdc:docs/how_to_update_index.md).
   - **Validate Frontmatter:** Ensure proper YAML frontmatter follows [DSS Config](mdc:meta/dss_config.yml) standards across all workflows.
   - **Check Links:** Verify all MDC links remain valid during workflow transitions.
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance.

## Reference Materials

### Workflow Relationship Map

The DSS Assistant operates with core workflows that frequently interact:

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

### Context Preservation Guidelines

| Context Element | How to Preserve |
|-----------------|-----------------|
| Task Goals | Explicitly restate the overall goal at the beginning of the new workflow |
| User Requirements | Summarize key requirements that must be satisfied |
| Progress Status | Use consistent status tracking across workflows |
| Key Decisions | Note important decisions made that affect the current work |
| Related Files | Maintain awareness of all files involved in the task |
| Dependencies | Track dependencies between tasks across workflow boundaries |

### Transition Decision Trees

#### From Quick Tasks Workflow

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

#### From Code Modification Workflow

```
Is the code change revealing larger complexity?
├── YES → Transition to Task Decomposition Workflow
└── NO → Is significant documentation needed?
         ├── YES → Transition to Docs-Driven Development
         └── NO → Continue with Code Modification Workflow
```

#### From Docs-Driven Development

```
Does the documentation reveal the need for significant code changes?
├── YES → Is the implementation complex?
│         ├── YES → Transition to Task Decomposition, then Code Modification
│         └── NO → Transition directly to Code Modification
└── NO → Continue with Docs-Driven Development
```

#### From Task Decomposition

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

#### From Documentation Refactoring

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

## Decision Points

If during any workflow you discover that:
- **Task complexity has fundamentally changed** → Assess against all workflow criteria and transition to the most appropriate one
- **Multiple workflow types are needed** → Transition to Task Decomposition to coordinate different workflow applications
- **Current workflow feels inefficient or wrong** → Stop and reassess using the decision trees above
- **User requirements have shifted** → Document the change and reassess workflow appropriateness

## Practical Examples

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

## Integration with Core Process

This transition protocol integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc) in the following ways:

- **Step 3 (Categorize Task Type)**: Provides detailed guidance on selecting the appropriate workflow and recognizing when recategorization is needed
- **Step 5 (Plan & Cross-Reference)**: Offers structured approach to transitions when multiple workflows are needed
- **Step 6 (Execute & Integrate)**: Ensures context is preserved during workflow changes and transitions are handled smoothly

## Integration with Other Workflows

### Related Workflows
- **[Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)**: Most common starting point for simple tasks that may need escalation
- **[Code Modification](mdc:meta/assistant_workflows/code_modification.md)**: Frequent transition target for tasks requiring code changes
- **[Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)**: Common transition for tasks requiring documentation creation
- **[Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)**: Coordination workflow when multiple other workflows are needed
- **[Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)**: Specialized workflow for multi-file documentation updates

### Implementation Guidelines
1. **Be Explicit**: Always explicitly announce a workflow transition to maintain clarity
2. **Document Transitions**: Record workflow transitions in task documentation
3. **Preserve Progress**: Ensure no progress or context is lost during transitions
4. **Avoid Churn**: Don't transition unnecessarily - only when the current workflow is clearly insufficient
5. **Complete Cycles**: When possible, complete the current workflow cycle before transitioning 