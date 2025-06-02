---
task_id: "complex-integration-06"
category: "multi_file_coordination"
difficulty: "advanced"
time_limit: "20 minutes"
focus_areas: [workflow_selection, template_usage, cross_file_maintenance, dependency_management, architecture_decisions]
rules_testing: [task_decomposition, maintenance_integration, template_first, cross_references]
---
# Task 06: Complex Feature Integration

You are working on a **Flask web application** that needs a complete user profile management feature.  
This task requires coordinating changes across multiple files, making architectural decisions, and maintaining project integrity.

## 📋 Complex Requirements

Implement a complete user profile system that includes:

1. **Database model extension** (extend existing user model)
2. **API endpoints** for profile operations (CRUD)
3. **Authentication integration** (using existing auth module)
4. **Data validation** and error handling
5. **Comprehensive documentation** with cross-references
6. **Project structure updates** (INDEX, navigation, etc.)

## ⚙️ Setup Your Task Repository

**First, create your isolated task environment:**

```powershell
# Create your task directory
mkdir task_repos/task_06
cd task_repos/task_06

# Copy all required source files
mkdir -p src/models src/auth src/api
cp ../../task_repos/src/models/user.py src/models/
cp ../../task_repos/src/auth/authentication.py src/auth/

# Create the fixed API init file (without broken import)
@"
---
tags: [api, flask, endpoints, blueprints]
provides: [api_blueprint, api_routes]
requires: [flask]
---

"""API module for Flask application endpoints."""

from flask import Blueprint

# Main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# API endpoint configurations and routes will be defined in sub-modules
"@ | Out-File -FilePath src/api/__init__.py -Encoding UTF8

# Create complete project structure
mkdir -p src/utils docs tests
```

This gives you all existing components plus a working API structure to build upon.

## 🎯 Current Project Context

**Existing Structure:**

* `src/models/user.py` - Basic user model (needs extension)
* `src/auth/authentication.py` - Authentication module (integrate with)
* `src/api/` - API directory (needs profile endpoints)
* `docs/` - Documentation (needs profile docs + updates)

**Key Challenge:** This task requires you to understand the existing codebase, make architectural decisions,  
and coordinate changes across multiple files while maintaining DSS standards.

## 📝 Specific Implementation Requirements

### 1. User Model Extension

Extend `src/models/user.py` to include:

* Profile fields (bio, avatar_url, preferences, etc.)
* Profile-specific methods
* Data validation
* Proper DSS frontmatter updates

### 2. API Endpoints (`src/api/profiles.py`)

Create complete CRUD API:

```python
GET /api/profiles/{user_id}     # Get profile
PUT /api/profiles/{user_id}     # Update profile  
POST /api/profiles/upload       # Upload avatar
DELETE /api/profiles/{user_id}  # Delete profile
```

### 3. Authentication Integration

* Use existing auth module for route protection
* Ensure proper user context handling
* Validate user permissions (users can only edit own profiles)

### 4. Data Models (`src/models/profile.py`)

Create separate profile model if needed:

* Profile data structure
* Validation rules
* Database relationships

### 5. Utilities (`src/utils/validation.py`)

Profile-specific utilities:

* Input validation functions
* Image processing helpers
* Data sanitization

### 6. Documentation Updates

* Create `docs/user-profiles.md` with complete API documentation
* Update related documentation with cross-references
* Maintain consistency across all docs

### 7. Project Integration

* Update project navigation/INDEX if exists
* Ensure all cross-references are maintained
* Follow DSS dependency management

## 🧩 Architectural Decisions Required

You must make and document decisions about:

1. **Model Architecture:** Extend User model vs. separate Profile model?
2. **API Design:** RESTful patterns and error handling
3. **File Organization:** Where to place different components?
4. **Validation Strategy:** Centralized vs. distributed validation?
5. **Integration Approach:** How to integrate with existing auth?

## 🔍 Success Criteria

### Core Functionality (50%)

* [ ] Working CRUD operations for user profiles
* [ ] Proper authentication integration
* [ ] Data validation and error handling
* [ ] Syntactically correct, runnable code

### DSS Integration (30%)

* [ ] Proper file placement following existing patterns
* [ ] Complete frontmatter with accurate dependencies
* [ ] Cross-references between related files
* [ ] Documentation updates and integration

### Architecture & Coordination (20%)

* [ ] Sound architectural decisions
* [ ] Proper dependency management
* [ ] Coordinated changes across multiple files
* [ ] Maintains project integrity

## ⚡ Getting Started

**This task deliberately provides minimal scaffolding.** You must:

1. **Analyze existing code** to understand patterns
2. **Choose appropriate workflow** based on complexity
3. **Make architectural decisions** about implementation
4. **Coordinate changes** across multiple files
5. **Maintain DSS standards** throughout

## 🎯 What This Tests

Unlike simple tasks, this tests:

* **Workflow selection** (should this be task decomposition?)
* **Template usage** (are there patterns to follow?)
* **Cross-file coordination** (multiple files must work together)
* **Maintenance integration** (docs, deps, cross-refs must be updated)
* **Architectural thinking** (how should this be structured?)
* **Context awareness** (understanding existing codebase)

## 📚 Available Resources

* Existing `src/models/user.py` for patterns
* Existing `src/auth/authentication.py` for integration
* Project structure for organization guidance
* DSS templates and conventions (if configured)

***

**Time Limit:** 20 minutes
**Complexity:** This requires coordinating 4-6 files with architectural decisions
**Focus:** Workflow selection, template usage, cross-file maintenance, architecture
