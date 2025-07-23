---
tags: [documentation, rules_injector, mcp_server, dss_workflow]
provides: [Rules Injector Documentation, Design Overview, Implementation Guide]
requires: [DSS Core Structure and Concepts, MCP Server Framework]
---

# DSS Rules Injector MCP Server

## Overview

The Rules Injector is an MCP server that provides context-aware access to DSS workflow rules and guidelines. It enables AI agents to progressively discover and load the appropriate DSS rules based on task context.

## Design Philosophy

This implementation aligns with DSS's core principles:

- **Modular**: Rules are loaded incrementally as needed
- **Self-organizing**: Rules include activation triggers and next-rule suggestions  
- **LLM-native**: Progressive disclosure prevents context overload
- **Context-aware**: Smart rule selection based on task requirements

## How DSS Workflows Operate

DSS uses a structured methodology for LLM-native project organization:

### Core Philosophy

- **Plaintext everything** - Markdown, code, JSON with light metadata
- **Unified structure** - Works across GitHub, Obsidian, Cursor, and GPT
- **Self-organizing** - Clear cross-references and dependencies

### The Agent Workflow System

DSS uses **Riley** (the agent persona) who follows a structured adherence process:

1. **7-Step Process** (from `02-assistant-adherence.mdc`):
   - Understand → Gather Context → Identify Guidelines → Plan → Execute → Review → Respond

2. **Decision Tree Routing** (from `00-workflow-selection.mdc`):
   - Routes tasks through 6 workflows based on complexity/type
   - Quick Tasks → Code Modification → Documentation → Task Decomposition → etc.

3. **Automatic Maintenance Integration**:
   - Updates frontmatter, cross-references, INDEX.md
   - Follows template-first approach
   - Preserves structure and intent

4. **Context-Aware Rule Loading**:
   - Different guidelines activate based on task triggers
   - Conversational patterns determine which rules to consult

## Tools Provided

### `get_dss_rules`

**Purpose**: Retrieve DSS rule files with intelligent context-based suggestions

**Default Behavior**: Returns the "bootstrap trilogy":

- `00-dss-core.mdc` - Core DSS concepts and structure
- `01-dss-behavior.mdc` - Riley personality and behaviors  
- `00-workflow-selection.mdc` - Workflow decision tree

**Smart Context Detection**: Based on context parameter, automatically suggests additional rules:

- "code changes" → include `02-code-modification.mdc` + `11-documentation-standards.mdc`
- "documentation" → include `03-documentation-driven.mdc` + `07-folder-readme-policy.mdc`
- "validation errors" → include `04-validation-rules.mdc` + `09-error-recovery.mdc`

### `list_available_rules`

**Purpose**: Provide organized catalog of all available DSS rule files

**Categories**:

- **workflows/**: Task-specific workflow guidance
- **guidelines/**: Specific conventions and standards
- **config/**: Configuration and setup information

## Enhanced Rule File Format

Each DSS rule file includes:

```markdown
---
tags: [Workflow, Quick Tasks, Simple Changes]
provides: [Quick Task Process, Simple Change Guidelines]
requires: [Workflow Selection Logic]
activation_triggers: ["simple task", "small change", "quick fix", "minor edit"]
next_rules: ["02-code-modification.mdc", "04-validation-rules.mdc"]
---

# Rule Content

## When to Request Next Rules
- If task grows beyond 1-2 files → request `02-code-modification.mdc`
- If validation errors occur → request `04-validation-rules.mdc`
- If documentation updates needed → request `11-documentation-standards.mdc`
```

## Usage Pattern

1. **Bootstrap**: Agent calls `get_dss_rules()` with default parameters
2. **Context Analysis**: Agent reads core rules, identifies task type
3. **Progressive Loading**: Agent requests additional specific rules as needed
4. **Self-Discovery**: Rules guide agent to next relevant rule files

## Benefits

- **Token Efficiency**: Only loads relevant rules, prevents context overload
- **Progressive Disclosure**: Agent learns incrementally as task complexity grows
- **Self-Healing**: Rules include their own navigation and dependency information
- **Context Awareness**: Smart suggestions based on task requirements

## Implementation

The server uses FastMCP for streamlined tool implementation with rich parameter metadata that displays properly in Cursor's MCP Tools interface.
