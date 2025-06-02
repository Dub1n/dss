---
task_id: "complex-integration-06"
max_score: 100
evaluator_version: "1.0"
hidden: true
evaluation_categories: [workflow_selection, rule_utilization, cross_file_coordination, maintenance_integration, architectural_decisions, technical_implementation]
rule_effectiveness_focus: true
---

# MARKING SCHEME: Complex Feature Integration (HIDDEN)

> **⚠️ DO NOT SHOW THIS TO THE ASSISTANT DURING TESTING**

This rubric focuses on **rule effectiveness** rather than basic competence.  
It tests whether DSS rules actually help assistants work better on complex tasks.

## Scoring Breakdown (100 points total)

### 1. Workflow Selection & Application (20 points)

#### Workflow Identification (10 points)

* [ ] **Recognized task complexity** (5 points)
  * ✅ Identified this as multi-file coordination task
  * ✅ Chose appropriate workflow (task decomposition, code modification, etc.)
  * ⚠️ Partial recognition (-2 points)
  * ❌ Treated as simple single-file task

* [ ] **Applied workflow steps** (5 points)
  * ✅ Followed structured workflow approach
  * ✅ Broke down task into phases/steps
  * ❌ Ad-hoc approach without structure

#### Rule Adherence Evidence (10 points)

* [ ] **Template-first approach** (3 points)
  * ✅ Checked for existing patterns before creating new files
  * ✅ Used existing file structures as templates
  * ❌ Created files from scratch without checking patterns

* [ ] **Maintenance integration** (4 points)
  * ✅ Updated cross-references automatically
  * ✅ Maintained frontmatter dependencies
  * ✅ Updated documentation links
  * ❌ Created files without considering maintenance

* [ ] **DSS guideline following** (3 points)
  * ✅ Clear evidence of following DSS principles
  * ✅ Consistent application of conventions
  * ❌ Generic approach without DSS consideration

### 2. Cross-File Coordination (25 points)

#### Dependency Analysis (10 points)

* [ ] **Identified existing dependencies** (5 points)
  * ✅ Analyzed relationship between User and Auth modules
  * ✅ Understood integration requirements
  * ❌ Missed key dependencies

* [ ] **Planned coordination** (5 points)
  * ✅ Clear strategy for integrating with existing code
  * ✅ Considered impact on multiple files
  * ❌ Piecemeal approach without coordination

#### Implementation Coordination (15 points)

* [ ] **Multiple file updates** (8 points)
  * ✅ Modified/extended existing user model appropriately
  * ✅ Created API endpoints with proper integration
  * ✅ Added utilities where appropriate
  * ⚠️ Some files missing or poorly integrated (-3 points each)
  * ❌ Single file approach

* [ ] **Consistency across files** (4 points)
  * ✅ Consistent patterns and conventions
  * ✅ Matching frontmatter and dependencies
  * ❌ Inconsistent implementation

* [ ] **Integration testing consideration** (3 points)
  * ✅ Demonstrated understanding of how files work together
  * ✅ Proper imports and references
  * ❌ Files don't properly integrate

### 3. Template Usage & Pattern Recognition (15 points)

#### Pattern Analysis (8 points)

* [ ] **Analyzed existing patterns** (4 points)
  * ✅ Studied existing user.py structure
  * ✅ Examined auth.py for integration patterns
  * ❌ Didn't examine existing code for patterns

* [ ] **Applied learned patterns** (4 points)
  * ✅ Used consistent naming conventions
  * ✅ Followed existing architectural patterns
  * ❌ Ignored existing patterns

#### Template Utilization (7 points)

* [ ] **DSS template awareness** (3 points)
  * ✅ Evidence of checking for templates
  * ✅ Used template-based approach
  * ❌ No evidence of template consideration

* [ ] **Frontmatter templating** (2 points)
  * ✅ Consistent frontmatter patterns
  * ❌ Ad-hoc frontmatter creation

* [ ] **Documentation templating** (2 points)
  * ✅ Followed documentation patterns
  * ❌ Generic documentation without patterns

### 4. Maintenance Integration (15 points)

#### Automatic Maintenance (10 points)

* [ ] **Cross-reference management** (4 points)
  * ✅ Added mdc: links between related files
  * ✅ Updated existing documentation with new references
  * ❌ No cross-reference considerations

* [ ] **Dependency tracking** (3 points)
  * ✅ Accurate provides/requires in frontmatter
  * ✅ Updated dependencies when adding new functionality
  * ❌ Inaccurate or missing dependency info

* [ ] **Documentation updates** (3 points)
  * ✅ Updated existing docs to reference new functionality
  * ✅ Maintained documentation consistency
  * ❌ Created new docs without updating existing ones

#### Project Integration (5 points)

* [ ] **INDEX/navigation consideration** (2 points)
  * ✅ Mentioned or updated project navigation
  * ❌ No consideration of project-wide navigation

* [ ] **Tag consistency** (1 point)
  * ✅ Consistent tagging across all files
  * ❌ Inconsistent or missing tags

* [ ] **Version/status tracking** (2 points)
  * ✅ Proper status fields in frontmatter
  * ✅ Version considerations
  * ❌ No status/version tracking

### 5. Architectural Decision Making (15 points)

#### Decision Quality (8 points)

* [ ] **Model architecture decision** (3 points)
  * ✅ Clear decision on User extension vs. separate Profile model
  * ✅ Justified architectural choice
  * ❌ No clear architectural decision

* [ ] **API design decisions** (3 points)
  * ✅ Sound RESTful API design
  * ✅ Proper error handling strategy
  * ❌ Poor or no API design consideration

* [ ] **Integration strategy** (2 points)
  * ✅ Clear strategy for auth integration
  * ❌ Ad-hoc integration approach

#### Decision Documentation (7 points)

* [ ] **Rationale provided** (4 points)
  * ✅ Documented reasoning for major decisions
  * ✅ Explained trade-offs considered
  * ❌ Decisions made without explanation

* [ ] **Impact consideration** (3 points)
  * ✅ Considered impact on existing codebase
  * ✅ Addressed potential breaking changes
  * ❌ No impact consideration

### 6. Technical Implementation (10 points)

#### Code Quality (6 points)

* [ ] **Syntax and functionality** (3 points)
  * ✅ Syntactically correct code
  * ✅ Logical implementation
  * ❌ Syntax errors or logical flaws

* [ ] **Integration correctness** (3 points)
  * ✅ Proper imports and dependencies
  * ✅ Correct use of existing modules
  * ❌ Integration errors

#### Completeness (4 points)

* [ ] **Requirement fulfillment** (4 points)
  * ✅ All major requirements addressed
  * ⚠️ Most requirements met (-1 point per missing major requirement)
  * ❌ Major requirements missing

## Rule Effectiveness Indicators

### Strong Rule Utilization (90-100 points)

* Clear evidence of workflow selection and application
* Template-first approach with pattern recognition
* Automatic maintenance integration
* Coordinated multi-file changes
* Sound architectural decisions with documentation

### Moderate Rule Utilization (70-89 points)

* Some workflow structure but inconsistent application
* Partial template usage
* Some maintenance considerations
* Basic cross-file coordination
* Reasonable decisions but poor documentation

### Weak Rule Utilization (50-69 points)

* Little evidence of structured workflow
* Minimal template usage
* Poor maintenance integration
* Limited cross-file coordination
* Ad-hoc decisions without justification

### No Rule Utilization (Below 50 points)

* Ad-hoc approach without structure
* No evidence of template consideration
* No maintenance integration
* Single-file or poorly coordinated approach
* Poor architectural decisions

## Deductions & Bonuses

### Major Deductions

* **No workflow structure:** -20 points
* **Single file approach:** -15 points
* **No template consideration:** -10 points
* **Poor cross-file coordination:** -15 points
* **No maintenance integration:** -10 points

### Bonus Points (up to +10)

* **Exceptional workflow execution:** +3 points
* **Creative template utilization:** +2 points
* **Proactive maintenance beyond requirements:** +3 points
* **Outstanding architectural thinking:** +2 points

## Evaluation Focus

This test specifically measures:

1. **Whether rules help with complex task decomposition**
2. **Template and pattern utilization effectiveness**
3. **Maintenance integration automation**
4. **Cross-file coordination capabilities**
5. **Architectural decision support**

**Key Question:** Does an assistant with good DSS rules significantly outperform one without rules on this complex task?

## Red Flags for Poor Rule Effectiveness

* Assistant treats this as multiple simple tasks instead of coordinated complex task
* No evidence of checking existing patterns or templates
* Creates files without considering integration
* No automatic maintenance of cross-references or documentation
* Ad-hoc decisions without leveraging DSS principles

***

**Expected Score Differential:** Assistants with effective DSS rules should score 15-25 points higher than those without rules on this task.
