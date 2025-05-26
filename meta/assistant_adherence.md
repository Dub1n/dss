---
tags: [assistant_instructions, meta]
provides: [assistant_guideline_adherence]
requires: []
---

# Assistant Guideline Adherence Commitment

This document outlines the commitment and strategy for the AI assistant to ensure consistent adherence to the DSS operating instructions and broader guidelines.

To ensure consistent adherence to these operating instructions and the broader DSS guidelines, I commit to the following:

1.  **Structured Internal Process:** I will utilize a structured internal checklist or process, derived from these operating instructions ([.cursor/rules/assistant.mdc](.cursor/rules/assistant.mdc)) and the DSS Guide ([meta/DSS_GUIDE.md](meta/DSS_GUIDE.md)), to systematically evaluate user requests and planned actions against all relevant guidelines before proceeding. This process includes, but is not limited to, the following steps for each user prompt:
    *   **Understand Prompt:** Fully comprehend the user's request or instruction.
    *   **Gather Context:** Access and process relevant information from the current file, attached files, project structure ([INDEX.md](INDEX.md)), and conversation history.
    *   **Identify Applicable Guidelines:** Determine which instructions from `assistant.mdc`, the DSS Guide, and other relevant documentation (e.g., `meta/dss_config.yml`) are pertinent to the task.
    *   **Plan & Cross-Reference:** Develop a plan to address the prompt, explicitly cross-referencing necessary steps with detailed workflows (e.g., code modification, documentation generation) and maintenance tasks (e.g., updating TODOs ([meta/TODO.md](meta/TODO.md)), roadmap ([meta/roadmap.md](meta/roadmap.md)), frontmatter, links) as defined in the guidelines.
    *   **Execute & Integrate:** Perform planned actions (tool calls, text generation), ensuring that documentation updates and maintenance tasks are integrated into the execution flow.
    *   **Review & Verify:** Check the outcomes of actions against the prompt's requirements and applicable guidelines.
    *   **Respond:** Formulate a clear and comprehensive response to the user.

2.  **Contextual Guideline Activation:** I will actively recognize conversational triggers (keywords, phrases, or topics) that indicate the relevance of specific guidelines, workflows, or documentation files, even if not explicitly instructed to consult them. Upon recognizing such a trigger, I will incorporate the associated instructions into my planning and execution for the current prompt. Initial triggers include:
    *   Discussion of assistant capabilities or improvements: Consult `docs/brainstorming_assistant_dev.md`.
    *   Discussion of documentation structure or indexing: Consult `INDEX.md` and `docs/how_to_update_index.md`.
    *   Discussion of task tracking or project status: Consult `meta/TODO.md` and `meta/roadmap.md`.

3.  **Proactive Guideline Check:** Before generating a response or executing a tool call (especially file edits), I will perform an explicit internal check to identify all relevant instructions in `assistant.mdc` and other project documentation that apply to the user's request and the intended action.
4.  **Integrated Documentation Maintenance:** I will treat the update of relevant documentation files (e.g., `meta/TODO.md`, `meta/roadmap.md`) as an integral part of fulfilling the user's request, not as a separate, lower-priority task.
5.  **Reaction to Feedback:** I will use feedback from tool outputs (e.g., successful edits, rejected edits, command results) as triggers to revisit and potentially update relevant documentation or adjust my internal state according to the guidelines.
6.  **Handling Ambiguity:** In cases of uncertainty regarding guideline application or conflicting instructions, I will seek clarification (from the user or by consulting other DSS documentation) before acting and propose updates to `assistant.mdc` as necessary.
7.  **Prioritization of Core Documentation:** I will internally prioritize tasks related to maintaining the accuracy and integrity of core DSS documentation (`INDEX.md`, `meta/roadmap.md`, `meta/TODO.md`, `assistant.mdc`).