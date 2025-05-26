---
tags: [meta, guidelines, naming, ai_interaction]
provides: [naming_conventions, llm_optimized_naming]
requires: [meta/dss_config.yml, docs/designing_ai_interaction.md]
---

# LLM-Optimized Naming Conventions in DSS

## Overview

This document outlines naming conventions designed to enhance semantic discoverability by LLMs within the DSS framework. Properly named files and directories are more easily discoverable through semantic search and context-aware tools, improving both human and AI navigation of the codebase.

## Core Principles for Semantic Discoverability

### 1. Descriptive Clarity

- **Be explicit over implicit**: Use names that directly describe the content or purpose rather than relying on context.
- **Avoid abbreviations**: Spell out terms fully unless they are extremely common in the domain (e.g., API, HTTP).
- **Include purpose in name**: Indicate what the file does or contains in its name.

### 2. Contextual Consistency

- **Use consistent terminology**: Maintain the same terms for the same concepts throughout the repository.
- **Follow domain-specific conventions**: Use terminology that aligns with the project's domain.
- **Maintain consistent patterns**: Use similar naming patterns for files that serve similar purposes.

### 3. Hierarchical Organization

- **Folder names as contexts**: Name folders to provide clear context for the files they contain.
- **Progressive specificity**: Move from general to specific as you navigate deeper into the directory structure.
- **Group related items**: Files with related functionality should be in the same directory with names that show their relationship.

### 4. Semantic Richness

- **Use distinctive keywords**: Include terms that would naturally appear in queries about the file's content.
- **Avoid generic names**: Prefer specific, descriptive names over generic ones (e.g., `user_authentication.py` over `auth.py`).
- **Consider searchability**: Include terms that might be used when searching for the file or its functionality.

## File Naming Conventions

### Format Rules

1. **Case formatting**:
   - Python files: `snake_case.py`
   - JavaScript/TypeScript files: `camelCase.js` or `PascalCase.tsx` for React components
   - Documentation: `kebab-case.md` or `snake_case.md` (consistently throughout the project)
   - Configuration files: `kebab-case.yml` or `snake_case.json`

2. **Word separation**:
   - Use appropriate case conventions rather than spaces
   - For documentation and configuration, use hyphens or underscores consistently

3. **Special characters**:
   - Avoid special characters except underscores or hyphens according to the convention
   - No spaces in filenames

### Naming Patterns by File Type

#### Documentation Files

- **Guides**: `how-to-{action}.md` or `{topic}-guide.md`
- **References**: `{topic}-reference.md`
- **Explanations**: `understanding-{concept}.md` or `{concept}-explained.md`
- **Workflows**: `{topic}-workflow.md`
- **Templates**: `{type}_template.md`

#### Source Code Files

- **Modules**: `{functionality}_{type}.py`
- **Utilities**: `{purpose}_utils.py`
- **Classes**: Match the primary class name within the file
- **Components**: `{component_name}_{type}.{ext}`
- **Tests**: `test_{module_being_tested}.py`

#### Configuration Files

- **Main config**: `{scope}_config.{ext}`
- **Environment**: `.env.{environment}`
- **Settings**: `{component}_settings.{ext}`

#### Scripts

- **Command-line tools**: `{action}_{target}.py`
- **Automation scripts**: `{purpose}_{automation}.py`
- **Conversions**: `{source}_to_{destination}.py`

## Directory Naming Conventions

- **Top-level directories**: Use simple, clear nouns (`docs`, `src`, `tests`)
- **Functional groups**: Name by domain or functionality (`authentication`, `data_processing`)
- **Feature modules**: Name after the feature they implement (`user_management`, `reporting`)
- **Component collections**: Name after the type of components they contain (`templates`, `utilities`)

## Examples

### Before and After Transformation

| Before | After | Explanation |
|--------|-------|-------------|
| `utils.py` | `string_utils.py` | Specifies the type of utilities |
| `handlers.py` | `event_handlers.py` | Clarifies what is being handled |
| `config.json` | `database_config.json` | Indicates the scope of configuration |
| `script.py` | `data_import_script.py` | Describes the script's purpose |
| `README.txt` | `api_usage_guide.md` | More specific about content and uses Markdown |
| `docs/info.md` | `docs/system_architecture.md` | Clearly states the document's content |
| `lib/` | `libraries/` | Full word is more discoverable |
| `impl/` | `implementation/` | Avoids abbreviation |

## Implementation Guidelines

1. **Apply consistently**: When implementing these conventions, apply them consistently across the entire repository.
2. **Document exceptions**: If exceptions to these rules are necessary, document them in the relevant README files.
3. **Migrate gradually**: For existing projects, migrate to these naming conventions gradually, focusing on the most important or frequently accessed files first.
4. **Update references**: When renaming files, ensure all references to them in other files are updated.

## Semantic Search Optimization

To optimize for semantic search by LLMs:

1. **Include key terms**: Incorporate terms that users or AI assistants might use when looking for the file.
2. **Consider variations**: Think about different ways someone might describe the file's purpose or content.
3. **Balance specificity and generality**: Names should be specific enough to distinguish the file but general enough to be discovered through related queries.
4. **Align with content**: The filename should directly relate to the primary content or functionality of the file.

## Related Documentation

- [DSS Configuration](mdc:meta/dss_config.yml) - Defines file classification patterns
- [Designing AI Interaction](mdc:docs/designing_ai_interaction.md) - Principles for AI-human collaboration
- [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) - Tagging system for additional discoverability 