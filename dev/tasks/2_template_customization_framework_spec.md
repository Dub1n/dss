---
tags: [implementation, specification, templates, customization, framework]
provides: [template_customization_spec, implementation_details, acceptance_criteria]
requires: [dev/tasks/complete.md, meta/templates/]
status: draft
priority: medium
---

# Template Customization Framework - Implementation Specification

## 1. Component Overview

The Template Customization Framework provides a flexible system for creating, customizing, and applying templates for different project types and file formats, ensuring consistent structure and metadata across the repository.

### 1.1 Purpose

- Standardize file creation across different project types and domains
- Reduce manual effort in creating properly structured files
- Ensure consistent metadata and format across similar files
- Support project-specific customizations while maintaining DSS standards
- Enable automated template application through scripts and tools

### 1.2 Core Functions

- Template discovery and categorization
- Customization point identification and processing
- Variable substitution and conditional content
- Template inheritance and composition
- Project type detection and template selection
- Metadata injection and validation

## 2. Technical Design

### 2.1 Architecture

```text
meta/
├── templates/                        # Template storage
│   ├── python/                       # Python-specific templates
│   │   ├── module.py.template        # Python module template
│   │   └── class.py.template         # Python class template
│   ├── markdown/                     # Markdown templates
│   │   ├── documentation.md.template # Documentation template
│   │   └── index.md.template         # Index template
│   ├── javascript/                   # JavaScript templates
│   │   └── component.js.template     # JS component template
│   └── project_types/                # Project type configurations
│       ├── data_science.yml          # Data science project config
│       ├── web_application.yml       # Web application project config
│       └── documentation.yml         # Documentation project config
└── scripts/
    ├── template_processor.py         # Main template processing script
    ├── lib/
    │   ├── template_engine.py        # Template rendering engine
    │   ├── variable_resolver.py      # Variable resolution logic
    │   └── project_detector.py       # Project type detection
    └── templates/
        └── cli_templates/            # Templates for CLI output
```

### 2.2 Template Format

Templates use a Jinja2-inspired syntax with DSS-specific extensions:

```text
---
template_name: "Python Module Template"
template_description: "Standard Python module with DSS frontmatter"
template_version: "1.0.0"
template_variables:
  module_name:
    description: "Name of the module"
    required: true
  author:
    description: "Author name"
    required: false
    default: ""
  requires:
    description: "Module dependencies"
    required: false
    default: []
  provides:
    description: "Module exports"
    required: true
---
"""---
tags: [python, module, {% if tags %}{{ tags|join(', ') }}{% endif %}]
provides: [{{ module_name }}{% if provides %}, {{ provides|join(', ') }}{% endif %}]
requires: [{% if requires %}{{ requires|join(', ') }}{% endif %}]
{% if author %}author: {{ author }}{% endif %}
---"""

# {{ module_name }}.py
{% if module_description %}"""
{{ module_description }}
"""{% endif %}

{% if imports %}
{{ imports }}
{% endif %}

{% if classes %}
{{ classes }}
{% endif %}

{% if functions %}
{{ functions }}
{% endif %}

{% if __main__ %}
if __name__ == "__main__":
    {{ __main__ }}
{% endif %}
```

### 2.3 Project Type Configuration

Project types are defined in YAML configuration files:

```yaml
name: "Data Science Project"
description: "Template configuration for data science projects"
default_templates:
  python_module: "python/module.py.template"
  notebook: "jupyter/analysis.ipynb.template"
  documentation: "markdown/documentation.md.template"
  readme: "markdown/data_science_readme.md.template"
default_variables:
  author: ""
  organization: ""
  license: "MIT"
directory_structure:
  - name: "data"
    description: "Data files and datasets"
    templates:
      readme: "markdown/data_readme.md.template"
  - name: "notebooks"
    description: "Jupyter notebooks for analysis"
    templates:
      exploration: "jupyter/exploration.ipynb.template"
      visualization: "jupyter/visualization.ipynb.template"
  - name: "src"
    description: "Source code"
    templates:
      module: "python/module.py.template"
      utils: "python/utils.py.template"
  - name: "docs"
    description: "Documentation"
    templates:
      readme: "markdown/documentation.md.template"
```

### 2.4 Template Processing Algorithm

```python
def process_template(template_path, output_path, variables, project_type=None):
    """
    Process a template and generate output file.
    
    Args:
        template_path: Path to template file
        output_path: Path for generated output file
        variables: Dictionary of variables for substitution
        project_type: Optional project type for additional configuration
        
    Returns:
        Boolean indicating success
    """
    # Load project type configuration if specified
    project_config = {}
    if project_type:
        project_config = load_project_configuration(project_type)
        
    # Merge project default variables with provided variables
    merged_variables = {**project_config.get('default_variables', {}), **variables}
    
    # Load and parse template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract template metadata
    template_metadata = extract_template_metadata(template_content)
    
    # Validate required variables
    missing_variables = validate_required_variables(
        template_metadata.get('template_variables', {}),
        merged_variables
    )
    
    if missing_variables:
        raise ValueError(f"Missing required variables: {', '.join(missing_variables)}")
    
    # Apply template engine
    output_content = render_template(
        strip_template_metadata(template_content),
        merged_variables
    )
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    return True
```

### 2.5 Project Type Detection

```python
def detect_project_type(directory_path):
    """
    Detect project type based on existing files and structure.
    
    Args:
        directory_path: Path to project directory
        
    Returns:
        String with detected project type or None
    """
    # Check for key indicators
    has_notebooks = glob.glob(os.path.join(directory_path, "**/*.ipynb"), recursive=True)
    has_package_json = os.path.exists(os.path.join(directory_path, "package.json"))
    has_requirements_txt = os.path.exists(os.path.join(directory_path, "requirements.txt"))
    has_setup_py = os.path.exists(os.path.join(directory_path, "setup.py"))
    has_mkdocs_yml = os.path.exists(os.path.join(directory_path, "mkdocs.yml"))
    
    # Check for data directories
    has_data_dir = os.path.isdir(os.path.join(directory_path, "data"))
    
    # Decision tree for project type
    if has_notebooks and has_data_dir:
        return "data_science"
    elif has_package_json:
        return "web_application"
    elif has_setup_py:
        return "python_package"
    elif has_mkdocs_yml:
        return "documentation"
    
    # Check content of key files for more hints
    # [additional detection logic]
    
    return None
```

## 3. Implementation Plan

### 3.1 Phase 1: Core Template Engine (Week 1)

- Implement basic template parsing and rendering
- Create variable substitution logic
- Build template metadata extraction
- Develop required variable validation

### 3.2 Phase 2: Project Type System (Week 1-2)

- Implement project type configuration format
- Create project type detection logic
- Build directory structure generation
- Develop template selection based on project type

### 3.3 Phase 3: Template Library (Week 2)

- Create standard templates for common file types:
  - Python modules, classes, scripts
  - Markdown documentation
  - Jupyter notebooks
  - JavaScript/TypeScript files
  - Configuration files (YAML, JSON)
- Develop project type configurations for:
  - Data science projects
  - Web applications
  - Documentation projects
  - Python packages

### 3.4 Phase 4: CLI and Integration (Week 3)

- Create command-line interface for template application
- Build interactive template selection and customization
- Implement project initialization commands
- Add file creation commands

## 4. Acceptance Criteria

### 4.1 Functional Requirements

- [ ] **Template Variety**: Includes templates for all common file types in DSS projects
- [ ] **Variable Substitution**: Correctly processes all template variables
- [ ] **Project Type Support**: Detects and configures for at least 4 standard project types
- [ ] **Customization Points**: Supports at least 10 customization points per template
- [ ] **Directory Generation**: Creates directory structures based on project type
- [ ] **Inheritance**: Supports template inheritance and composition

### 4.2 Technical Requirements

- [ ] **Extensible Engine**: Template engine can be extended with new features
- [ ] **Error Handling**: Provides clear errors for template problems
- [ ] **Performance**: Processes templates in under 1 second
- [ ] **Compatibility**: Works on Windows, macOS, and Linux
- [ ] **Documentation**: Includes clear documentation on creating and extending templates

### 4.3 User Experience Requirements

- [ ] **Intuitive CLI**: Clear help text and interactive prompts
- [ ] **Useful Defaults**: Sensible defaults for all optional variables
- [ ] **Customization Flow**: Logical flow for template customization
- [ ] **Helpful Errors**: Clear error messages with suggested fixes
- [ ] **Preview Mode**: Option to preview generated files before creating

## 5. Integration Points

### 5.1 Integration with Dynamic INDEX.md Generator

```python
# After creating files from templates, update INDEX.md
if update_index:
    try:
        subprocess.run(["python", "meta/scripts/generate_index.py"], check=True)
        print("Updated INDEX.md successfully")
    except subprocess.CalledProcessError:
        print("Warning: Failed to update INDEX.md")
```

### 5.2 Integration with Frontmatter Validation

```python
# After creating files from templates, validate frontmatter
if validate_frontmatter:
    try:
        subprocess.run(["python", "meta/scripts/validate_frontmatter.py", 
                       "--files", output_path], check=True)
        print("Validated frontmatter successfully")
    except subprocess.CalledProcessError:
        print("Warning: Frontmatter validation failed")
```

### 5.3 Editor Integration

```javascript
// VS Code extension snippet for template selection
function activateTemplateSelection(context) {
    let disposable = vscode.commands.registerCommand(
        'dss.createFromTemplate', 
        async function() {
            // Get template categories
            const categories = await getTemplateCategories();
            
            // Show quick pick for category
            const category = await vscode.window.showQuickPick(
                categories, 
                { placeHolder: 'Select template category' }
            );
            
            if (!category) return;
            
            // Get templates in selected category
            const templates = await getTemplatesInCategory(category);
            
            // Show quick pick for template
            const template = await vscode.window.showQuickPick(
                templates, 
                { placeHolder: 'Select template' }
            );
            
            if (!template) return;
            
            // Get template variables
            const variables = await promptForVariables(template);
            
            // Apply template
            await applyTemplate(template, variables);
        }
    );
    
    context.subscriptions.push(disposable);
}
```

## 6. Performance Considerations

- **Template Caching**: Cache parsed templates to avoid repeated parsing
- **Lazy Loading**: Load project type configurations only when needed
- **Efficient Rendering**: Use optimized template rendering for large templates
- **Parallelization**: Process multiple files in parallel when generating projects

## 7. Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Template syntax errors | High | Medium | Validation before processing; clear error reporting |
| Missing template variables | Medium | High | Required variable validation; interactive prompts |
| Template compatibility issues | Medium | Medium | Template versioning; compatibility checks |
| Project type misdetection | Medium | Medium | Manual override option; confidence scoring |
| Output file conflicts | High | Low | Confirmation prompts; backup existing files |

## 8. Future Enhancements

- **Template Marketplace**: Community-contributed templates
- **Remote Templates**: Support for fetching templates from Git repositories
- **Template Updates**: Mechanism to update existing files with template changes
- **AI-assisted Customization**: Integrate with LLMs for intelligent template filling
- **Visual Template Editor**: GUI for creating and editing templates
- **Template Analytics**: Track template usage and customization patterns

## 9. Development Estimates

| Task | Effort (days) | Dependencies |
|------|---------------|--------------|
| Core template engine | 3 | None |
| Project type system | 2 | Core template engine |
| Template library | 3 | Core template engine |
| CLI and integration | 2 | All previous tasks |
| Testing and validation | 2 | All previous tasks |
| Documentation | 1 | All previous tasks |

**Total Estimated Time**: 2-3 weeks (1 developer)

## 10. Implementation Assistant Prompts

The following prompts can be used to guide an AI assistant through implementing this specification using the DSS Code Modification workflow:

0.
    > _**Initial Setup Phase**_

1. **Project Structure Setup**:
   "Create the directory structure for the Template Customization Framework following the architecture in section 2.1 of the specification. Set up the `meta/scripts/template_processor.py` main file and create placeholder files for the supporting modules in the lib directory."

2. **Template Format Design**:
   "Define the template format specification in `meta/scripts/lib/template_format.py`, implementing the Jinja2-inspired syntax with DSS-specific extensions shown in section 2.2. Include comprehensive documentation of the syntax."

3. **Project Type Configuration Format**:
   "Create the YAML schema for project type configurations as shown in section 2.3. Implement validation functions to ensure configurations follow this schema correctly."

    > _**Core Implementation Phase**_

4. **Template Engine Core Implementation**:
   "Implement the core template engine in `meta/scripts/lib/template_engine.py` that can parse templates, extract metadata, and handle variable substitution. Follow the implementation in section 2.2 with support for conditional blocks and loops."

5. **Variable Resolution Implementation**:
   "Create the variable resolution system in `meta/scripts/lib/variable_resolver.py` that handles default values, required variables, and variable type validation. Include robust error reporting for missing or invalid variables."

6. **Project Type Detection Implementation**:
   "Implement the project type detection algorithm in `meta/scripts/lib/project_detector.py` based on the pseudocode in section 2.5. Ensure it correctly identifies project types based on file patterns and directory structures."

7. **Template Processing Implementation**:
   "Implement the main template processing function in `meta/scripts/lib/template_processor.py` following the algorithm in section 2.4. Include support for project type configuration, variable merging, and template rendering."

8. **Template Library Creation**:
   "Create the standard template library for common file types as listed in section 3.3. Include templates for Python modules, classes, Markdown documentation, Jupyter notebooks, and configuration files."

    > _**CLI and Integration Phase**_

9. **Command-line Interface Implementation**:
   "Implement the command-line interface in the main `template_processor.py` script, including argument parsing, help text, and interactive prompts for template customization. Follow DSS CLI standards with clear help messages and examples."

10. **Project Initialization Command**:
    "Add the project initialization command to the CLI that can set up a complete project structure based on project type configurations. Implement directory creation, template application, and initial file generation."

11. **File Creation Command**:
    "Implement the file creation command that applies a single template to create a new file. Include support for variable specification via command line and interactive prompts for required variables."

12. **Integration with Dynamic INDEX.md Generator**:
    "Implement the integration with the INDEX.md generator as specified in section 5.1. Ensure that after creating files from templates, the INDEX.md is automatically updated to include the new files."

13. **Integration with Frontmatter Validation**:
    "Implement the integration with the frontmatter validation tool as specified in section 5.2. Ensure that after creating files from templates, the frontmatter is validated to confirm correctness."

    > _**Editor Integration Phase**_

14. **VS Code Extension Integration**:
    "Implement the VS Code extension integration as shown in section 5.3. Create the necessary functions for template selection, category browsing, and variable prompting within the VS Code environment."

15. **Template Preview Implementation**:
    "Add a preview mode to the template processor that shows the generated file content without actually creating the file. This allows users to verify the output before committing to file creation."

    > _**Testing and Documentation Phase((_))

16. **Unit Test Implementation**:
    "Create comprehensive unit tests for the template engine, variable resolution, and project detection functions. Include tests for edge cases like complex templates, missing variables, and unusual project structures."

17. **Integration Test Implementation**:
    "Implement integration tests that verify the entire template processing workflow, including project type detection, template selection, variable resolution, and file creation. Use the test fixtures described in the Integration Testing specification."

18. **Documentation Creation**:
    "Create user documentation for the Template Customization Framework in `docs/tools/template_framework.md`, including installation, usage examples, template syntax guide, and project type configuration reference."

19. **Template Authoring Guide**:
    "Create a detailed template authoring guide in `docs/tools/template_authoring.md` that explains how to create custom templates, use the template syntax, define variables, and implement conditional logic."

20. **Project Type Configuration Guide**:
    "Write a project type configuration guide in `docs/tools/project_types.md` that explains how to define custom project types, specify default templates, and configure directory structures."

    > _**Final Verification Phase**_

21. **Cross-component Integration Check**:
    "Verify that the Template Customization Framework integrates correctly with the Dynamic INDEX.md Generator and Frontmatter Validation tools. Fix any integration issues that arise."

22. **Template Library Verification**:
    "Review all templates in the standard library to ensure they follow DSS conventions, include proper frontmatter, and generate correctly formatted output for all supported file types."

23. **End-to-end Testing**:
    "Perform end-to-end testing of the Template Customization Framework by creating a complete project from scratch, adding new files with templates, and verifying that all generated files meet DSS standards."

24. **Performance Optimization**:
    "Implement the performance optimizations described in section 6, including template caching, lazy loading, and efficient rendering. Measure and document the performance improvements."

25. **Final Code Review**:
    "Conduct a final code review using the DSS code review criteria. Ensure the code is clean, well-documented, and adheres to all DSS standards."

When implementing each part, follow the Code Modification workflow from the DSS guidelines, which includes:

1. Analyze the current state and the specification
2. Check for existing templates or patterns
3. Implement the changes with proper testing
4. Update documentation
5. Validate dependencies and cross-references
