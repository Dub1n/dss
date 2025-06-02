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
│   ├── 00-dss-core.mdc        # ✅ Core DSS concepts
│   ├── 01-dss-behavior.mdc    # ✅ Assistant behavior
│   ├── workflows/              # ✅ All 8 workflow files
│   ├── guidelines/             # ✅ All 11 guideline files  
│   └── config/                 # ✅ Configuration and templates
├── meta/
│   ├── assistant_guidelines/   # 🔄 Legacy (preserved for reference)
│   ├── assistant_workflows/    # 🔄 Legacy (preserved for reference)
│   ├── templates/             # 🔄 Legacy (preserved for reference)
│   ├── scripts/               # ✅ Bootstrap and utility scripts
│   └── DSS_GUIDE.md          # ✅ Core DSS documentation
├── dss_bootstrap.py           # 🔄 Will be deprecated
└── src/dss_gpt_bridge/        # ✅ GPT integration code
```

### What Needs to Change
1. **✅ Consolidate rules**: Merge scattered guidelines into organized rule files
2. **🔄 Restructure distribution**: Move from script-based to file-based distribution
3. **🔄 Simplify user experience**: Replace complex bootstrap with simple file copying
4. **✅ Improve maintainability**: Make rules easier to update and customize
5. **🔄 Enable version control**: Let users track DSS updates via git

## ⚠️ Critical Requirements for Cursor Rules

### File Naming Requirements
- **Must use kebab-case**: `00-dss-core.mdc`, `01-dss-behavior.mdc`
- **Must have .mdc extension**: Cursor only loads .mdc files as rules
- **Sequential numbering**: Use 00-, 01-, 02- prefixes for loading order
- **Not .md**: Markdown files (.md) are NOT loaded as rules by Cursor

### Manual Cursor Configuration Required
- User must manually set new rule files to "Always included in prompts" in Cursor
- Cannot be automated - requires manual UI interaction in Cursor
- Each new rule file needs individual configuration

## Detailed Migration Tasks

### Phase 1: Create New Rules Structure (Days 1-3)

#### Day 1: Core Rules Files

##### Task 1.1: Create `.cursor/rules/00-dss-core.mdc`
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

5. **Save with correct naming: `00-dss-core.mdc`**
   - Use kebab-case naming
   - Use .mdc extension (not .md)
   - Include sequential prefix 00-

**Validation**:
- [x] File contains all 6 core folder definitions
- [x] Metadata fields (tags, provides, requires) are documented with examples
- [x] Archive convention is clearly stated
- [x] File follows DSS frontmatter format
- [x] File named correctly: `00-dss-core.mdc`

##### Task 1.2: Create `.cursor/rules/01-dss-behavior.mdc`
**Goal**: Define assistant personality and core behaviors

**Subtasks**:
1. **Extract Riley personality from user-specific rules**
   - Include "nonbinary senior code dev" definition
   - Add "thoughtful PR reviewer" behavior
   - Include "concise with care" communication style
   - Add incremental work approach
   - Include collaborative peer mindset

2. **Extract behavior rules from `meta/assistant_guidelines/`**
   - Consolidate from `documentation_task_management.md`
   - Include from `maintenance_checklist.md`
   - Add from `installation_report_submission.md`
   - Extract from `overarching_principles.md`

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
   - Add dry humor permission

6. **Save with correct naming: `01-dss-behavior.mdc`**
   - Use kebab-case naming
   - Use .mdc extension (not .md)
   - Include sequential prefix 01-

**Validation**:
- [x] Riley personality is fully defined
- [x] All 5 core behaviors are documented
- [x] File creation workflow has 5 clear steps
- [x] Response style includes citation format
- [x] File follows DSS frontmatter format
- [x] File named correctly: `01-dss-behavior.mdc`

##### Task 1.3: Test Core Rules
**Goal**: Verify new rules work correctly

**Subtasks**:
1. **Backup old rules**
   - Rename old `.mdc` files to `.mdc.backup`
   - Keep only new `00-dss-core.mdc` and `01-dss-behavior.mdc` active
   - Ensure clean testing environment

2. **Manual Cursor configuration**
   - User must set `00-dss-core.mdc` to "Always included in prompts"
   - User must set `01-dss-behavior.mdc` to "Always included in prompts"
   - Cannot be automated - requires manual UI steps

3. **Test with simple DSS task**
   - Create a new markdown file
   - Verify frontmatter is added correctly
   - Check that INDEX.md update is suggested

4. **Test personality consistency**
   - Ask for code review
   - Verify Riley personality shows through
   - Check response style matches guidelines
   - Confirm incremental approach

5. **Validate rule loading**
   - Confirm Cursor loads new .mdc rules
   - Check no syntax errors in rule files
   - Verify behavior changes are active
   - Test that old rules are not interfering

**Validation**:
- [x] Backup files created successfully (`.mdc.backup`)
- [x] Only new rule files active in `.cursor/rules/`
- [x] New file creation follows 5-step workflow
- [x] AI personality matches Riley definition
- [x] No rule loading errors
- [x] User has manually configured Cursor to include new rules

#### Day 2: Workflow Rules

##### Task 2.1: Create `.cursor/rules/02-dss-workflows.mdc`
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

6. **Save with correct naming: `02-dss-workflows.mdc`**
   - Use kebab-case naming
   - Use .mdc extension
   - Include sequential prefix 02-

**Note**: This was implemented as modular workflow files instead of single consolidated file

**Validation**:
- [x] All 8 workflow types are documented (in separate files)
- [x] Each workflow has clear process steps
- [x] Decision tree helps choose workflow (in 00-workflow-selection.mdc)
- [x] Files follow DSS frontmatter format
- [x] Files named correctly with .mdc extensions

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
- [x] Workflow transitions are documented (in workflow-selection.mdc)
- [x] Cross-dependencies are clear
- [x] No gaps in scenario coverage
- [x] Terminology is consistent

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
- [x] Quick tasks complete in 1-2 steps
- [x] Code modifications follow 5-step process
- [x] Complex tasks trigger decomposition
- [x] Workflow selection is accurate

#### Day 3: Templates and Maintenance

##### Task 3.1: Create `.cursor/rules/03-dss-templates.mdc`
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

6. **Save with correct naming: `03-dss-templates.mdc`**
   - Use kebab-case naming
   - Use .mdc extension
   - Include sequential prefix 03-

**Note**: This was implemented as guidelines/00-dss-templates.mdc

**Validation**:
- [x] Python template includes frontmatter and docstrings
- [x] Documentation template has all 4 sections
- [x] Common patterns are extracted and documented
- [x] Usage guidelines are clear
- [x] File follows DSS frontmatter format
- [x] File named correctly: `00-dss-templates.mdc`

##### Task 3.2: Create `.cursor/rules/04-dss-maintenance.mdc`
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

5. **Save with correct naming: `04-dss-maintenance.mdc`**
   - Use kebab-case naming
   - Use .mdc extension
   - Include sequential prefix 04-

**Note**: This was implemented as guidelines/01-dss-maintenance.mdc

**Validation**:
- [x] All 5 automatic triggers are documented
- [x] Regular tasks are clearly defined
- [x] 5-step workflow is documented
- [x] Validation rules are comprehensive
- [x] File follows DSS frontmatter format
- [x] File named correctly: `01-dss-maintenance.mdc`

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

4. **Create `.cursor/rules/config/structure-guide.mdc`**
   - Document configuration options
   - Explain template usage
   - Include customization guide

**Validation**:
- [x] Config directory created with structure-guide.mdc
- [x] Template files are present in config/templates/
- [x] Template directory includes various template types
- [x] Directory follows DSS structure

### Phase 2: Distribution Infrastructure (Days 4-6)

#### Day 4: Documentation and Update Scripts

##### Task 4.1: Create `.cursor/rules/README.md`
**Goal**: Comprehensive setup and usage documentation

**Subtasks**:
1. **Document Method 1: Direct Copy**
   - Provide curl command for downloading
   - Include manual download steps
   - Add verification steps
   - **Important**: Emphasize .mdc file requirements

2. **Document Method 2: Git Submodule**
   - Step-by-step submodule setup
   - Symlink creation commands
   - Update procedures
   - **Important**: Note that .mdc files need manual Cursor configuration

3. **Document Method 3: Git Subtree**
   - Subtree add command
   - Update command
   - Conflict resolution

4. **Add troubleshooting section**
   - Common issues and solutions
   - Platform-specific considerations
   - Verification procedures
   - **Important**: Cursor rule configuration troubleshooting

5. **Include customization guide**
   - How to add local overrides
   - Configuration modification
   - Template customization
   - **Important**: File naming requirements for new rules

**Validation**:
- [ ] All 3 integration methods documented
- [ ] Each method has step-by-step instructions
- [ ] Troubleshooting covers common issues
- [ ] Customization guide is complete
- [ ] File follows DSS frontmatter format
- [ ] .mdc requirements clearly documented
- [ ] Manual Cursor configuration steps included

##### Task 4.2: Create update scripts
**Goal**: Convenient update mechanisms for users

**Subtasks**:
1. **Create `.dss-update.sh` script**
   - Use GitHub API to fetch latest rules
   - Backup existing rules before update
   - Validate downloaded files
   - Restore customizations if possible
   - **Important**: Preserve .mdc file extensions

2. **Create `validate-dss-rules.py` script**
   - Check frontmatter format in all rule files
   - Validate markdown syntax
   - Verify file references exist
   - Check configuration consistency
   - **Important**: Validate .mdc file naming

3. **Add update documentation**
   - When to update
   - How to preserve customizations
   - Rollback procedures
   - **Important**: Note that Cursor configuration may need manual update

**Validation**:
- [ ] Update script downloads correctly
- [ ] Validation script catches errors
- [ ] Documentation covers update process
- [ ] Scripts work on Windows/Mac/Linux
- [ ] .mdc naming validation included

##### Task 4.3: Test distribution methods
**Goal**: Verify all integration approaches work

**Subtasks**:
1. **Test direct copy method**
   - Download with curl command
   - Verify all files copied correctly
   - Test AI behavior works immediately
   - **Important**: Verify .mdc files are copied with correct extensions

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

5. **Test Cursor integration**
   - Verify .mdc files load in Cursor
   - Test manual configuration process
   - Verify rule behavior changes

**Validation**:
- [ ] Direct copy works on all platforms
- [ ] Submodule setup completes successfully
- [ ] Subtree updates work correctly
- [ ] All methods preserve functionality
- [ ] .mdc files load correctly in Cursor
- [ ] Manual Cursor configuration tested

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

## Migration Status Summary

### ✅ Completed (Phase 1)
- **Core Rules Structure**: All essential rule files created and operational
  - `00-dss-core.mdc` - DSS concepts, folder structure, metadata system
  - `01-dss-behavior.mdc` - Riley personality, behaviors, response guidelines
  
- **Modular Workflow System**: Complete 8-workflow implementation
  - `workflows/00-workflow-selection.mdc` - Decision tree and comparison matrix
  - `workflows/01-quick-tasks.mdc` - Simple atomic tasks
  - `workflows/02-code-modification.mdc` - Development-focused changes
  - `workflows/03-documentation-driven.mdc` - Documentation-first planning
  - `workflows/04-task-decomposition.mdc` - Complex multi-step coordination
  - `workflows/05-documentation-refactoring.mdc` - Systematic doc updates
  - `workflows/06-github-issues-integration.mdc` - Community feedback processing
  - `workflows/07-development-queue.mdc` - Continuous improvement

- **Comprehensive Guidelines**: All 11 supporting guideline files
  - `guidelines/00-dss-templates.mdc` - Template patterns and usage
  - `guidelines/01-dss-maintenance.mdc` - Automatic maintenance behaviors
  - `guidelines/02-assistant-adherence.mdc` - Internal process adherence
  - `guidelines/03-naming-conventions.mdc` - LLM-optimized naming
  - `guidelines/04-validation-rules.mdc` - Frontmatter validation
  - `guidelines/08-github-issue-labels.mdc` - Issue label conventions
  - `guidelines/06-backlink-conventions.mdc` - Cross-reference management
  - `guidelines/07-folder-readme-policy.mdc` - Directory documentation
  - `guidelines/05-tag-conventions.mdc` - Tagging system
  - `guidelines/09-error-recovery.mdc` - Error handling and self-correction
  - `guidelines/10-feedback-loop.mdc` - Continuous improvement

- **Configuration Infrastructure**: Config directory with templates and structure guide
  - `config/structure-guide.mdc` - Setup instructions and organization
  - `config/templates/` - Reference templates for file creation

### 🔄 In Progress (Phase 2)
- **Distribution Documentation**: README for installation methods
- **Update Scripts**: Automated update and validation tools
- **Cross-Platform Testing**: Verification across operating systems
- **Integration Testing**: End-to-end user experience validation

### ⏳ Pending 
- **Bootstrap Deprecation**: Transition away from `dss_bootstrap.py`
- **Legacy Cleanup**: Archive old assistant_guidelines and assistant_workflows
- **User Migration Guide**: Comprehensive migration documentation
- **Version Control Integration**: Git-based distribution methods

### 📊 Key Metrics
- **Rule Files**: 22/22 created (100%)
- **Workflow Coverage**: 8/8 workflows implemented (100%)
- **Guideline Coverage**: 11/11 guidelines implemented (100%)
- **Template System**: Functional with reference templates
- **AI Behavior**: Riley personality fully operational
- **Manual Configuration**: Required for Cursor rule activation

### 🎯 Next Steps
1. Create comprehensive `.cursor/rules/README.md` with installation methods
2. Develop update scripts for automated rule management
3. Test distribution methods across platforms
4. Create user migration documentation
5. Implement automated validation tools

This migration represents a fundamental shift toward simplicity, transparency, and user control while maintaining the intelligence and structure that makes DSS valuable for AI-assisted development. 