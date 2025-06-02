---
tags: [evaluation, framework, realistic, user_prompts, task_design, minimal_specification]
provides: [realistic_prompt_framework, ultra_minimal_task_design, natural_user_interaction_patterns]
requires: [DSS_Benchmark_Analysis, Benchmark Tasks, User Interaction Patterns]
date: 2025-01-27
---

# Realistic User Prompt Framework

## The Core Insight

**Real users don't write requirements documents** - they express needs naturally and expect the assistant to figure out the details.

**Current Problem:** Even "stripped" tasks still look like requirements specifications, not natural user requests.

**Solution:** Transform tasks to match actual Cursor usage patterns - brief, conversational, assumption-heavy.

## Task Evolution Analysis

### Stage 1: Instructional (task-01.md - 106 lines)
- Explicit DSS instructions
- Step-by-step workflows
- Process guidance throughout

### Stage 2: Requirements-Focused (task-01-s.md - 77 lines)
- Removed DSS instructions
- Still formal requirements structure
- Detailed success criteria
- Multiple organized sections

### Stage 3: Realistic User Prompt (task-01-xs.md - 21 lines)
- Natural user language
- Minimal context
- Implicit assumptions
- Conversational tone

## What Makes Tasks "Realistic"

### Natural User Language Patterns

**Real users say:**
- "I need auth functionality for my Flask app"
- "Users should be able to log in and out"
- "Add authentication to this project"

**Real users DON'T say:**
- "Create a complete authentication module that includes..."
- "The authentication system must provide: 1. User login functionality..."
- "Function specifications: def login_user(username: str, password: str) -> bool:"

### Implicit Context Assumptions

**Real users assume:**
- You'll figure out appropriate file structure
- You'll use existing patterns in the project
- You'll make reasonable architectural decisions
- You'll add proper documentation automatically

**Real users DON'T:**
- Specify file organization requirements
- List metadata requirements
- Explain project structure in detail
- Provide function signatures

### Conversational Brevity

**Real users:**
- Get to the point quickly
- Assume shared context
- Trust assistant judgment
- Focus on business needs

**Requirements documents:**
- Exhaustively specify details
- Explain all context explicitly
- Define success criteria formally
- Cover edge cases comprehensively

## Transformation Principles

### 1. **User Intent Only**

Strip everything except the core user need:

**Before (Requirements Style):**
```markdown
## Requirements
The authentication system must provide:
1. User login functionality - authenticate user credentials and create session
2. User logout functionality - end user session and cleanup
3. Authentication verification - verify authentication token and return user info
```

**After (User Intent Style):**
```markdown
The Flask web application needs user authentication functionality. 
Users should be able to log in, log out, and the system should verify authentication tokens.
```

### 2. **Minimal Context**

Include only essential context the user would naturally mention:

**Before (Comprehensive Context):**
```markdown
## Current System
**Existing Project Structure:**
- `src/api/` - REST API endpoints
- `src/models/` - Database models (includes `user.py`)
- `src/utils/` - Utility functions
- `docs/` - Project documentation
- `tests/` - Test files

**Available Resources:**
- `src/models/user.py` contains user data structure
- Project follows Flask patterns and conventions
```

**After (Natural Context):**
```markdown
## Current System
- Flask web app with existing user model at `src/models/user.py`
- Standard project structure with `src/`, `docs/`, `tests/` directories
```

### 3. **Implicit Expectations**

Let the assistant infer professional standards rather than specifying them:

**Remove Entirely:**
- Success criteria lists
- Function specifications
- Quality requirements
- Documentation requirements
- Error handling requirements

**Trust Assistant To:**
- Figure out appropriate implementation
- Add proper error handling
- Create necessary documentation
- Follow professional practices

### 4. **Conversational Tone**

Write like a real user talking to an assistant:

**Formal:** "The authentication module should include these core functions:"
**Natural:** "Users need to be able to log in and out"

**Formal:** "Integration with existing user model - work with existing src/models/user.py"
**Natural:** "There's already a user model at src/models/user.py"

## Task Transformation Process

### Step 1: Extract Core User Need

Identify the single business need driving the request:

**Example:**
- Complex description → "Need authentication for Flask app"
- Multiple requirements → "Users need to log in and out"
- Technical specifications → "Add auth functionality"

### Step 2: Strip Requirements Language

Remove formal requirements structure:

**Remove:**
- Numbered requirement lists
- "Must provide" language
- "Success criteria" sections
- Function specifications
- Quality requirements

**Keep:**
- Core functionality description
- Essential context only

### Step 3: Add Natural Context

Include only context a real user would mention:

**Include:**
- Existing relevant files/systems
- Basic project setup information
- Essential constraints

**Exclude:**
- Detailed project structure explanations
- Comprehensive resource lists
- Architectural explanations

### Step 4: Simplify Language

Write in natural, conversational style:

**Formal:** "The system requires authentication verification capability"
**Natural:** "The system should verify authentication tokens"

**Formal:** "Users must be able to authenticate with username and password"
**Natural:** "Users should be able to log in"

## Ultra-Minimal Task Template

```markdown
---
task_id: "meaningful-id"
category: "task-type"
difficulty: "level"
time_limit: "X minutes"
---

# Task: [Natural Title]

[One sentence describing the core user need]

## Current System
[Essential context only - existing files/systems the user would mention]

## Working Environment
[Basic setup - where to work]
```

**Example Application:**

```markdown
---
task_id: "auth-module"
category: "feature_addition"
difficulty: "basic"
time_limit: "10 minutes"
---

# Task: Authentication Module

The Flask web application needs user authentication functionality. 
Users should be able to log in, log out, and the system should verify authentication tokens.

## Current System
- Flask web app with existing user model at `src/models/user.py`
- Standard project structure with `src/`, `docs/`, `tests/` directories

## Working Environment
Create workspace: `task_repos/task_01/`
```

## What This Enables

### True DSS Testing

**Realistic tasks test whether:**
- DSS rules enable automatic professional practices
- Assistants naturally infer good architectural decisions
- Template usage emerges without prompting
- Documentation happens automatically
- File organization follows logical patterns

### Natural User Experience

**Tasks feel like real Cursor usage:**
- Brief, conversational requests
- Assumption of assistant competence
- Focus on business value, not implementation details
- Trust in professional development practices

### Authentic Decision Making

**Assistants must:**
- Interpret user intent intelligently
- Make architectural decisions autonomously
- Apply professional standards automatically
- Coordinate across project systems naturally

## Evaluation Implications

### What We Can Now Measure

**Automatic Intelligence:**
- Does assistant ask clarifying questions naturally?
- Are professional practices applied without instruction?
- Does solution demonstrate understanding of project context?
- Is implementation appropriate for user's apparent skill level?

### What We Can't Measure Directly

**Process Compliance:**
- Can't measure "did you add frontmatter" because task doesn't mention it
- Can't measure "did you follow templates" because task doesn't reference them
- Can't measure "did you update cross-references" because task doesn't specify it

### What We Should Measure Instead

**Emergent Quality:**
- Professional development practices appear automatically
- Solution demonstrates contextual intelligence
- Implementation shows understanding of user needs
- Code quality reflects professional standards

## Implementation Guidelines

### For Task Authors

1. **Start with user conversation:** How would someone actually ask for this?
2. **Strip formal language:** Remove requirements-speak entirely
3. **Minimize context:** Include only what user would naturally mention
4. **Trust assistant judgment:** Don't specify implementation details
5. **Test with humans:** Would a real user write this request?

### For Evaluators

1. **Focus on automatic behaviors:** What happened without being asked?
2. **Assess contextual intelligence:** Did assistant understand the situation?
3. **Measure emergent quality:** Are professional practices evident?
4. **Look for natural decision-making:** Do choices make sense for the context?
5. **Evaluate user experience:** Would the solution satisfy the request?

### For DSS Rule Development

1. **Use realistic tasks as tests:** Rules should enable success on natural requests
2. **Focus on automatic behaviors:** Rules should trigger without explicit instruction
3. **Enable contextual intelligence:** Rules should help assistants read situations
4. **Support natural workflows:** Rules should feel invisible to users
5. **Measure by absence:** Best rules create behaviors users don't have to request

## Conclusion

**The goal is invisible excellence:** DSS rules that enable assistants to handle realistic user requests with automatic professional practices.

**Success metric:** User gets exactly what they need without having to specify how to build it - just like working with a competent human developer.

**Ultimate test:** Could you give this task to a junior developer and expect similar quality results? If yes, the task is realistic. If no, it's still too prescriptive.
