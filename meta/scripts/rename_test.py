#!/usr/bin/env python
"""
rename_test.py
===============

A simple script to test filename transformations on specific files.
"""

import os
import re
import yaml
from pathlib import Path

# Load config
config_path = Path(__file__).parent.parent / "dss_config.yml"
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

naming_rules = config.get('naming_rules', {})
print(f"Loaded naming rules: {bool(naming_rules)}")
print(f"Generic terms: {naming_rules.get('generic_terms')}")
print(f"Domain prefixes: {naming_rules.get('domain_prefixes')}")

# Only focus on hypothetical files that would be transformed
files_to_check = [
    # Hypothetical files that would be transformed
    "meta/scripts/utils.py",           # Generic term, should be prefixed
    "meta/scripts/api.py",             # Generic term, should be prefixed
    "meta/scripts/camelCaseFile.py",   # Camel case, should be snake_case
    "meta/scripts/PascalCaseFile.py",  # Pascal case, should be snake_case
    "meta/scripts/kebab-case-file.py", # Kebab case, should be snake_case
    "docs/utils.md",                   # Generic term but no prefix defined for 'docs'
    "src/utils.py",                    # Generic term with prefix defined for 'src'
    "src/api.py",                      # Generic term with prefix defined for 'src'
    "src/App.py",                      # Generic term with prefix defined for 'src'
]

# Functions from apply_naming_conventions.py
def transform_filename(path_str, rules):
    """Transform a filename according to naming conventions"""
    path = Path(path_str)
    
    # Extract file stem and extension
    stem = path.stem
    suffix = path.suffix.lower() if path.suffix else ""
    
    # Always treat these as hypothetical
    print("  (Hypothetical file for testing)")
    
    # Get transformation style based on file extension
    transformations = rules.get('transformations', {})
    transform_style = transformations.get(suffix, "keep")
    
    print(f"File: {path.name}, Extension: {suffix}, Style: {transform_style}")
    
    # If no transformation rule, keep original
    if transform_style == "keep":
        print("  - No transformation rule")
        return path.name
    
    # Transform based on style
    original_stem = stem
    if transform_style == "snake_case":
        # Convert PascalCase or camelCase to snake_case
        transformed = re.sub(r'(?<!^)(?=[A-Z])', '_', stem).lower()
        transformed = re.sub(r'[-\s]', '_', transformed)
    elif transform_style == "kebab-case":
        # Convert to kebab-case
        transformed = re.sub(r'(?<!^)(?=[A-Z])', '-', stem).lower()
        transformed = re.sub(r'[_\s]', '-', transformed)
    elif transform_style == "camelCase":
        # Convert to camelCase
        parts = re.split(r'[-_\s]', stem)
        transformed = parts[0].lower() + ''.join(p.capitalize() for p in parts[1:])
    elif transform_style == "PascalCase":
        # Convert to PascalCase
        parts = re.split(r'[-_\s]', stem)
        transformed = ''.join(p.capitalize() for p in parts)
    else:
        # Unknown style, keep original
        transformed = stem
    
    # Did the case style transform change anything?
    if transformed != original_stem:
        print(f"  - After case transform: {original_stem} -> {transformed}")
    else:
        print(f"  - No case transformation needed")
    
    # Check for generic terms that should be prefixed
    generic_terms = rules.get('generic_terms', [])
    domain_prefixes = rules.get('domain_prefixes', {})
    
    parent_name = path.parent.name
    if transformed.lower() in generic_terms:
        print(f"  - Term '{transformed}' is in generic terms list")
        
        if parent_name in domain_prefixes:
            prefix = domain_prefixes[parent_name]
            print(f"  - Adding prefix '{prefix}' from parent directory '{parent_name}'")
            
            # Apply the same case style to the prefix
            if transform_style == "snake_case":
                prefix = prefix.lower()
                transformed = f"{prefix}_{transformed}"
            elif transform_style == "kebab-case":
                prefix = prefix.lower()
                transformed = f"{prefix}-{transformed}"
            elif transform_style == "camelCase":
                transformed = prefix.lower() + transformed[0].upper() + transformed[1:]
            elif transform_style == "PascalCase":
                transformed = prefix.capitalize() + transformed
        else:
            print(f"  - No prefix defined for parent directory '{parent_name}'")
    
    new_filename = transformed + suffix
    if new_filename != path.name:
        print(f"  - Result: {path.name} -> {new_filename}")
    else:
        print(f"  - No change in filename")
    
    return new_filename

# Process each file
for file_path in files_to_check:
    print("\n" + "=" * 50)
    print(f"Processing: {file_path}")
    
    path = Path(file_path)
    
    # Compute new name
    new_name = transform_filename(file_path, naming_rules)
    
    if new_name != path.name:
        print(f"  Would rename to: {new_name}")
    else:
        print(f"  No change needed")

print("\nDone") 