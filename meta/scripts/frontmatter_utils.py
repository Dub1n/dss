#!/usr/bin/env python
"""---
tags: [utility, frontmatter, validation, automation]
provides: [frontmatter_validation, frontmatter_correction]
requires: [yaml, pathlib, typing]
---
Frontmatter Validation and Auto-correction Utilities

This module provides functions for validating and auto-correcting YAML frontmatter
in Markdown and Python files according to DSS standards.
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any, Union

# Regular expressions for identifying frontmatter blocks
MD_FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PY_FRONTMATTER_PATTERN = re.compile(r'"""---\s*\n(.*?)\n---\s*"""', re.DOTALL)

# Configuration
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "dss_config.yml"

def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load DSS configuration from the specified path or use the default location.
    
    Args:
        config_path: Path to the configuration file, or None to use default
        
    Returns:
        Dictionary containing DSS configuration
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH
        
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def extract_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extract frontmatter from a file based on its extension.
    
    Args:
        file_path: Path to the file to extract frontmatter from
        
    Returns:
        Dictionary containing the parsed frontmatter, or None if no frontmatter was found
    """
    content = file_path.read_text(encoding="utf-8")
    
    # Select pattern based on file extension
    if file_path.suffix.lower() == ".md":
        match = MD_FRONTMATTER_PATTERN.match(content)
    elif file_path.suffix.lower() == ".py":
        match = PY_FRONTMATTER_PATTERN.search(content)
    else:
        # For now, we only support .md and .py files
        return None
        
    if not match:
        return None
        
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        # Return an empty dict for malformed YAML
        return {}

def validate_frontmatter(
    frontmatter: Dict[str, Any], 
    config: Dict[str, Any]
) -> List[str]:
    """
    Validate frontmatter against DSS rules from config.
    
    Args:
        frontmatter: Dictionary containing parsed frontmatter
        config: Dictionary containing DSS configuration
        
    Returns:
        List of validation errors, empty if valid
    """
    errors = []
    
    # Check for required fields based on defaults in config
    if "defaults" in config:
        for field in config["defaults"]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")
    
    # Check for valid tags format
    if "tags" in frontmatter:
        if not isinstance(frontmatter["tags"], list):
            errors.append("Tags must be a list")
        else:
            for tag in frontmatter["tags"]:
                if not isinstance(tag, str):
                    errors.append(f"Tag must be a string: {tag}")
    
    # Check for valid provides/requires format
    for field in ["provides", "requires"]:
        if field in frontmatter:
            if not isinstance(frontmatter[field], list):
                errors.append(f"{field} must be a list")
            else:
                for item in frontmatter[field]:
                    if not isinstance(item, str):
                        errors.append(f"Item in {field} must be a string: {item}")
    
    return errors

def auto_correct_frontmatter(
    frontmatter: Dict[str, Any], 
    config: Dict[str, Any]
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Auto-correct common frontmatter issues.
    
    Args:
        frontmatter: Dictionary containing parsed frontmatter
        config: Dictionary containing DSS configuration
        
    Returns:
        Tuple of (corrected frontmatter, list of corrections made)
    """
    corrections = []
    corrected = frontmatter.copy()
    
    # Add missing required fields
    if "defaults" in config:
        for field, default_value in config["defaults"].items():
            if field not in corrected:
                corrected[field] = default_value
                corrections.append(f"Added missing field: {field}")
    
    # Correct tags format
    if "tags" in corrected:
        if not isinstance(corrected["tags"], list):
            # Convert scalar or dict to list
            if isinstance(corrected["tags"], str):
                corrected["tags"] = [corrected["tags"]]
                corrections.append("Converted tags from string to list")
            else:
                corrected["tags"] = ["draft"]
                corrections.append("Replaced invalid tags with ['draft']")
    
    # Correct provides/requires format
    for field in ["provides", "requires"]:
        if field in corrected:
            if not isinstance(corrected[field], list):
                # Convert scalar to list
                if isinstance(corrected[field], str):
                    corrected[field] = [corrected[field]]
                    corrections.append(f"Converted {field} from string to list")
                else:
                    corrected[field] = []
                    corrections.append(f"Replaced invalid {field} with empty list")
    
    return corrected, corrections

def process_file(
    file_path: Path, 
    config: Dict[str, Any], 
    dry_run: bool = False,
    auto_correct: bool = False
) -> Tuple[bool, List[str]]:
    """
    Process a file for frontmatter validation and optional auto-correction.
    
    Args:
        file_path: Path to the file to process
        config: Dictionary containing DSS configuration
        dry_run: If True, only validate but don't modify files
        auto_correct: If True, attempt to auto-correct issues
        
    Returns:
        Tuple of (success, list of messages)
    """
    messages = []
    
    # Check if this is a supported file type
    if file_path.suffix.lower() not in [".md", ".py"]:
        messages.append(f"Skipping unsupported file type: {file_path}")
        return False, messages
    
    # Check if file should be excluded based on patterns
    if "ignore" in config:
        for pattern in config["ignore"]:
            if file_path.match(pattern):
                messages.append(f"Skipping ignored file: {file_path}")
                return False, messages
    
    # Extract frontmatter
    frontmatter = extract_frontmatter(file_path)
    
    if frontmatter is None:
        messages.append(f"No frontmatter found in: {file_path}")
        
        # Add frontmatter if auto-correction is enabled
        if auto_correct and not dry_run:
            file_type = "markdown" if file_path.suffix.lower() == ".md" else "python"
            default_frontmatter = config.get("defaults", {})
            
            try:
                # Create content with new frontmatter
                content = file_path.read_text(encoding="utf-8")
                
                if file_type == "markdown":
                    yaml_str = yaml.dump(default_frontmatter, default_flow_style=False)
                    new_content = f"---\n{yaml_str}---\n\n{content}"
                else:  # python
                    yaml_str = yaml.dump(default_frontmatter, default_flow_style=False)
                    new_content = f'"""---\n{yaml_str}---"""\n\n{content}'
                
                if not dry_run:
                    file_path.write_text(new_content, encoding="utf-8")
                    messages.append(f"Added default frontmatter to: {file_path}")
                    return True, messages
            except Exception as e:
                messages.append(f"Error adding frontmatter to {file_path}: {str(e)}")
                return False, messages
        
        return False, messages
    
    # Empty dictionary means YAML parsing failed
    if frontmatter == {}:
        messages.append(f"Malformed YAML in frontmatter: {file_path}")
        return False, messages
    
    # Validate frontmatter
    errors = validate_frontmatter(frontmatter, config)
    
    if errors:
        messages.extend([f"Validation error: {error}" for error in errors])
        
        # Auto-correct if enabled
        if auto_correct:
            corrected_frontmatter, corrections = auto_correct_frontmatter(frontmatter, config)
            
            if corrections:
                messages.extend([f"Auto-correction: {correction}" for correction in corrections])
                
                if not dry_run:
                    try:
                        # Update file with corrected frontmatter
                        content = file_path.read_text(encoding="utf-8")
                        
                        if file_path.suffix.lower() == ".md":
                            match = MD_FRONTMATTER_PATTERN.match(content)
                            if match:
                                # Replace the frontmatter section
                                yaml_str = yaml.dump(corrected_frontmatter, default_flow_style=False)
                                new_frontmatter = f"---\n{yaml_str}---\n"
                                new_content = new_frontmatter + content[match.end():]
                                file_path.write_text(new_content, encoding="utf-8")
                                messages.append(f"Updated frontmatter in: {file_path}")
                        else:  # python
                            match = PY_FRONTMATTER_PATTERN.search(content)
                            if match:
                                # Replace the frontmatter section
                                yaml_str = yaml.dump(corrected_frontmatter, default_flow_style=False)
                                new_frontmatter = f'"""---\n{yaml_str}---"""'
                                new_content = content[:match.start()] + new_frontmatter + content[match.end():]
                                file_path.write_text(new_content, encoding="utf-8")
                                messages.append(f"Updated frontmatter in: {file_path}")
                    except Exception as e:
                        messages.append(f"Error updating frontmatter in {file_path}: {str(e)}")
                        return False, messages
        
        return False, messages
    
    messages.append(f"Frontmatter validation passed: {file_path}")
    return True, messages

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Validate and auto-correct YAML frontmatter in DSS files"
    )
    parser.add_argument(
        "paths", nargs="+", help="Files or directories to process"
    )
    parser.add_argument(
        "--config", "-c", type=Path, help="Path to DSS config file"
    )
    parser.add_argument(
        "--auto-correct", "-a", action="store_true", 
        help="Automatically correct issues"
    )
    parser.add_argument(
        "--dry-run", "-d", action="store_true",
        help="Only validate, don't modify files"
    )
    parser.add_argument(
        "--recursive", "-r", action="store_true",
        help="Process directories recursively"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed validation messages"
    )
    
    args = parser.parse_args()
    
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        return 1
    
    # Process paths
    all_files = []
    for path in args.paths:
        path_obj = Path(path)
        if path_obj.is_file():
            all_files.append(path_obj)
        elif path_obj.is_dir():
            if args.recursive:
                # Get all .md and .py files recursively
                all_files.extend(path_obj.glob("**/*.md"))
                all_files.extend(path_obj.glob("**/*.py"))
            else:
                # Get only top-level .md and .py files
                all_files.extend(path_obj.glob("*.md"))
                all_files.extend(path_obj.glob("*.py"))
    
    # Track overall results
    success_count = 0
    error_count = 0
    
    # Process each file
    for file_path in all_files:
        success, messages = process_file(
            file_path, config, args.dry_run, args.auto_correct
        )
        
        if success:
            success_count += 1
            if args.verbose:
                print(f"✅ {file_path}")
                for msg in messages:
                    print(f"  - {msg}")
        else:
            error_count += 1
            print(f"❌ {file_path}")
            for msg in messages:
                print(f"  - {msg}")
    
    # Print summary
    print(f"\nProcessed {len(all_files)} files:")
    print(f"  - {success_count} passed validation")
    print(f"  - {error_count} had validation errors")
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main()) 