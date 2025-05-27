---
tags: [documentation, algorithm, validation, frontmatter]
provides: [frontmatter_validation_algorithm]
requires: [meta/guidelines/validation_rules.md, meta/scripts/frontmatter_utils.py]
---

# Frontmatter Validation Algorithm Design

This document describes the algorithm design for validating and auto-correcting frontmatter in DSS files as implemented in `meta/scripts/frontmatter_utils.py`.

## 1. Validation Algorithm

### High-Level Flow

```
START
  ├─ Load configuration
  ├─ For each file:
  │   ├─ Extract frontmatter based on file type
  │   │   ├─ If no frontmatter exists:
  │   │   │   └─ Report missing frontmatter
  │   │   └─ If frontmatter exists:
  │   │       ├─ Parse YAML
  │   │       │   ├─ If parse fails:
  │   │       │   │   └─ Report malformed YAML
  │   │       │   └─ If parse succeeds:
  │   │       │       └─ Validate against rules
  │   │       └─ Report validation results
  │   └─ If auto-correction enabled:
  │       ├─ Apply corrections
  │       └─ Update file if not in dry-run mode
  └─ Report overall results
END
```

### Detailed Steps

#### 1.1 Configuration Loading

1. Attempt to load the DSS configuration from `meta/dss_config.yml`
2. Extract validation-related settings:
   - Default field values
   - Required fields
   - File patterns to include/exclude
3. Handle missing or malformed configuration with sensible defaults

#### 1.2 Frontmatter Extraction

1. Determine file type based on extension
2. Apply appropriate regex pattern to extract frontmatter:
   - Markdown: `^---\s*\n(.*?)\n---\s*\n`
   - Python: `"""---\s*\n(.*?)\n---\s*"""`
3. Return None if no frontmatter is found
4. Return empty dict if YAML is malformed

#### 1.3 Validation Rules Application

1. Check for presence of required fields:
   - `tags`: Required, must be a list of strings
   - `provides`: Required, must be a list of strings
   - `requires`: Required, must be a list of strings
2. Check data types of each field
3. For each validation rule:
   - Apply rule to frontmatter
   - Collect errors with clear messages
4. Return list of validation errors, empty if valid

## 2. Auto-correction Algorithm

### High-Level Flow

```
START
  ├─ Copy original frontmatter
  ├─ For each required field:
  │   └─ If field is missing:
  │       └─ Add field with default value from config
  ├─ For specific fields (tags, provides, requires):
  │   ├─ If field exists but is not a list:
  │   │   ├─ If field is a string:
  │   │   │   └─ Convert to single-item list
  │   │   └─ If field is other type:
  │   │       └─ Replace with appropriate default
  │   └─ If field exists and is a list:
  │       └─ Validate each item is a string
  ├─ Format corrected frontmatter as YAML
  └─ Return corrected frontmatter and list of corrections
END
```

### Detailed Steps

#### 2.1 Default Values Addition

1. Copy the original frontmatter to avoid modifying the input
2. For each field in the configuration defaults:
   - If field is missing in frontmatter, add with default value
   - Record the addition in the corrections list

#### 2.2 Type Correction

1. For each special field (tags, provides, requires):
   - If not a list, but is a string: convert to single-item list
   - If not a list and not a string: replace with appropriate default
   - Record the correction in the corrections list

#### 2.3 File Update

1. Extract the original content around the frontmatter
2. Generate new frontmatter in the appropriate format for the file type
3. Combine with original content
4. If not in dry-run mode, write back to the file

## 3. File Processing Algorithm

### High-Level Flow

```
START
  ├─ Check if file is of a supported type
  ├─ Extract frontmatter
  │   ├─ If extraction fails:
  │   │   └─ Return error
  │   └─ If extraction succeeds:
  │       ├─ Validate frontmatter
  │       ├─ If validation fails and auto-correct is enabled:
  │       │   ├─ Apply auto-corrections
  │       │   └─ If not in dry-run mode:
  │       │       └─ Update file with corrected frontmatter
  │       └─ Return validation results and corrections
  └─ END
```

### Detailed Steps

#### 3.1 File Selection

1. Check if file has an extension that supports frontmatter (.md, .py)
2. Check if file should be excluded based on config patterns
3. Only proceed with supported files that aren't excluded

#### 3.2 Processing and Reporting

1. Extract and validate frontmatter
2. If auto-correction is enabled:
   - Apply corrections
   - If not in dry-run mode, update the file
3. Report:
   - File path
   - Validation status (valid/invalid)
   - List of errors (if any)
   - List of corrections applied (if any)
   - Whether file was modified

## 4. Extension Points

The algorithm is designed with the following extension points:

1. **Custom Validators**: Additional validation functions can be added
2. **Custom Correctors**: Additional correction strategies can be added
3. **File Type Support**: Additional file types can be supported by adding appropriate extraction patterns
4. **Configuration Options**: Additional configuration options can be added to control behavior

## 5. Implementation Considerations

1. **Performance**: Optimize for handling large repositories with many files
2. **Error Handling**: Provide clear, actionable error messages
3. **Non-destructive**: Ensure original file content outside frontmatter is preserved
4. **Testability**: Design for comprehensive unit testing
5. **User Experience**: Focus on providing useful feedback and minimal false positives 