---
tags: [roadmap, migration, cursor_rules, restructure, implementation]
provides: [migration_roadmap, restructure_plan, implementation_steps]
requires: [meta/integrations/cursor_rules_integration.md, meta/DSS_GUIDE.md]
status: active
priority: high
---

# DSS Repository Restructure: Bootstrap → Cursor Rules Migration

## Current State Analysis

### What We Have Now
```
dss_template_repo/
├── .cursor/rules/
│   ├── assistant.mdc          # Current assistant behavior
│   └── dss-overview.mdc       # DSS overview
├── meta/
│   ├── assistant_guidelines/   # Scattered guidelines
│   ├── assistant_workflows/    # Workflow documentation  
│   ├── templates/             # File templates
│   ├── scripts/               # Bootstrap and utility scripts
│   └── DSS_GUIDE.md          # Core DSS documentation
├── dss_bootstrap.py           # Will be removed/archived
└── src/dss_gpt_bridge/        # GPT integration code
```

### What Needs to Change
1. **Consolidate rules**: Merge scattered guidelines into organized rule files
2. **Restructure distribution**: Move from script-based to file-based distribution
3. **Simplify user experience**: Replace complex bootstrap with simple file copying
4. **Improve maintainability**: Make rules easier to update and customize
5. **Enable version control**: Let users track DSS updates via git

## Detailed Migration Tasks

### Phase 1: Create New Rules Structure (Days 1-3)

#### Day 1: Core Rules Files

##### Task 1.1: Create `.cursor/rules/00_dss_core.md`
**Goal**: Establish fundamental DSS concepts for AI understanding

**Subtasks**:
1. **Extract folder structure from `meta/DSS_GUIDE.md` lines 45-65**
   - Copy folder definitions (src/, docs/, data/, meta/, tests/, canvas/)
   - Add purpose statement for each folder
   - Include file organization principles

2. **Extract metadata system from `meta/DSS_GUIDE.md` lines 120-140**
   - Document YAML frontmatter structure
   - Explain tags, provides, requires fields
   - Add metadata inheritance rules

3. **Add archive convention documentation**
   - Document `docs/🔒archive/` purpose
   - Add exclusion rules for AI context
   - Include archival procedures

4. **Add file extension mapping from `meta/dss_config.yml`**
   - Include code patterns: `**/*.py`, `**/*.js`, `**/*.ts`
   - Include data patterns: `**/*.csv`, `**/*.json`, `**/*.parquet`
   - Include docs patterns: `**/*.md`, `**/*.rst`

**Validation**:
- [ ] File contains all 6 core folder definitions
- [ ] Metadata fields (tags, provides, requires) are documented with examples
- [ ] Archive convention is clearly stated
- [ ] File follows DSS frontmatter format

##### Task 1.2: Create `.cursor/rules/01_dss_behavior.md`
**Goal**: Define assistant personality and core behaviors

**Subtasks**:
1. **Extract Riley personality from `.cursor/rules/assistant.mdc` lines 1-20**
   - Include "nonbinary senior code dev" definition
   - Add "thoughtful PR reviewer" behavior
   - Include "concise with care" communication style

2. **Extract behavior rules from `meta/assistant_guidelines/`**
   - Consolidate from `documentation_task_management.md`
   - Include from `maintenance_checklist.md`
   - Add from `installation_report_submission.md`

3. **Add frontmatter preservation rules**
   - Document preservation for .md, .py, .ipynb files
   - Include YAML and triple-quote format rules
   - Add examples of correct preservation

4. **Create file creation workflow**
   - Step 1: Check `meta/templates/` for existing template
   - Step 2: Use template if available, customize for use case
   - Step 3: Add appropriate frontmatter based on file type
   - Step 4: Update INDEX.md and related documentation
   - Step 5: Consider provides/requires relationships

5. **Define response style guidelines**
   - Include line number citation format: `12:15:file.tsx`
   - Add architectural reasoning requirements
   - Include transparency expectations

**Validation**:
- [ ] Riley personality is fully defined
- [ ] All 5 core behaviors are documented
- [ ] File creation workflow has 5 clear steps
- [ ] Response style includes citation format
- [ ] File follows DSS frontmatter format

##### Task 1.3: Test Core Rules
**Goal**: Verify new rules work correctly

**Subtasks**:
1. **Backup current rules**
   - Rename `assistant.mdc` → `assistant.mdc.backup`
   - Rename `dss-overview.mdc` → `dss-overview.mdc.backup`

2. **Test with simple DSS task**
   - Create a new markdown file
   - Verify frontmatter is added correctly
   - Check that INDEX.md update is suggested

3. **Test personality consistency**
   - Ask for code review
   - Verify Riley personality shows through
   - Check response style matches guidelines

4. **Validate rule loading**
   - Confirm Cursor loads new rules
   - Check no syntax errors in markdown
   - Verify behavior changes are active

**Validation**:
- [ ] Backup files created successfully
- [ ] New file creation follows workflow
- [ ] AI personality matches Riley definition
- [ ] No rule loading errors

#### Day 2: Workflow Rules

##### Task 2.1: Create `.cursor/rules/02_dss_workflows.md`
**Goal**: Convert workflow documentation into actionable rules

**Subtasks**:
1. **Extract Quick Tasks from `meta/assistant_workflows/quick_tasks.md`**
   - Copy task types: bug fixes, documentation updates, config tweaks, file moves
   - Include process: Make change → Update metadata → Done
   - Add trigger conditions for quick workflow

2. **Extract Code Modification from `meta/assistant_workflows/code_modification.md`**
   - Copy task types: new features, refactoring, API changes
   - Include process: Analyze → Check templates → Implement → Update docs → Update deps
   - Add impact analysis requirements

3. **Extract Documentation Generation from `meta/assistant_workflows/docs_driven_development.md`**
   - Copy task types: README creation, INDEX.md updates, module docs
   - Include process: Analyze structure → Generate following patterns → Cross-link
   - Add documentation standards

4. **Extract Task Decomposition from `meta/assistant_workflows/task_decomposition.md`**
   - Copy task types: multi-file changes, architectural mods, large features
   - Include process: Break into phases → Document plan → Execute incrementally → Update
   - Add complexity thresholds

5. **Add workflow decision tree**
   - Create flowchart for workflow selection
   - Include complexity indicators
   - Add transition points between workflows

**Validation**:
- [ ] All 4 workflow types are documented
- [ ] Each workflow has clear process steps
- [ ] Decision tree helps choose workflow
- [ ] File follows DSS frontmatter format

##### Task 2.2: Cross-reference workflow files
**Goal**: Ensure workflow integration works correctly

**Subtasks**:
1. **Map workflow transitions from `meta/assistant_workflows/workflow_transitions.md`**
   - Document when to escalate from quick → code modification
   - Add criteria for moving to task decomposition
   - Include de-escalation scenarios

2. **Add cross-workflow dependencies**
   - Link documentation generation to code modification
   - Connect maintenance tasks to all workflows
   - Include template usage across workflows

3. **Validate workflow completeness**
   - Check all scenarios from existing files are covered
   - Verify no gaps in workflow coverage
   - Ensure consistent terminology

**Validation**:
- [ ] Workflow transitions are documented
- [ ] Cross-dependencies are clear
- [ ] No gaps in scenario coverage
- [ ] Terminology is consistent

##### Task 2.3: Test workflow integration
**Goal**: Verify workflows guide AI correctly

**Subtasks**:
1. **Test quick task workflow**
   - Make a simple documentation update
   - Verify metadata update is suggested
   - Check workflow completion

2. **Test code modification workflow**
   - Add a new function
   - Verify template checking occurs
   - Check documentation updates are suggested

3. **Test workflow selection**
   - Present a complex task
   - Verify task decomposition is suggested
   - Check workflow escalation works

**Validation**:
- [ ] Quick tasks complete in 1-2 steps
- [ ] Code modifications follow 5-step process
- [ ] Complex tasks trigger decomposition
- [ ] Workflow selection is accurate

#### Day 3: Templates and Maintenance

##### Task 3.1: Create `.cursor/rules/03_dss_templates.md`
**Goal**: Consolidate template information for easy AI access

**Subtasks**:
1. **Extract Python module template from `meta/templates/docs/module_doc_template.md`**
   - Include frontmatter structure with tags, provides, requires
   - Add standard module docstring format
   - Include common import patterns

2. **Extract documentation template from `meta/templates/docs/`**
   - Include markdown frontmatter
   - Add standard documentation sections: Purpose, Usage, Dependencies, Exports
   - Include cross-reference patterns

3. **Add JavaScript/TypeScript template**
   - Include JSDoc format with frontmatter
   - Add export/import patterns
   - Include testing template references

4. **Extract common patterns from existing codebase**
   - Error handling: Custom exception classes with detailed messages
   - Testing: Pytest with fixtures, coverage requirements
   - API design: RESTful with OpenAPI documentation
   - Documentation: Detailed with examples

5. **Add template usage guidelines**
   - When to use each template
   - How to customize templates
   - Template inheritance rules

**Validation**:
- [ ] Python template includes frontmatter and docstrings
- [ ] Documentation template has all 4 sections
- [ ] Common patterns are extracted and documented
- [ ] Usage guidelines are clear
- [ ] File follows DSS frontmatter format

##### Task 3.2: Create `.cursor/rules/04_dss_maintenance.md`
**Goal**: Define automatic maintenance behaviors

**Subtasks**:
1. **Extract maintenance triggers from `meta/assistant_guidelines/maintenance_checklist.md`**
   - New file created → Add frontmatter
   - File moved → Update cross-references
   - Structure changed → Update INDEX.md
   - Dependencies changed → Update provides/requires
   - Documentation outdated → Suggest updates

2. **Add regular maintenance tasks**
   - Broken link checking procedures
   - Provides/requires consistency validation
   - Test coverage monitoring
   - Archive management rules

3. **Define maintenance workflow**
   - Step 1: Identify maintenance need
   - Step 2: Check for existing patterns/templates
   - Step 3: Apply changes consistently
   - Step 4: Update related documentation
   - Step 5: Verify no breaking changes

4. **Add validation rules**
   - Frontmatter format checking
   - Cross-reference validation
   - Dependency graph consistency
   - Archive compliance

**Validation**:
- [ ] All 5 automatic triggers are documented
- [ ] Regular tasks are clearly defined
- [ ] 5-step workflow is documented
- [ ] Validation rules are comprehensive
- [ ] File follows DSS frontmatter format

##### Task 3.3: Create `.cursor/rules/config/` directory
**Goal**: Provide default configuration and templates

**Subtasks**:
1. **Create `.cursor/rules/config/dss_config.yml`**
   - Copy from `meta/dss_config.yml`
   - Add comments explaining each section
   - Include customization examples

2. **Create `.cursor/rules/config/file_templates/`**
   - Copy `meta/templates/docs/module_doc_template.md`
   - Copy `meta/templates/meta/assistant_guideline_template.md`
   - Add Python module template
   - Add TypeScript component template

3. **Create `.cursor/rules/config/README.md`**
   - Document configuration options
   - Explain template usage
   - Include customization guide

**Validation**:
- [ ] Config file copied with comments
- [ ] Template files are present
- [ ] README explains configuration
- [ ] Directory follows DSS structure

### Phase 2: Distribution Infrastructure (Days 4-6)

#### Day 4: Documentation and Update Scripts

##### Task 4.1: Create `.cursor/rules/README.md`
**Goal**: Comprehensive setup and usage documentation

**Subtasks**:
1. **Document Method 1: Direct Copy**
   - Provide curl command for downloading
   - Include manual download steps
   - Add verification steps

2. **Document Method 2: Git Submodule**
   - Step-by-step submodule setup
   - Symlink creation commands
   - Update procedures

3. **Document Method 3: Git Subtree**
   - Subtree add command
   - Update command
   - Conflict resolution

4. **Add troubleshooting section**
   - Common issues and solutions
   - Platform-specific considerations
   - Verification procedures

5. **Include customization guide**
   - How to add local overrides
   - Configuration modification
   - Template customization

**Validation**:
- [ ] All 3 integration methods documented
- [ ] Each method has step-by-step instructions
- [ ] Troubleshooting covers common issues
- [ ] Customization guide is complete
- [ ] File follows DSS frontmatter format

##### Task 4.2: Create update scripts
**Goal**: Convenient update mechanisms for users

**Subtasks**:
1. **Create `.dss-update.sh` script**
   - Use GitHub API to fetch latest rules
   - Backup existing rules before update
   - Validate downloaded files
   - Restore customizations if possible

2. **Create `validate-dss-rules.py` script**
   - Check frontmatter format in all rule files
   - Validate markdown syntax
   - Verify file references exist
   - Check configuration consistency

3. **Add update documentation**
   - When to update
   - How to preserve customizations
   - Rollback procedures

**Validation**:
- [ ] Update script downloads correctly
- [ ] Validation script catches errors
- [ ] Documentation covers update process
- [ ] Scripts work on Windows/Mac/Linux

##### Task 4.3: Test distribution methods
**Goal**: Verify all integration approaches work

**Subtasks**:
1. **Test direct copy method**
   - Download with curl command
   - Verify all files copied correctly
   - Test AI behavior works immediately

2. **Test git submodule method**
   - Add submodule to test repository
   - Create symlink successfully
   - Test update process

3. **Test git subtree method**
   - Add subtree to test repository
   - Test update without conflicts
   - Verify file integrity

4. **Test cross-platform compatibility**
   - Test on Windows PowerShell
   - Test on macOS Terminal
   - Test on Linux bash

**Validation**:
- [ ] Direct copy works on all platforms
- [ ] Submodule setup completes successfully
- [ ] Subtree updates work correctly
- [ ] All methods preserve functionality

#### Day 5: Documentation Updates

##### Task 5.1: Update `README.md`
**Goal**: Replace bootstrap instructions with rules-based approach

**Subtasks**:
1. **Replace installation section**
   - Remove bootstrap script references
   - Add 3 integration methods
   - Include quick start guide

2. **Update project overview**
   - Explain rules-based distribution
   - Highlight simplicity benefits
   - Update workflow descriptions

3. **Add migration section**
   - Guide for existing users
   - Deprecation timeline
   - Support information

**Validation**:
- [ ] Bootstrap references removed
- [ ] 3 integration methods documented
- [ ] Migration guide is clear
- [ ] File follows DSS structure

##### Task 5.2: Update project documentation
**Goal**: Align all docs with new approach

**Subtasks**:
1. **Update `docs/DSS_OVERVIEW.md`**
   - Remove bootstrap script references
   - Add rules distribution explanation
   - Update getting started section

2. **Update `INDEX.md`**
   - Reflect new repository structure
   - Add .cursor/rules/ section
   - Update file organization

3. **Create migration guide**
   - Document migration steps for existing users
   - Include backup procedures
   - Add troubleshooting for migration issues

**Validation**:
- [ ] Overview updated consistently
- [ ] INDEX.md reflects new structure
- [ ] Migration guide is comprehensive
- [ ] All docs reference new approach

#### Day 6: Testing and Validation

##### Task 6.1: Integration testing
**Goal**: Comprehensive testing across scenarios

**Subtasks**:
1. **Test with fresh repository**
   - Create new empty repository
   - Install DSS rules using each method
   - Verify AI behavior is correct
   - Test file creation and maintenance

2. **Test with existing DSS project**
   - Use current DSS project
   - Replace old rules with new ones
   - Verify no behavior regression
   - Test all workflows

3. **Test update scenarios**
   - Simulate rule updates
   - Test each update method
   - Verify customizations preserved
   - Check for conflicts

**Validation**:
- [ ] Fresh install works perfectly
- [ ] Existing projects migrate successfully
- [ ] Updates work smoothly
- [ ] No functionality lost

##### Task 6.2: User experience testing
**Goal**: Ensure setup is truly simple

**Subtasks**:
1. **Time setup process**
   - Measure direct copy: target < 2 minutes
   - Measure submodule setup: target < 5 minutes
   - Measure subtree setup: target < 3 minutes

2. **Test with non-technical users**
   - Provide instructions only
   - Observe friction points
   - Document common questions

3. **Validate documentation clarity**
   - Check instructions are unambiguous
   - Verify examples work exactly as written
   - Test troubleshooting effectiveness

**Validation**:
- [ ] All methods complete within time targets
- [ ] Non-technical users succeed
- [ ] Documentation needs no clarification
- [ ] Troubleshooting resolves issues

### Phase 3: Migration Execution (Days 7-9)

#### Day 7: Repository Restructure

##### Task 7.1: Clean up meta directory
**Goal**: Remove user-facing content, keep development tools

**Subtasks**:
1. **Archive obsolete files**
   - Move `meta/assistant_guidelines/` → `docs/🔒archive/assistant_guidelines/`
   - Move `meta/assistant_workflows/` → `docs/🔒archive/assistant_workflows/`
   - Move `dss_bootstrap.py` → `docs/🔒archive/dss_bootstrap.py`

2. **Keep development tools in meta/**
   - Retain `meta/scripts/` for DSS development
   - Keep `meta/config/` for development configuration
   - Maintain `meta/development_queue/` for roadmap items

3. **Update meta/dss_config.yml**
   - Add note that this is for DSS development
   - Reference rules/config/dss_config.yml for users
   - Update ignore patterns if needed

**Validation**:
- [ ] User-facing content moved to archive
- [ ] Development tools remain in meta/
- [ ] Config file properly referenced
- [ ] Archive follows convention

##### Task 7.2: Update file references
**Goal**: Fix all broken links and references

**Subtasks**:
1. **Update internal documentation links**
   - Fix links in `docs/` files
   - Update `INDEX.md` references
   - Correct `meta/` documentation

2. **Update script imports**
   - Fix imports in `src/` files
   - Update script references
   - Correct configuration paths

3. **Fix cross-references**
   - Update provides/requires relationships
   - Fix template references
   - Correct workflow links

**Validation**:
- [ ] No broken links in documentation
- [ ] Scripts import correctly
- [ ] All cross-references work
- [ ] Provides/requires are accurate

##### Task 7.3: Repository structure validation
**Goal**: Ensure new structure follows DSS conventions

**Subtasks**:
1. **Validate folder structure**
   - Check .cursor/rules/ organization
   - Verify meta/ contains only development tools
   - Confirm docs/ structure is correct

2. **Update INDEX.md**
   - Reflect new .cursor/rules/ section
   - Update meta/ description
   - Add migration notes

3. **Validate metadata consistency**
   - Check frontmatter in all files
   - Verify provides/requires relationships
   - Confirm tags are consistent

**Validation**:
- [ ] Structure follows DSS conventions
- [ ] INDEX.md is comprehensive
- [ ] Metadata is consistent
- [ ] All files have proper frontmatter

#### Day 8: Final Testing and Documentation

##### Task 8.1: End-to-end testing
**Goal**: Complete validation before release

**Subtasks**:
1. **Test complete workflow**
   - Fresh repository setup
   - Rule installation
   - Project development simulation
   - Update process

2. **Cross-platform verification**
   - Test Windows PowerShell completion
   - Test macOS Terminal completion  
   - Test Linux bash completion

3. **Performance validation**
   - Verify rule loading speed
   - Check AI response quality
   - Confirm no degradation

**Validation**:
- [ ] End-to-end workflow succeeds
- [ ] All platforms work correctly
- [ ] Performance meets standards
- [ ] No quality degradation

##### Task 8.2: Release preparation
**Goal**: Prepare for public release

**Subtasks**:
1. **Create release tag**
   - Tag version for new approach
   - Document breaking changes
   - Include migration timeline

2. **Prepare changelog**
   - Document all changes
   - Include migration instructions
   - Add deprecation notices

3. **Update project status**
   - Mark roadmap items as complete
   - Update project documentation
   - Prepare announcement

**Validation**:
- [ ] Release properly tagged
- [ ] Changelog is comprehensive
- [ ] Documentation updated
- [ ] Ready for announcement

#### Day 9: Support and Monitoring

##### Task 9.1: User support preparation
**Goal**: Ready to help users migrate

**Subtasks**:
1. **Prepare support documentation**
   - Common migration issues
   - Quick troubleshooting guide
   - Contact information

2. **Monitor for issues**
   - Watch GitHub issues
   - Check discussion forums
   - Monitor social media mentions

3. **Document problems and solutions**
   - Track common issues
   - Update troubleshooting guide
   - Improve documentation based on feedback

**Validation**:
- [ ] Support docs are ready
- [ ] Monitoring systems active
- [ ] Issue tracking configured
- [ ] Team ready to respond

## Success Metrics

### User Experience
- **Setup time**: < 5 minutes for any integration method
- **Success rate**: > 95% successful setups on first try
- **User satisfaction**: Positive feedback on simplicity
- **Adoption rate**: > 80% of users migrate within 4 weeks

### Technical Quality
- **Rule effectiveness**: AI behavior matches expectations
- **Update reliability**: Updates work smoothly across all methods
- **Documentation accuracy**: No significant gaps or errors
- **Performance**: No degradation in AI response quality

## Related Documentation

- [Cursor Rules Integration Plan](../integrations/cursor_rules_integration.md) - Detailed technical approach
- [Current Assistant Guidelines](../assistant_guidelines/) - What we're consolidating
- [DSS Guide](../DSS_GUIDE.md) - Core concepts being migrated

This migration represents a fundamental shift toward simplicity, transparency, and user control while maintaining the intelligence and structure that makes DSS valuable for AI-assisted development. 