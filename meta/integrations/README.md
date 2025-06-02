---
tags: [meta, integrations, documentation]
provides: [integrations_overview, integration_guidelines]
requires: [meta/DSS_GUIDE.md]
---

# DSS Integrations

This directory contains documentation for proposed and developed integrations that extend DSS functionality across different tools and platforms.

## Purpose

DSS is designed to work seamlessly across multiple tools (GitHub, Obsidian, Cursor, etc.) and with various AI systems. This directory documents:

1. **Proposed integrations** - Solutions to improve DSS compatibility with existing tools
2. **Developed integrations** - Completed plugins, scripts, or configurations
3. **Integration specifications** - Technical requirements and implementation details
4. **Compatibility documentation** - How DSS works with different tool ecosystems

## Directory Structure

```text
meta/integrations/
├── README.md                           # This file
├── obsidian_mdc_links_plugin.md        # Obsidian plugin for mdc: link navigation
├── cursor_extensions/                   # Cursor-specific integrations
├── github_actions/                      # GitHub workflow integrations
├── vscode_extensions/                   # VS Code extension specifications
└── ai_tool_integrations/               # LLM and AI tool compatibility docs
```

## Integration Categories

### Editor Integrations

- **Obsidian plugins** - Enhance DSS functionality within Obsidian
- **Cursor extensions** - Improve AI-assisted development workflows
- **VS Code extensions** - Adapt DSS for VS Code environments

### Platform Integrations

- **GitHub Actions** - Automate DSS workflows in CI/CD
- **Git hooks** - Ensure DSS compliance during development
- **Documentation platforms** - Sync with external documentation systems

### AI Tool Integrations

- **LLM prompt optimization** - Improve AI understanding of DSS structure
- **Custom AI tools** - Specialized tools for DSS projects
- **API integrations** - Connect DSS with external AI services

## Integration Lifecycle

### 1. Proposed (Status: `proposed`)

- Problem identification and analysis
- Solution specification and alternatives
- Development planning and requirements

### 2. In Development (Status: `in_development`)

- Active development work
- Testing and iteration
- Documentation updates

### 3. Beta Testing (Status: `beta`)

- Community testing and feedback
- Bug fixes and refinements
- Performance optimization

### 4. Released (Status: `released`)

- Stable version available
- Documentation complete
- Maintenance mode

### 5. Deprecated (Status: `deprecated`)

- No longer recommended
- Migration path provided
- Historical reference only

## Documentation Standards

Each integration document should include:

### Required Sections

1. **Problem Statement** - What issue does this solve?
2. **Why This Should Be Solved** - Justification and benefits
3. **Desired Outcome** - Success criteria and goals
4. **Proposed Solution** - Technical approach and architecture
5. **Development Plan** - Implementation timeline and phases

### Optional Sections

- **Alternative Approaches** - Other solutions considered
- **Technical Requirements** - Dependencies and compatibility
- **Testing Strategy** - Validation and quality assurance
- **Distribution Plan** - How users will access the integration
- **Success Metrics** - How to measure success

### Metadata Requirements

```yaml
---
tags: [integration, platform_name, tool_category]
provides: [integration_name, solution_type]
requires: [dependencies]
status: proposed|in_development|beta|released|deprecated
priority: low|medium|high|critical
---
```

## Contributing Integrations

### Proposing New Integrations

1. Identify a compatibility gap or workflow friction point
2. Research existing solutions and alternatives
3. Create a detailed specification document in this directory using the [Integration Template](../templates/meta/integration_template.md)
4. Add the proposal to `meta/TODO.md` with appropriate roadmap references
5. Discuss with the DSS community for feedback and prioritization

### Developing Integrations

1. Follow the development plan outlined in the specification
2. Update the document status as work progresses
3. Create separate repositories for substantial integrations
4. Link to external repositories from the specification document

### Testing and Quality Assurance

- Test integrations across multiple platforms and use cases
- Ensure compatibility with DSS conventions and guidelines
- Validate that integrations don't break existing workflows
- Document known limitations and troubleshooting steps

## Current Integrations

### Proposed

- [Obsidian MDC Links Plugin](obsidian_mdc_links_plugin.md) - Enable clickable `mdc:` links in Obsidian

### In Development

- *None currently*

### Released

- *None currently*

## Related Documentation

- [DSS Guide](../DSS_GUIDE.md) - Core DSS principles and structure
- [Backlink Conventions](../guidelines/backlink_conventions.md) - Cross-reference management
- [Assistant Guidelines](../assistant_guidelines/) - AI assistant integration patterns
- [Project Roadmap](../roadmap.md) - Long-term integration planning

## Integration Requests

To request a new integration or report issues with existing ones:

1. Check existing documentation to avoid duplicates
2. Create a detailed issue description in `meta/TODO.md`
3. Reference relevant roadmap sections using `(@roadmap: [Section Name])`
4. Provide specific use cases and workflow examples

## Maintenance

This directory is maintained as part of the DSS framework evolution. Integration documents should be:

- **Kept current** with tool and platform updates
- **Archived appropriately** when tools become obsolete
- **Cross-referenced** with related DSS documentation
- **Updated** based on community feedback and usage patterns
