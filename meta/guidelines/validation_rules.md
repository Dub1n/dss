---
tags: [guidelines, validation, frontmatter, automation]
provides: [frontmatter_validation_rules]
requires: [meta/dss_config.yml, meta/guidelines/tag_conventions.md]
---

# Frontmatter Validation Rules

This document defines the validation rules for YAML frontmatter in DSS files. These rules are implemented in the `frontmatter_utils.py` script and are used to ensure consistency across documentation and code files.

## Required Fields

All DSS files with frontmatter must include the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `tags` | Array of strings | Categorization tags following [tag conventions](mdc:meta/guidelines/tag_conventions.md) |
| `provides` | Array of strings | Resources or concepts that the file provides to the project |
| `requires` | Array of strings | Dependencies that the file needs from other parts of the project |

## Field Format Rules

### Tags

- Must be an array/list, even for a single tag
- Each tag must be a string
- Tags should follow the [tag conventions](mdc:meta/guidelines/tag_conventions.md)
- At least one tag is required
- Tag names should be lowercase with underscores for spaces
- Example: `tags: [documentation, automation, phase1]`

### Provides

- Must be an array/list, even for a single item
- Each item must be a string
- Items should represent resources, concepts, or artifacts that the file contributes
- Empty array is allowed if the file doesn't explicitly provide any resources
- Example: `provides: [frontmatter_validation_rules, validation_schema]`

### Requires

- Must be an array/list, even for a single item
- Each item must be a string
- Items should reference existing files or resources in the project
- Empty array is allowed if the file has no dependencies
- For file references, use relative paths from the project root
- Example: `requires: [meta/dss_config.yml, docs/automated_formatting.md]`

## Format Consistency

### Markdown Files

Frontmatter in Markdown files must:
- Begin at the very start of the file
- Start with a line containing only `---`
- End with a line containing only `---`
- Contain valid YAML between the delimiters

Example:
```markdown
---
tags: [documentation, template]
provides: [frontmatter_example]
requires: []
---

# Document Title
```

### Python Files

Frontmatter in Python files must:
- Be contained within a docstring at the beginning of the file
- Start with `"""---`
- End with `---"""`
- Contain valid YAML between the delimiters

Example:
```python
"""---
tags: [utility, automation]
provides: [frontmatter_validation]
requires: [yaml, pathlib]
---
Module description here.
"""

import yaml
from pathlib import Path
```

## Auto-correction Behavior

The frontmatter validation script can automatically correct certain issues:

1. Missing required fields will be added with default values from `dss_config.yml`
2. String values for `tags`, `provides`, or `requires` will be converted to single-item arrays
3. Non-string, non-array values will be replaced with appropriate defaults
4. Invalid YAML will be reported but cannot be auto-corrected

## Implementation

These rules are implemented in:

1. `meta/scripts/frontmatter_utils.py` - Script for validation and auto-correction
2. Pre-commit hooks for automated validation during git operations
3. Documentation generators that enforce frontmatter rules

## Related Documentation

- [DSS Configuration](mdc:meta/dss_config.yml) - Contains default values and patterns
- [Tag Conventions](mdc:meta/guidelines/tag_conventions.md) - Detailed guidelines for tag usage
- [Automated Formatting](mdc:docs/automated_formatting.md) - Overview of automation tools 