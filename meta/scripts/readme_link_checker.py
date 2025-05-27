#!/usr/bin/env python3
"""---
tags: [automation, documentation, validation]
provides: [readme_link_checker]
requires: [meta/dss_config.yml]
---"""

"""
README Link Checker

Scans README.md files throughout the project to identify files that are not 
properly linked in their folder's README.md. Generates a temporary TODO file
and creates a prompt for the assistant to update the relevant READMEs.

Usage:
    python meta/scripts/readme_link_checker.py [--dry-run] [--output temp_readme_todos.md]
"""

import os
import sys
import yaml
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple
import argparse


def load_dss_config(config_path: str = "meta/dss_config.yml") -> dict:
    """Load DSS configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Config file {config_path} not found, using defaults")
        return {
            'ignore': [],
            'patterns': {
                'docs': ['**/*.md'],
                'code': ['**/*.py'],
                'data': ['**/*.csv', '**/*.json'],
                'binary': ['**/*.png', '**/*.jpg']
            }
        }


def should_ignore_path(path: Path, ignore_patterns: List[str]) -> bool:
    """Check if a path should be ignored based on ignore patterns."""
    path_str = str(path)
    for pattern in ignore_patterns:
        if pattern in path_str or path.match(pattern):
            return True
    return False


def extract_mdc_links(readme_content: str) -> Set[str]:
    """Extract all MDC links from README content."""
    # Pattern to match [text](mdc:filepath)
    mdc_pattern = r'\[.*?\]\(mdc:([^)]+)\)'
    matches = re.findall(mdc_pattern, readme_content)
    return set(matches)


def extract_table_files(readme_content: str) -> Set[str]:
    """Extract filenames mentioned in Files table."""
    files = set()
    
    # Look for Files table section
    lines = readme_content.split('\n')
    in_files_table = False
    
    for line in lines:
        if line.strip().startswith('## Files'):
            in_files_table = True
            continue
        elif line.strip().startswith('##') and in_files_table:
            break
        
        if in_files_table and '|' in line and not line.strip().startswith('|---'):
            # Extract filename from table row
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2 and parts[1]:
                # Extract filename from potential MDC link
                filename = parts[1]
                if filename.startswith('[') and '](mdc:' in filename:
                    # Extract from MDC link: [file.md](mdc:file.md)
                    match = re.search(r'\[([^]]+)\]\(mdc:[^)]+\)', filename)
                    if match:
                        filename = match.group(1)
                elif filename.startswith('[') and '](' in filename:
                    # Extract from regular link: [file.md](file.md)
                    match = re.search(r'\[([^]]+)\]', filename)
                    if match:
                        filename = match.group(1)
                
                if filename and filename != 'file':  # Skip template placeholder
                    files.add(filename)
    
    return files


def get_directory_files(directory: Path, ignore_patterns: List[str]) -> Set[str]:
    """Get all files in a directory that should be documented."""
    files = set()
    
    if not directory.is_dir():
        return files
    
    for item in directory.iterdir():
        if item.is_file() and not should_ignore_path(item, ignore_patterns):
            files.add(item.name)
    
    return files


def check_readme_completeness(readme_path: Path, ignore_patterns: List[str]) -> Tuple[Set[str], Set[str]]:
    """Check if README includes all files in its directory."""
    directory = readme_path.parent
    
    # Get all files that should be documented
    all_files = get_directory_files(directory, ignore_patterns)
    
    # Read README content
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return set(), all_files
    
    # Extract files mentioned in README
    linked_files = extract_mdc_links(readme_content)
    table_files = extract_table_files(readme_content)
    
    # Combine all mentioned files (remove directory paths for comparison)
    mentioned_files = set()
    for f in linked_files | table_files:
        mentioned_files.add(Path(f).name)
    
    # Find missing files
    missing_files = all_files - mentioned_files
    
    return mentioned_files, missing_files


def scan_project_readmes(ignore_patterns: List[str]) -> Dict[str, Set[str]]:
    """Scan all README.md files in the project for missing file links."""
    missing_by_readme = {}
    
    # Find all README.md files
    for readme_path in Path('.').rglob('README.md'):
        if should_ignore_path(readme_path, ignore_patterns):
            continue
        
        mentioned, missing = check_readme_completeness(readme_path, ignore_patterns)
        
        if missing:
            missing_by_readme[str(readme_path)] = missing
    
    return missing_by_readme


def generate_todo_file(missing_by_readme: Dict[str, Set[str]], output_path: str):
    """Generate a temporary TODO file with missing links."""
    content = """---
tags: [temporary, documentation, todo]
provides: [readme_update_tasks]
requires: []
---

# Temporary README Update Tasks

This file was automatically generated by `readme_link_checker.py` to identify 
README.md files that are missing links to files in their directories.

## Missing File Links

"""
    
    for readme_path, missing_files in missing_by_readme.items():
        content += f"### {readme_path}\n\n"
        content += "Missing file links:\n"
        for file in sorted(missing_files):
            content += f"- `{file}`\n"
        content += "\n"
    
    content += """
## Instructions for Assistant

Please update the README.md files listed above to include the missing files in their Files tables using the following format:

```markdown
| file | purpose | tags |
|------|---------|------|
| [filename.ext](mdc:filename.ext) | Description needed | [tag1, tag2] |
```

For each missing file:
1. Add an appropriate entry to the Files table
2. Include an MDC link in the format: `[filename.ext](mdc:filename.ext)`
3. Add a meaningful purpose description
4. Extract tags from the file's YAML front-matter (if present)

After updating, delete this temporary file.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Check README.md files for missing file links')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show results without generating TODO file')
    parser.add_argument('--output', default='temp_readme_todos.md',
                       help='Output file for TODO list (default: temp_readme_todos.md)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_dss_config()
    ignore_patterns = config.get('ignore', [])
    
    # Add common ignore patterns
    ignore_patterns.extend([
        '**/.git/**',
        '**/.venv/**',
        '**/node_modules/**',
        '**/__pycache__/**',
        '**/🔒archive/**'
    ])
    
    print("Scanning README.md files for missing file links...")
    missing_by_readme = scan_project_readmes(ignore_patterns)
    
    if not missing_by_readme:
        print("✅ All README.md files appear to include links to their directory files!")
        return
    
    print(f"\n📋 Found {len(missing_by_readme)} README.md files with missing links:")
    
    for readme_path, missing_files in missing_by_readme.items():
        print(f"\n📁 {readme_path}")
        for file in sorted(missing_files):
            print(f"   ❌ {file}")
    
    if args.dry_run:
        print(f"\n🔍 Dry run mode - would generate TODO file at: {args.output}")
    else:
        generate_todo_file(missing_by_readme, args.output)
        print(f"\n📝 Generated TODO file: {args.output}")
        print(f"Please review and use this file to update the relevant README.md files.")


if __name__ == "__main__":
    main() 