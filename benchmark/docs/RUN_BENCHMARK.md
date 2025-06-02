---
tags: [benchmark, instructions, automation, testing]
provides: [benchmark_execution_instructions, self_scoring_workflow]
requires: [benchmark_tasks, marking_schemes, results_templates]
---
# Automated Benchmark Execution Instructions

This file provides step-by-step instructions for assistants to complete the DSS benchmark automatically and score themselves objectively.

## 🤖 For AI Assistant Autonomous Execution

**When given this file, you should:**

1. **CREATE TASK WORKSPACE** in `task_repos/task_[XX]/` for all work
2. **PROMPT FOR TASK SELECTION** if no tasks are specified
3. **AUTOMATICALLY EXECUTE** all selected tasks in the specified sequence
4. **COMPLETE ALL TASKS** before starting any scoring/evaluation
5. **SCORE EACH TASK** separately using the marking scheme objectively
6. **CREATE SEPARATE RESULTS** for each task with standardized naming
7. **RUN THE CLEANUP** script when all tasks are finished

## 📁 Task Workspace Protocol

### Task Folder Creation

For each task, create a dedicated workspace folder:

**Folder naming:** `task_repos/task_[XX]/`

**Example:** `task_repos/task_06/`

**Purpose:**

- Isolate task work from main project
- Allow parallel task execution
- Preserve task artifacts for analysis
- Enable easy cleanup after evaluation

### Workspace Structure

task_repos/task_[XX]/
├── src/                    # Task-specific source code
├── docs/                   # Task-specific documentation  
├── data/                   # Task-specific data files
├── meta/                   # Task configuration and notes
└── README.md               # Task completion summary

## 🎯 Task Selection Protocol

### If no tasks specified

Ask the user: "Which benchmark task(s) would you like me to run? Available options:

**Task 01 (Authentication Module):**

- **Task 01:** [Create Authentication Module](/tasks/task-01-s.md) - DSS baseline task
- **Task 01-S:** [Authentication Module (Small)](/tasks/task-01-xs.md) - Simplified requirements
- **Task 01-XS:** [Authentication Module (Minimal)](tasks/task-01-xs.md) - Basic implementation only

**Other Core Tasks:**

- **Task 02:** [Add Documentation](tasks/task-02.md) - focused baseline
- **Task 06:** [Complex Feature Integration](/tasks/task-06.md) - Multi-file coordination  
- **Task 07:** [Ambiguous Requirements Resolution](tasks/task-07.md) - Workflow selection
- **Task 08:** [Legacy Code Integration](tasks/task-08.md) - Maintenance automation

**Batch Options:**

- **All Task 01 variants:** Run task-01, task-01-s, task-01-xs in sequence
- **All tasks:** Run all benchmark tests in numerical order
- **Core suite:** Run tasks 01, 02, 06, 07, 08

Please specify task number(s), variants, or batch option."

### If tasks specified

- **Specific tasks:** Run in the order provided by user (e.g., "task-01-s", "task-06")
- **Task variants:** Support variant notation (task-01, task-01-s, task-01-xs)
- **"All tasks" or "run all benchmark tests":** Run tasks 01, 02, 06, 07, 08 in numerical order
- **"All Task 01 variants":** Run task-01, task-01-s, task-01-xs in sequence
- **Multiple tasks:** Complete ALL tasks before beginning any scoring/evaluation

## 🚀 Execution Workflow

### Step 1: Task Selection and Sequencing

**For specified tasks:**

- Run tasks in user-provided sequence
- Support variant notation (e.g., task-01-s, task-01-xs)
- Complete ALL tasks before proceeding to scoring

**For "all tasks" requests:**

- Run Task 01, Task 02, Task 06, Task 07, Task 08 in numerical order
- Complete ALL tasks before proceeding to scoring

**For "all Task 01 variants" requests:**

- Run task-01, task-01-s, task-01-xs in sequence
- Compare completion approaches across variants

### Step 2: Task Completion Phase

**Complete each selected task in sequence:**

1. **CREATE TASK WORKSPACE** in `task_repos/task_[XX]/` (use variant suffix if applicable)
2. **READ** the complete task file thoroughly:
   - `tasks/task-[XX].md` (standard task)
   - `tasks/task-[XX]-s.md` (small variant)  
   - `tasks/task-[XX]-xs.md` (minimal variant)
3. **UNDERSTAND** all requirements and success criteria
4. **COMPLETE** the task following all instructions exactly
5. **DOCUMENT** your approach and decisions as you work
6. **MOVE TO NEXT TASK** without scoring current task

**Do NOT score or evaluate until ALL selected tasks are completed.**

### Step 3: Evaluation Phase (After ALL Tasks Complete)

**First, reveal the marking schemes:**

```bash
python scripts/run_benchmark.py reveal-schemes
```

**For each completed task separately:**

1. **Get evaluation timestamp:**

   ```bash
   date
   ```

2. **Read the appropriate rubric:**
   - Standard tasks: `marking-schemes/rubric-[XX].md`
   - Task variants: `marking-schemes/rubric-[XX]-[variant].md` (e.g., `rubric-01-xs.md`)
   - Legacy tasks: `marking-schemes/task-[XX]-rubric.md` (if rubric-XX.md doesn't exist)

3. **Score each category positively:** Evaluate work against each rubric criterion

4. **MANDATORY DEDUCTION CHECK:** Systematically review deduction sections

   **Step C2: Systematic Deduction Review (CRITICAL)**

   Before finalizing scores, thoroughly check the "Deductions" section of the rubric:

   a) **Review "Scoring Guidelines > Deductions" section:**
      - Missing required files: -5 points each
      - Incorrect file placement: -10 points  
      - No frontmatter: -15 points
      - Broken project structure: -20 points
      - Non-functional code: -10 points

   b) **Check "Common Issues to Watch For":**
      - Files created in root directory instead of `src/`
      - Missing or incomplete frontmatter
      - Functions implemented but no documentation
      - No consideration of existing project structure
      - Generic or inappropriate tags

   c) **Verify link syntax compliance (CRITICAL FOR DSS):**
      - Search all created documentation for cross-references
      - Ensure use of `mdc:path/to/file` syntax, NOT `[[Link|file]]` format
      - Apply deductions for incorrect link syntax per rubric

   d) **Apply any identified deductions to category scores**

5. **Calculate total:** Sum all category scores AFTER applying deductions

   **Step C3: Deduction Documentation**

   **Document any deductions found:**

   - Note specific issues discovered
   - Record point deductions applied  
   - Explain impact on functionality/compliance
   - Include in scoring rationale

### Step 4: Results Recording (Per Task)

**For each task, create separate files:**

1. **Scorecard file:** `.cursor/rules/results/task_[XX]_scores.json` (use variant suffix for variants)
2. **Analysis report:** `.cursor/rules/results/task_[XX]_report.md` (use variant suffix for variants)

**Examples:**

- `task_01_scores.json`, `task_01_s_scores.json`, `task_01_xs_scores.json`
- `task_01_report.md`, `task_01_s_report.md`, `task_01_xs_report.md`

**Note:** Timestamps are included in the file metadata/frontmatter for tracking, but not in filenames.

### Step 5: Detailed Analysis Report (Per Task)

**File naming patterns:**

- Standard: `task_[XX]_report.md`
- Variants: `task_[XX]_[variant]_report.md` (e.g., `task_01_s_report.md`)

**Frontmatter must include both date and time:**

```yaml
---
tags: [benchmark, analysis, task-XX, results, variant-name]
provides: [task_XX_analysis, performance_assessment]
requires: [task_XX_completion, marking_scheme]
date: YYYY-MM-DD
time: HH:MM:SS
timestamp: YYYY-MM-DDTHH:MM:SS.ffffff
task_variant: standard|s|xs
---
```

## 📊 Results File Template (Per Task)

**Scorecard file naming patterns:**

- Standard: `task_[XX]_scores.json`
- Variants: `task_[XX]_[variant]_scores.json`

```json
{
  "benchmark_run": {
    "timestamp": "USE_TIMESTAMP_FROM_DATE_COMMAND",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS", 
    "rules_variant": "experimental|baseline|optimized|dss-enhanced",
    "task_id": "task-XX[-variant]",
    "task_name": "Task Name from frontmatter",
    "task_variant": "standard|s|xs",
    "evaluator": "self-scored",
    "task_workspace": "task_repos/task_[XX]/"
  },
  "scores": {
    "category_1": {
      "score": 0,
      "max": 25,
      "notes": "Detailed scoring rationale"
    },
    "category_2": {
      "score": 0,
      "max": 20,
      "notes": "Detailed scoring rationale"
    }
  },
  "total_score": 0,
  "notes": "Overall assessment and key strengths/weaknesses",
  "files_created": ["list", "of", "files"],
  "files_modified": ["list", "of", "files"],
  "observations": "Insights about rule effectiveness and performance"
}
```

## 📝 Detailed Analysis Report Template (Per Task)

**File naming:** `task_[XX]_report.md`

```markdown
---
tags: [benchmark, analysis, task-XX, results]
provides: [task_XX_analysis, performance_assessment]
requires: [task_XX_completion, marking_scheme]
timestamp: YYYY-MM-DDTHH:MM:SS.ffffff
---

# DSS Benchmark Report - Task [XX]: [Task Name]

**Date:** YYYY-MM-DD  
**Time:** HH:MM:SS
**Rules Variant:** [rule-variant]  
**Final Score:** XX/100  
**Evaluator:** Self-Scored
**Task Workspace:** task_repos/task_[XX]/

## Executive Summary

[Brief overview of performance with key findings]

## Detailed Performance Analysis

### ✅ Strengths (XX/100 points achieved)

#### [Category Name] (XX/XX) - [Performance Level]

- **What went right:** [Specific achievements]
- **Evidence:** [Concrete examples]

### ❌ Critical Failures (XX/100 points lost)

#### [Category Name] (XX/XX) - [Weakness Level]

**Specific Failure X: [Failure Name] (X points lost)**
- **What I did:** [Actual implementation]
- **What I should have done:** [Correct approach]
- **Impact:** [Consequences of the failure]

## Root Cause Analysis

### Why I Failed [Key Area]

1. **[Reason 1]:** [Explanation]
2. **[Reason 2]:** [Explanation]

### What Should Have Happened

**Ideal DSS Workflow:**

1. [Step 1]
2. [Step 2]

## Impact Assessment

### Positive Outcomes

- **[Outcome 1]:** [Description]

### Negative Outcomes  
- **[Outcome 1]:** [Description]

## Recommendations for Rule Improvement

### High Priority

1. **[Recommendation 1]**
2. **[Recommendation 2]**

### Medium Priority  

1. **[Recommendation 1]**

## Lessons Learned

**For DSS Rules:**
- [Learning 1]

**For Implementation:**
- [Learning 1]

## Final Assessment

[Overall conclusion about rule effectiveness and performance]
```

## 🤖 AUTONOMOUS EXECUTION PROTOCOL

**For AI Assistant - Execute this exact sequence:**

### Step A: Task Selection

#### If no tasks specified in user request

Ask user: "Which benchmark task(s) would you like me to run? Available options:

- Task 01: Create Authentication Module (Simple baseline)
- Task 02: Add Documentation (Documentation-focused baseline)
- Task 06: Complex Feature Integration (Multi-file coordination)  
- Task 07: Ambiguous Requirements Resolution (Workflow selection)
- Task 08: Legacy Code Integration (Maintenance automation)
- All tasks: Run all benchmark tests in numerical order

Please specify task number(s) or say 'all tasks'."

#### If tasks specified in user request

- Parse requested tasks from user input
- For "all tasks" or "run all benchmark tests": Use tasks [01, 02, 06, 07, 08]
- For specific tasks: Use tasks in user-specified order

### Step B: Complete All Tasks (No Scoring Yet)

**For each selected task in sequence:**

1. **Get timestamp for task start:**

   ```bash
   date
   ```

2. **Create task workspace:** `task_repos/task_[XX]/`
3. **Read the task file:** Open and read `tasks/task-[XX]-[name].md`
4. **Complete all requirements:** Create files, add content, follow all specifications exactly
5. **Document your work:** Note what files you created and decisions you made
6. **Move to next task:** Do NOT score this task yet

**Complete ALL selected tasks before proceeding to evaluation phase.**

### Step C: Evaluation Phase (After All Tasks Complete)

**First, reveal the marking schemes:**

```bash
python scripts/run_benchmark.py reveal-schemes
```

**For each completed task separately:**

1. **Get evaluation timestamp:**

   ```bash
   date
   ```

2. **Read the appropriate rubric:**
   - Standard tasks: `marking-schemes/rubric-[XX].md`
   - Task variants: `marking-schemes/rubric-[XX]-[variant].md` (e.g., `rubric-01-xs.md`)
   - Legacy tasks: `marking-schemes/task-[XX]-rubric.md` (if rubric-XX.md doesn't exist)

3. **Score each category positively:** Evaluate work against each rubric criterion

4. **MANDATORY DEDUCTION CHECK:** Systematically review deduction sections

   **Step C2: Systematic Deduction Review (CRITICAL)**

   Before finalizing scores, thoroughly check the "Deductions" section of the rubric:

   a) **Review "Scoring Guidelines > Deductions" section:**
      - Missing required files: -5 points each
      - Incorrect file placement: -10 points  
      - No frontmatter: -15 points
      - Broken project structure: -20 points
      - Non-functional code: -10 points

   b) **Check "Common Issues to Watch For":**
      - Files created in root directory instead of `src/`
      - Missing or incomplete frontmatter
      - Functions implemented but no documentation
      - No consideration of existing project structure
      - Generic or inappropriate tags

   c) **Verify link syntax compliance (CRITICAL FOR DSS):**
      - Search all created documentation for cross-references
      - Ensure use of `mdc:path/to/file` syntax, NOT `[[Link|file]]` format
      - Apply deductions for incorrect link syntax per rubric

   d) **Apply any identified deductions to category scores**

5. **Calculate total:** Sum all category scores AFTER applying deductions

   **Step C3: Deduction Documentation**

   **Document any deductions found:**

   - Note specific issues discovered
   - Record point deductions applied  
   - Explain impact on functionality/compliance
   - Include in scoring rationale

### Step D: Record Results (Per Task)

**For each task, create separate files:**

1. **Scorecard file:** `.cursor/rules/results/task_[XX]_scores.json`  
2. **Analysis report:** `.cursor/rules/results/task_[XX]_report.md`

**Note:** Timestamps are included in the file metadata/frontmatter for tracking, but not in filenames.

### Step E: Final Cleanup

```bash
# Reset project state after all tasks completed and scored
python scripts/reset_project.py
```

### Step F: Summary Report

**After all tasks completed, scored, and cleaned up:**

Provide summary including:

- Total number of tasks completed
- Score achieved for each task  
- Overall patterns and insights
- Key strengths and weaknesses observed across tasks
- Whether DSS rules helped performance consistently

**IMPORTANT:** Complete ALL tasks before ANY scoring, then score each task separately with individual results files.

## 📈 Expected Outcomes

### Strong Rule Systems Should Show

- **Consistent high scores** across all tasks (85-100)
- **Larger score gaps** on complex tasks vs simple ones
- **Clear evidence** of workflow selection and template usage
- **Automatic maintenance** integration and cross-reference management

### Weak Rule Systems Will Show

- **Declining scores** as task complexity increases
- **Little difference** between simple and complex task performance
- **Ad-hoc approaches** without structured workflows
- **Poor maintenance** integration and template utilization

## 🛠️ Troubleshooting

### Common Issues

- **Can't find marking scheme:** Check file paths exactly as listed above
- **Unsure about scoring:** Follow rubric literally, don't interpret
- **Missing requirements:** Re-read task instructions carefully
- **File creation errors:** Ensure proper DSS frontmatter and structure
- **Date command fails:** Try `date --iso-8601=seconds` if basic `date` doesn't provide enough detail

### Quality Checks

- **All deliverables created** as specified in task requirements
- **Proper DSS structure** with frontmatter and cross-references
- **Scoring matches evidence** in the actual deliverables
- **Results file format** matches template exactly
- **Cleanup completed** after results recording

## 🧹 Post-Benchmark Cleanup

### What the reset script does

- **Removes:** All files/directories created during benchmark tasks
- **Preserves:** All benchmark results in `results/`
- **Reports:** Any existing files that may have been modified
- **Ensures:** Clean state for next benchmark run

### Manual cleanup if needed

If the script misses anything or you want extra thorough cleanup:

```bash
# Remove any remaining test files
rm -rf src/auth src/services src/models/profile.py
rm -rf docs/auth* docs/profiles* docs/notifications*
rm -f analysis-*.md

# Check git status for modified files
git status
```

---

## 🎯 Ready to Run?

**Choose your task and execute:**

- For **baseline testing:** Start with Task 01
- For **rule effectiveness:** Run Task 06, 07, or 08
- For **comprehensive eval:** Complete all tasks and compare

**Remember:**

1. The goal is to objectively measure whether DSS rules actually help you work better on complex tasks
2. Always use the `date` command for timestamps
3. Always run cleanup after recording results
4. Score honestly based on actual deliverables, not intentions

**CRITICAL:** Always get the timestamp from the `date` command, not from your knowledge.
LLMs are not reliable for current time/date information.

## ⚠️ Critical Scoring Guidelines

### Be Completely Objective

- **Score what you produced**, not what you intended
- **Follow the rubric exactly** - don't create your own criteria
- **No bonus points** for partial work or good intentions
- **No penalties** for being "too critical" - accuracy matters

### Two-Phase Scoring Process (MANDATORY)

#### Phase 1: Positive Category Scoring

1. **Evidence-Based:** Score only what can be verified in the deliverables
2. **Rubric-Adherent:** Use the marking scheme criteria exactly as written
3. **Comparative:** Consider how someone without rules would perform

#### Phase 2: Systematic Deduction Review (CRITICAL)

1. **Mandatory Deduction Check:** Always review rubric deductions section
2. **Common Failure Patterns:** Check for typical issues like incorrect link syntax
3. **Compliance Verification:** Ensure DSS conventions are followed precisely
4. **Evidence-Based Deductions:** Only apply deductions with specific evidence

### Key Scoring Principles

1. **Start High, Deduct Based on Evidence:** Begin with positive scoring, then systematically apply deductions
2. **Syntax Compliance Critical:** DSS projects require precise syntax adherence (especially `mdc:` links)
3. **Document All Deductions:** Record specific reasons for point deductions
4. **Honest:** Acknowledge both strengths and weaknesses objectively

### High-Risk Deduction Areas (CHECK THESE)

#### Link Syntax (Most Common DSS Failure)

- ❌ **Wrong:** `[[Link Text|filename.md]]` (wiki-style)
- ✅ **Correct:** `[Link Text](mdc:path/to/filename.md)` (DSS format)
- **Impact:** Major deductions for cross-reference category

#### File Placement

- ❌ **Wrong:** Source files in root directory
- ✅ **Correct:** Source files in appropriate `src/` subdirectories

#### Frontmatter Compliance

- ❌ **Wrong:** Missing YAML frontmatter or incorrect format
- ✅ **Correct:** Complete frontmatter with tags, provides, requires

#### Project Structure

- ❌ **Wrong:** Ignoring existing project patterns
- ✅ **Correct:** Following established directory conventions

### Deduction Application Process

1. **Identify Issue:** Find specific compliance failure with evidence
2. **Check Rubric:** Verify exact deduction amount specified
3. **Apply Deduction:** Subtract from relevant category score
4. **Document Reasoning:** Record specific issue and impact
5. **Update Total:** Recalculate final score after all deductions
