---
tags: [assistant_guidelines, meta, principles]
provides: [assistant_overarching_principles]
requires: [meta/DSS_GUIDE.md, meta/guidelines/tag_conventions.md]
---

# Assistant Guidelines: Overarching Principles

This document outlines the fundamental principles and conventions that the AI assistant must adhere to within the Data SuperStructure (DSS) project.

Adhere to the DSS Guide and all documented conventions and instructions within the repository, including the [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) for consistent metadata application.

When working on a specific aspect of the project (e.g., a script, a function, a documentation section), the order of development steps should be determined by what would overall make the development process the easiest and quickest, provided it does not jeopardize other aspects of the repository or conflict with established DSS principles.

Apply appropriate tags to all files and tasks according to the established conventions, ensuring proper categorization and discoverability across the project.

**Long-running scripts should emit periodic output** (e.g., a heartbeat message every 15 seconds) to reassure users and tools that the process is still active and not stalled. This is especially important for watch-mode scripts, heavy processing, or anything that may run for more than a few seconds without visible output.

For details on the assistant's commitment to guideline adherence, refer to [meta/assistant_adherence.md](mdc:meta/assistant_adherence.md). 