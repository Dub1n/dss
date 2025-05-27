---
tags: [meta, guidelines, github, issue_labels, tagging]
provides: [github_label_conventions, issue_tagging_guidance]
requires: [meta/scripts/dss_bootstrap.py, meta/assistant_guidelines/installation_report_submission.md]
---

# GitHub Issue Label Conventions

## Overview

This document outlines the standardized GitHub issue labels used in the DSS project. These labels help categorize, prioritize, and track issues efficiently. Both users and the AI assistant should refer to this guide when creating or managing GitHub issues.

## Label Categories

DSS uses several categories of labels to organize GitHub issues:

### 1. Installation Report Labels

These labels are specifically for DSS installation reports:

| Label | Description | Color |
|-------|-------------|-------|
| `installation-report` | Reports from DSS installations | #0E8A16 |
| `platform-windows` | Issues specific to Windows platforms | #0052CC |
| `platform-linux` | Issues specific to Linux platforms | #22863a |
| `platform-macos` | Issues specific to macOS platforms | #d93f0b |
| `project-android_wearos` | WearOS project related issues | #c5def5 |
| `project-android_kotlin` | Android Kotlin project related issues | #6f42c1 |
| `project-android_java` | Android Java project related issues | #1d76db |
| `project-data_science` | Data science project related issues | #fbca04 |
| `project-web_application` | Web application project related issues | #0366d6 |
| `project-python_package` | Python package project related issues | #5319e7 |
| `project-documentation` | Documentation project related issues | #0075ca |
| `project-general` | General project related issues | #bfdadc |

### 2. Priority Labels

These labels indicate the urgency of addressing an issue:

| Label | Description | Color |
|-------|-------------|-------|
| `priority-critical` | Must be fixed as soon as possible | #b60205 |
| `priority-high` | Should be fixed in the next release | #d93f0b |
| `priority-medium` | Should be fixed in a future release | #fbca04 |
| `priority-low` | Fix when convenient | #c2e0c6 |

### 3. Status Labels

These labels indicate the current state of an issue:

| Label | Description | Color |
|-------|-------------|-------|
| `status-blocked` | Blocked by another issue or external factor | #b60205 |
| `status-in-progress` | Work in progress | #0e8a16 |
| `status-needs-review` | Ready for review | #fbca04 |
| `status-needs-testing` | Needs testing before merge | #d4c5f9 |

### 4. Type Labels

These labels indicate the nature of the issue:

| Label | Description | Color |
|-------|-------------|-------|
| `bug` | Something isn't working | #d73a4a |
| `enhancement` | New feature or request | #a2eeef |
| `documentation` | Improvements or additions to documentation | #0075ca |
| `question` | Further information is requested | #d876e3 |
| `duplicate` | This issue or pull request already exists | #cfd3d7 |
| `invalid` | This doesn't seem right | #e4e669 |
| `wontfix` | This will not be worked on | #ffffff |
| `help wanted` | Extra attention is needed | #008672 |
| `good first issue` | Good for newcomers | #7057ff |
| `type-feature` | New feature implementation | #0075ca |
| `type-bugfix` | Fix for a bug | #d73a4a |
| `type-refactor` | Code refactoring without functional changes | #6f42c1 |
| `type-performance` | Performance improvements | #5319e7 |
| `type-security` | Security-related issues | #b60205 |
| `type-maintenance` | Repository maintenance and housekeeping | #bfdadc |
| `type-tests` | Test-related changes | #c5def5 |

### 5. Component Labels

These labels indicate which part of the system is affected:

| Label | Description | Color |
|-------|-------------|-------|
| `component-ui` | User interface related issues | #c2e0c6 |
| `component-api` | API related issues | #0366d6 |
| `component-docs` | Documentation component issues | #0075ca |
| `component-infrastructure` | Infrastructure and CI/CD issues | #5319e7 |

## Label Usage Guidelines

1. **Use Multiple Categories**: Most issues should have at least one label from the Type category and can include labels from other categories as appropriate.

2. **Installation Reports**: When submitting installation reports, the `dss_bootstrap.py` script will attempt to automatically apply the following labels:
   - `installation-report`
   - A platform-specific label (e.g., `platform-windows`)
   - A project-type label (e.g., `project-data_science`)

3. **Manual Label Application**: Repository maintainers can add labels to a GitHub issue with:
   ```bash
   gh issue edit ISSUE_NUMBER --add-label "LABEL_NAME"
   ```

4. **Creating New Labels**: Repository maintainers can create new labels with:
   ```bash
   gh label create LABEL_NAME --description "DESCRIPTION" --color COLOR_CODE
   ```

## Automated Label Validation

The DSS Bootstrap script includes label validation to prevent errors when submitting issues with non-existent labels. This validation:

1. Fetches available labels from the repository
2. Filters out any proposed labels that don't exist
3. Only uses valid labels in the GitHub issue creation command

If validation fails, the issue will still be created, just without the invalid labels.

## Label Creation Commands

For repository maintainers, here are the commands to create all the labels defined in this document:

```bash
# Installation Report Labels
gh label create installation-report --description "Reports from DSS installations" --color 0E8A16
gh label create platform-windows --description "Issues specific to Windows platforms" --color 0052CC
gh label create platform-linux --description "Issues specific to Linux platforms" --color 22863a
gh label create platform-macos --description "Issues specific to macOS platforms" --color d93f0b
gh label create project-android_wearos --description "WearOS project related issues" --color c5def5
gh label create project-android_kotlin --description "Android Kotlin project related issues" --color 6f42c1
gh label create project-android_java --description "Android Java project related issues" --color 1d76db
gh label create project-data_science --description "Data science project related issues" --color fbca04
gh label create project-web_application --description "Web application project related issues" --color 0366d6
gh label create project-python_package --description "Python package project related issues" --color 5319e7
gh label create project-documentation --description "Documentation project related issues" --color 0075ca
gh label create project-general --description "General project related issues" --color bfdadc

# Priority Labels
gh label create priority-critical --description "Must be fixed as soon as possible" --color b60205
gh label create priority-high --description "Should be fixed in the next release" --color d93f0b
gh label create priority-medium --description "Should be fixed in a future release" --color fbca04
gh label create priority-low --description "Fix when convenient" --color c2e0c6

# Status Labels
gh label create status-blocked --description "Blocked by another issue or external factor" --color b60205
gh label create status-in-progress --description "Work in progress" --color 0e8a16
gh label create status-needs-review --description "Ready for review" --color fbca04
gh label create status-needs-testing --description "Needs testing before merge" --color d4c5f9

# Type Labels
gh label create type-feature --description "New feature implementation" --color 0075ca
gh label create type-bugfix --description "Fix for a bug" --color d73a4a
gh label create type-refactor --description "Code refactoring without functional changes" --color 6f42c1
gh label create type-performance --description "Performance improvements" --color 5319e7
gh label create type-security --description "Security-related issues" --color b60205
gh label create type-maintenance --description "Repository maintenance and housekeeping" --color bfdadc
gh label create type-tests --description "Test-related changes" --color c5def5

# Component Labels
gh label create component-ui --description "User interface related issues" --color c2e0c6
gh label create component-api --description "API related issues" --color 0366d6
gh label create component-docs --description "Documentation component issues" --color 0075ca
gh label create component-infrastructure --description "Infrastructure and CI/CD issues" --color 5319e7
```

## Related Documentation

- [Installation Report Submission Guidelines](mdc:meta/assistant_guidelines/installation_report_submission.md) - Guidelines for submitting installation reports
- [DSS Bootstrap Script](mdc:meta/scripts/dss_bootstrap.py) - Script that generates installation reports and handles GitHub submission 