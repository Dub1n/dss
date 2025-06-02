---
task_id: "create-module-01"
max_score: 100
evaluator_version: "1.0"
hidden: true
evaluation_categories: [file_placement, frontmatter_quality, code_structure, documentation, dss_integration, technical_accuracy]
---

# MARKING SCHEME: Create Authentication Module (HIDDEN)

> **⚠️ DO NOT SHOW THIS TO THE ASSISTANT DURING TESTING**

## Scoring Breakdown (100 points total)

### 1. File Placement (25 points)

#### Primary Source File Location (15 points)

* [ ] **Created main auth file in `src/` directory** (8 points)
  * ✅ Full points: File created in `src/auth/` or `src/`
  * ⚠️ Partial: File in `src/` but poor organization (-3 points)
  * ❌ Zero: File outside `src/` directory

* [ ] **Appropriate subdirectory structure** (7 points)
  * ✅ Full points: `src/auth/` or similar logical grouping
  * ⚠️ Partial: `src/` root but reasonable (-3 points)
  * ❌ Zero: Poor directory choice

#### File Organization Logic (10 points)

* [ ] **Follows existing project patterns** (5 points)
  * ✅ Mirrors structure of `api/`, `models/`, `utils/`
  * ❌ Inconsistent with project conventions

* [ ] **Logical file naming** (5 points)
  * ✅ Names like `auth.py`, `authentication.py`, `auth_service.py`
  * ⚠️ Acceptable but not ideal: `login.py`, `user_auth.py` (-2 points)
  * ❌ Poor naming: `module.py`, `file.py`, unclear names

### 2. Frontmatter Quality (20 points)

#### Frontmatter Presence (8 points)

* [ ] **YAML frontmatter present** (8 points)
  * ✅ Complete YAML block with `---` delimiters
  * ⚠️ Present but malformed (-4 points)
  * ❌ Missing frontmatter

#### Required Fields (8 points)

* [ ] **Tags included** (3 points)
  * ✅ Relevant tags: `auth`, `authentication`, `security`, `flask`
  * ⚠️ Generic or minimal tags (-1 point)
  * ❌ Missing tags

* [ ] **Provides specified** (3 points)
  * ✅ Clear exports: `login_user`, `logout_user`, `check_auth`, `auth_service`
  * ⚠️ Vague or incomplete (-1 point)
  * ❌ Missing provides

* [ ] **Requires specified** (2 points)
  * ✅ Dependencies: `user_model`, `session_management`, database, etc.
  * ⚠️ Incomplete dependencies (-1 point)
  * ❌ Missing requires

#### Metadata Quality (4 points)

* [ ] **Appropriate additional fields** (2 points)
  * ✅ Module name, status, or other relevant metadata
  * ❌ No additional relevant metadata

* [ ] **Consistent formatting** (2 points)
  * ✅ Proper YAML syntax, consistent style
  * ❌ Formatting issues

### 3. Code Structure (20 points)

#### Function Implementation (12 points)

* [ ] **All three required functions present** (6 points)
  * ✅ `login_user`, `logout_user`, `check_auth` all implemented
  * ⚠️ 2/3 functions (-2 points)
  * ⚠️ 1/3 functions (-4 points)
  * ❌ Missing core functions

* [ ] **Function signatures correct** (3 points)
  * ✅ Proper parameters and type hints
  * ⚠️ Minor signature issues (-1 point)
  * ❌ Incorrect or missing signatures

* [ ] **Logical function structure** (3 points)
  * ✅ Functions have logical flow and organization
  * ❌ Poor organization or illogical structure

#### Code Quality (8 points)

* [ ] **Docstrings present** (4 points)
  * ✅ All functions have clear docstrings
  * ⚠️ Some docstrings missing (-2 points)
  * ❌ No docstrings

* [ ] **Error handling considered** (2 points)
  * ✅ Basic error handling or try/catch patterns
  * ❌ No error handling consideration

* [ ] **Appropriate imports** (2 points)
  * ✅ Relevant imports for Flask, typing, etc.
  * ❌ Missing or irrelevant imports

### 4. Documentation (15 points)

#### Module Documentation (8 points)

* [ ] **Created documentation file** (4 points)
  * ✅ Documentation in `docs/` directory
  * ⚠️ Documentation in source file only (-2 points)
  * ❌ No dedicated documentation

* [ ] **Usage explanation provided** (4 points)
  * ✅ Clear explanation of how to use the module
  * ⚠️ Basic but incomplete explanation (-2 points)
  * ❌ No usage documentation

#### Documentation Quality (7 points)

* [ ] **Example usage included** (3 points)
  * ✅ Code examples showing how to use functions
  * ❌ No examples

* [ ] **Clear and helpful content** (2 points)
  * ✅ Documentation is clear and useful
  * ❌ Unclear or unhelpful documentation

* [ ] **Proper documentation frontmatter** (2 points)
  * ✅ Documentation file has DSS frontmatter
  * ❌ Missing or incomplete frontmatter

### 5. DSS Integration (10 points)

#### Cross-References (4 points)

* [ ] **Links to related modules** (2 points)
  * ✅ References to `user.py` or other relevant files
  * ❌ No cross-references

* [ ] **Proper mdc: link syntax** (2 points)
  * ✅ Uses `mdc:path/to/file` for internal links
  * ❌ Incorrect or missing link syntax

#### Project Integration (6 points)

* [ ] **INDEX.md consideration** (3 points)
  * ✅ Updated or mentioned need to update INDEX.md
  * ❌ No consideration of project index

* [ ] **Maintains DSS conventions** (3 points)
  * ✅ Follows established patterns throughout
  * ❌ Inconsistent with DSS principles

### 6. Technical Accuracy (10 points)

#### Syntax and Functionality (7 points)

* [ ] **Python syntax correct** (4 points)
  * ✅ Code is syntactically valid Python
  * ⚠️ Minor syntax issues (-2 points)
  * ❌ Major syntax errors

* [ ] **Flask patterns appropriate** (3 points)
  * ✅ Uses Flask conventions and patterns
  * ❌ Doesn't follow Flask best practices

#### Requirements Fulfillment (3 points)

* [ ] **Addresses all task requirements** (3 points)
  * ✅ All specified requirements addressed
  * ⚠️ Most requirements met (-1 point)
  * ❌ Major requirements missing

## Scoring Guidelines

### Deductions

* **Missing required files:** -5 points each
* **Incorrect file placement:** -10 points
* **No frontmatter:** -15 points
* **Broken project structure:** -20 points
* **Non-functional code:** -10 points

### Bonus Points (up to +5)

* **Exceptional organization:** +2 points
* **Creative but appropriate solutions:** +2 points
* **Proactive improvements** (tests, additional docs): +3 points
* **Security considerations:** +2 points

## Evaluation Notes

### Common Issues to Watch For

* Files created in root directory instead of `src/`
* Missing or incomplete frontmatter
* Functions implemented but no documentation
* No consideration of existing project structure
* Generic or inappropriate tags

### Excellent Performance Indicators

* Clean, logical file organization
* Complete, accurate frontmatter
* Well-documented code with examples
* Proper integration with existing structure
* Consideration of security and error handling

### Red Flags

* Files in wrong directories
* No frontmatter at all
* Copy-paste code without understanding
* No documentation or examples
* Ignoring project context

***

**Evaluator Instructions:**

1. Check each criterion systematically
2. Award points based on rubric, not personal preference
3. Document reasoning for partial credit
4. Note patterns for rule effectiveness analysis
5. Record total score and category breakdown
