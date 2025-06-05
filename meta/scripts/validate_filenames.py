#!/usr/bin/env python
"""
⚠️  WARNING: This script is in need of significant rework and is kept for reference only.
    It was written for an earlier version of DSS and does not match the current repo structure.
    DO NOT USE in production - significant updates required before it can be functional.
    
    For current DSS functionality, see the main documentation and newer scripts.
"""

"""---
tags: [script, automation, naming_conventions, validation]
provides: [filename_validation]
requires: [meta/dss_config.yml]
---"""

import os
import sys
import yaml
import re
import subprocess

def get_repo_root():
    """Get the root directory of the git repository."""
    return subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'], 
        universal_newlines=True
    ).strip()

def load_config():
    """Load the DSS configuration file."""
    repo_root = get_repo_root()
    config_path = os.path.join(repo_root, 'meta', 'dss_config.yml')
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_staged_files():
    """Get list of files staged for commit."""
    output = subprocess.check_output(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
        universal_newlines=True
    )
    return [f for f in output.splitlines() if os.path.exists(f)]

def validate_filename(filename, config):
    """Validate a filename against naming conventions."""
    # Skip files in ignore list
    for ignore_pattern in config.get('ignore', []):
        if fnmatch_pattern(ignore_pattern, filename):
            return True
    
    # Skip common directories that shouldn't be checked
    skip_paths = [
        'node_modules/',
        '.venv/',
        '__pycache__/',
        '.git/',
        'docs/🔒archive/',
        '.cursor/rules/'  # Special naming for cursor rules
    ]
    
    for skip_path in skip_paths:
        if filename.startswith(skip_path):
            return True
    
    # Skip files that are allowed to have special naming
    allowed_special_names = [
        'README.md',
        'INDEX.md',
        'package.json',
        'package-lock.json',
        '.gitignore',
        '.cursorignore',
        'LICENSE',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        'DSS_GUIDE.md',
        'TODO.md',
        'readme_frontmatter.md',
        'folder_README_template.md'
    ]
    
    basename = os.path.basename(filename)
    if basename in allowed_special_names:
        return True
    
    # Skip files in binary category
    for binary_pattern in config.get('patterns', {}).get('binary', []):
        # Convert glob pattern to simple regex
        pattern = binary_pattern.replace('**/', '').replace('*', '.*')
        if re.search(pattern, filename):
            return True
    
    # Get the basename without extension
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    
    # Basic validation - snake_case check
    if not re.match(r'^[a-z0-9_]+$', name):
        return False
    
    # Check for camelCase or PascalCase
    if any(c.isupper() for c in name):
        return False
    
    # Check for consecutive underscores
    if '__' in name:
        return False
    
    return True

def fnmatch_pattern(pattern, string):
    """Simple glob pattern matching."""
    # Convert glob pattern to regex
    regex = pattern.replace('.', r'\.').replace('*', '.*').replace('?', '.')
    return re.search(f"^{regex}$", string) is not None

def main():
    config = load_config()
    staged_files = get_staged_files()
    
    invalid_files = []
    for filename in staged_files:
        if not validate_filename(filename, config):
            invalid_files.append(filename)
    
    if invalid_files:
        print("The following files don't follow naming conventions:")
        for f in invalid_files:
            print(f"- {f}")
        print("\nPlease rename these files to follow snake_case conventions.")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main() 