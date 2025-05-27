---
tags: [assistant_workflow, meta, documentation, docs_first]
provides: [assistant_docs_driven_workflow]
requires: [INDEX.md, meta/assistant_guidelines/maintenance_checklist.md, meta/dss_config.yml, meta/assistant_workflows/task_decomposition.md, meta/templates/README.md, .cursor/rules/assistant.mdc]
---

# Assistant Workflow: Docs-Driven Development

This document outlines the workflow the AI assistant follows when starting the development process by creating documentation first, then optionally implementing corresponding code.

## When to Use Docs-Driven Development

A task should use this workflow if it meets MOST of the following criteria:

1. **Documentation Focus**: The primary deliverable is new documentation (concepts, guides, specifications)
2. **Planning Requirement**: The task benefits from thorough planning and specification before implementation
3. **Communication Need**: Documentation will help clarify requirements or design decisions with stakeholders
4. **Implementation Uncertainty**: Code implementation details are unclear and documentation will help define them
5. **Template Availability**: Appropriate templates exist that would accelerate documentation creation

Examples of docs-driven development tasks:
- Creating comprehensive feature specifications before development
- Writing integration guides for new tool compatibility
- Developing API documentation that will guide implementation
- Creating workflow documentation for new assistant processes
- Planning complex features through detailed design documents

## Docs-Driven Development Steps

For tasks meeting the above criteria, follow this workflow:

1️⃣ **Create New Documentation File:**
   - Create the new `.md` file (or other appropriate documentation format) in the relevant directory (e.g., `/docs/`, `/meta/`)
   - Always check [meta/templates/](mdc:meta/templates/) for appropriate templates before starting:
     - For integration documentation: Use [Integration Template](mdc:meta/templates/meta/integration_template.md)
     - For assistant workflows: Use [Assistant Workflow Template](mdc:meta/templates/meta/assistant_workflow_template.md)
     - For other file types: Check [Templates Overview](mdc:meta/templates/README.md) for available options

2️⃣ **Add Initial Structure & Frontmatter:**
   - Add the basic section structure and initial content using the selected template
   - Add required YAML frontmatter stub (`tags`, `provides`, `requires`) based on [DSS Config](mdc:meta/dss_config.yml)
   - Follow [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) when selecting appropriate tags
   - Replace template placeholders with specific values relevant to your task

3️⃣ **Develop Comprehensive Content:**
   - Flesh out the detailed content of the documentation, including explanations, examples, and specifications
   - Add cross-references and links to other relevant documents or code using MDC format
   - Include practical examples, use cases, or implementation guidance where appropriate
   - Ensure content follows DSS documentation standards and conventions
   - **Prettify markdown tables:** If the documentation contains tables, run `meta/scripts/prettify_md.ps1 filename.md` to ensure consistent table formatting

4️⃣ **Generate Code Stubs (Optional):**
   - If applicable, generate initial code stubs in the `/src/` directory based on the documentation
   - Ensure code stubs include proper frontmatter and follow DSS conventions
   - Link documentation to code stubs using appropriate MDC references

5️⃣ **Refine and Integrate:**
   - Review documentation for completeness, clarity, and accuracy
   - Continue refining both documentation and any generated code
   - For subsequent code changes, potentially transition to [Code Modification Workflow](mdc:meta/assistant_workflows/code_modification.md)

🔧 **DSS Maintenance Integration:**
   - **Update INDEX.md:** Add the new documentation file to [INDEX.md](mdc:INDEX.md) with an appropriate description and categorization. See [How to Update Index](mdc:docs/how_to_update_index.md).
   - **Validate Frontmatter:** Ensure proper YAML frontmatter follows [DSS Config](mdc:meta/dss_config.yml) standards.
   - **Check Links:** Verify all MDC links remain valid and point to existing files.
   - **Consult Checklist:** Reference [Maintenance Checklist](mdc:meta/assistant_guidelines/maintenance_checklist.md) for comprehensive guidance.

## Decision Points

If during execution you discover that:
- **Task requires significant code implementation beyond documentation scope** → Transition to [Code Modification](mdc:meta/assistant_workflows/code_modification.md)
- **Task is more complex and needs structured breakdown** → Transition to [Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)
- **Task is simpler than initially assessed** → Transition to [Quick Tasks](mdc:meta/assistant_workflows/quick_tasks.md)
- **Task requires coordinated updates across existing documentation** → Transition to [Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)

## Integration with Core Process

This workflow integrates with the [Core Process Checklist](mdc:.cursor/rules/assistant.mdc):

- **Step 3 (Categorize Task Type)**: Identifies documentation-first tasks through criteria assessment and template availability
- **Steps 5-8**: Implemented through the detailed workflow steps with emphasis on template usage and comprehensive content development

## Integration with Other Workflows

### Related Workflows
- **[Code Modification](mdc:meta/assistant_workflows/code_modification.md)**: Natural transition when moving from documentation to implementation
- **[Task Decomposition](mdc:meta/assistant_workflows/task_decomposition.md)**: Use for complex documentation projects requiring structured breakdown
- **[Documentation Refactoring](mdc:meta/assistant_workflows/documentation_refactoring.md)**: Use when updating existing documentation systematically

### Transition Protocol
When transitioning from this workflow to others, refer to [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md) for guidance on preserving context and maintaining continuity. 