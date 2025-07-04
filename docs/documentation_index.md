---
tags: [documentation, index, navigation, reference]
provides: [documentation_index]
requires: [meta/DSS_GUIDE.md]
---

# DSS Documentation Index

This index organizes all documentation files by category, purpose, and relationships. Use this as your starting point for navigating the  
DSS documentation.

## 🧭 Getting Started

Documentation to help new users get oriented and begin using DSS:

| Document | Description | Keywords |
|----------|-------------|----------|
| [Documentation Overview](mdc:docs/README.md) | Overview of all documentation resources | #overview #guide #documentation |
| [Getting Started Guide](mdc:docs/getting_started.md) | Complete introduction for new users | #beginner #setup #introduction |
| [DSS Guide](mdc:meta/DSS_GUIDE.md) | Overview of DSS principles and structure | #overview #principles #architecture |
| [How to Update Index](mdc:docs/how_to_update_index.md) | Instructions for maintaining the INDEX.md file | #index #maintenance |
| [Index Template Usage](mdc:docs/index_template_usage.md) | Guide for using the INDEX.md template | #template #index |
| [Troubleshooting Guide](mdc:docs/troubleshooting.md) | Solutions for common issues and problems | #help #support #troubleshooting |

## 📚 Core Concepts

Documentation explaining the fundamental concepts of DSS:

| Document | Description | Keywords |
|----------|-------------|----------|
| [Technical Overview](mdc:docs/technical_overview.md) | Comprehensive technical details and advanced features | #technical #autoformatter #benchmark #requirements |
| [Task Decomposition](mdc:docs/task_decomposition.md) | Method for breaking down tasks into atomic subtasks | #tasks #organization #methodology |
| [Designing AI Interaction](mdc:docs/designing_ai_interaction.md) | Guidelines for effective LLM interaction | #ai #llm #interaction |
| [Architecture](mdc:docs/architecture.md) | System architecture overview | #architecture #system #design |

## 🔧 Tools & Automation

Documentation for DSS automation tools and utilities:

| Document | Description | Keywords |
|----------|-------------|----------|
| [Automated Formatting](mdc:docs/automated_formatting) | Guide to automatic formatting tools | #formatting #automation |
| [DSS Bootstrap Guide](mdc:docs/dss_bootstrap_guide.md) | Bootstrap script documentation | #bootstrap #setup #transformation |
| [DSS Autoformatter Usage](mdc:docs/dss_autoformatter_usage.md) | Detailed autoformatter usage guide | #autoformatter #transformation #usage |
| [Filename Transformations](mdc:docs/filename_transformations.md) | Examples of filename standardization | #filenames #naming #conventions |
| [API Reference](mdc:docs/api_reference.md) | Reference for DSS API | #api #reference |

## 🤖 AI Integration

Documentation for AI assistant integration and configuration:

| Document | Description | Keywords |
|----------|-------------|----------|
| [Cursor Integration](mdc:docs/cursor_integration.md) | Complete Cursor AI assistant setup | #cursor #ai #integration |
| [Cursor Native Integration](mdc:docs/cursor_native_integration.md) | Native Cursor IDE integration | #cursor #native #ide |
| [Windows WearOS Troubleshooting](mdc:docs/windows_wearos_troubleshooting.md) | Platform-specific troubleshooting | #windows #wearos #troubleshooting |

## 📋 Templates & Guidelines

Documentation providing templates and standardized approaches:

| Document | Description | Keywords |
|----------|-------------|----------|
| [Brainstorming Assistant Dev](mdc:docs/brainstorming_assistant_dev.md) | Guidelines for assistant development | #assistant #development |
| [Documentation Templates](mdc:meta/templates/docs/README.md) | Standardized templates for documentation | #templates #standardization |

## 📁 Directory Structure

The DSS documentation is organized into the following directories:

```text
/docs/
  ├── README.md                           # Documentation overview
  ├── getting_started.md                  # Introduction for new users
  ├── technical_overview.md               # Technical details and advanced features
  ├── documentation_index.md              # This file
  ├── task_decomposition.md               # Task breakdown methodology
  ├── automated_formatting                # Formatting automation guide
  ├── dss_bootstrap_guide.md              # Bootstrap script documentation
  ├── dss_autoformatter_usage.md          # Autoformatter usage guide
  ├── cursor_integration.md               # Cursor AI assistant setup
  ├── cursor_native_integration.md        # Native Cursor IDE integration
  ├── windows_wearos_troubleshooting.md   # Platform-specific troubleshooting
  ├── filename_transformations.md         # Filename conventions
  ├── how_to_update_index.md              # INDEX.md maintenance guide
  ├── index_template_usage.md             # Template usage instructions
  ├── brainstorming_assistant_dev.md      # Assistant development notes
  ├── architecture.md                     # System architecture overview
  ├── api_reference.md                    # API documentation
  ├── designing_ai_interaction.md         # LLM interaction design
  ├── troubleshooting.md                  # Guide for resolving common issues
  └── 🔒archive/                          # Archived documentation
```

## 🔄 Cross-Reference Map

This diagram shows how documentation files relate to each other:

```text
getting_started.md ──────► DSS_GUIDE.md
       │                      │
       ▼                      ▼
documentation_index.md     technical_overview.md
       │                      │
       ├──────► how_to_update_index.md
       │            │
       │            ▼
       ├──────► index_template_usage.md
       │
       ├──────► task_decomposition.md
       │
       ├──────► automated_formatting
       │            │
       │            ▼
       └──────► filename_transformations.md
```

## 🔍 Search by Topic

Find documentation by common topics and use cases:

### Project Setup

- [Getting Started Guide](mdc:docs/getting_started.md)
- [DSS Guide](mdc:meta/DSS_GUIDE.md)
- [Technical Overview](mdc:docs/technical_overview.md)
- [Troubleshooting Guide](mdc:docs/troubleshooting.md)

### Documentation Management

- [How to Update Index](mdc:docs/how_to_update_index.md)
- [Index Template Usage](mdc:docs/index_template_usage.md)

### Project Organization

- [Task Decomposition](mdc:docs/task_decomposition.md)
- [Architecture](mdc:docs/architecture.md)

### Automation and Tools

- [Technical Overview](mdc:docs/technical_overview.md)
- [Automated Formatting](mdc:docs/automated_formatting)
- [DSS Bootstrap Guide](mdc:docs/dss_bootstrap_guide.md)
- [DSS Autoformatter Usage](mdc:docs/dss_autoformatter_usage.md)
- [Filename Transformations](mdc:docs/filename_transformations.md)

### AI Integration

- [Cursor Integration](mdc:docs/cursor_integration.md)
- [Cursor Native Integration](mdc:docs/cursor_native_integration.md)
- [Designing AI Interaction](mdc:docs/designing_ai_interaction.md)
- [Brainstorming Assistant Dev](mdc:docs/brainstorming_assistant_dev.md)

### Templates and Standards

- [Documentation Templates](mdc:meta/templates/docs/README.md)
- [Index Template Usage](mdc:docs/index_template_usage.md)

## 📝 Missing Documentation

The following documentation is planned but not yet created:

- CLI Reference
- Interactive Examples
- Quickstart Templates
- Contribution Guidelines
- FAQ Document

## 🆕 Recent Updates

Recent additions and updates to the documentation:

- Added [Technical Overview](mdc:docs/technical_overview.md) - Comprehensive technical details and advanced features
- Added [Documentation Overview](mdc:docs/README.md) - Overview of all documentation resources
- Added [Getting Started Guide](mdc:docs/getting_started.md) - Comprehensive introduction for new users
- Added [Documentation Index](mdc:docs/documentation_index.md) - This file
- Added [Troubleshooting Guide](mdc:docs/troubleshooting.md) - Guide for resolving common issues
- Added [Documentation Templates](mdc:meta/templates/docs/README.md) - Standardized templates for documentation
- Updated cross-references in existing documentation

---

This index is automatically updated when new documentation is added to the repository. Last updated: 2023-07-12
