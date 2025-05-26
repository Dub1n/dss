---
tags: [documentation, ai_interaction, development]
provides: [assistant_development_brainstorming]
requires: [assistant.mdc]
---

# Brainstorming Future Development of assistant.mdc

This document serves as a space to brainstorm ideas, potential improvements, and new instructions for the `.cursor/rules/assistant.mdc` file. The goal is to continuously refine the AI assistant's capabilities and alignment with the DSS framework and development workflows.

## Initial Brainstorming Ideas

*   **More Granular Workflow Definitions:** Explore breaking down complex processes (e.g., adding a new feature, refactoring) into detailed, step-by-step instructions documented within `assistant.mdc` or linked guides.
*   **Specific Tool Usage Guidance:** Add explicit examples or preferred patterns for using specific tools (e.g., `grep_search`, `codebase_search`, `edit_file`) for common DSS tasks, ensuring efficient and DSS-aligned tool usage.
*   **Contextual Awareness Enhancement:** Develop instructions on how the AI should prioritize and integrate information from various DSS documentation sources (`dss-guide`, `automated_formatting`, `meta/dss_config.yml`, etc.) when making decisions or performing tasks.
*   **Proactive Task Identification:** Define guidelines that enable the AI to proactively identify potential tasks that should be added to `meta/TODO.md` based on observing user queries, analyzing code structure (if possible), or noticing inconsistencies.
*   **Refining Self-Correction Triggers:** Establish more specific criteria or provide examples of situations that should trigger the self-correction mechanism defined in `assistant.mdc`.
*   **Documentation Generation/Maintenance Rules:** Detail expected output formats, internal linking conventions, metadata requirements, and verification steps for generating or updating documentation.
*   **Interaction Style and Tone:** Further refine the expected interaction style, including how to ask clarifying questions effectively, propose alternative approaches, and provide clear explanations for actions.
*   **Integration with other meta scripts:** Instructions on when and how to suggest or automatically trigger other meta scripts (e.g., `meta/update_links.py`) as part of a workflow.

## Ideas from Interaction

*   Add ideas here as they arise during collaboration.
*   **Automated TODO Sorting:** Implement a script that reads `meta/TODO.md`, sorts tasks into 'Tasks' and 'Completed Tasks' sections based on the `[ ]` or `[x]` status, and rewrites the file. This would prevent manual formatting errors when moving completed items and could be automated via a pre-commit hook or similar. 
*   **Modularizing Assistant Instructions:** Discussed the idea of breaking down the main `assistant.mdc` file into smaller, dedicated files for specific workflows or guideline sets (e.g., a separate file for the guideline adherence commitment, as was done with `meta/assistant_adherence.md`). This aims to improve context clarity and maintainability. Potential benefits and challenges were considered. (See also: [meta/assistant_adherence.md](meta/assistant_adherence.md))
*   **Refining Guideline Adherence:** Explore ways to improve consistent application of guidelines, including:
    *   Adding explicit trigger conditions for maintenance tasks in the `maintenance_checklist.md`.
    *   Integrating relevant maintenance checks directly into workflow documents (e.g., `code_modification.md`).
    *   Adding guidance on prioritizing maintenance tasks or applying checks based on the type of user query.
    *   Refining guidance on handling ambiguity, outlining common ambiguous areas and preferred resolution strategies.

## Expand/integrate these where appropriate:
- [ ] Making it so that the DSS repo can be retrieved and/or updated by other repos, so that it can exist as one unified Documentation source for any number of repos, but without being stagnant;
    This main repo should include a way to easily apply any changes that are made to it to any other repo that follows DSS, e.g. if the yaml format is changed that can easily be updated with a script and automated.
    How much of this repo actually needs to be carried over/duplicated to other repos if it is always accessible? Is even the docs file needed if it can be easily called? Maybe a git retrieval and push automated system means that the files can be stored locally (outside of each repo) and push requests etc can be made by each separate repo as it uses DSS.
- [ ] Repos in DSS should be be able to interact with others for info retrieval: an LLM assistant based in a DSS repo should get data from the user's other DSS repos via some protocol/standard.
- [ ] This is definitely a template that should be able to host an LLM API agent so that it can function as the memory system for an AI Assistant.
    - [ ] API calls to other apps should be integrated, so that adding to calendar and other useful systems can be interacted with by the LLM