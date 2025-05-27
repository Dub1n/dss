---
tags: [assistant_workflow, meta, code, development]
provides: [assistant_code_modification_workflow]
requires: [meta/roadmap.md, docs/api_reference.md, canvas/architecture.canvas, meta/update_links.py, meta/assistant_workflows/task_decomposition.md, meta/assistant_guidelines/maintenance_checklist.md, .cursor/rules/assistant.mdc]
---

# Assistant Workflow: Code Modification

This document details the step-by-step process the AI assistant follows when adding or modifying code within the DSS repository.

## When to Use Code Modification

A task should use this workflow if it meets MOST of the following criteria:

1. **Primary Focus**: The task primarily involves creating, editing, or refactoring source code files
2. **API Impact**: Changes may affect public APIs, interfaces, or module boundaries
3. **Architecture Integration**: Code changes need to be reflected in system architecture documentation
4. **Testing Requirements**: Changes require corresponding updates to tests or validation
5. **Documentation Coupling**: Code modifications necessitate updates to technical documentation

Examples of code modification tasks:
- Implementing new functions or classes in existing modules
- Refactoring code structure while maintaining functionality
- Adding new features that extend the public API
- Fixing bugs that affect multiple code components
- Updating code to integrate with new dependencies or frameworks

## Code Modification Steps

For tasks meeting the above criteria, follow this workflow:

1️⃣ **Locate Documentation Context:**
   - Find and read any existing documentation stubs related to the code being modified
   - Review relevant sections in [API Reference](mdc:docs/api_reference.md)
   - Check [Architecture Canvas](mdc:canvas/architecture.canvas) for system context

2️⃣ **Update Documentation and Metadata:**
   - Insert or update YAML front-matter (`provides`, `requires`) following [DSS Config](mdc:meta/dss_config.yml)
   - Add appropriate tags following [Tag Conventions](mdc:meta/guidelines/tag_conventions.md)
   - Add short "Why/How" summary under `## Overview` section
   - Link to any new types/functions in existing documentation
   - **Prettify markdown tables:** If documentation files contain tables that were edited, run `meta/scripts/prettify_md.ps1 filename.md` to ensure consistent table formatting

3️⃣ **Handle Public API Changes:**
   - If creating new public API endpoints or interfaces, append entry in [API Reference](mdc:docs/api_reference.md)
   - Add corresponding visual elements (cards and arrows) in [Architecture Canvas](mdc:canvas/architecture.canvas)
   - Update any affected interface documentation

4️⃣ **Update Project Tracking:**
   - Update [Roadmap](mdc:meta/roadmap.md) – move relevant tickets from *Planned* → *In Progress* or mark as complete
   - Document progress and any scope changes encountered

5️⃣ **Validate and Link Check:**
   - Validate frontmatter using `meta/scripts/frontmatter_utils.py` guidelines for any created or modified files
   - Run `meta/update_links.py` script to fix any dead links created by the changes

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** If new files were created or existing files were significantly restructured, update [INDEX.md](mdc:INDEX.md). See [How to Update Index](mdc:docs/how_to_update_index.md).
   - **Validate Frontmatter:** Ensure proper YAML frontmatter follows [DSS Config](mdc:meta/dss_config.yml) standards.
   - **Check Links:** Verify all MDC links remain valid, especially after code structure changes.
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance.

## Reference Materials

### Git Operations Guidelines

#### When to Commit Changes
- Commit after meaningful, logically complete changes
- Use semantic commit messages: `feat|fix|docs|style|refactor|test|chore: <description>`
- Include both code changes and related documentation/metadata updates in the same commit
- Example: `feat: add user authentication | docs+meta auto-update`

#### When to Push Changes
- ✅ Push when a logical unit of work is complete
- ✅ Push when changes have been tested (if applicable)
- ✅ Push when working in a personal branch or fork
- ✅ Always push when explicitly requested by the user
- ❌ Don't push work-in-progress code unless specifically requested
- ❌ Don't push if tests are failing or missing where required
- ❌ Exercise caution when pushing to shared development or main branches

#### Git Operation Process
1. Stage changes: `git add <files>`
2. Commit with semantic message: `git commit -m "<type>: <description>"`
3. Push when appropriate: `git push`
4. Inform user of completed Git operations

## Decision Points

If during execution you discover that:
- **Task affects more than 5 files or requires complex coordination** → Transition to [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
- **Primary focus shifts to creating new documentation** → Transition to [Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)
- **Task is simpler than initially assessed** → Transition to [Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)
- **Task requires systematic documentation updates across multiple files** → Transition to [Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- **Step 3 (Categorize Task Type)**: Identifies code-focused tasks through criteria assessment
- **Steps 5-8**: Implemented through the detailed workflow steps with emphasis on documentation coupling and architecture integration

## Integration with Other Workflows

### Related Workflows
- **[Docs-Driven Development](mdc:meta/assistant_workflows/docs_driven_development.md)**: Use when starting with documentation before implementing code
- **[Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)**: Use for complex implementations requiring structured breakdown
- **[Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)**: Use for simple, isolated code fixes

### Transition Protocol
When transitioning from this workflow to others, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on preserving context and maintaining continuity. 