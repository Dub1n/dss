---
tags: [meta, guidelines, tagging]
provides: [tag_conventions, tagging_guidelines]
requires: [meta/dss_config.yml, docs/task_decomposition.md]
---

# Tag Conventions in DSS

## Overview

This document outlines the tagging conventions used in the DSS framework, including standardized tag formats, categorization principles, and specific tagging recommendations for task decomposition documents.

## Tag Structure and Format

### Basic Tag Format

Tags in DSS follow these format rules:

1. **Format in YAML frontmatter**: 
   ```yaml
   tags: [tag1, tag2, tag3]
   ```

2. **Lowercase with underscores**: Use `snake_case` for multi-word tags (e.g., `task_management`, not `TaskManagement` or `task-management`).

3. **No special characters**: Avoid using symbols or special characters except underscores.

4. **No spaces**: Use underscores instead of spaces.

5. **No # prefix**: Unlike some other tagging systems, DSS tags do not use hashtag prefixes within the YAML frontmatter.

## Tag Categories

Tags in DSS generally fall into the following categories:

### 1. File Type Tags

Identify the type of document:

- `docs` - Documentation files
- `code` - Source code files
- `meta` - Project metadata files
- `dataset` - Data files
- `template` - Template files

### 2. Purpose Tags

Describe the purpose or role of the document:

- `guide` - How-to guides and tutorials
- `reference` - Reference documentation
- `project_management` - Planning and management documents
- `task_breakdown` - Task decomposition documents
- `assistant_workflow` - Assistant workflow definitions
- `assistant_guidelines` - Guidelines for assistant behavior

### 3. Status Tags

Indicate the document's status:

- `draft` - Initial or incomplete content
- `review` - Ready for review
- `approved` - Approved content
- `archived` - Historical content no longer actively maintained

### 4. Topic Tags

Describe the subject matter:

- `ai_interaction` - AI-related topics
- `development` - Development processes
- `task_management` - Task management and organization

## Task Decomposition Tagging

For task decomposition documents, the following tagging recommendations apply:

### Required Tags

Every task decomposition document should include:

```yaml
tags: [task_breakdown, project_management]
```

### Additional Recommended Tags

Add topic-specific tags to indicate the focus area:

- `frontend` - For frontend development tasks
- `backend` - For backend development tasks
- `data_processing` - For data-related tasks
- `documentation` - For documentation tasks
- `infrastructure` - For infrastructure or DevOps tasks
- `research` - For research-oriented tasks

### In-Text Task Tagging

Within task decomposition documents, you can also use inline tags for subtasks to enable better filtering and organization:

```markdown
#### 1.1. Research Component Implementation `[NOT STARTED]` #research #frontend
```

These inline tags use the `#tag` format and serve as additional metadata that can be extracted by tools or used for visual identification.

## Task Status vs. Tags

It's important to distinguish between task status markers and tags:

- **Status markers** use the format `[STATUS]` (e.g., `[NOT STARTED]`, `[IN PROGRESS]`) and indicate the current state of work.
- **Tags** use the format `#tag` when inline or are listed in the YAML frontmatter and indicate categories or classification.

## Recommended Task-Related Tags

| Tag | Usage |
|-----|-------|
| `task_breakdown` | Main tag for all task decomposition documents |
| `project_management` | For project planning and management documents |
| `milestone` | For tasks associated with project milestones |
| `phase1`, `phase2`, etc. | For tasks associated with specific project phases |
| `high_priority` | For tasks requiring immediate attention |
| `blocker` | For tasks that are blocking other work |
| `quick_win` | For low-effort, high-value tasks |
| `technical_debt` | For tasks addressing technical debt |
| `enhancement` | For feature enhancement tasks |
| `bugfix` | For bug-fixing tasks |
| `refactoring` | For code restructuring tasks |
| `testing` | For testing-related tasks |
| `documentation` | For documentation tasks |
| `automation` | For tasks related to workflow automation |

## Tag Usage Guidelines

1. **Be Consistent**: Use the same tags for similar content across the repository.
2. **Be Specific**: Choose specific tags that accurately reflect the content.
3. **Be Concise**: Limit to 3-5 tags per document to maintain focus.
4. **Be Hierarchical**: Use both general and specific tags when appropriate.
5. **Tag for Discoverability**: Consider how users might search for or filter content.

## Examples

### Task Decomposition Document

```yaml
---
tags: [task_breakdown, project_management, frontend, phase1]
provides: [login_screen_implementation_plan]
requires: [docs/architecture.md, meta/roadmap.md]
---
```

### Subtask with Inline Tags

```markdown
### 1. Design Authentication Flow `[IN PROGRESS]` #security #user_experience
```

## Integration with Workflow

To integrate tagging into the task decomposition workflow:

1. Start with required tags in the frontmatter
2. Add topic-specific tags based on the task domain
3. Use inline tags for individual subtasks when helpful for filtering
4. Consider adding phase or priority tags for better project management

## Related Documentation

- [DSS Configuration](mdc:meta/dss_config.yml) - Defines default tag settings
- [Task Decomposition Guide](mdc:docs/task_decomposition.md) - Outlines task breakdown methodology 