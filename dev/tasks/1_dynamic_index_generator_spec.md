---
tags: [implementation, specification, automation, INDEX, script, python]
provides: [dynamic_index_generator_spec, implementation_details, acceptance_criteria]
requires: [dev/tasks/complete.md, meta/dss_config.yml]
status: draft
priority: high
---

# Dynamic INDEX.md Generator - Implementation Specification

## 1. Component Overview

The Dynamic INDEX.md Generator creates and maintains a comprehensive, navigable index of the entire repository structure that serves as the central navigation hub for both humans and AI assistants.

### 1.1 Purpose

- Eliminate manual maintenance of the repository's navigation document
- Ensure INDEX.md always accurately reflects the current repository structure
- Extract and organize metadata from files to create semantic navigation
- Generate consistent cross-references and maintain link integrity
- Provide LLM-optimized entry point for repository exploration

### 1.2 Core Functions

- Repository structure extraction with configurable depth
- Frontmatter parsing and metadata integration
- Section generation based on folder structure and file tags
- MDC-style linking for Cursor/Obsidian compatibility
- Customizable output formatting with template support
- Preservation of manually added sections and comments

## 2. Technical Design

### 2.1 Architecture

```text
meta/scripts/
├── generate_index.py        # Main script with CLI interface
├── lib/
│   ├── frontmatter.py       # Frontmatter extraction utilities
│   ├── structure.py         # Directory traversal and structure building
│   ├── formatters.py        # Output formatters for different styles
│   └── template.py          # Template engine for custom output
└── templates/
    ├── index_default.jinja  # Default INDEX.md template
    └── index_detailed.jinja # Detailed INDEX.md template
```

### 2.2 Directory Traversal Algorithm

```python
def traverse_directory(root_path, ignore_patterns=None, max_depth=None, current_depth=0):
    """
    Traverse directory structure and build representation.
    
    Args:
        root_path: Path to start traversal
        ignore_patterns: List of glob patterns to ignore
        max_depth: Maximum depth to traverse
        current_depth: Current traversal depth
        
    Returns:
        Dictionary representing directory structure
    """
    if max_depth is not None and current_depth > max_depth:
        return None
        
    result = {
        'path': root_path,
        'name': os.path.basename(root_path),
        'type': 'directory',
        'children': [],
        'metadata': {}
    }
    
    # Check for README.md and extract metadata
    readme_path = os.path.join(root_path, 'README.md')
    if os.path.exists(readme_path):
        result['metadata'] = extract_frontmatter(readme_path)
        result['description'] = extract_description(readme_path)
    
    # Get sorted list of entries in directory
    entries = sorted(os.listdir(root_path))
    
    for entry in entries:
        entry_path = os.path.join(root_path, entry)
        
        # Skip if matches ignore pattern
        if ignore_patterns and any(fnmatch.fnmatch(entry, pattern) for pattern in ignore_patterns):
            continue
            
        if os.path.isdir(entry_path):
            child = traverse_directory(
                entry_path, 
                ignore_patterns, 
                max_depth, 
                current_depth + 1
            )
            if child:
                result['children'].append(child)
        else:
            # Only process files with supported extensions
            if any(entry.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_info = {
                    'path': entry_path,
                    'name': entry,
                    'type': 'file',
                    'metadata': extract_frontmatter(entry_path)
                }
                result['children'].append(file_info)
    
    return result
```

### 2.3 Frontmatter Processing

```python
def extract_frontmatter(file_path):
    """
    Extract frontmatter from file.
    
    Supports:
    - Markdown YAML frontmatter
    - Python triple-quote docstring YAML
    - JavaScript/TypeScript JSDoc YAML
    
    Args:
        file_path: Path to file
        
    Returns:
        Dictionary of frontmatter data
    """
    extension = os.path.splitext(file_path)[1].lower()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if extension in ['.md', '.mdc']:
        # Markdown frontmatter
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return {}
    
    elif extension in ['.py']:
        # Python docstring frontmatter
        match = re.search(r'"""---\s*\n(.*?)\n---\s*"""', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return {}
    
    # Add other file types as needed
    
    return {}
```

### 2.4 Index Generation

```python
def generate_index(structure, template_path=None, preservations=None):
    """
    Generate INDEX.md content from structure.
    
    Args:
        structure: Directory structure from traverse_directory
        template_path: Optional path to custom template
        preservations: Dictionary of sections to preserve from existing INDEX.md
        
    Returns:
        String containing generated INDEX.md content
    """
    if template_path and os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        # Use template engine to render
        return render_template(template_content, {
            'structure': structure,
            'preservations': preservations or {}
        })
    
    # Default generation without template
    output = ["# Repository Index\n\n"]
    
    # Add frontmatter
    output.append("---\n")
    output.append("tags: [index, navigation, documentation]\n")
    output.append("provides: [repository_structure, navigation]\n")
    output.append("requires: []\n")
    output.append("---\n\n")
    
    # Generate Quick Navigation section
    output.append("## Quick Navigation\n\n")
    
    # Add top-level directories
    for child in structure['children']:
        if child['type'] == 'directory':
            name = child['name']
            output.append(f"- [{name}](#{name.lower()})\n")
    
    output.append("\n")
    
    # Generate directory sections
    for child in structure['children']:
        if child['type'] == 'directory':
            generate_directory_section(child, output)
    
    return "".join(output)
```

## 3. Implementation Plan

### 3.1 Phase 1: Core Structure Extraction (Week 1)

- Implement directory traversal with ignore patterns
- Add support for custom depth
- Build basic file information gathering
- Set up configuration loading from meta/dss_config.yml

### 3.2 Phase 2: Metadata Integration (Week 1-2)

- Implement frontmatter extraction for all supported file types
- Add tag-based organization capabilities
- Create metadata index structure
- Implement caching for performance optimization

### 3.3 Phase 3: Output Generation (Week 2)

- Create default INDEX.md format
- Implement template engine for custom formats
- Add preservation of manual sections
- Generate navigation sections based on structure

### 3.4 Phase 4: CLI and Integration (Week 3)

- Create command-line interface
- Add Git hooks integration
- Implement validation and error handling
- Create documentation and examples

## 4. Acceptance Criteria

### 4.1 Functional Requirements

- [ ] **Complete Structure Extraction**: Correctly traverses all directories and files with proper filtering
- [ ] **Accurate Metadata**: Extracts and processes frontmatter from all supported file types
- [ ] **Configurable Output**: Supports different output formats through templates
- [ ] **Link Integrity**: All generated links are valid and properly formatted
- [ ] **Manual Preservation**: Preserves user-defined sections when regenerating
- [ ] **Performance**: Processes repositories with 1000+ files in under 30 seconds

### 4.2 Technical Requirements

- [ ] **Well-documented Code**: All functions have docstrings and clear parameter descriptions
- [ ] **Extensive Error Handling**: Gracefully handles malformed frontmatter, missing files, and permission issues
- [ ] **Test Coverage**: 90%+ unit test coverage for all core functions
- [ ] **Modular Architecture**: Separation of concerns between traversal, metadata, and generation
- [ ] **Configuration Support**: Reads settings from meta/dss_config.yml with sensible defaults

### 4.3 User Experience Requirements

- [ ] **Intuitive CLI**: Clear help text and error messages
- [ ] **Useful Output**: Generated INDEX.md is immediately useful for navigation
- [ ] **Non-destructive**: Does not destroy user customizations
- [ ] **Visible Progress**: Shows progress during generation for large repositories

## 5. Integration Points

### 5.1 Git Integration

```bash
#!/bin/bash
# Pre-commit hook to update INDEX.md

python meta/scripts/generate_index.py --check
if [ $? -ne 0 ]; then
    echo "INDEX.md is out of date. Running generator..."
    python meta/scripts/generate_index.py
    git add INDEX.md
fi
```

### 5.2 GitHub Actions Integration

```yaml
name: Update INDEX.md

on:
  push:
    branches: [ main ]
    paths-ignore:
      - 'INDEX.md'

jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate INDEX.md
        run: python meta/scripts/generate_index.py
      - name: Commit changes
        uses: EndBug/add-and-commit@v7
        with:
          add: 'INDEX.md'
          message: 'Auto-update INDEX.md'
```

## 6. Performance Considerations

- **Caching**: Implement file hash-based caching to avoid reprocessing unchanged files
- **Parallelization**: Use multi-threading for frontmatter extraction in large repositories
- **Memory Efficiency**: Stream large files rather than loading entirely in memory
- **Incremental Updates**: Support updating only changed portions of INDEX.md

## 7. Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Incorrect frontmatter parsing | High | Medium | Extensive testing with various formats; fallback mechanisms |
| Performance issues with large repos | Medium | Medium | Implement caching and incremental generation |
| Conflicts with user edits | High | High | Clear documentation on preserved sections; conflict resolution |
| Template engine failures | Medium | Low | Fallback to simple generation; error reporting |

## 8. Future Enhancements

- **Intelligent Section Organization**: Use AI to suggest logical groupings of files
- **Embedded Visualizations**: Add mermaid.js diagrams of repository structure
- **Search Optimization**: Generate additional metadata to improve search relevance
- **Custom Views**: Support different views (technical, business, etc.) of the same repository
- **Incremental Updates**: Support updating only portions of INDEX.md that have changed

## 9. Development Estimates

| Task | Effort (days) | Dependencies |
|------|---------------|--------------|
| Core structure extraction | 2 | None |
| Frontmatter processing | 3 | Core structure extraction |
| Output generation | 2 | Frontmatter processing |
| CLI and integration | 2 | Output generation |
| Testing and validation | 3 | All previous tasks |
| Documentation | 1 | All previous tasks |

**Total Estimated Time**: 2-3 weeks (1 developer)

## 10. Implementation Assistant Prompts

0.
    > _**Initial Setup Phase**_

1. **Project Structure Setup**:
   "Create the directory structure for the INDEX.md generator script following the architecture in the specification. Set up the `meta/scripts/generate_index.py` main file and create placeholder files for the supporting modules in the lib directory."

2. **Define Core Types**:
   "Define the core data structures for representing directory structure, file metadata, and generation options in a new file `meta/scripts/lib/types.py`. Include type hints and docstrings that clearly explain the purpose of each type."

3. **Dependency Management**:
   "Add the necessary dependencies to requirements.txt for the INDEX.md generator, including libraries for YAML parsing, path manipulation, and any other required functionality."

    > _**Core Implementation Phase**_

4. **Directory Traversal Implementation**:
   "Implement the directory traversal algorithm in `meta/scripts/lib/structure.py` based on the pseudocode in the specification. Include support for ignore patterns, depth limiting, and metadata extraction."

5. **Frontmatter Processing Implementation**:
   "Implement the frontmatter extraction functions in `meta/scripts/lib/frontmatter.py` with support for Markdown, Python, and other file types as shown in the specification. Ensure proper error handling for malformed frontmatter."

6. **Index Generation Implementation**:
   "Implement the INDEX.md content generation logic in `meta/scripts/lib/formatters.py`. Include support for both default generation and template-based generation, ensuring proper Markdown formatting."

7. **Template Engine Integration**:
   "Create a simple template engine in `meta/scripts/lib/template.py` that can parse and render Jinja-like templates for INDEX.md generation, allowing for customizable output formats."

8. **Section Preservation Logic**:
   "Implement the logic for preserving custom sections when regenerating INDEX.md. This should identify and extract user-defined sections and reintegrate them during generation."

    > _**CLI and Integration Phase**_

9. **Command-line Interface Implementation**:
   "Implement the command-line interface in the main `generate_index.py` script, including argument parsing, help text, and exit code handling. Follow the DSS CLI standards with clear help messages and examples."

10. **Configuration Integration**:
    "Add support for reading configuration from `meta/dss_config.yml`, implementing fallbacks for missing settings and documentation for available options."

11. **Git Hook Integration**:
    "Create the Git pre-commit hook script as specified in section 5.1 of the specification. Ensure it properly checks and updates INDEX.md when needed."

12. **GitHub Actions Integration**:
    "Implement the GitHub Actions workflow file as specified in section 5.2 for automatically updating INDEX.md on pushes to main."

    > _**Testing and Documentation Phase**_

13. **Unit Test Implementation**:
    "Create comprehensive unit tests for the directory traversal, frontmatter extraction, and INDEX generation functions. Include edge cases like empty directories, malformed frontmatter, and special characters in paths."

14. **Integration Test Implementation**:
    "Implement integration tests that verify the entire INDEX.md generation process works correctly with various repository structures. Use the test fixtures described in the Integration Testing specification."

15. **Documentation Updates**:
    "Create user documentation for the INDEX.md generator in `docs/tools/index_generator.md`, including installation, usage examples, and configuration options."

16. **Code Quality Review**:
    "Review the entire implementation for code quality, performance optimization, and adherence to the specification. Apply the improvements from section 6 (Performance Considerations) of the specification."

    > _**Final Verification Phase**_

17. **Cross-component Integration Check**:
    "Verify that the INDEX.md generator integrates correctly with the Template Customization Framework and Frontmatter Validation tools. Fix any integration issues that arise."

18. **End-to-end Testing**:
    "Perform an end-to-end test of the INDEX.md generator on a complex repository structure. Verify that all functional and performance requirements are met."

19. **Documentation Verification**:
    "Review all documentation, help text, and error messages to ensure they are clear, accurate, and helpful to users."

20. **Final Code Review**:
    "Conduct a final code review using the DSS code review criteria. Ensure the code is clean, well-documented, and adheres to all DSS standards."

When implementing each part, follow the Code Modification workflow from the DSS guidelines, which includes:

1. Analyze the current state and the specification
2. Check for existing templates or patterns
3. Implement the changes with proper testing
4. Update documentation
5. Validate dependencies and cross-references
