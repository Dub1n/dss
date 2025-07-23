# Notes

## General

- [ ] What rule/rules/change to the current rules would enable non-thinking models to break down their approach to responses in the same way that a thinking model would?

- [ ] What rule/change to the rules would be best to enable a lower quality model (gpt-4o compared to claude-4) to work and follow DSS as efficiently as a better model?

- [ ] Sometimes need to tell the agent to update relevant files that need updating for the changes to work at all, e.g. adding a new module but not including it in any workflow files or referenced anywhere else.
    This is probably due to not having enough useful frontmatter/stubs, such as "this file's - is refrences by that file's -" or "this file is executed during - in - and needs details for how to do so to be included there". In what ways can this issue be addressed?

## Formatting

- [ ] Should only mdc files have mdc: links? It is the only file format that supports them for the user both functionally and aesthetically and makes integration into other apps easier.

- [ ] template for filetrees - do they use links or not? do they show items in folders? one deep, two deep? This should be its own template file but be referenced by any template that has filetrees (unless the ones needed for that file would differ from the standard one)

- [ ] should we migrate to kebab case? which is better for LLMs? kebab-case is more readable, and either is fine for filenames

- [ ] Need to update the markdown rules file so it meets the linter's requirements: check what the linter's requirements are (and which are excluded/changed in the user settings.json) and specify that in the file. Also as a custom rule, every time text is in [**] and has a : at the end, the : should come before the [**] rather than after, e.g. [**Rules:**] rather than [**Rules**:] (same goes for using just one * )

- [ ] In .mdc files the frontmatter needs to be formatted (This info should be included in the rules template):

```text
---
description: When and What
globs: 
alwaysApply: true/false
---
---
tags: [tags]
provides: [provides]
requires: [requires]
---
```

- [ ] The cursor assistant might actually be ignoring the yaml frontmatter as it could see it as a comment to be ignored. This needs to be looked into and addressed; if it can be fixed while keeping the format the same (like with a rules file) that would be ideal so that it can still function perfectly in Obsidian, but if it needs adjusting that would be a necessary change.

## Further Development

- [ ] The dev_output_table file table should put the files from different folders together with a separator between the sections: the separator should be a row with the name of the folder in the File column and the remaining cells blank.
The other project files in dev should be updated to have the status and priority labels in their frontmatter

- [ ] Making it so that the DSS repo can be retrieved and/or updated by other repos, so that it can exist as one unified Documentation source for any number of repos, but without being stagnant;
    This main repo should include a way to easily apply any changes that are made to it to any other repo that follows DSS, e.g. if the yaml format is changed that can easily be updated with a script and automated.

- [ ] Repos in DSS should be be able to interact with others for info retrieval: an LLM assistant based in a DSS repo should get data from the user's other DSS repos via some protocol/standard.

## Implementation Assistant Prompts

The following prompts can be used to guide an AI assistant through implementing the tasks and experiments mentioned in this notes file:

0.
    > _**General Improvements**_

1. **Analysis of Model Response Structuring**:
   "Analyze the differences in how thinking and non-thinking models structure their responses to complex development tasks. Identify specific patterns that could be formalized into rules or templates to guide non-thinking models to break down problems systematically. Create a document in `dev/ideas/model_response_patterns.md` with your findings and recommendations for rule improvements."

2. **Cross-Model Compatibility Rules**:
   "Review the current DSS rules and identify areas where lower-capability models (like GPT-4o compared to Claude-4) might struggle to follow the guidelines effectively. Create a document in `dev/ideas/cross_model_compatibility.md` with specific rule modifications or additions that would improve performance consistency across different model capabilities."

3. **Dependency Tracking Enhancement**:
   "Design an enhanced frontmatter system that explicitly tracks file dependencies and references between components. Implement a proof-of-concept in `meta/scripts/lib/dependency_tracker.py` that can analyze a repository, detect implicit dependencies, and suggest frontmatter updates to make these relationships explicit."

    > _**Formatting Improvements**_

4. **MDC Link Policy Analysis**:
   "Analyze the pros and cons of restricting mdc: links to only .mdc files versus allowing them in all markdown files. Consider impacts on tool integration, user experience, and markdown compatibility. Create a recommendation document in `docs/reference/mdc_link_policy.md` with a clear policy statement and implementation plan."

5. **Filetree Template Creation**:
   "Create a standardized template for file tree representations in documentation at `meta/templates/docs/filetree_template.md`. Include options for different depth levels, link inclusion policies, and formatting standards. Ensure the template has clear usage instructions and examples."

6. **Kebab Case Migration Plan**:
   "Evaluate the benefits of migrating to kebab-case for filenames and directory names. Research LLM-specific benefits and create a migration plan in `dev/ideas/kebab_case_migration.md` including tooling for automated conversion, compatibility considerations, and a phased implementation strategy."

7. **Markdown Linting Rules Update**:
   "Analyze the current markdown linting requirements and create an updated ruleset in `meta/config/markdown_lint_rules.json`. Include specific rules for formatting headings with colons (e.g., [**Rules:**] instead of [**Rules**:]) and update related documentation to reflect these standards."

8. **MDC Frontmatter Structure Standardization**:
   "Create a comprehensive guide for MDC file frontmatter structure in `docs/reference/mdc_frontmatter_standard.md`. Include the dual frontmatter format with clear examples, validation rules, and integration guidance for both Cursor and Obsidian compatibility."

9. **Cursor YAML Frontmatter Recognition Analysis**:
   "Investigate why Cursor might be ignoring YAML frontmatter in MDC files. Test various formatting approaches to determine what works reliably, and document your findings in `dev/ideas/cursor_frontmatter_compatibility.md`. Include recommended solutions that maintain cross-tool compatibility."

    > _**Further Development**_

10. **Development Output Table Enhancement**:
    "Implement the enhanced table format for dev_output_table files that organizes files by folder with separator rows. Create an example implementation in `dev/examples/enhanced_output_table.md` and update any related processing scripts to support this format."

11. **DSS Repository Synchronization System**:
    "Design a system for synchronizing DSS standards across multiple repositories. Create a specification document in `dev/ideas/dss_sync_system.md` that outlines the synchronization mechanism, version handling, conflict resolution, and automated updating of DSS components."

12. **Cross-Repository Information Exchange Protocol**:
    "Design a protocol for DSS repositories to exchange information and context. Create a specification in `dev/ideas/cross_repo_exchange.md` that outlines the data exchange format, authentication mechanism, privacy considerations, and integration with LLM assistants."

    > _**Experimental Features**_

13. **Bidirectional Reference Tracking**:
    "Implement an experimental bidirectional reference tracking system in `meta/scripts/experimental/reference_tracker.py` that automatically maintains 'referenced-by' relationships in frontmatter when 'requires' relationships are created or modified."

14. **Automatic Dependency Inference**:
    "Create a proof-of-concept tool in `meta/scripts/experimental/dependency_inference.py` that analyzes code and documentation to automatically infer and suggest missing dependency relationships based on content analysis and reference patterns."

15. **Dynamic Rule Activation System**:
    "Design and implement a prototype for dynamic rule activation in `meta/scripts/experimental/dynamic_rules.py` that can selectively load and apply DSS rules based on context, file type, or explicit user guidance rather than loading all rules at once."

Each of these prompts should be approached using the Code Modification workflow from the DSS guidelines, including thorough analysis, implementation with proper testing, documentation updates, and validation of dependencies and cross-references.
