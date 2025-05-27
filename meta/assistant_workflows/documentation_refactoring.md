---
tags: [assistant_workflow, meta, documentation, refactoring]
provides: [assistant_documentation_refactoring_workflow]
requires: [meta/assistant_guidelines/maintenance_checklist.md, .cursor/rules/assistant.mdc, meta/assistant_workflows/workflow_transitions.md, meta/dss_config.yml]
---

# Assistant Workflow: Documentation Refactoring

This document outlines a specialized workflow for systematically updating, improving, or restructuring existing documentation across multiple files. It's designed for tasks that require coordinated changes to documentation that don't involve creating new documentation from scratch or significant code modifications.

## When to Use Documentation Refactoring

A task should use this workflow if it meets MOST of the following criteria:

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

## Documentation Refactoring Steps

For tasks meeting the above criteria, follow this workflow:

1️⃣ **Analyze Documentation Structure:**
   - Identify all affected documentation files across the project
   - Understand the relationships and dependencies between the files
   - Map out how changes to one file will cascade to affect others
   - Review existing frontmatter and cross-references

2️⃣ **Plan Coordinated Changes:**
   - Create a clear, systematic plan for what changes are needed across all files
   - Establish patterns, templates, or standards for consistent changes
   - Identify any potential conflicts, dependencies, or breaking changes
   - Prioritize changes based on dependencies and impact

3️⃣ **Apply Changes Systematically:**
   - Make changes to one file at a time, following a logical dependency order
   - Ensure consistent formatting, terminology, and structure across all files
   - Preserve existing YAML frontmatter (`tags`, `provides`, `requires`) unless specifically updating metadata
   - Update frontmatter as needed to reflect new content relationships and dependencies

4️⃣ **Update Cross-References:**
   - Ensure all internal links between documents remain valid and accurate
   - Update any cross-references to reflect the new or modified content
   - Check external references for consistency and accuracy
   - Verify MDC links point to correct file paths
   - **Prettify markdown tables:** For any files containing tables that were edited, run `meta/scripts/prettify_md.ps1 filename.md` to ensure consistent table formatting

5️⃣ **Validate Documentation Integrity:**
   - Check for and fix any broken links introduced by the changes
   - Ensure consistent formatting and style across all updated files
   - Verify all files have appropriate and accurate frontmatter
   - Validate frontmatter using `meta/scripts/frontmatter_utils.py` guidelines

6️⃣ **Review for Consistency:**
   - Verify that changes are applied consistently across all affected files
   - Check that terminology, formatting, and structural patterns are uniform
   - Ensure the overall documentation coherence and flow is maintained
   - Confirm that the documentation set achieves the intended improvements

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** If documentation structure has changed significantly, update [INDEX.md](mdc:INDEX.md) to reflect new organization. See [How to Update Index](mdc:docs/how_to_update_index.md).
   - **Validate Frontmatter:** Ensure proper YAML frontmatter follows [DSS Config](mdc:meta/dss_config.yml) standards across all modified files.
   - **Check Links:** Verify all MDC links remain valid after restructuring or content changes.
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance.

## Decision Points

If during execution you discover that:
- **Task requires creating entirely new documentation from scratch** → Transition to [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
- **Task requires significant code changes to accompany documentation updates** → Transition to [Code Modification](mdc:meta/assistant_workflows/code_modification.md)
- **Task scope is much larger than anticipated and needs structured breakdown** → Transition to [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
- **Task affects only 1-2 files with minimal coordination needed** → Consider switching to [Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- **Step 3 (Categorize Task Type)**: Identifies documentation refactoring tasks through multi-file scope and coordination requirements
- **Steps 5-8**: Implemented through systematic planning and coordinated execution with emphasis on consistency and cross-reference integrity

## Integration with Other Workflows

### Related Workflows
- **[Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)**: Use for simple documentation changes affecting 1-2 files
- **[Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)**: Use when creating new documentation from scratch
- **[Code Modification](mdc:meta/assistant_workflows/code_modification.md)**: Use when documentation changes must be accompanied by significant code changes
- **[Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)**: Use for large-scale documentation restructuring requiring multiple phases

### Transition Protocol
When transitioning from this workflow to others, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on preserving completed work and maintaining continuity across the remaining tasks. 