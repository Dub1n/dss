#!/usr/bin/env python
"""
auto_rename.py
=============

A script to watch for new files in the repository and automatically rename them
according to LLM-optimized naming conventions.

Usage:
    python meta/scripts/auto_rename.py [--watch]

Options:
    --watch  Run in watch mode to monitor for new files (requires watchdog package)
"""

import os
import re
import yaml
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional

def load_config() -> Dict:
    """Load naming rules from dss_config.yml"""
    config_path = Path(__file__).parent.parent / "dss_config.yml"
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}")
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config.get('naming_rules', {})

def transform_filename(path: Path, rules: Dict) -> str:
    """Transform a filename according to naming conventions"""
    if not rules:
        return path.name
    
    # Extract file stem and extension
    stem = path.stem
    suffix = path.suffix.lower() if path.suffix else ""
    
    # Check if this file should be ignored
    rel_path_str = path.relative_to(Path.cwd()).as_posix()
    ignore_patterns = rules.get('ignore_patterns', [])
    for pattern in ignore_patterns:
        if Path(rel_path_str).match(pattern):
            return path.name  # Skip transformation for ignored patterns
    
    # Check for specific overrides
    overrides = rules.get('overrides', {})
    if rel_path_str in overrides:
        return overrides[rel_path_str]
    
    # Get transformation style based on file extension
    transformations = rules.get('transformations', {})
    transform_style = transformations.get(suffix, "keep")
    
    # If no transformation rule, keep original
    if transform_style == "keep":
        return path.name
    
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
    
    return transformed + suffix

def rename_file(path: Path, rules: Dict) -> Optional[Path]:
    """Rename a file according to naming conventions if needed"""
    new_name = transform_filename(path, rules)
    
    if new_name != path.name:
        new_path = path.parent / new_name
        
        # Ensure we don't overwrite existing files
        if new_path.exists() and new_path != path:
            print(f"Warning: Cannot rename {path.name} to {new_name} as it already exists")
            return None
        
        try:
            path.rename(new_path)
            print(f"Renamed: {path.relative_to(Path.cwd())} -> {new_path.relative_to(Path.cwd())}")
            return new_path
        except Exception as e:
            print(f"Error renaming {path}: {e}")
            return None
    
    return None

def scan_repository(rules: Dict) -> List[Path]:
    """Scan the repository for files that need to be renamed"""
    renamed_files = []
    
    # Directories to scan
    directories = [
        Path.cwd() / "src",
        Path.cwd() / "meta/scripts",
        Path.cwd() / "docs",
        Path.cwd() / "tests"
    ]
    
    for directory in directories:
        if directory.exists():
            print(f"Scanning {directory.relative_to(Path.cwd())}...")
            
            for item in directory.rglob('*'):
                if item.is_file():
                    new_path = rename_file(item, rules)
                    if new_path:
                        renamed_files.append(new_path)
    
    return renamed_files

def watch_repository(rules: Dict):
    """Watch repository for new files and rename them according to conventions"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Error: watchdog package is required for watch mode.")
        print("Install it with: pip install watchdog")
        return
    
    class FileHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                path = Path(event.src_path)
                print(f"New file detected: {path}")
                rename_file(path, rules)
    
    # Set up observer
    event_handler = FileHandler()
    observer = Observer()
    
    # Directories to watch
    directories = [
        Path.cwd() / "src",
        Path.cwd() / "meta/scripts",
        Path.cwd() / "docs",
        Path.cwd() / "tests"
    ]
    
    for directory in directories:
        if directory.exists():
            observer.schedule(event_handler, str(directory), recursive=True)
            print(f"Watching {directory.relative_to(Path.cwd())}...")
    
    observer.start()
    
    try:
        print("Watching for new files (Ctrl+C to exit)...")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Apply LLM-optimized naming conventions to files")
    parser.add_argument("--watch", action="store_true", help="Watch for new files")
    args = parser.parse_args()
    
    # Load naming rules
    rules = load_config()
    if not rules:
        print("Error: No naming rules found in configuration")
        return
    
    print(f"Loaded naming rules: {bool(rules)}")
    
    if args.watch:
        watch_repository(rules)
    else:
        # Scan once
        renamed_files = scan_repository(rules)
        print(f"\nSummary: {len(renamed_files)} files renamed")

if __name__ == "__main__":
    main() 