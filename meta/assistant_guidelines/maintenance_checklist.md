---
tags: [assistant_guidelines, meta, maintenance]
provides: [assistant_maintenance_checklist]
requires: [meta/TODO.md, INDEX.md, meta/dss_config.yml, meta/roadmap.md, docs/automated_formatting, meta/assistant_guidelines/documentation_task_management.md, meta/guidelines/tag_conventions.md, meta/assistant_guidelines/installation_report_submission.md]
---

# Assistant Guidelines: Maintenance Checklist

This document serves as a checklist and reference for the key maintenance tasks the AI assistant should consider and integrate into its workflow whenever processing a user prompt that might require updates to the project's structure, documentation, or metadata. It includes explicit trigger conditions to help ensure consistent adherence.

These tasks are integral to ensuring the integrity, discoverability, and currentness of the DSS project.

## Key Maintenance Tasks & Triggers

-   **Task Management:**
    *   **Add New Tasks:** *Triggered when a potential task or improvement is identified during the conversation or analysis.* Add it to the 'Tasks' section of `meta/TODO.md`.
    *   **Mark Tasks as Completed (within interaction):** *Triggered immediately upon successfully completing a minor task within the current turn.* Mark it as `[x]` in the 'Tasks' section of `meta/TODO.md`.
    *   **Move Major Tasks to Completed:** *Triggered upon successfully completing a significant, multi-step, or user-requested task.* Move the `[x]` marked task from 'Tasks' to the 'Completed Tasks' section in `meta/TODO.md`.
    *   **Add Code Comments for TODOs:** *Triggered when a task in `meta/TODO.md` is directly related to a specific code location being discussed or modified.* Add a comment in the code referencing `meta/TODO.md` and the task.
    *   **Add Roadmap Links to TODOs:** *Triggered when reviewing `meta/TODO.md` tasks or when adding a new task that clearly aligns with a roadmap item.* Add `(@roadmap: [Section Name])` links where appropriate.

-   **Installation Report Submission:**
    *   **Guide GitHub Issue Submission:** *Triggered when a user mentions submitting installation reports, feedback, or GitHub issues.* Refer to the [Installation Report Submission Guidelines](mdc:meta/assistant_guidelines/installation_report_submission.md) to provide accurate guidance on the submission process with label validation.
    *   **Handle Label Errors:** *Triggered when a user reports label-related errors during GitHub issue submission.* Explain the label validation process and assure the user that the content is more important than the labels.
    *   **Recommend Script Updates:** *Triggered when troubleshooting installation report submission issues.* Check if the user has the latest version of the DSS Bootstrap script with label validation.

-   **Index Maintenance:**
    *   **Update INDEX.md:** *Triggered whenever a file is created, deleted, moved, or renamed, or when a significant new section or directory is added or removed.* Update `INDEX.md` to accurately reflect the current project structure.

-   **Frontmatter Management:**
    *   **Add Frontmatter Stubs:** *Triggered when a new `.md`, `.py`, or `.ipynb` file is created.* Add appropriate YAML (or triple-quoted) frontmatter stubs (`tags`, `provides`, `requires`) based on the rules in `meta/dss_config.yml` and following the guidelines in `meta/guidelines/tag_conventions.md`.
    *   **Add Appropriate Tags:** *Triggered when creating or modifying files.* Apply tags following the conventions in `meta/guidelines/tag_conventions.md`, including file type tags, purpose tags, status tags, and topic tags as appropriate.
    *   **Preserve Existing Frontmatter:** *Triggered whenever editing an existing file that already has frontmatter.* Ensure existing frontmatter is retained.
    *   **Validate Frontmatter:** *Triggered when creating or modifying files with frontmatter, or when frontmatter validation is explicitly requested.* Use the frontmatter validation tool (`meta/scripts/frontmatter_utils.py`) to ensure frontmatter adheres to validation rules defined in `meta/guidelines/validation_rules.md`. Fix any validation errors following the auto-correction logic in `meta/scripts/docs/frontmatter_auto_correction.md`.
    *   **Report Validation Issues:** *Triggered when frontmatter validation fails and cannot be automatically corrected.* Inform the user of the validation issues and suggest appropriate fixes.

-   **Link Validation:**
    *   **Check and Update Links:** *Triggered after any file is created, deleted, moved, or renamed, particularly if it's linked from other documents or contains links to other documents.* Ensure links, particularly `.mdc` links, are valid.

-   **Documentation Updates:**
    *   **Add Plans/Info to Docs:** *Triggered when a discussion reveals useful information, decisions, or plans not yet captured in relevant documentation files.* Automatically add this information to the appropriate file(s) (e.g., `meta/TODO.md`, `docs/automated_formatting`, `meta/roadmap.md`) without waiting for explicit confirmation unless the location is ambiguous.
    *   **Ensure Docs Reflect Current State:** *Ongoing check, part of gathering context and reviewing output, especially after code or structural changes.* Ensure documentation reflects the current design state and ignore archived content (`docs/🔒archive/`).

-   **Structure Preservation:**
    *   **Respect Folder Structure:** *Ongoing principle, applied whenever creating or moving files.* Adhere to the canonical folder structure defined in `docs/automated_formatting` and `meta/dss_config.yml`.

-   **Config Deference:**
    *   **Consult Config Files:** *Triggered when needing to understand file handling, metadata rules, or ignore patterns, especially when creating or processing files.* Refer to `meta/dss_config.yml` and other config files.
    *   **Follow Tag Conventions:** *Triggered when adding or modifying tags.* Adhere to the conventions defined in `meta/guidelines/tag_conventions.md` for consistency in tagging across the project.

-   **Self-Correction/Improvement:**
    *   **Identify Missed Guidelines:** *Triggered when reviewing performance, receiving user feedback, or encountering unexpected results.* Identify instances where guidelines were not fully followed.
    *   **Analyze Why Missed:** *Triggered after identifying a missed guideline.* Analyze the cause.
    *   **Implement Corrective Actions:** *Triggered after analyzing the cause of a missed guideline.* Implement actions, which may include updating the guidelines themselves.

## Prioritization and Contextual Guidance

While the trigger conditions indicate *when* a maintenance task is relevant, the following guidance helps determine the priority and how to apply the checks based on the context of the user's request and the ongoing interaction:

-   **High Priority (Must Do Now):** Tasks that have immediate impact on the project's integrity or the current interaction should be addressed promptly. This includes:
    *   Updating `INDEX.md` immediately after file creation, deletion, movement, or renaming to prevent broken links and ensure discoverability.
    *   Adding Frontmatter Stubs when creating new files, as this is a foundational aspect of DSS structure and metadata.
    *   Marking tasks as Completed (`[x]`) within the current interaction for minor tasks finished in a single turn, providing immediate feedback.

-   **Standard Priority (Integrate into Workflow):** Most maintenance tasks should be integrated seamlessly into the relevant workflows (Code Modification, Docs-Driven Development, etc.) as defined in the assistant workflow documents. These are triggered by actions within the workflow and should be performed as part of that process (e.g., adding tasks to TODO.md as they are identified during planning or execution).

-   **Lower Priority (Can Be Batched/Context Dependent):** Some tasks are less critical for the immediate interaction and can be batched or performed when specifically prompted or during natural breaks. This includes:
    *   Moving major completed tasks to the 'Completed Tasks' section in `meta/TODO.md` (can be done at the end of a major task or conversation segment).
    *   Adding Roadmap Links to TODOs (can be done during a review of `meta/TODO.md`).
    *   Comprehensive Link Validation across the entire codebase (can be a periodic task or performed when focusing on documentation integrity).
    *   Self-Correction/Improvement analysis (often occurs after a user points out an issue or during a self-review, not necessarily after every single interaction).

-   **Contextual Awareness:** Always consider the user's explicit focus and the type of query. If the user is specifically working on documentation, prioritize documentation-related maintenance tasks. If the user is focused on coding, prioritize code and structure-related maintenance tasks.

By applying this guidance, the AI assistant can ensure that maintenance tasks are not only triggered at the right time but also prioritized and performed in a manner that best supports the user's current goals and the overall project integrity. 

## Handling Ambiguity

Navigating the project and user requests may sometimes involve ambiguous situations. This section provides guidance on how to handle such cases to maintain progress while ensuring accuracy and alignment with DSS principles.

-   **Common Areas of Ambiguity:** Be aware of potential ambiguities, including:
    *   **File Classification:** Uncertainty about the correct directory (`/src/`, `/data/`, `/docs/`, etc.) for a new file or the appropriate `tags` for frontmatter based on `meta/dss_config.yml`.
    *   **Link Resolution:** Ambiguity when multiple files have similar names or when the target of a link is not immediately clear.
    *   **Instruction Interpretation:** User requests that are vague, contradictory, or could be interpreted in multiple ways.
    *   **Tool Usage:** Uncertainty about which tool is best suited for a specific task or how to best formulate a query (e.g., `grep_search` vs. `codebase_search`).

-   **Decision Framework:** When encountering ambiguity:
    *   **Prioritize Clarification:** If the ambiguity significantly impacts the ability to perform a task correctly or maintain project integrity (e.g., unsure where a critical file should go, uncertain about the user's core intent), **ask the user for clarification**. Explain the ambiguity and the options as you understand them.
    *   **Make Reasoned Assumptions (with Documentation):** If the ambiguity is minor and unlikely to cause significant issues, or if waiting for clarification would unduly block progress, you may make a reasoned assumption. However, you **must document the assumption** made, either in a comment in the affected file (referencing `meta/assistant_guidelines/maintenance_checklist.md`) or in the conversation summary, explaining why the assumption was made.

-   **Documenting Assumptions:** When making a reasoned assumption, clearly state:
    *   What the ambiguity was.
    *   What assumption was made.
    *   Briefly explain the reasoning behind the assumption.
    *   Suggest that the user review the change and provide feedback if the assumption was incorrect.

By actively identifying and appropriately handling ambiguity, the AI assistant can operate more effectively and collaboratively, minimizing errors and ensuring the user is informed about decisions made under uncertainty. 