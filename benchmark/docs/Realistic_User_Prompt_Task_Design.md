---
tags: [task_design, realistic, user_prompts, minimal_specification, task_transformation]
provides: [realistic_task_design_framework, user_prompt_transformation_process, ultra_minimal_task_templates]
requires: [DSS_Benchmark_Analysis, Realistic_Task_Evaluation_Framework, User Interaction Patterns]
date: 2025-01-27
---

# Realistic User Prompt Task Design Framework

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

## Real-World Task Examples

### Task Type: API Development

**Before (Requirements Style):**
```markdown
# Task: User Profile API

## Requirements
Create a comprehensive RESTful API for user profile management that includes:
1. GET /api/users/{id} - Retrieve user profile data
2. PUT /api/users/{id} - Update user profile information
3. POST /api/users/{id}/avatar - Upload profile image
4. DELETE /api/users/{id}/avatar - Remove profile image

## Success Criteria
- All endpoints return appropriate HTTP status codes
- Input validation on all endpoints
- Proper error handling and error messages
- Integration with existing authentication system
- Comprehensive API documentation
```

**After (Realistic Style):**
```markdown
# Task: User Profile API

Users need to be able to view and edit their profiles through the API. 
They should also be able to upload and manage profile pictures.

## Current System
- Flask app with existing auth system
- User model at `src/models/user.py`
```

### Task Type: Frontend Component

**Before (Requirements Style):**
```markdown
# Task: Dashboard Component

## Requirements
Create a React dashboard component that displays:
1. User statistics in card format
2. Recent activity feed
3. Quick action buttons for common tasks
4. Responsive design for mobile and desktop

## Technical Specifications
- Use TypeScript with proper type definitions
- Implement proper loading states
- Include error handling for failed API calls
- Follow existing component patterns
- Add comprehensive unit tests
```

**After (Realistic Style):**
```markdown
# Task: User Dashboard

The app needs a dashboard where users can see their stats, recent activity, and quick actions.

## Current System
- React/TypeScript app
- Existing components in `src/components/`
- API endpoints for user data
```

### Task Type: Data Processing

**Before (Requirements Style):**
```markdown
# Task: CSV Data Import

## Requirements
Implement a data import system that:
1. Accepts CSV file uploads
2. Validates data format and content
3. Processes data in batches for performance
4. Provides import progress feedback
5. Handles errors gracefully with detailed reporting

## Technical Requirements
- Support files up to 10MB
- Validate against existing data schema
- Queue processing for large files
- Rollback capability for failed imports
```

**After (Realistic Style):**
```markdown
# Task: CSV Import

Users need to be able to upload CSV files to import their data into the system.

## Current System
- Python backend with existing data models
- Current data schema in `src/models/`
```

## Common Transformation Patterns

### Pattern 1: Requirements Lists → Single Sentence

**Before:** "The system must provide: 1. Feature A, 2. Feature B, 3. Feature C"
**After:** "Users need [core functionality described naturally]"

### Pattern 2: Technical Specs → Context Mention

**Before:** "Use proper error handling, input validation, and security measures"
**After:** [Remove entirely - trust assistant to apply professional standards]

### Pattern 3: Detailed Context → Essential Context

**Before:** Full project structure explanation with role descriptions
**After:** "Standard [framework] app with existing [relevant files]"

### Pattern 4: Success Criteria → Implicit Expectations

**Before:** Comprehensive list of what constitutes success
**After:** [Remove entirely - judge by user satisfaction with result]

## Quality Checks for Realistic Tasks

### The "Junior Developer Test"

Could you give this task to a competent junior developer and expect them to figure out the details?

**If YES:** Task is realistic
**If NO:** Task is still too prescriptive

### The "Real User Test"

Would someone actually ask for this feature using these exact words?

**If YES:** Language is natural
**If NO:** Still too formal/requirements-like

### The "Context Test"

Does the task include only information the user would naturally mention?

**If YES:** Context is appropriate
**If NO:** Too much explanatory detail

### The "Assumption Test"

Does the task trust the assistant to apply professional standards automatically?

**If YES:** Properly minimal
**If NO:** Over-specified

## Implementation Guidelines

### For Task Authors

1. **Start with user conversation:** How would someone actually ask for this?
2. **Strip formal language:** Remove requirements-speak entirely
3. **Minimize context:** Include only what user would naturally mention
4. **Trust assistant judgment:** Don't specify implementation details
5. **Test with humans:** Would a real user write this request?

### Common Pitfalls to Avoid

**Pitfall 1: Requirements in Disguise**
- Writing "Users should be able to:" followed by numbered lists
- Still thinking in requirements terms, just with different words

**Pitfall 2: Over-Contextualization**
- Explaining project structure in detail
- Providing architectural guidance
- Listing available resources comprehensively

**Pitfall 3: Hidden Instructions**
- Sneaking in quality requirements
- Mentioning specific technologies unnecessarily
- Providing implementation hints

**Pitfall 4: Formal Tone**
- Using "must," "shall," "requirements" language
- Writing like a project specification
- Avoiding conversational phrasing

### Success Indicators

**Good Realistic Task:**
- Reads like actual user request
- Under 30 lines total
- Conversational tone throughout
- Minimal but sufficient context
- Single clear need expressed naturally

**Poor Realistic Task:**
- Still feels like requirements document
- Over-explains context or expectations
- Uses formal specification language
- Provides implementation guidance
- Multiple organized sections

## Measuring Task Realism

### Quantitative Indicators

- **Line count:** Ultra-realistic tasks typically under 25 lines
- **Section count:** Maximum 3 sections (Title, Context, Setup)
- **Specification language:** Zero instances of "must," "shall," "requirements"
- **Lists:** Minimal use of numbered or bulleted lists

### Qualitative Indicators

- **Conversational flow:** Reads like spoken request
- **Natural assumptions:** User assumes assistant competence
- **Business focus:** Emphasizes user value, not technical details
- **Trust-based:** Delegates implementation decisions to assistant

## Conclusion

**The goal is invisible excellence:** Create tasks that feel like real user requests while testing whether DSS rules enable automatic professional practices.

**Success metric:** User gets exactly what they need without having to specify how to build it - just like working with a competent human developer.

**Ultimate test:** Could you give this task to a junior developer and expect similar quality results? If yes, the task is realistic. If no, it's still too prescriptive.

**Key principle:** Real users don't manage developers - they express needs and trust professionals to handle the details. Our realistic tasks should mirror this natural interaction pattern. 