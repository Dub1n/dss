---
tags: [templates, documentation, marking-schemes, evaluation, rubrics]
provides: [marking_scheme_template_guide, rubric_creation_patterns, evaluation_categories, scoring_guidelines]
requires: [marking_scheme_template, benchmark_structure, task_categories]
---

# Marking Scheme Template Usage Guide

## Template Variables Reference

### Basic Information

- `{{TASK_ID}}`: Matches the task_id from corresponding task file (e.g., "create-module-01")
- `{{MAX_SCORE}}`: Total points for the task (typically 100)
- `{{EVALUATOR_VERSION}}`: Version string for tracking rubric iterations (e.g., "1.0")
- `{{EVALUATION_CATEGORIES}}`: Comma-separated list of evaluation focus areas
- `{{TASK_TITLE}}`: Human-readable title matching the task

### Rule Effectiveness Focus (Advanced Tasks Only)

- `{{#RULE_EFFECTIVENESS}}...{{/RULE_EFFECTIVENESS}}`: Include this section for advanced tasks testing DSS rules
- `{{RULE_FOCUS_TEXT}}`: Description of what rule behaviors are being tested

### Scoring Structure

- `{{CATEGORY_NUMBER}}`: Sequential numbering (1, 2, 3, etc.)
- `{{CATEGORY_TITLE}}`: Main evaluation category name
- `{{CATEGORY_POINTS}}`: Points allocated to this category
- `{{SUBCATEGORY_TITLE}}`: Subdivision within category
- `{{SUBCATEGORY_POINTS}}`: Points for subcategory

### Criteria Details

- `{{CRITERION_TITLE}}`: Specific item being evaluated
- `{{CRITERION_POINTS}}`: Points for this criterion
- `{{FULL_POINTS_DESCRIPTION}}`: What earns full points
- `{{PARTIAL_DESCRIPTION}}`: Partial credit scenarios
- `{{PARTIAL_DEDUCTION}}`: Points deducted for partial credit
- `{{ZERO_POINTS_DESCRIPTION}}`: What earns zero points

### Scoring Guidelines

- `{{DEDUCTION_REASON}}`: Major deduction categories
- `{{DEDUCTION_AMOUNT}}`: Points deducted
- `{{BONUS_MAX}}`: Maximum bonus points possible
- `{{BONUS_REASON}}`: What earns bonus points
- `{{BONUS_POINTS}}`: Bonus point amounts

### Evaluation Notes

- `{{EXCELLENCE_TITLE}}`: Title for excellence section (e.g., "Excellent Performance Indicators")
- `{{EXCELLENCE_ITEM}}`: Indicators of excellent work
- `{{ISSUE_ITEM}}`: Common problems to watch for
- `{{RED_FLAG_ITEM}}`: Serious issues that indicate failure

### Instructions

- `{{INSTRUCTION_1}}` through `{{INSTRUCTION_5}}`: Step-by-step evaluator instructions

## Evaluation Categories by Task Type

### Basic File Creation Tasks (task-01 style)

**Categories (6):**

- `file_placement` - Where files are created and organized
- `frontmatter_quality` - DSS metadata compliance
- `code_structure` - Function implementation and organization
- `documentation` - Module documentation creation
- `dss_integration` - Cross-references and project integration
- `technical_accuracy` - Syntax and functionality

**Point Distribution:**

- File Placement: 25 points
- Frontmatter Quality: 20 points
- Code Structure: 20 points
- Documentation: 15 points
- DSS Integration: 10 points
- Technical Accuracy: 10 points

### Documentation Tasks (task-02 style)

**Categories (6):**

- `documentation_creation` - File creation and structure
- `content_quality` - Documentation completeness and clarity
- `cross_references` - Internal linking and integration
- `frontmatter_quality` - DSS metadata compliance
- `examples` - Code examples and usage guidance
- `dss_integration` - Project integration

**Point Distribution:**

- Documentation Creation: 20 points
- Content Quality: 25 points
- Cross-References: 20 points
- Frontmatter Quality: 15 points
- Examples and Usage: 15 points
- DSS Integration: 5 points

### Complex Integration Tasks (task-06 style)

**Categories (6):**

- `workflow_selection` - Choosing and applying appropriate workflows
- `rule_utilization` - Evidence of DSS rule usage
- `cross_file_coordination` - Multi-file integration
- `maintenance_integration` - Automatic maintenance behaviors
- `architectural_decisions` - Design choices and documentation
- `technical_implementation` - Code quality and completeness

**Point Distribution:**

- Workflow Selection: 20 points
- Cross-File Coordination: 25 points
- Template Usage & Pattern Recognition: 15 points
- Maintenance Integration: 15 points
- Architectural Decision Making: 15 points
- Technical Implementation: 10 points

### Workflow Application Tasks (task-07 style)

**Categories (4):**

- `workflow_selection` - Choosing appropriate workflow
- `process_following` - Following structured process
- `decision_documentation` - Recording decisions and rationale
- `rule_adherence` - Evidence of DSS rule application

### Maintenance Integration Tasks (task-08 style)

**Categories (6):**

- `template_usage` - Template discovery and application
- `maintenance_automation` - Automatic maintenance behaviors
- `cross_references` - Cross-reference management
- `documentation_consistency` - Maintaining doc consistency
- `integration_quality` - Technical integration
- `project_coherence` - Overall project fit

## Scoring Patterns

### Standard Deductions

**Major Structural Issues:**

- Missing required files: -5 to -20 points
- Incorrect file placement: -10 points
- No frontmatter: -10 to -15 points
- Broken project structure: -20 points
- Non-functional code: -10 points

**Common Deductions by Category:**

- Poor file organization: -3 to -5 points
- Incomplete frontmatter: -1 to -4 points
- Missing documentation: -2 to -10 points
- No cross-references: -15 points
- Syntax errors: -2 to -4 points

### Bonus Point Categories

**Excellence Bonuses (+2 to +5 total):**

- Exceptional organization: +2 points
- Creative but appropriate solutions: +2 points
- Proactive improvements: +3 points
- Security considerations: +2 points
- Additional helpful features: +2 points

## Rubric Patterns by Difficulty

### Basic Tasks (8-10 minutes)

**Focus Areas:**

- File placement and organization
- DSS frontmatter compliance
- Basic code/documentation quality
- Simple cross-references

**Scoring Emphasis:**

- Heavy weight on correct placement and DSS conventions
- Moderate focus on content quality
- Basic technical requirements

### Intermediate Tasks (15 minutes)

**Focus Areas:**

- Workflow selection and application
- Template usage and pattern recognition
- Maintenance integration
- Process documentation

**Scoring Emphasis:**

- Process over pure technical implementation
- Evidence of rule-guided behavior
- Systematic approach demonstration

### Advanced Tasks (20 minutes)

**Focus Areas:**

- Rule effectiveness indicators
- Complex multi-file coordination
- Architectural decision making
- Comprehensive maintenance integration

**Scoring Emphasis:**

- Heavy focus on DSS rule effectiveness
- Multi-dimensional evaluation
- Evidence of advanced rule utilization

## Rule Effectiveness Indicators

### High Effectiveness Indicators (85+ points)

- Clear evidence of template checking and usage
- Automatic maintenance of cross-references and links
- Structured workflow application
- Proactive documentation updates
- Sound architectural decision documentation

### Low Effectiveness Indicators (40-65 points)

- Files created without pattern analysis
- No maintenance of existing documentation
- Ad-hoc approach without workflow structure
- Inconsistent frontmatter and conventions
- Poor integration with existing systems

## Common Evaluation Patterns

### Checkpoint-Style Criteria

Use checkbox format for systematic evaluation:

```markdown
* [ ] **Criterion Title** (X points)
  * ✅ Full points description
  * ⚠️ Partial credit scenario (-Y points)
  * ❌ Zero points description
```

### Point Distribution Guidelines

**File Placement (Basic Tasks):** 20-25% of total points
**DSS Integration (All Tasks):** 10-20% of total points
**Technical Quality (All Tasks):** 10-15% of total points
**Rule Effectiveness (Advanced):** 30-40% of total points

### Evaluator Instructions Template

1. Check each criterion systematically
2. Award points based on rubric, not personal preference
3. Document reasoning for partial credit
4. Note patterns for rule effectiveness analysis
5. Record total score and category breakdown

## Usage Instructions

1. **Copy the template** to create a new marking scheme
2. **Replace all {{VARIABLES}}** with task-specific values
3. **Remove conditional sections** that don't apply
4. **Customize criteria** based on task requirements
5. **Adjust point distributions** based on task complexity
6. **Add task-specific red flags** and common issues
7. **Review against existing rubrics** for consistency

## Key Conventions to Maintain

- **Always mark as hidden** in frontmatter
- **Use warning about not showing to assistant**
- **Include systematic checkbox criteria**
- **Provide clear point distributions**
- **End with evaluator instructions**
- **Use consistent emoji symbols** (✅ ⚠️ ❌)
- **Include rule effectiveness sections** for advanced tasks
- **Document both what to award points for and what to penalize**
