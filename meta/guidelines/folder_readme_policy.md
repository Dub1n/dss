---
tags: [policy, documentation, guidelines]
provides: [folder_readme_policy]
requires: []
---

# Folder README.md Content Policy

## Decision: Subdirectory File Listing

**Recommendation: Folder README.md files should include subdirectory listings when appropriate for navigation and context.**

### Rationale

Based on analysis of existing README files in the DSS project, the most effective pattern is:

1. **List direct files** in the current directory in a "Files" table
2. **List subdirectories** in a separate "Subdirectories" section with brief descriptions
3. **Include key files from subdirectories** when they are particularly relevant to understanding the parent directory's purpose

### Examples of Current Best Practice

- `meta/templates/README.md` - Includes both direct files and a subdirectories section
- `docs/README.md` - References key files from subdirectories using MDC links for navigation
- `meta/README.md` - Lists both local files and subdirectory folders

### Guidelines

#### Required Sections
1. **Files** - Table listing all direct child files with purpose descriptions, tags, and MDC links
2. **Subdirectories** (if any exist) - Table listing subdirectories with brief descriptions

#### Optional Sections
3. **Key Subdirectory Files** - Highlight particularly important files from subdirectories that users should know about
4. **Cross-references** - Use MDC links to reference related files in subdirectories

#### Template Structure
```markdown
## Files
| file | purpose | tags |
|------|---------|------|
| [README.md](mdc:README.md) | Folder overview | [documentation] |
| [file1.md](mdc:file1.md) | Description | [tag1, tag2] |

## Subdirectories
| directory | purpose |
|-----------|---------|
| [subdir/](mdc:subdir/README.md) | Description |

## Key Files (Optional)
- [Important File](mdc:subdir/important.md) - Critical component
```

#### Linking Policy

1. **All file references** should use MDC links: `[filename.ext](mdc:filename.ext)`
2. **Subdirectory links** should point to the subdirectory's README: `[subdir/](mdc:subdir/README.md)`
3. **Tags column** should list the main tags from the file's YAML front-matter in square brackets
4. **Relative paths** should be used for files in the same directory
5. **Full paths** should be used for files in other directories: `[file.md](mdc:path/to/file.md)`

### Benefits of This Approach

1. **Complete Navigation** - Users can see the full structure at a glance with clickable links
2. **Context Preservation** - Understand relationships between directories and file purposes
3. **LLM Efficiency** - AI assistants can quickly understand directory structure and file metadata
4. **Tag Visibility** - Tags provide immediate context about file content and classification
5. **Direct Access** - MDC links enable instant navigation to referenced files
6. **Scalability** - Works for both simple and complex directory hierarchies
7. **Consistency** - Matches existing successful patterns in the project

### Implementation

This policy should be:
1. Applied to the folder README template in `meta/templates/folder_README_template.md`
2. Used when updating existing README files
3. Referenced in documentation guidelines

## Tools

- [meta/scripts/readme_link_checker.py](mdc:meta/scripts/readme_link_checker.py) - Script to systematically check README files for missing links

## Referenced By

- [meta/TODO.md](mdc:meta/TODO.md) - Completed tasks: folder README policy decisions and link implementation
- [meta/templates/folder_README_template.md](mdc:meta/templates/folder_README_template.md) - Implementation location 