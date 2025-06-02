---
tags: [benchmark, execution, minimal_guidance]
provides: [task_execution_workflow, workspace_setup]
requires: [realistic_tasks]
---

# Benchmark Task Execution Guide

*Minimal guidance for completing benchmark tasks without evaluation contamination.*

## 🎯 Quick Instructions

**Your job:** Complete the specified benchmark task using only your rules and the task requirements.

**Key principle:** Work exactly as you would if a real user asked you to implement the functionality described.

## 📁 Workspace Setup

### Create Task Workspace

For each task, work in an isolated environment:

```bash
# Create your task directory
mkdir task_repos/task_[XX]
cd task_repos/task_[XX]

# Basic structure (create as needed)
mkdir -p src docs tests
```

**Examples:**

- `task_repos/task_01/` for task-01-xs.md
- `task_repos/task_06/` for task-06-xs.md

## 🎯 Available Tasks

### Realistic Authentication Tasks

- **task-01-xs.md** - Minimal authentication module
- **task-001.md** - Authentication module (alternative realistic version)

### Realistic Integration Tasks

- **task-06-xs.md** - User profile management
- **task-08-xs.md** - Notification system integration

### Task Selection

**If user specifies task:** Complete that specific task
**If user says "run benchmark":** Ask which task they want you to complete

Example user request patterns:

- "Complete benchmark task 01-xs"
- "Run task-001"
- "Complete task-06-xs following this guide"

## 🚀 Execution Workflow

### Step 1: Read Task

- Open the specified task file (e.g., `tasks/task-01-xs.md`)
- Read the requirements and context
- Understand what functionality is needed

### Step 2: Complete Task

- Work in your task workspace (`task_repos/task_XX/`)
- Implement the required functionality
- Work exactly as you would for a real user request
- Use your DSS rules and professional judgment

### Step 3: Ready for Evaluation

- When finished, inform the user you've completed the task
- Be ready to evaluate your work (separate process)

## 📋 What You're Implementing

### Task Examples

**Authentication Module (task-01-xs):**

- Users need to log in, log out, verify tokens
- Flask web application context
- Integrate with existing user model

**Profile Management (task-06-xs):**

- Users need profile viewing/editing capability
- Include bio, avatar, preferences functionality
- Work with existing authentication system

**Notification Integration (task-08-xs):**

- Legacy notification system needs integration
- Email and in-app notifications required
- User preference management needed

## ⚡ Key Points

### Work Naturally

- **Follow your rules** for organization, documentation, patterns
- **Use professional judgment** for implementation decisions
- **Work as you would** for any real user request

### Stay Focused

- **Complete the functionality** described in the task
- **Don't worry about evaluation** during implementation
- **Don't overthink the process** - just implement what's needed

### Workspace Isolation

- **All work in task_repos/task_XX/** to keep things organized
- **Copy existing files** if you need to reference/modify them
- **Document your approach** as you would normally

## 🔄 Example Session

```text
User: "Complete benchmark task 01-xs following this guide"

You: 
1. Create task_repos/task_01/ workspace
2. Read tasks/task-01-xs.md 
3. Implement authentication functionality using your rules
4. Report completion: "Task completed. Ready for evaluation."
```

## 🎯 Success = Natural Implementation

**Good signs:**

- You implement functionality that meets the user's needs
- You follow your normal professional practices
- You organize and document work as you typically would
- You make sound technical decisions based on context

**Remember:** There's no "trick" or special approach needed. Just implement the requested functionality professionally using your  
rules as guidance.

---

**When ready to evaluate your work:** Use the separate evaluation guide (EVALUATE_BENCHMARK.md) to score your implementation.
