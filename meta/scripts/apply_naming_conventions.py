#!/usr/bin/env python
"""
apply_naming_conventions.py
===========================

A script to apply LLM-optimized naming conventions to the repository.
This script reads naming rules from dss_config.yml and renames files accordingly.

Usage:
    python meta/scripts/apply_naming_conventions.py [--dry-run]
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Optional

# Load configuration
def load_config() -> Dict:
    """Load naming rules from dss_config.yml"""
    config_path = Path(__file__).parent.parent / "dss_config.yml"
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}")
        return {}
    
    print(f"Loading configuration from {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    naming_rules = config.get('naming_rules', {})
    print(f"Found naming_rules: {bool(naming_rules)}")
    if naming_rules:
        print(f"  - Document format: {naming_rules.get('doc_format')}")
        print(f"  - Generic terms: {len(naming_rules.get('generic_terms', []))} terms")
        print(f"  - Transformations: {len(naming_rules.get('transformations', {}))} rules")
    
    return naming_rules

def transform_filename(path: Path, rules: Dict) -> str:
    """Transform a filename according to naming conventions"""
    if not rules:
        print(f"  No rules provided for {path.name}")
        return path.name
    
    # Extract file stem and extension
    stem = path.stem
    suffix = path.suffix.lower()
    
    # Check if this file should be ignored
    rel_path_str = path.relative_to(Path.cwd()).as_posix()
    ignore_patterns = rules.get('ignore_patterns', [])
    for pattern in ignore_patterns:
        if Path(rel_path_str).match(pattern):
            print(f"  - Ignoring {path.name} (matches pattern {pattern})")
            return path.name  # Skip transformation for ignored patterns
    
    # Check for specific overrides
    overrides = rules.get('overrides', {})
    if rel_path_str in overrides:
        new_name = overrides[rel_path_str]
        print(f"  - Override for {path.name} -> {new_name}")
        return new_name
    
    # Get transformation style based on file extension
    transformations = rules.get('transformations', {})
    transform_style = transformations.get(suffix, "keep")
    
    # If no transformation rule, keep original
    if transform_style == "keep":
        print(f"  - No transformation rule for extension {suffix}")
        return path.name
    
    print(f"  - Transforming {path.name} using style: {transform_style}")
    
    # Transform based on style
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
    
    # Check for generic terms that should be prefixed
    generic_terms = rules.get('generic_terms', [])
    domain_prefixes = rules.get('domain_prefixes', {})
    
    parent_name = path.parent.name
    if transformed.lower() in generic_terms and parent_name in domain_prefixes:
        prefix = domain_prefixes[parent_name]
        print(f"  - Adding prefix {prefix} to {transformed}")
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
    
    new_filename = transformed + suffix
    print(f"  - Result: {path.name} -> {new_filename}")
    return new_filename

def process_directory(directory: Path, rules: Dict, dry_run: bool = False) -> List[tuple]:
    """Process a directory recursively and rename files according to conventions"""
    renamed_files = []
    file_count = 0
    
    for item in directory.rglob('*'):
        if item.is_file():
            file_count += 1
            # Get new filename
            new_name = transform_filename(item, rules)
            
            # Debug
            rel_path = item.relative_to(Path.cwd())
            print(f"  Checking {rel_path}")
            
            # If filename would change
            if new_name != item.name:
                new_path = item.parent / new_name
                
                # Check if destination already exists
                if new_path.exists() and new_path != item:
                    print(f"Warning: Cannot rename {item.name} to {new_name} as it already exists")
                    continue
                
                renamed_files.append((item, new_path))
                
                if not dry_run:
                    try:
                        # Rename the file
                        item.rename(new_path)
                        print(f"Renamed: {item.relative_to(Path.cwd())} -> {new_path.relative_to(Path.cwd())}")
                    except Exception as e:
                        print(f"Error renaming {item}: {e}")
                else:
                    print(f"Would rename: {item.relative_to(Path.cwd())} -> {new_path.relative_to(Path.cwd())}")
    
    print(f"  Found {file_count} files, {len(renamed_files)} to rename")
    return renamed_files

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Apply LLM-optimized naming conventions to the repository")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be renamed without making changes")
    args = parser.parse_args()
    
    # Load naming rules
    rules = load_config()
    if not rules:
        print("Error: No naming rules found in configuration")
        return
    
    print(f"{'Dry run mode - ' if args.dry_run else ''}Applying naming conventions...")
    
    # Process directories
    directories_to_process = [
        Path.cwd() / "src",
        Path.cwd() / "meta/scripts",
        Path.cwd() / "docs",
        Path.cwd() / "tests"
    ]
    
    all_renamed = []
    for directory in directories_to_process:
        if directory.exists():
            print(f"\nProcessing {directory.relative_to(Path.cwd())}...")
            renamed = process_directory(directory, rules, args.dry_run)
            all_renamed.extend(renamed)
    
    # Summary
    print(f"\nSummary: {len(all_renamed)} files would be renamed" if args.dry_run 
          else f"\nSummary: {len(all_renamed)} files renamed")

if __name__ == "__main__":
    main() 