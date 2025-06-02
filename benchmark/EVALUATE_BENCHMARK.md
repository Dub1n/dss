---
tags: [benchmark, evaluation, scoring, rubrics]
provides: [evaluation_workflow, scoring_criteria, results_recording]
requires: [completed_tasks, realistic_rubrics]
---

# Benchmark Evaluation Guide

*Comprehensive scoring and evaluation procedures for completed benchmark tasks.*

## 🎯 Evaluation Overview

**Purpose:** Objectively assess whether DSS rules enabled automatic professional behavior during task completion.

**Key Focus:** Evidence of rule-guided behavior, not just functional completion.

## 🔒 Evaluation Security

### Reveal Evaluation Criteria

**ONLY after task completion:**

```bash
python scripts/run_benchmark.py reveal-schemes
```

This makes evaluation rubrics visible that were hidden during task execution.

### Hidden During Task Execution

- All rubric files were hidden to prevent evaluation contamination
- Task execution should rely purely on DSS rules and task requirements
- No scoring criteria should influence implementation approach

## 📊 Available Evaluations

### Realistic Task Rubrics

- **task-001-rubric.md** - Realistic authentication module evaluation
- **task-01-xs-rubric.md** - Minimal authentication evaluation (if exists)
- **task-06-xs-rubric.md** - Profile management evaluation
- **task-08-xs-rubric.md** - Notification integration evaluation

### Evaluation Framework

All realistic tasks use the **Automatic Behavior Assessment** framework:

- **40% Automatic DSS Behaviors** - Evidence of rule-guided professionalism
- **35% Technical Solution Quality** - Professional implementation merit  
- **25% Decision-Making Quality** - Intelligence of automatic choices

## 🚀 Evaluation Workflow

### Step 1: Get Evaluation Timestamp

```bash
date
```

Record exact timestamp for evaluation tracking.

### Step 2: Read Appropriate Rubric

Open the evaluation rubric for your completed task:

- `marking-schemes/task-001-rubric.md` for task-001.md
- `marking-schemes/task-01-xs-rubric.md` for task-01-xs.md
- `marking-schemes/task-06-xs-rubric.md` for task-06-xs.md
- `marking-schemes/task-08-xs-rubric.md` for task-08-xs.md

### Step 3: Evidence-Based Scoring

#### Phase 1: Automatic DSS Behaviors (40 points)

**File Organization (10 points):**

- Look for evidence of logical placement without placement instructions
- Check if files follow existing project patterns automatically
- Assess whether organization shows study of existing structure

**Metadata & Documentation (10 points):**

- Check if frontmatter appeared automatically
- Look for documentation created without documentation instructions
- Assess cross-references to existing project files

**Template & Pattern Recognition (10 points):**

- Evidence of studying existing code patterns (e.g., `src/models/user.py`)
- Consistency with existing project style and conventions
- Appropriate framework patterns (Flask, etc.) applied automatically

**Maintenance Integration (10 points):**

- Check for automatic cross-reference updates
- Look for dependency tracking in frontmatter
- Assess whether project-wide integrity was maintained

#### Phase 2: Technical Solution Quality (35 points)

**Architecture & Design (15 points):**

- Sound architectural decisions for the functionality
- Professional design patterns and security considerations
- Appropriate module structure and interfaces

**Implementation Quality (10 points):**

- Clean, secure, robust implementation
- Proper error handling and edge case consideration
- Professional coding practices and data validation

**Integration & Compatibility (10 points):**

- Seamless integration with existing systems
- Compatibility with existing project structure
- Uses existing patterns and conventions appropriately

#### Phase 3: Decision-Making Quality (25 points)

**Requirements Interpretation (10 points):**

- Thoughtful interpretation of minimal requirements
- Inferred appropriate functionality beyond basic requirements
- Professional scope and feature selection

**Technical Choices (10 points):**

- Excellent technical decisions and tool choices
- Appropriate mechanisms and approaches selected
- Professional patterns and libraries used

**Scope & Completeness (5 points):**

- Balanced feature set - not over/under-engineered
- Professional judgment in scope determination

### Step 4: Systematic Deduction Review

**Critical:** Always check for these common failures:

#### DSS Compliance Issues

- **No frontmatter anywhere:** -10 points from Metadata score
- **Files in root directory:** -5 points from File Organization
- **No documentation created:** -8 points from Metadata score
- **No integration with existing systems:** -8 points from Integration score

#### Link Syntax Compliance (Critical for DSS)

Search all documentation for cross-references:

- ❌ **Wrong:** `[[Link Text|filename.md]]` (wiki-style)
- ✅ **Correct:** `[Link Text](mdc:path/to/filename.md)` (DSS format)
- **Deduction:** Major points from cross-reference categories

#### Project Integration Failures

- Generic implementations that ignore project context
- No evidence of studying existing project patterns
- Breaking existing project conventions without justification

### Step 5: Calculate Final Score

- Sum all category scores AFTER applying deductions
- Document specific evidence for all scoring decisions
- Record any deductions with specific reasoning

## 📊 Results Recording

### Create Results Files

**For each evaluated task:**

1. **Scorecard:** `.cursor/rules/task_[XX]_scores.json`
2. **Analysis Report:** `.cursor/rules/task_[XX]_report.md`

**Example file names:**

- `task_001_scores.json` and `task_001_report.md`
- `task_01_xs_scores.json` and `task_01_xs_report.md`

**Note:** Writing results directly to `.cursor/rules/` ensures they get archived together with the rules automatically.

### Scorecard Template

```json
{
  "benchmark_run": {
    "timestamp": "USE_TIMESTAMP_FROM_DATE_COMMAND",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "rules_variant": "dss-enhanced|baseline|experimental",
    "task_id": "task-001|task-01-xs|task-06-xs|task-08-xs",
    "task_name": "Task Name from frontmatter",
    "evaluator": "self-scored",
    "task_workspace": "task_repos/task_XX/",
    "evaluation_framework": "realistic_automatic_behavior"
  },
  "scores": {
    "automatic_dss_behaviors": {
      "file_organization": {
        "score": 0,
        "max": 10,
        "notes": "Evidence of automatic organization without instructions"
      },
      "metadata_documentation": {
        "score": 0,
        "max": 10,
        "notes": "Automatic frontmatter and documentation creation"
      },
      "pattern_recognition": {
        "score": 0,
        "max": 10,
        "notes": "Evidence of studying existing patterns"
      },
      "maintenance_integration": {
        "score": 0,
        "max": 10,
        "notes": "Automatic cross-references and dependencies"
      }
    },
    "technical_quality": {
      "architecture_design": {
        "score": 0,
        "max": 15,
        "notes": "Sound architectural decisions"
      },
      "implementation_quality": {
        "score": 0,
        "max": 10,
        "notes": "Professional implementation practices"
      },
      "integration_compatibility": {
        "score": 0,
        "max": 10,
        "notes": "Integration with existing systems"
      }
    },
    "decision_making": {
      "requirements_interpretation": {
        "score": 0,
        "max": 10,
        "notes": "Understanding of minimal requirements"
      },
      "technical_choices": {
        "score": 0,
        "max": 10,
        "notes": "Quality of automatic technical decisions"
      },
      "scope_completeness": {
        "score": 0,
        "max": 5,
        "notes": "Appropriate scope determination"
      }
    }
  },
  "total_score": 0,
  "deductions_applied": [
    {
      "category": "category_name",
      "points": 0,
      "reason": "Specific issue description"
    }
  ],
  "files_created": ["list", "of", "files"],
  "files_modified": ["list", "of", "files"],
  "dss_behaviors_observed": [
    "List of automatic behaviors that emerged"
  ],
  "dss_behaviors_missing": [
    "List of expected behaviors that didn't emerge"
  ],
  "rule_effectiveness_assessment": "High|Medium|Low effectiveness based on automatic behaviors"
}
```

### Analysis Report Template

```markdown
---
tags: [benchmark, analysis, task-XX, results, realistic_evaluation]
provides: [task_XX_analysis, automatic_behavior_assessment]
requires: [task_XX_completion, realistic_evaluation_framework]
date: YYYY-MM-DD
time: HH:MM:SS
timestamp: YYYY-MM-DDTHH:MM:SS.ffffff
evaluation_framework: realistic_automatic_behavior
---

# DSS Benchmark Report - Task [XX]: [Task Name]

**Date:** YYYY-MM-DD  
**Time:** HH:MM:SS  
**Evaluation Framework:** Realistic Automatic Behavior Assessment
**Final Score:** XX/100  
**Evaluator:** Self-Scored
**Task Workspace:** task_repos/task_XX/

## Executive Summary

[Brief assessment of whether DSS rules enabled automatic professional behavior]

## Automatic DSS Behavior Analysis

### ✅ Evidence of Rule-Guided Behavior (XX/40 points)

#### File Organization (XX/10)
- **Evidence observed:** [Specific examples of automatic organization]
- **Pattern recognition:** [Evidence of studying existing project structure]
- **DSS impact:** [How rules guided file placement decisions]

#### Metadata & Documentation (XX/10)  
- **Automatic documentation:** [Evidence of docs created without instruction]
- **Frontmatter habits:** [Quality and appropriateness of metadata]
- **Cross-references:** [Evidence of automatic project integration]

#### Pattern Recognition (XX/10)
- **Existing code study:** [Evidence of examining src/models/user.py, etc.]
- **Style consistency:** [Matching existing project patterns]
- **Framework integration:** [Appropriate Flask/other patterns]

#### Maintenance Integration (XX/10)
- **Project integrity:** [Evidence of automatic maintenance behaviors]
- **Dependency tracking:** [Proper provides/requires relationships]
- **Cross-reference management:** [Automatic link updates]

### ❌ Missing Automatic Behaviors (Points Lost)

#### [Behavior Category] (XX points lost)
- **What should have happened:** [Expected automatic behavior]
- **What actually happened:** [Actual behavior observed]
- **Rule gap identified:** [What rules failed to enable]

## Technical Solution Assessment

### Architecture & Design (XX/15)
[Assessment of architectural decisions made automatically]

### Implementation Quality (XX/10)
[Professional practices and code quality]

### Integration & Compatibility (XX/10)
[How well solution integrated with existing systems]

## Decision-Making Quality Assessment

### Requirements Interpretation (XX/10)
[How well minimal requirements were understood and expanded]

### Technical Choices (XX/10)
[Quality of automatic technical decisions]

### Scope & Completeness (XX/5)
[Appropriateness of scope determination]

## DSS Rule Effectiveness Analysis

### Strong Rule Performance
- [List areas where rules clearly enabled professional behavior]

### Rule Gaps Identified
- [List areas where automatic behavior didn't emerge]

### Recommendations for Rule Improvement
1. **[Area]:** [Specific recommendation]
2. **[Area]:** [Specific recommendation]

## Evidence-Based Conclusions

### Automatic Behavior Emergence: [High|Medium|Low]
**Rationale:** [Evidence for classification]

### Rule-Guided vs Manual Behavior
**Rule-guided:** [Behaviors that emerged automatically]
**Manual:** [Behaviors that required conscious effort]

### Overall DSS Effectiveness: [Score]/100
**Summary:** [Whether rules successfully enabled automatic professionalism]

## Final Assessment

[Conclusion about whether DSS rules enabled the assistant to work like a senior developer who naturally knows best practices, or like a junior developer following instructions]
```

## 🎯 Key Evaluation Principles

### Evidence-Based Assessment

- **Score what was produced**, not intentions
- **Look for concrete evidence** of automatic behaviors
- **Document specific examples** of rule-guided decisions

### Automatic Behavior Focus

- **High scores:** Professional practices emerged without instruction
- **Medium scores:** Some automatic behaviors with some manual effort
- **Low scores:** Little evidence of rule-guided automatic behavior

### Multiple Valid Approaches

Accept various solutions that demonstrate DSS principles:

- Different architectural approaches (if sound)
- Various file organization schemes (if logical)
- Different technical implementations (if appropriate)

### Process Over Outcome

Focus on whether DSS rules enabled good process:

- Evidence of studying existing patterns
- Automatic maintenance of project integrity
- Professional practices without explicit instruction

## 🧹 Post-Evaluation Cleanup

### After Recording Results

**Ask the user before cleanup:**

"Evaluation complete! Would you like me to reset the project to clean up task files and prepare for the next benchmark run? This will:

- Remove all task-created files  
- Archive current rules and results to `rules_store/v{X}_{date}/`
- Re-hide evaluation rubrics
- Prepare for next benchmark run

Should I run the reset script? (yes/no)"

**If user confirms, run:**

```bash
# Reset project state after evaluation
python scripts/reset_project.py
```

### What the Reset Script Does

- Remove all task-created files
- Archive current rules and results to `rules_store/v{X}_{date}/`
- Re-hide evaluation rubrics  
- Prepare for next benchmark run

### Results Preservation

- All results are archived with the rules automatically
- Cleanup never touches results files
- Historical tracking across rule iterations maintained

### Manual Cleanup (If Script Unavailable)

If the reset script doesn't work, you can manually:

```bash
# Remove task workspaces
rm -rf task_repos/

# Check for any remaining task files
ls -la src/ docs/

# Re-hide rubrics (if needed)
# This is handled by .cursorignore automatically
```

---

## 🎯 Success Indicators

### Strong DSS Rule Performance

- **High automatic behavior scores (32+ / 40)**
- **Clear evidence of pattern recognition**
- **Professional organization without instruction**
- **Maintenance behaviors happening automatically**

### Weak Rule Performance

- **Low automatic behavior scores (< 20 / 40)**
- **No evidence of template or pattern usage**
- **Generic solutions ignoring project context**
- **Manual prompting needed for basic practices**

**Remember:** The goal is measuring whether DSS rules enable automatic professional behavior, not just functional completion.
