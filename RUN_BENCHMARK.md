---
tags: [benchmark, instructions, automation, testing]
provides: [benchmark_execution_instructions, self_scoring_workflow]
requires: [benchmark_tasks, marking_schemes, results_templates]
---
# Automated Benchmark Execution Instructions

This file provides step-by-step instructions for assistants to complete the DSS benchmark automatically and score themselves objectively.

## 🤖 For AI Assistant Autonomous Execution

**When given this file, you should:**

1. **PROMPT FOR TASK SELECTION** if no tasks are specified
2. **AUTOMATICALLY EXECUTE** all selected tasks in the specified sequence
3. **COMPLETE ALL TASKS** before starting any scoring/evaluation
4. **SCORE EACH TASK** separately using the marking scheme objectively
5. **CREATE SEPARATE RESULTS** for each task with standardized naming
6. **RUN THE CLEANUP** script when all tasks are finished

## 🎯 Task Selection Protocol

### If no tasks specified:
Ask the user: "Which benchmark task(s) would you like me to run? Available options:
- **Task 01:** Create Authentication Module (Simple baseline)
- **Task 06:** Complex Feature Integration (Multi-file coordination)
- **Task 07:** Ambiguous Requirements Resolution (Workflow selection) 
- **Task 08:** Legacy Code Integration (Maintenance automation)
- **All tasks:** Run all benchmark tests in numerical order (01, 06, 07, 08)

Please specify task number(s) or say 'all tasks'."

### If tasks specified:
- **Specific tasks:** Run in the order provided by user
- **"All tasks" or "run all benchmark tests":** Run tasks 01, 06, 07, 08 in numerical order
- **Multiple tasks:** Complete ALL tasks before beginning any scoring/evaluation

## 🚀 Execution Workflow

### Step 1: Task Selection and Sequencing

**For specified tasks:**
- Run tasks in user-provided sequence
- Complete ALL tasks before proceeding to scoring

**For "all tasks" requests:**
- Run Task 01, Task 06, Task 07, Task 08 in numerical order
- Complete ALL tasks before proceeding to scoring

### Step 2: Task Completion Phase

**Complete each selected task in sequence:**

1. **READ** the complete task file thoroughly
2. **UNDERSTAND** all requirements and success criteria
3. **COMPLETE** the task following all instructions exactly
4. **DOCUMENT** your approach and decisions as you work
5. **MOVE TO NEXT TASK** without scoring current task

**Do NOT score or evaluate until ALL selected tasks are completed.**

### Step 3: Evaluation Phase (After ALL Tasks Complete)

**First, reveal the marking schemes:**
```bash
python meta/scripts/run_benchmark.py reveal-schemes
```

**For each completed task separately:**

1. **Get evaluation timestamp:**
   ```bash
   python -c "import datetime; dt=datetime.datetime.now(); print('Evaluation timestamp:', dt.isoformat()); print('Date:', dt.strftime('%Y-%m-%d')); print('Time:', dt.strftime('%H-%M-%S'))"
   ```

2. **Read the rubric:** Open `meta/benchmark/marking-schemes/task-[XX]-rubric.md`
3. **Score objectively:** Evaluate work against each rubric criterion
4. **Calculate total:** Sum all category scores

### Step 4: Results Recording (Per Task)

1. **GET CURRENT TIMESTAMP:** Run this command for each task evaluation:

   **Unix/Linux/Mac/PowerShell:**
   ```bash
   date -u +"%Y-%m-%dT%H:%M:%S.%6N"
   ```

   **PowerShell alternative:**
   ```powershell
   Get-Date -Format "yyyy-MM-ddTHH:mm:ss.ffffff"
   ```

2. **CREATE** results files for each task in both locations:

   **Scorecard files:**
   - **Benchmark archive:** `meta/benchmark/results/task_[XX]_scores_YYYY-MM-DD_HH-MM-SS.json`
   - **Rules analysis:** `rules_store/[rule-variant]/results/task_[XX]_scores_YYYY-MM-DD_HH-MM-SS.json`

   **Report files:**
   - **Rules analysis:** `rules_store/[rule-variant]/analysis/task_[XX]_report_YYYY-MM-DD_HH-MM-SS.md`

3. **USE** the timestamp from step 1 for consistent file naming
4. **INCLUDE** timestamp in frontmatter for both scorecard and report files

### Step 5: Detailed Analysis Report (Per Task)

**File naming:** `task_[XX]_report_YYYY-MM-DD_HH-MM-SS.md`

**Frontmatter must include both date and time:**
```markdown
---
tags: [benchmark, analysis, task-XX, results]
provides: [task_XX_analysis, performance_assessment]
requires: [task_XX_completion, marking_scheme]
date: YYYY-MM-DD
time: HH:MM:SS
timestamp: YYYY-MM-DDTHH:MM:SS.ffffff
---
```

## 📊 Results File Template (Per Task)

**Scorecard file naming:** `task_[XX]_scores.json`

```json
{
  "benchmark_run": {
    "timestamp": "USE_TIMESTAMP_FROM_DATE_COMMAND",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS", 
    "rules_variant": "experimental|baseline|optimized|dss-enhanced",
    "task_id": "task-XX",
    "task_name": "Task Name from frontmatter",
    "evaluator": "self-scored"
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
- Task 06: Complex Feature Integration (Multi-file coordination)  
- Task 07: Ambiguous Requirements Resolution (Workflow selection)
- Task 08: Legacy Code Integration (Maintenance automation)
- All tasks: Run all benchmark tests in numerical order

Please specify task number(s) or say 'all tasks'."

#### If tasks specified in user request

- Parse requested tasks from user input
- For "all tasks" or "run all benchmark tests": Use tasks [01, 06, 07, 08]
- For specific tasks: Use tasks in user-specified order

### Step B: Complete All Tasks (No Scoring Yet)

**For each selected task in sequence:**

1. **Get timestamp for task start:**

   ```bash
   python -c "import datetime; print('Task [XX] started:', datetime.datetime.now().isoformat())"
   ```

2. **Read the task file:** Open and read `meta/benchmark/tasks/task-[XX]-[name].md`
3. **Complete all requirements:** Create files, add content, follow all specifications exactly
4. **Document your work:** Note what files you created and decisions you made
5. **Move to next task:** Do NOT score this task yet

**Complete ALL selected tasks before proceeding to evaluation phase.**

### Step C: Evaluation Phase (After All Tasks Complete)

**First, reveal the marking schemes:**
```bash
python meta/scripts/run_benchmark.py reveal-schemes
```

**For each completed task separately:**

1. **Get evaluation timestamp:**
   ```bash
   python -c "import datetime; dt=datetime.datetime.now(); print('Evaluation timestamp:', dt.isoformat()); print('Date:', dt.strftime('%Y-%m-%d')); print('Time:', dt.strftime('%H-%M-%S'))"
   ```

2. **Read the rubric:** Open `meta/benchmark/marking-schemes/task-[XX]-rubric.md`
3. **Score objectively:** Evaluate work against each rubric criterion
4. **Calculate total:** Sum all category scores

### Step D: Record Results (Per Task)

**For each task, create separate files:**

1. **Scorecard file:** `meta/benchmark/results/task_[XX]_scores_YYYY-MM-DD_HH-MM-SS.json`
2. **Scorecard copy:** `rules_store/assistant-test/results/task_[XX]_scores_YYYY-MM-DD_HH-MM-SS.json`  
3. **Analysis report:** `rules_store/assistant-test/analysis/task_[XX]_report_YYYY-MM-DD_HH-MM-SS.md`

**Use consistent timestamp from Step C for all files related to same task.**

### Step E: Final Cleanup

```bash
# Reset project state after all tasks completed and scored
python meta/scripts/reset_project.py
```

### Step F: Summary Report

**After all tasks completed, scored, and cleaned up:**

Provide summary including:

- Total number of tasks completed
- Score achieved for each task  
- Overall patterns and insights
- Key strengths and weaknesses observed across tasks
- Whether DSS rules helped performance consistently

**IMPORTANT:** Complete ALL tasks before ANY scoring, then score each task separately with individual timestamped files.

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
- **Date command fails:** Try these alternatives:
  - `date --iso-8601=seconds` (Unix/Linux)
  - `Get-Date -Format "yyyy-MM-ddTHH:mm:ss"` (PowerShell)
  - `python -c "import datetime; print(datetime.datetime.now().isoformat())"` (Python)

### Quality Checks

- **All deliverables created** as specified in task requirements
- **Proper DSS structure** with frontmatter and cross-references
- **Scoring matches evidence** in the actual deliverables
- **Results file format** matches template exactly
- **Cleanup completed** after results recording

## 🧹 Post-Benchmark Cleanup

### What the reset script does

- **Removes:** All files/directories created during benchmark tasks
- **Preserves:** All benchmark results in `meta/benchmark/results/`
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

### Key Scoring Principles

1. **Evidence-Based:** Score only what can be verified in the deliverables
2. **Rubric-Adherent:** Use the marking scheme criteria exactly as written
3. **Comparative:** Consider how someone without rules would perform
4. **Honest:** Acknowledge both strengths and weaknesses objectively
