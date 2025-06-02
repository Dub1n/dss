---
task_id: "maintenance-heavy-08"
category: "maintenance_integration"
difficulty: "intermediate"
time_limit: "15 minutes"
focus_areas: [template_usage, maintenance_automation, cross_references, documentation_consistency]
rules_testing: [template_first_approach, automatic_maintenance, cross_reference_management, documentation_refactoring]
---

# Task 08: Legacy Code Integration & Documentation Overhaul

You need to integrate a **legacy notification system** into the existing DSS project and update all related documentation.  
This task heavily tests template usage, maintenance automation, and cross-reference management.

## 📋 Requirements

### 1. Integration Task

Add a notification system with these components:

* **Email notifications** for user events
* **In-app notifications** for real-time alerts
* **Notification preferences** user management
* **Integration with existing auth/user systems**

### 2. Heavy Maintenance Requirements

This task specifically requires:

* **Template utilization** for consistent file creation
* **Cross-reference management** across multiple existing docs
* **Documentation updates** to maintain consistency
* **Dependency tracking** and frontmatter maintenance
* **Link integrity** maintenance across the project

## ⚙️ Setup Your Task Repository

**First, create your isolated task environment:**

```powershell
# Create your task directory
mkdir task_repos/task_08
cd task_repos/task_08

# Copy all existing source files
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

# Create existing documentation structure
mkdir -p docs
@"
---
tags: [documentation, authentication, api]
provides: [auth_documentation, authentication_guide]
requires: [authentication_module]
---

# Authentication Documentation

Complete authentication system documentation.

## Features
- User authentication via authentication.py module
- Session management and user context
- Integration with user management system

## Integration Points
- Works with User model from models/user.py
- Provides decorators for route protection
- Supports user identification via headers

## Related Systems
- User management: See models/user.py
- API endpoints: See api/ modules
"@ | Out-File -FilePath docs/authentication.md -Encoding UTF8

# Create complete project structure
mkdir -p src/utils src/services tests
```

This gives you the complete existing system to integrate with, plus documentation that needs maintenance updates.

## 🎯 Current Project State

**Existing Files to Work With:**

* `src/models/user.py` - Needs notification preferences
* `src/auth/authentication.py` - Needs notification triggers
* `docs/authentication.md` - Needs notification cross-references
* `docs/` - Multiple docs need updates
* Various other project files

**Legacy Code to Integrate:**

```python
# Legacy notification code (needs DSS integration)
class NotificationService:
    def send_email(self, user_id, message):
        # Basic email sending
        pass
    
    def create_notification(self, user_id, type, content):
        # Create in-app notification
        pass
```

## 🧪 Success Criteria Focus

This task specifically tests **maintenance and template effectiveness:**

### Template Usage (30%)

* [ ] **Template discovery:** Evidence of checking for existing templates
* [ ] **Pattern following:** New files follow existing project patterns
* [ ] **Frontmatter templating:** Consistent metadata across all files
* [ ] **Documentation templating:** Docs follow established formats

### Maintenance Integration (40%)

* [ ] **Cross-reference updates:** Updated existing docs with new references
* [ ] **Link integrity:** Proper mdc: links between related files
* [ ] **Dependency tracking:** Accurate provides/requires updates
* [ ] **Documentation consistency:** Maintained style and structure across docs

### Integration Quality (30%)

* [ ] **Code integration:** Properly integrated with existing auth/user systems
* [ ] **DSS compliance:** All files follow DSS conventions
* [ ] **Project coherence:** Changes feel like natural extensions of existing code

## 📝 Specific Deliverables

### 1. New Files (Using Templates)

* `src/services/notifications.py` - Main notification service
* `src/models/notification.py` - Notification data model
* `src/utils/email_sender.py` - Email utility functions
* `docs/notifications.md` - Complete notification documentation

### 2. Updated Files (Maintenance Focus)

* `src/models/user.py` - Add notification preferences
* `src/auth/authentication.py` - Add notification triggers
* `docs/authentication.md` - Add notification cross-references
* Any other relevant documentation requiring updates

### 3. Project-Wide Maintenance

* Update cross-references in ALL relevant documentation
* Ensure link integrity across the project
* Maintain frontmatter consistency
* Update any project navigation/index files

## 🎯 Template-First Testing

This task specifically tests whether you:

1. **Look for templates** before creating new files
2. **Follow existing patterns** from similar files in the project
3. **Use consistent frontmatter** patterns across all files
4. **Apply documentation templates** for new docs

## 🔧 Maintenance Automation Testing

This task tests whether you automatically:

1. **Update cross-references** when adding new functionality
2. **Maintain link integrity** across documentation
3. **Update dependencies** in frontmatter when integrating systems
4. **Keep documentation consistent** when adding new content

## ⚠️ Maintenance Traps

This task includes several scenarios that test maintenance automation:

* **New notification system** should be cross-referenced in auth docs
* **User model changes** should be reflected in related documentation
* **Service integration** should update dependency tracking
* **New docs** should be linked from existing relevant docs

**Without good rules:** Assistant creates files in isolation without maintenance

**With good rules:** Assistant automatically maintains project integrity

## 🧪 Key Tests

### Template Utilization Test

🔍 Does the assistant:

* Check existing files for patterns before creating new ones?
* Use consistent frontmatter across all files?
* Follow established naming and structure conventions?
* Leverage existing documentation formats?

### Maintenance Integration Test

🔍 Does the assistant:

* Update existing documentation with new cross-references?
* Maintain link integrity when adding new files?
* Update dependency tracking automatically?
* Keep project navigation consistent?

### Cross-Reference Management Test

🔍 Does the assistant:

* Add mdc: links between related files?
* Update existing docs to reference new functionality?
* Maintain bidirectional linking where appropriate?
* Consider impact on existing documentation?

## 📊 Expected Outcomes

### With Effective DSS Rules (85-100 points)

* Clear evidence of template checking and usage
* Automatic maintenance of cross-references and links
* Consistent frontmatter and documentation patterns
* Proactive updates to existing documentation
* Sound integration with existing systems

### Without Effective Rules (40-65 points)

* Files created without checking templates
* No maintenance of existing documentation
* Inconsistent frontmatter and patterns
* Poor integration with existing systems
* Isolated file creation without project consideration

## ⏱️ Time Allocation

**Recommended:**

* **Template research (3-4 minutes):** Understanding existing patterns
* **File creation (6-8 minutes):** Creating new files following templates
* **Maintenance (4-5 minutes):** Updating existing files and documentation
* **Integration validation (2-3 minutes):** Ensuring everything works together

## 📚 Resources

* Existing codebase for pattern analysis
* DSS templates (if configured)
* Current documentation structure
* Cross-reference and linking conventions

***

**Core Test:** This task should show a dramatic difference between assistants with good DSS rules (who automatically handle maintenance)  
versus those without (who create files in isolation).
