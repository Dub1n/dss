---
tags: [templates, documentation, task-creation, benchmark, guidelines]
provides: [task_template_usage_guide, template_variable_reference, task_creation_patterns, category_guidelines]
requires: [task_template, DSS_conventions, benchmark_structure]
---

# Task Template Usage Guide

## Template Variables Reference

### Basic Information

- `{{TASK_ID}}`: Unique identifier (e.g., "create-module-01", "complex-integration-06")
- `{{CATEGORY}}`: Task category (file_creation, documentation, multi_file_coordination, workflow_application, maintenance_integration)
- `{{DIFFICULTY}}`: basic, intermediate, advanced
- `{{TIME_LIMIT}}`: Time limit string (e.g., "10 minutes", "20 minutes")
- `{{FOCUS_AREAS}}`: Comma-separated focus areas in brackets (e.g., [file_placement, frontmatter, dss_structure])
- `{{RULES_TESTING}}`: Optional comma-separated rules being tested (e.g., [task_decomposition, maintenance_integration])

### Content Structure

- `{{TASK_NUMBER}}`: Task number (01, 02, 06, etc.)
- `{{TASK_TITLE}}`: Descriptive title
- `{{TASK_DESCRIPTION}}`: Opening description paragraph
- `{{REQUIREMENTS_DESCRIPTION}}`: Description before requirements list

### Setup Section (Critical for Independence)

- `{{COPY_COMMANDS}}`: PowerShell commands to copy existing files
- `{{CREATE_FILES}}`: PowerShell here-strings to create new files
- `{{PROJECT_DIRECTORIES}}`: Space-separated directory structure to create
- `{{SETUP_DESCRIPTION}}`: Explanation of what setup provides

### Context and Tasks

- `{{CONTEXT_TYPE}}`: "Project Context", "Current Context", etc.
- `{{CONTEXT_DESCRIPTION}}`: Description of current state
- `{{TASKS_TYPE}}`: "Tasks", "Implementation Requirements", etc.

### Conditional Sections (Include as needed)

- `{{#CODE_REQUIREMENTS}}...{{/CODE_REQUIREMENTS}}`: Code examples and requirements
- `{{#SUCCESS_CRITERIA}}...{{/SUCCESS_CRITERIA}}`: Success criteria with percentages
- `{{#WHAT_THIS_TESTS}}...{{/WHAT_THIS_TESTS}}`: What the task tests (for advanced tasks)
- `{{#PITFALLS}}...{{/PITFALLS}}`: Common mistakes to avoid
- `{{#DELIVERABLES}}...{{/DELIVERABLES}}`: Expected deliverables
- `{{#TIME_ALLOCATION}}...{{/TIME_ALLOCATION}}`: Recommended time allocation

## Category Guidelines

### "file_creation" (basic)

- Focus on creating new files with proper DSS conventions
- Simple setup (usually just user.py)
- Basic success criteria
- 8-10 minute time limit

### "documentation" (basic)

- Focus on creating or updating documentation
- Simple setup with existing files to document
- Cross-reference and DSS integration focus
- 8-10 minute time limit

### "multi_file_coordination" (advanced)

- Complex setup with multiple existing files
- Detailed success criteria with percentages
- "What This Tests" section
- Architecture and coordination focus
- 15-20 minute time limit

### "workflow_application" (intermediate)

- Tests workflow selection and process following
- Analysis and planning deliverables
- Process discipline focus
- 15 minute time limit

### "maintenance_integration" (intermediate)

- Heavy maintenance and template testing
- Template-first approach testing
- Cross-reference management focus
- 15 minute time limit

## Setup Section Patterns

### Basic Tasks (01, 02)

```powershell
mkdir task_repos/task_{{TASK_NUMBER}}
cd task_repos/task_{{TASK_NUMBER}}
mkdir -p src/models
cp ../../task_repos/src/models/user.py src/models/
mkdir -p [basic structure]
```

### Complex Tasks (06, 07, 08)

```powershell
mkdir task_repos/task_{{TASK_NUMBER}}
cd task_repos/task_{{TASK_NUMBER}}
mkdir -p src/models src/auth src/api
cp ../../task_repos/src/models/user.py src/models/
cp ../../task_repos/src/auth/authentication.py src/auth/
[Create fixed API init file with here-string]
[Create documentation files if needed]
mkdir -p [full structure]
```

## Usage Instructions

1. **Copy this template** to create a new task file
2. **Fill in all {{VARIABLES}}** with appropriate values
3. **Remove conditional sections** that don't apply (marked with {{#SECTION}}...{{/SECTION}})
4. **Customize the setup section** based on what files the task needs
5. **Add task-specific content** in place of generic descriptions
6. **Review against existing tasks** to ensure consistency

## Key Conventions to Maintain

- **Always include setup section** for task independence
- **Use emoji headers** consistently (📋, ⚙️, 🎯, 📝, etc.)
- **Include DSS frontmatter** requirements in all tasks
- **Provide clear success criteria** with measurable outcomes
- **End with resources and focus summary**
- **Use PowerShell commands** for Windows compatibility
- **Create fixed API files** to avoid import errors
