---
tags: [documentation, algorithm, frontmatter, auto_correction]
provides: [frontmatter_auto_correction_logic]
requires: [meta/guidelines/validation_rules.md, meta/scripts/frontmatter_utils.py]
---

# Frontmatter Auto-Correction Logic

This document describes the detailed auto-correction logic for fixing frontmatter issues in DSS files. This logic is implemented in `meta/scripts/frontmatter_utils.py` and follows the validation rules defined in `meta/guidelines/validation_rules.md`.

## Auto-Correction Strategy

The auto-correction logic is designed to fix common frontmatter issues while preserving as much of the original content as possible. The strategy prioritizes:

1. **Non-destructive fixes**: Corrections that add missing information or fix formats without losing existing data
2. **Minimal changes**: Making only the changes necessary to meet validation requirements
3. **Clear reporting**: Providing detailed information about what was changed and why

## Correction Rules

### 1. Missing Required Fields

When required fields are missing:

```python
for field, default_value in config["defaults"].items():
    if field not in frontmatter:
        frontmatter[field] = default_value
        corrections.append(f"Added missing field: {field}")
```

#### Examples:

| Original | Corrected | Correction Message |
|----------|-----------|-------------------|
| `{}` | `{"tags": ["draft"], "provides": [], "requires": []}` | Added missing field: tags<br>Added missing field: provides<br>Added missing field: requires |
| `{"tags": ["doc"]}` | `{"tags": ["doc"], "provides": [], "requires": []}` | Added missing field: provides<br>Added missing field: requires |

### 2. Invalid Field Types

When fields have incorrect types:

#### 2.1 Tags Field

```python
if "tags" in frontmatter:
    if not isinstance(frontmatter["tags"], list):
        if isinstance(frontmatter["tags"], str):
            frontmatter["tags"] = [frontmatter["tags"]]
            corrections.append("Converted tags from string to list")
        else:
            frontmatter["tags"] = ["draft"]
            corrections.append("Replaced invalid tags with ['draft']")
```

#### Examples:

| Original | Corrected | Correction Message |
|----------|-----------|-------------------|
| `{"tags": "documentation"}` | `{"tags": ["documentation"]}` | Converted tags from string to list |
| `{"tags": {"key": "value"}}` | `{"tags": ["draft"]}` | Replaced invalid tags with ['draft'] |

#### 2.2 Provides/Requires Fields

```python
for field in ["provides", "requires"]:
    if field in frontmatter:
        if not isinstance(frontmatter[field], list):
            if isinstance(frontmatter[field], str):
                frontmatter[field] = [frontmatter[field]]
                corrections.append(f"Converted {field} from string to list")
            else:
                frontmatter[field] = []
                corrections.append(f"Replaced invalid {field} with empty list")
```

#### Examples:

| Original | Corrected | Correction Message |
|----------|-----------|-------------------|
| `{"provides": "data_model"}` | `{"provides": ["data_model"]}` | Converted provides from string to list |
| `{"requires": 123}` | `{"requires": []}` | Replaced invalid requires with empty list |

### 3. Invalid Items in Lists

When list items have incorrect types:

```python
for field in ["tags", "provides", "requires"]:
    if field in frontmatter and isinstance(frontmatter[field], list):
        corrected_list = []
        list_corrected = False
        
        for item in frontmatter[field]:
            if isinstance(item, str):
                corrected_list.append(item)
            else:
                list_corrected = True
                # Skip non-string items
        
        if list_corrected:
            frontmatter[field] = corrected_list
            corrections.append(f"Removed non-string items from {field}")
```

#### Examples:

| Original | Corrected | Correction Message |
|----------|-----------|-------------------|
| `{"tags": ["doc", 123, "code"]}` | `{"tags": ["doc", "code"]}` | Removed non-string items from tags |
| `{"provides": [{"name": "model"}, "data"]}` | `{"provides": ["data"]}` | Removed non-string items from provides |

## File Update Process

### Markdown Files

For Markdown files, the frontmatter is updated by:

1. Extracting the content after the frontmatter section
2. Creating new frontmatter with the corrected values
3. Combining the new frontmatter with the original content

```python
def update_markdown_frontmatter(file_path, corrected_frontmatter):
    content = file_path.read_text(encoding="utf-8")
    match = MD_FRONTMATTER_PATTERN.match(content)
    
    if match:
        # Extract content after frontmatter
        remainder = content[match.end():]
        
        # Create new frontmatter
        yaml_str = yaml.dump(corrected_frontmatter, default_flow_style=False)
        new_frontmatter = f"---\n{yaml_str}---\n"
        
        # Combine and write back
        new_content = new_frontmatter + remainder
        file_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False
```

### Python Files

For Python files, the frontmatter is updated by:

1. Extracting the content before and after the frontmatter section
2. Creating new frontmatter with the corrected values
3. Combining the parts while preserving any other docstring content

```python
def update_python_frontmatter(file_path, corrected_frontmatter):
    content = file_path.read_text(encoding="utf-8")
    match = PY_FRONTMATTER_PATTERN.search(content)
    
    if match:
        # Extract content before and after frontmatter
        prefix = content[:match.start()]
        suffix = content[match.end():]
        
        # Check if there's additional docstring content
        docstring_match = re.match(r'"""(.*?)"""', content[match.end():], re.DOTALL)
        additional_docstring = docstring_match.group(1) if docstring_match else ""
        
        # Create new frontmatter
        yaml_str = yaml.dump(corrected_frontmatter, default_flow_style=False)
        new_frontmatter = f'"""---\n{yaml_str}---{additional_docstring}"""'
        
        # Combine and write back
        new_content = prefix + new_frontmatter + suffix
        file_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False
```

## Special Cases

### 1. Adding Frontmatter to Files Without It

For files that should have frontmatter but don't:

```python
def add_frontmatter_to_file(file_path, file_type, config):
    # Create default frontmatter
    frontmatter = config.get("defaults", {})
    
    # Get file content
    content = file_path.read_text(encoding="utf-8")
    
    if file_type == "markdown":
        # Add markdown frontmatter
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        new_content = f"---\n{yaml_str}---\n\n{content}"
    elif file_type == "python":
        # Add python frontmatter
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        
        # Check if file already has a docstring
        docstring_match = re.match(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            # Replace existing docstring
            docstring_content = docstring_match.group(1)
            new_docstring = f'"""---\n{yaml_str}---\n{docstring_content}"""'
            new_content = re.sub(r'""".*?"""', new_docstring, content, 1, re.DOTALL)
        else:
            # Add new docstring with frontmatter
            new_content = f'"""---\n{yaml_str}---"""\n\n{content}'
    
    file_path.write_text(new_content, encoding="utf-8")
    return True
```

### 2. Handling Malformed YAML

For frontmatter with syntax errors:

```python
def fix_malformed_yaml(yaml_str):
    # Common YAML syntax errors and their fixes
    fixes = [
        # Missing quotes around strings with special characters
        (r'(\w+):\s*([^{\[\]}\n]*[:#].+)', r'\1: "\2"'),
        # Fix indentation
        (r'^(\s+)-\s+(.+)$', r'\1- \2'),
        # Add quotes around dates
        (r'(\w+):\s*(\d{4}-\d{2}-\d{2})', r'\1: "\2"'),
    ]
    
    fixed_str = yaml_str
    for pattern, replacement in fixes:
        fixed_str = re.sub(pattern, replacement, fixed_str, flags=re.MULTILINE)
    
    try:
        # Test if the fixed YAML is valid
        yaml.safe_load(fixed_str)
        return fixed_str
    except yaml.YAMLError:
        # If still invalid, return a minimal valid YAML
        return '{"tags": ["draft"], "provides": [], "requires": []}'
```

## Related Documentation

- [Frontmatter Validation Rules](mdc:meta/guidelines/validation_rules.md)
- [Frontmatter Validation Algorithm](mdc:meta/scripts/docs/frontmatter_validation_algorithm.md)
- [DSS Configuration](mdc:meta/dss_config.yml) 