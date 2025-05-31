---
tags: [integration, cursor, rules, bootstrap, distribution, git_submodule]
provides: [cursor_rules_integration, dss_distribution_method, simplified_bootstrap]
requires: [meta/DSS_GUIDE.md, meta/dss_config.yml]
status: proposed
priority: high
---

# DSS Integration via Cursor Rules Folder

## Problem with Current Bootstrap Approach

The current `dss_bootstrap.py` script approach has several friction points:

1. **Complex Setup**: Users need to run Python scripts, manage dependencies
2. **Version Drift**: No easy way to update DSS assistant behavior after initial setup
3. **Customization Conflicts**: Hard to merge updates with user customizations
4. **Platform Dependencies**: Scripts may behave differently across environments
5. **Discoverability**: Users don't know what DSS behavior they're getting

## The Cursor Rules Solution

### Core Concept

Instead of bootstrap scripts, distribute DSS as a **complete `.cursor/rules/` folder** that users can:

- **Download directly** → Copy to their project's `.cursor/rules/`
- **Git submodule** → `git submodule add` for automatic updates
- **Git subtree** → `git subtree add` for embedded but updateable copy
- **Manual sync** → Periodically copy updated files

### Why This Works Better

✅ **Zero Setup Friction**: Works immediately after copying files  
✅ **Version Control Native**: Uses git for updates and customization tracking  
✅ **Transparent**: Users see exactly what assistant behavior they're getting  
✅ **Modular**: Users can pick and choose which rules to include  
✅ **Platform Agnostic**: No script execution, just file copying  
✅ **IDE Native**: Leverages Cursor's existing rule loading system  

## Proposed Implementation

### 1. Repository Structure Redesign

```
dss_template_repo/
├── .cursor/
│   └── rules/                    # ← Complete distributable DSS package
│       ├── 00_dss_core.md       # Core DSS concepts and structure
│       ├── 01_dss_behavior.md   # Assistant behavior guidelines  
│       ├── 02_dss_workflows.md  # Development workflows
│       ├── 03_dss_templates.md  # File and folder templates
│       ├── 04_dss_maintenance.md # Maintenance and cleanup tasks
│       ├── config/
│       │   ├── dss_config.yml   # Default DSS configuration
│       │   └── file_templates/  # Template files for new DSS projects
│       └── README.md            # How to use these rules
├── meta/                        # Development of the DSS system itself
├── docs/                        # Documentation about DSS (not rules)
└── src/                         # DSS tooling and utilities
```

### 2. Distributable Rules Package

#### Core Rules Files

**`.cursor/rules/00_dss_core.md`**
```markdown
# DSS Core Structure and Concepts

This file defines the fundamental DSS concepts that the AI should understand.

## Folder Structure
- `src/` → Source code and implementation
- `docs/` → Human-readable documentation  
- `data/` → Data files and datasets
- `meta/` → Project metadata, config, scripts
- `tests/` → Test files and validation
- `canvas/` → Optional visual diagrams

## Metadata System
Every file should have YAML frontmatter with:
- `tags: []` - Classification tags
- `provides: []` - What this file/module provides
- `requires: []` - What this file/module depends on

## Archive Convention
- `docs/🔒archive/` contains deprecated content
- Never edit, reference, or summarize archived content
- Archive is excluded from AI context
```

**`.cursor/rules/01_dss_behavior.md`**
```markdown
# DSS Assistant Behavior Guidelines

## Core Personality
- Act like Riley: nonbinary senior code dev, thoughtful PR reviewer
- Be concise with care - let personality show when helpful
- Work incrementally, not prescriptively
- Preserve intent, not just structure

## When Working with DSS Projects
1. **Always preserve frontmatter** in .md, .py, .ipynb files
2. **Check for templates** in meta/templates/ before creating new files
3. **Update INDEX.md** when structure changes
4. **Maintain provides/requires** relationships
5. **Follow existing patterns** rather than imposing new ones

## File Creation Workflow
1. Check if template exists in meta/templates/
2. Use template if available, customize for specific use
3. Add appropriate frontmatter based on file type
4. Update any relevant documentation (INDEX.md, README.md)
5. Consider provides/requires relationships

## Response Style
- Reference files with line numbers when relevant: `12:15:app/components/Todo.tsx`
- Explain reasoning for architectural decisions
- Suggest small, modular changes that fit existing workflow
- Be transparent about changes being made
```

**`.cursor/rules/02_dss_workflows.md`**
```markdown
# DSS Development Workflows

## Quick Tasks (simple changes)
- Small bug fixes
- Documentation updates  
- Configuration tweaks
- File renames/moves

Process: Make change → Update metadata if needed → Done

## Code Modification Workflow
- Adding new features
- Refactoring existing code
- API changes

Process: Analyze impact → Check templates → Implement → Update docs → Update dependencies

## Documentation Generation
- Creating README files
- Updating INDEX.md
- Module documentation

Process: Analyze structure → Generate following patterns → Cross-link related files

## Task Decomposition (complex work)
- Multi-file changes
- Architectural modifications
- Large feature additions

Process: Break into phases → Document plan → Execute incrementally → Update as you go
```

**`.cursor/rules/03_dss_templates.md`**
```markdown
# DSS Templates and Patterns

## New Python Module Template
```python
"""---
tags: [CATEGORY, MODULE_TYPE]
provides: [MAIN_EXPORT, SECONDARY_EXPORTS]
requires: [DEPENDENCIES]
---"""

# Standard module structure following project patterns
```

## New Documentation Template
```markdown
---
tags: [docs, TOPIC]
provides: [DOCUMENTATION_TYPE]
requires: [RELATED_MODULES]
---

# Module Name

## Purpose
Brief description of what this module does

## Usage
Examples of how to use this module

## Dependencies  
What this module requires to function

## Exports
What this module provides to other parts of the system
```

## Common Patterns
- Error handling: Follow project's existing exception patterns
- Testing: Match existing test structure and coverage standards
- Documentation: Use project's established style and detail level
- API design: Maintain consistency with existing endpoints
```

**`.cursor/rules/04_dss_maintenance.md`**
```markdown
# DSS Maintenance Tasks

## Automatic Maintenance Triggers
- **New file created** → Add appropriate frontmatter
- **File moved** → Update any cross-references
- **Module structure changed** → Update INDEX.md
- **Dependencies changed** → Update provides/requires
- **Documentation outdated** → Suggest updates

## Regular Maintenance Tasks
- Check for broken internal links
- Validate provides/requires consistency
- Update INDEX.md when structure changes
- Archive deprecated files to docs/🔒archive/
- Check test coverage matches project standards

## Maintenance Workflow
1. Identify what needs maintenance
2. Check if templates or patterns exist
3. Apply changes consistently across project
4. Update documentation to reflect changes
5. Verify no breaking changes introduced
```

### 3. User Integration Methods

#### Method 1: Direct Copy (Simplest)

```bash
# User copies the rules to their project
curl -L https://github.com/org/dss_template_repo/archive/main.zip | \
  unzip -j "*/\.cursor/rules/*" -d .cursor/rules/

# Or manual download and copy
```

#### Method 2: Git Submodule (Updateable)

```bash
# Add as submodule
git submodule add https://github.com/org/dss_template_repo.git .dss-source

# Link rules folder  
ln -s .dss-source/.cursor/rules .cursor/rules

# Update when needed
git submodule update --remote .dss-source
```

#### Method 3: Git Subtree (Embedded + Updateable)

```bash
# Add as subtree (embeds files directly)
git subtree add --prefix=.cursor/rules \
  https://github.com/org/dss_template_repo.git main --squash

# Update when needed
git subtree pull --prefix=.cursor/rules \
  https://github.com/org/dss_template_repo.git main --squash
```

#### Method 4: Custom Update Script (Optional)

```bash
# .dss-update.sh (optional convenience script)
#!/bin/bash
echo "Updating DSS rules..."
curl -L https://api.github.com/repos/org/dss_template_repo/contents/.cursor/rules | \
  jq -r '.[] | select(.type=="file") | .download_url' | \
  while read url; do
    filename=$(basename $url)
    curl -L $url > .cursor/rules/$filename
  done
echo "DSS rules updated!"
```

### 4. Configuration and Customization

#### Default Configuration

**`.cursor/rules/config/dss_config.yml`**
```yaml
# Default DSS configuration - copy to project root as meta/dss_config.yml
patterns:
  code: ["**/*.py", "**/*.js", "**/*.ts"]
  data: ["**/*.csv", "**/*.json", "**/*.parquet"]  
  docs: ["**/*.md", "**/*.rst"]
  binary: ["**/*.png", "**/*.pdf"]

defaults:
  tags: ["draft"]
  provides: []
  requires: []

inject:
  markdown: |
    ---
    {yaml}
    ---
  python: |
    """---
    {yaml}
    ---"""

ignore:
  - "docs/🔒archive/**"
  - "node_modules/**"
  - ".git/**"
```

#### User Customization Strategy

1. **Copy default config**: User copies `config/dss_config.yml` to their `meta/` folder
2. **Customize behavior**: User modifies the config for their project needs  
3. **Override rules**: User can add `99_local_overrides.md` to `.cursor/rules/` for project-specific behavior
4. **Update safely**: When updating DSS rules, config and overrides are preserved

### 5. Migration from Current System

#### For This Repository

1. **Restructure**: Move current assistant files to `.cursor/rules/` with numbered prefixes
2. **Consolidate**: Combine scattered guidelines into organized rule files
3. **Template extraction**: Move templates from `meta/templates/` to `.cursor/rules/config/`
4. **Simplify meta/**: Keep only DSS development tools, not user-facing content
5. **Update docs**: Document the new distribution method

#### For Existing DSS Users

1. **Backup**: Save any customizations they've made
2. **Clean install**: Remove old bootstrap artifacts  
3. **New setup**: Install via preferred method (copy/submodule/subtree)
4. **Restore customizations**: Add back project-specific modifications
5. **Test**: Verify everything works as expected

## Benefits of This Approach

### For Users
- **Instant setup**: Copy files and it works
- **Transparent**: See exactly what AI behavior you're getting
- **Updateable**: Easy to get latest DSS improvements
- **Customizable**: Override behavior for specific projects
- **No dependencies**: No Python scripts or complex setup

### For DSS Development  
- **Easier testing**: Rules are just markdown files
- **Version control**: All changes tracked in git
- **Modular development**: Each rule file has specific purpose
- **User feedback**: Users can suggest rule improvements via PRs
- **Documentation**: Rules themselves serve as documentation

### For Distribution
- **Platform agnostic**: Works on any system with Cursor
- **Bandwidth efficient**: Only copy/update what changed
- **CDN friendly**: Can distribute via GitHub's CDN
- **Forkable**: Users can fork and customize extensively
- **No maintenance**: No servers or complex infrastructure

## Implementation Roadmap

### Phase 1: Restructure Current Repository (Week 1)
1. Create new `.cursor/rules/` structure
2. Migrate content from existing assistant files
3. Organize guidelines into numbered rule files
4. Test with current DSS projects

### Phase 2: Distribution Methods (Week 2)  
1. Document all integration methods
2. Create convenience scripts for each method
3. Test submodule and subtree approaches
4. Create update workflows

### Phase 3: User Experience (Week 3)
1. Create getting started documentation
2. Record setup videos for each method
3. Build troubleshooting guides
4. Test with external users

### Phase 4: Migration Support (Week 4)
1. Create migration guide for existing users
2. Build compatibility shims if needed
3. Deprecate old bootstrap approach
4. Update all documentation

## Related Documentation

- [Current Bootstrap System](../scripts/dss_bootstrap.py) - What we're replacing
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules) - How Cursor loads rules
- [Git Submodules Guide](https://git-scm.com/book/en/v2/Git-Tools-Submodules) - For updateable integration
- [DSS Configuration](../dss_config.yml) - Current config format to migrate

## Future Enhancements

### Advanced Distribution
- **NPM package**: `npx install-dss-rules` for Node.js projects
- **VS Code extension**: Install DSS rules via extension marketplace
- **GitHub App**: Install DSS rules via GitHub app integration
- **Template repositories**: GitHub template repos with DSS pre-installed

### Smart Updates
- **Selective updates**: Choose which rule files to update
- **Conflict resolution**: Merge user customizations with updates
- **Version pinning**: Lock to specific DSS rule versions
- **Update notifications**: Alert when new DSS rules available

This approach transforms DSS from a complex bootstrap system into a simple, git-native distribution method that's easy to adopt, customize, and maintain. 