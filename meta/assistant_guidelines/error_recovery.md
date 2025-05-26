---
tags: [assistant_guidelines, meta, error_handling, reliability]
provides: [assistant_error_recovery_process]
requires: [meta/assistant_guidelines/self_governance_improvement.md, meta/assistant_guidelines/status_tracking.md]
---

# Assistant Guidelines: Error Recovery Process

This document outlines a systematic approach for detecting, diagnosing, and recovering from errors that may occur during the assistant's operations. It provides categorized strategies for common error scenarios and establishes protocols for self-correction.

## Common Error Categories

### 1. Workflow Execution Errors

| Error Type | Description | Common Causes | 
|------------|-------------|---------------|
| **Workflow Selection** | Applying the wrong workflow to a task | Misunderstanding task complexity, insufficient context gathering |
| **Step Omission** | Skipping required steps in a workflow | Distraction, context switching, urgency |
| **Sequence Error** | Performing workflow steps in the wrong order | Misjudging dependencies, optimizing prematurely |
| **Incomplete Execution** | Stopping a workflow before completion | Reaching token limits, encountering unexpected blockers |

### 2. Tool Usage Errors

| Error Type | Description | Common Causes | 
|------------|-------------|---------------|
| **Wrong Tool** | Using an inappropriate tool for the task | Misunderstanding tool purpose, habit |
| **Parameter Error** | Providing incorrect parameters to a tool | Typos, misunderstanding requirements |
| **Tool Failure** | Tool execution fails despite correct usage | External system limitations, permissions issues |
| **Output Misinterpretation** | Misunderstanding the output of a tool | Incomplete analysis, assumption errors |

### 3. Content Generation Errors

| Error Type | Description | Common Causes | 
|------------|-------------|---------------|
| **Style Inconsistency** | Generated content doesn't match project style | Insufficient context, overlooking style guides |
| **Factual Error** | Generating incorrect information | Misremembering, reasoning errors |
| **Incomplete Content** | Generating partial or truncated content | Token limitations, planning errors |
| **Format Error** | Incorrect format for generated content | Misunderstanding requirements, template errors |

### 4. Documentation Errors

| Error Type | Description | Common Causes | 
|------------|-------------|---------------|
| **Missing Frontmatter** | Failing to include required frontmatter | Oversight, workflow error |
| **Link Errors** | Creating broken or incorrect links | Typos, incorrect path understanding |
| **Status Tracking** | Incorrect status indicators or tracking | Oversight, confusion about status definitions |
| **Metadata Errors** | Incorrect tags or metadata | Misunderstanding tag conventions |

## Error Detection Guidelines

### Active Detection Methods

1. **Post-Action Verification**:
   - After tool calls, explicitly verify the output matches expectations
   - Check that file modifications achieved the intended result
   - Verify that new content follows required formats and conventions

2. **Consistency Checks**:
   - Compare generated content against project style guides and conventions
   - Verify that frontmatter follows patterns in similar files
   - Ensure status tracking follows the [Status Tracking System](mdc:meta/assistant_guidelines/status_tracking.md)

3. **Workflow Checkpoint Validation**:
   - At key points in workflows, verify that all required steps so far have been completed
   - Confirm that the appropriate workflow is still being applied
   - Check for any skipped or incomplete steps

4. **Documentation Integrity Checks**:
   - Verify that all required files have been updated
   - Check that links point to valid resources
   - Ensure task tracking reflects current status

### Passive Detection Methods

1. **User Feedback Recognition**:
   - Interpret explicit user corrections as indicators of errors
   - Recognize implicit feedback in follow-up requests
   - Pay attention to clarifying questions that may indicate confusion

2. **Unexpected Results Recognition**:
   - Be alert to tool outputs that don't match expectations
   - Note when file contents differ significantly from anticipated structure
   - Identify when tasks take significantly longer than estimated

3. **Pattern Recognition**:
   - Note recurring issues in similar tasks
   - Identify error-prone areas based on past corrections
   - Recognize when tasks consistently deviate from planned approaches

## Recovery Strategies by Error Type

### Workflow Execution Recovery

| Error Type | Recovery Strategy |
|------------|-------------------|
| **Workflow Selection** | 1. Acknowledge incorrect workflow<br>2. Determine correct workflow<br>3. Document transition following [Workflow Transitions](mdc:meta/assistant_workflows/workflow_transitions.md)<br>4. Resume with correct workflow |
| **Step Omission** | 1. Identify missed step(s)<br>2. Assess impact of omission<br>3. Perform missed step if still relevant<br>4. Verify subsequent steps remain valid |
| **Sequence Error** | 1. Document current state<br>2. Identify correct sequence<br>3. Determine if work needs to be redone<br>4. Resume with correct sequence |
| **Incomplete Execution** | 1. Document progress made<br>2. Identify remaining steps<br>3. Continue workflow from appropriate point<br>4. Verify continuity |

### Tool Usage Recovery

| Error Type | Recovery Strategy |
|------------|-------------------|
| **Wrong Tool** | 1. Cancel impact of incorrect tool if possible<br>2. Select appropriate tool<br>3. Re-execute with correct tool<br>4. Verify outcome |
| **Parameter Error** | 1. Document incorrect parameters<br>2. Determine correct parameters<br>3. Re-execute with correct parameters<br>4. Verify outcome |
| **Tool Failure** | 1. Document error conditions<br>2. Determine alternative approach<br>3. Execute alternative approach<br>4. If persistent, flag to user |
| **Output Misinterpretation** | 1. Re-examine tool output<br>2. Correct interpretation<br>3. Adjust subsequent actions<br>4. Document learning |

### Content Generation Recovery

| Error Type | Recovery Strategy |
|------------|-------------------|
| **Style Inconsistency** | 1. Review project style guides<br>2. Identify specific inconsistencies<br>3. Edit content to match style<br>4. Verify consistency |
| **Factual Error** | 1. Document incorrect information<br>2. Research correct information<br>3. Update content with corrections<br>4. Verify accuracy |
| **Incomplete Content** | 1. Identify missing components<br>2. Generate remaining content<br>3. Integrate seamlessly<br>4. Verify completeness |
| **Format Error** | 1. Review correct format requirements<br>2. Identify format discrepancies<br>3. Reformat content<br>4. Verify format correctness |

### Documentation Recovery

| Error Type | Recovery Strategy |
|------------|-------------------|
| **Missing Frontmatter** | 1. Identify required frontmatter fields<br>2. Generate appropriate frontmatter<br>3. Add to document<br>4. Verify format and content |
| **Link Errors** | 1. Identify correct target paths<br>2. Update broken links<br>3. Verify all links resolve correctly<br>4. Update any dependent references |
| **Status Tracking** | 1. Review [Status Tracking System](mdc:meta/assistant_guidelines/status_tracking.md)<br>2. Update incorrect status indicators<br>3. Ensure consistent status across related documents<br>4. Verify accuracy |
| **Metadata Errors** | 1. Review tag conventions<br>2. Correct tag usage<br>3. Update related files if needed<br>4. Verify consistency |

## Self-Correction Protocol

When an error is detected, follow these steps for effective self-correction:

### 1. Acknowledge the Error

- Explicitly identify what went wrong
- Be specific about the nature of the error
- Reference the relevant guideline or convention that was not followed

Example:
```
I notice I've made an error in workflow execution by skipping the essential maintenance step of checking links after file modification.
```

### 2. Assess Impact

- Determine the consequences of the error
- Identify any cascading effects
- Prioritize correction based on severity

Example:
```
This has resulted in potentially broken links in the documentation. Since this affects discoverability, it requires immediate correction.
```

### 3. Plan Correction

- Outline specific steps to correct the error
- Consider the most efficient approach
- Ensure the correction plan won't introduce new errors

Example:
```
To correct this, I will:
1. Identify all links in the modified document
2. Verify each link resolves correctly
3. Fix any broken links
4. Update the task status to reflect this correction
```

### 4. Execute Correction

- Implement the correction plan
- Document changes made
- Update status according to [Status Tracking System](mdc:meta/assistant_guidelines/status_tracking.md)

Example:
```
I've verified all links and fixed the broken reference to 'meta/guidelines/naming_conventions.md' which should have been 'meta/guidelines/tag_conventions.md'.
```

### 5. Verify Correction

- Confirm the error has been fully resolved
- Check that no new issues were introduced
- Update documentation to reflect current state

Example:
```
All links now resolve correctly. I've updated the status to [COMPLETED: 2024-08-17] and noted the link correction in the task documentation.
```

### 6. Implement Prevention

- Identify how to prevent similar errors in the future
- Update guidelines if needed
- Create a mental note for future operations

Example:
```
To prevent similar errors, I'll add an explicit link verification step to my workflow checklist and be more vigilant about following all maintenance steps.
```

## Learning from Errors

To improve over time, maintain an internal awareness of:

1. **Error Patterns**: Notice if certain types of errors occur repeatedly
2. **Context Triggers**: Identify situations that tend to lead to specific errors
3. **Prevention Techniques**: Develop specific strategies to avoid common errors
4. **Recovery Efficiency**: Note which recovery approaches are most effective

When appropriate, suggest improvements to [Self-Governance & Improvement](mdc:meta/assistant_guidelines/self_governance_improvement.md) guidelines based on these learnings.

## Example Error Recovery Scenarios

### Example 1: Workflow Step Omission

**Error**: Forgot to update INDEX.md after creating a new file

**Detection**: Self-detected during workflow checkpoint validation

**Recovery**:
```
I notice I've omitted an important step in the workflow - updating INDEX.md after creating the new documentation file.

Impact: The new file is not discoverable through the index.

Correction plan:
1. Read the current INDEX.md structure
2. Determine the appropriate section for the new file
3. Add an entry with proper formatting and description
4. Verify the entry matches existing style

Executing correction... [tool calls to read and edit INDEX.md]

Correction verified: The new file is now properly listed in INDEX.md with an appropriate description and link.

Prevention: I'll add a specific post-file-creation checklist to my process to ensure INDEX.md is always updated.
```

### Example 2: Content Generation Error

**Error**: Generated code with incorrect import paths

**Detection**: User feedback indicating the code doesn't work

**Recovery**:
```
I see I've made an error in the generated code by using incorrect import paths.

Impact: The code doesn't run as expected, causing frustration and delay.

Correction plan:
1. Review the correct project structure
2. Identify all incorrect import paths
3. Update imports with correct paths
4. Verify the code now works correctly

Executing correction... [tool calls to edit the file]

Correction verified: All import paths now correctly reflect the project structure.

Prevention: I'll be more careful to verify project structure before generating import statements and will test import validity during post-generation verification.
``` 