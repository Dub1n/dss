---
task_id: "maintenance-heavy-08"
max_score: 100
evaluator_version: "1.0"
hidden: true
evaluation_categories: [template_usage, maintenance_integration, cross_reference_management, documentation_consistency, integration_quality, project_coherence]
rule_effectiveness_focus: true
---

# MARKING SCHEME: Legacy Code Integration & Documentation Overhaul (HIDDEN)

> **⚠️ DO NOT SHOW THIS TO THE ASSISTANT DURING TESTING**

This rubric focuses on whether DSS rules enable automatic maintenance integration and template-first approaches versus isolated file creation.

## Scoring Breakdown (100 points total)

### 1. Template Usage (30 points)

#### Template Discovery Evidence (10 points)

* [ ] **Checked existing patterns** (5 points)
  * ✅ Examined `src/models/user.py` for model patterns
  * ✅ Reviewed `src/auth/authentication.py` for service patterns
  * ✅ Analyzed existing documentation formats
  * ❌ No evidence of pattern checking

* [ ] **Used existing file structures as templates** (5 points)
  * ✅ Followed established file organization patterns
  * ✅ Used consistent naming conventions
  * ❌ Created files without pattern consideration

#### Pattern Following Implementation (12 points)

* [ ] **Consistent frontmatter patterns** (4 points)
  * ✅ Frontmatter matches existing file patterns
  * ✅ Same fields and structure as established files
  * ❌ Inconsistent or ad-hoc frontmatter

* [ ] **Naming convention consistency** (4 points)
  * ✅ File names follow project conventions
  * ✅ Function/class names match existing patterns
  * ❌ Inconsistent naming conventions

* [ ] **Structural consistency** (4 points)
  * ✅ Code organization matches existing patterns
  * ✅ Import patterns follow established conventions
  * ❌ Different structure from existing files

#### Documentation Templating (8 points)

* [ ] **Documentation format consistency** (4 points)
  * ✅ New docs match existing documentation format
  * ✅ Section structure follows established patterns
  * ❌ Different format from existing docs

* [ ] **Content organization patterns** (4 points)
  * ✅ Uses same organization approach as existing docs
  * ✅ Consistent style and tone
  * ❌ Different organization approach

### 2. Maintenance Integration (40 points)

#### Cross-Reference Updates (15 points)

* [ ] **Updated existing documentation** (8 points)
  * ✅ Added notification references to `docs/authentication.md`
  * ✅ Updated user-related documentation
  * ✅ Added cross-references in relevant docs
  * ⚠️ Some updates missing (-3 points each)
  * ❌ No existing doc updates

* [ ] **Proper mdc: link usage** (4 points)
  * ✅ Used `mdc:path/to/file` syntax correctly
  * ✅ All internal links use proper format
  * ❌ Incorrect or missing mdc: links

* [ ] **Bidirectional linking** (3 points)
  * ✅ Related files reference each other appropriately
  * ✅ New files linked from existing relevant docs
  * ❌ No bidirectional linking consideration

#### Dependency Tracking (12 points)

* [ ] **Frontmatter provides/requires accuracy** (6 points)
  * ✅ Accurate provides fields for new functionality
  * ✅ Correct requires fields for dependencies
  * ✅ Updated existing files' dependencies
  * ❌ Inaccurate or missing dependency info

* [ ] **Dependency chain maintenance** (6 points)
  * ✅ Updated user model frontmatter for notification dependencies
  * ✅ Updated auth module frontmatter for notification integration
  * ✅ Maintained dependency accuracy across all affected files
  * ❌ Broke or ignored dependency chains

#### Documentation Consistency (13 points)

* [ ] **Maintained style consistency** (5 points)
  * ✅ Documentation style matches existing docs
  * ✅ Consistent formatting and structure
  * ❌ Different style from existing documentation

* [ ] **Updated related content** (4 points)
  * ✅ Updated user documentation to mention notifications
  * ✅ Updated auth documentation with notification integration
  * ❌ No updates to related content

* [ ] **Link integrity maintenance** (4 points)
  * ✅ All links work correctly
  * ✅ No broken references introduced
  * ❌ Broken links or poor link maintenance

### 3. Integration Quality (30 points)

#### Code Integration Excellence (18 points)

* [ ] **Proper integration with user system** (6 points)
  * ✅ Extended user model appropriately for notification preferences
  * ✅ Maintained existing user functionality
  * ✅ Clean integration without breaking changes
  * ❌ Poor or missing user system integration

* [ ] **Authentication system integration** (6 points)
  * ✅ Added notification triggers to auth events
  * ✅ Used existing auth patterns for permission checking
  * ✅ Proper integration without breaking existing auth
  * ❌ Poor or missing auth integration

* [ ] **Service architecture consistency** (6 points)
  * ✅ Notification service follows existing service patterns
  * ✅ Proper separation of concerns maintained
  * ✅ Consistent error handling and logging approach
  * ❌ Poor service architecture or inconsistent patterns

#### DSS Compliance (12 points)

* [ ] **Proper file placement** (4 points)
  * ✅ Files placed in logical directories following project structure
  * ✅ Services in `src/services/`, models in `src/models/`, etc.
  * ❌ Poor file placement or organization

* [ ] **Complete frontmatter** (4 points)
  * ✅ All files have complete DSS frontmatter
  * ✅ Proper tags, provides, requires fields
  * ❌ Missing or incomplete frontmatter

* [ ] **Cross-file coordination** (4 points)
  * ✅ Changes coordinated across multiple files appropriately
  * ✅ All affected files updated consistently
  * ❌ Poor coordination or isolated changes

## Rule Effectiveness Indicators

### Strong Rule Utilization (85-100 points)

* Clear evidence of template checking before file creation
* Automatic maintenance of cross-references and documentation
* Consistent patterns and conventions across all new files
* Proactive updates to existing documentation
* Sound integration following established patterns

### Moderate Rule Utilization (65-84 points)

* Some template usage but inconsistent application
* Partial maintenance of cross-references
* Basic pattern following with some inconsistencies
* Some documentation updates but not comprehensive
* Reasonable integration but missing some connections

### Weak Rule Utilization (45-64 points)

* Minimal template consideration
* Poor maintenance integration
* Inconsistent patterns and conventions
* Little documentation update beyond new files
* Basic integration without following established patterns

### No Rule Utilization (Below 45 points)

* No evidence of template usage
* No maintenance of existing documentation
* Files created in isolation without pattern consideration
* No cross-reference updates or link maintenance
* Poor integration that doesn't follow project conventions

## Deductions & Bonuses

### Major Deductions

* **No template consideration:** -15 points
* **No maintenance of existing docs:** -20 points
* **Broken cross-references:** -10 points
* **Poor integration patterns:** -15 points
* **Isolated file creation:** -25 points

### Bonus Points (up to +10)

* **Exceptional template utilization:** +3 points
* **Proactive maintenance beyond requirements:** +4 points
* **Creative but consistent integration patterns:** +3 points

## Evaluation Focus

This test specifically measures:

1. **Template-first approach effectiveness**
2. **Automatic maintenance integration capabilities**
3. **Cross-reference and link management**
4. **Documentation consistency enforcement**
5. **Project-wide coordination and integration**

**Key Question:** Does an assistant with DSS rules automatically handle maintenance
and follow templates while one without rules creates isolated files?

## Red Flags for Poor Rule Effectiveness

* Files created without checking existing patterns
* No updates to existing documentation when adding new functionality
* Inconsistent frontmatter and conventions across files
* Poor cross-reference management and link integrity
* Integration done in isolation without considering project patterns

## Expected Score Patterns

### With Effective Rules

* High template usage scores (25+ points)
* Strong maintenance integration (35+ points)
* Excellent cross-reference management
* Automatic documentation consistency

### Without Effective Rules

* Low template usage (isolated file creation)
* Poor maintenance integration (no doc updates)
* Broken or missing cross-references
* Inconsistent patterns and conventions

## Specific Evidence to Look For

### Template Usage Evidence

* Comments or actions showing pattern analysis
* Consistent file structures matching existing files
* Similar frontmatter patterns across all files

### Maintenance Integration Evidence

* Updates to `docs/authentication.md` referencing notifications
* Cross-references between notification docs and existing docs
* Updated frontmatter dependencies in modified files

### Poor Rule Utilization Evidence

* Files created without examining existing patterns
* No updates to existing documentation
* Inconsistent or missing frontmatter
* No cross-references or link maintenance

***

**Expected Score Differential:**
Assistants with effective DSS rules should score 25-35 points higher than those without rules on this maintenance-heavy task.
