---
tags: [integration, obsidian, plugin, development]
provides: [obsidian_mdc_plugin_spec, link_navigation_solution]
requires: [meta/guidelines/backlink_conventions.md, meta/dss_config.yml]
status: proposed
priority: medium
---

# Obsidian MDC Links Plugin Integration

## Problem Statement

The DSS framework uses `mdc:` prefixed links (e.g., `[filename](mdc:path/to/file)`) to help LLMs understand file references and navigate the codebase effectively. However, this format creates usability issues for human users:

1. **Non-clickable links in Cursor**: The `mdc:` prefix breaks standard Markdown link functionality in editors like Cursor
2. **Navigation friction**: Users cannot Ctrl+click to navigate between files
3. **Inconsistent experience**: Links work for LLMs but not for humans
4. **Tool compatibility**: The format may not work properly in other tools like GitHub or standard Markdown editors

## Why This Should Be Solved

1. **Dual compatibility**: DSS needs to serve both human users and LLM automation effectively
2. **Workflow efficiency**: Manual navigation is essential for development and documentation work
3. **Tool ecosystem**: Better integration with the broader Obsidian ecosystem would increase DSS adoption
4. **User experience**: Seamless navigation is crucial for maintaining productivity

## Desired Outcome

An Obsidian plugin that:

1. **Preserves LLM functionality**: Keeps `mdc:` links intact for AI automation
2. **Enables human navigation**: Makes `mdc:` links clickable and functional for users
3. **Maintains file format**: No changes to the underlying Markdown files
4. **Provides visual feedback**: Clear indication that links are interactive
5. **Handles edge cases**: Graceful handling of missing files or invalid paths

## Proposed Solution

### Plugin Architecture

Create a lightweight Obsidian plugin called "DSS MDC Links" that:

1. **Registers a markdown post-processor** to detect and enhance `mdc:` links
2. **Adds click handlers** to make links functional
3. **Provides visual styling** to indicate clickable links
4. **Integrates with Obsidian's file resolution** system

### Core Implementation

```typescript
import { Plugin, MarkdownPostProcessorContext } from 'obsidian';

export default class MDCLinksPlugin extends Plugin {
    onload() {
        // Register markdown post-processor for mdc: links
        this.registerMarkdownPostProcessor(this.processMDCLinks.bind(this));
        
        // Add CSS for visual styling
        this.addStyle();
    }

    processMDCLinks(element: HTMLElement, context: MarkdownPostProcessorContext) {
        const mdcLinks = element.querySelectorAll('a[href^="mdc:"]');
        
        mdcLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            
            const filePath = href.replace('mdc:', '');
            
            // Add visual indication
            link.addClass('mdc-link');
            
            // Add click handler
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.openFile(filePath);
            });
            
            // Add hover preview using Obsidian's built-in system
            this.addHoverPreview(link, filePath);
        });
    }

    async openFile(filePath: string) {
        try {
            const file = this.app.metadataCache.getFirstLinkpathDest(filePath, '');
            if (file) {
                await this.app.workspace.getLeaf().openFile(file);
            } else {
                // Handle missing file
                new Notice(`File not found: ${filePath}`);
            }
        } catch (error) {
            console.error('Error opening file:', error);
        }
    }

    addHoverPreview(link: HTMLElement, filePath: string) {
        // Use Obsidian's built-in hover preview system
        link.addEventListener('mouseover', (event) => {
            this.app.workspace.trigger('hover-link', {
                event,
                source: 'mdc-links-plugin',
                hoverParent: link,
                targetEl: link,
                linktext: filePath
            });
        });
    }

    addStyle() {
        const style = document.createElement('style');
        style.textContent = `
            .mdc-link {
                color: var(--link-color);
                text-decoration: underline;
                cursor: pointer;
                border-bottom: 1px dotted var(--link-color);
            }
            .mdc-link:hover {
                opacity: 0.8;
                background-color: var(--link-hover-color);
            }
        `;
        document.head.appendChild(style);
    }
}
```

### Enhanced Features

1. **File preview on hover**: Leverages Obsidian's built-in hover preview system automatically
2. **Missing file handling**: Visual indication and options for creating missing files
3. **Multi-format support**: Handle both absolute and relative `mdc:` paths
4. **Settings panel**: Configure plugin behavior and appearance
5. **Command integration**: Add commands for bulk operations on `mdc:` links

## Development Plan

### Phase 1: Core Functionality (Week 1)
- [ ] Set up Obsidian plugin development environment
- [ ] Implement basic `mdc:` link detection and click handling
- [ ] Add basic CSS styling for visual feedback
- [ ] Test with DSS template repository files

### Phase 2: Enhanced Features (Week 2)
- [ ] Verify hover previews work correctly with Obsidian's built-in system
- [ ] Implement missing file detection and user feedback
- [ ] Add settings panel for customization options
- [ ] Comprehensive testing across different file types and link formats

### Phase 3: Polish and Distribution (Week 3)
- [ ] Add comprehensive error handling
- [ ] Create plugin documentation and README
- [ ] Submit to Obsidian Community Plugins repository
- [ ] Create installation and usage documentation for DSS

### Phase 4: Advanced Features (Future)
- [ ] Integration with graph view to show `mdc:` link relationships
- [ ] Bulk conversion utilities between link formats
- [ ] Analytics for link usage patterns
- [ ] Integration with other DSS automation tools

## Technical Requirements

### Dependencies
- Obsidian API (built-in)
- TypeScript 4.x+
- Node.js for development build process

### File Structure
```
obsidian-dss-mdc-links/
├── main.ts              # Main plugin file
├── styles.css           # Plugin styles
├── manifest.json        # Plugin manifest
├── versions.json        # Version compatibility
├── package.json         # Node dependencies
├── tsconfig.json        # TypeScript configuration
├── rollup.config.js     # Build configuration
└── README.md           # Plugin documentation
```

### Compatibility
- Obsidian API version: 0.15.0+
- Compatible with Live Preview and Reading modes
- Works in both desktop and mobile versions of Obsidian

## Testing Strategy

### Manual Testing
1. Test link clicking in various contexts (inline, lists, tables)
2. Verify preview functionality with different file types
3. Test edge cases (missing files, malformed links, special characters)
4. Verify performance with large documents containing many `mdc:` links

### Automated Testing
1. Unit tests for link parsing and path resolution
2. Integration tests with Obsidian API mocking
3. Performance tests for large document processing

## Distribution and Maintenance

### Initial Distribution
1. **GitHub repository**: Host source code and releases
2. **Obsidian BRAT**: Enable beta testing through BRAT plugin
3. **Community plugins**: Submit for official Obsidian plugin repository

### Long-term Maintenance
1. **Version compatibility**: Maintain compatibility with Obsidian updates
2. **Feature requests**: Accept and evaluate community feedback
3. **Bug fixes**: Regular maintenance and issue resolution
4. **DSS integration**: Keep aligned with DSS framework evolution

## Alternative Approaches Considered

### 1. Hybrid Link Format
Use both formats: `[filename](mdc:path) ([Navigate](path))`
- **Pros**: No plugin required, immediate compatibility
- **Cons**: Verbose, clutters documentation, maintenance overhead

### 2. Standard Relative Links
Convert all links to standard relative paths
- **Pros**: Universal compatibility
- **Cons**: Breaks LLM automation, loses context for AI tools

### 3. Custom CSS with JavaScript
Use CSS and browser JavaScript to handle links
- **Pros**: Lighter weight than full plugin
- **Cons**: Limited integration with Obsidian features, security concerns

## Success Metrics

1. **Functionality**: 100% of `mdc:` links become clickable and functional
2. **Performance**: No noticeable impact on document loading or editing performance
3. **Compatibility**: Works across all Obsidian platforms and modes
4. **User adoption**: Positive feedback from DSS users and broader Obsidian community
5. **Maintenance**: Stable operation with minimal required updates

## Related Documentation

- [Backlink Conventions](../guidelines/backlink_conventions.md) - How this integrates with DSS backlink system
- [DSS Configuration](../dss_config.yml) - Configuration options for link handling
- [Obsidian Plugin Development](https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin) - Official development guide

## Referenced By

- [meta/guidelines/backlink_conventions.md](../guidelines/backlink_conventions.md) - References this as a solution for link navigation issues 