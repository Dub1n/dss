"""convert_to_dss.py
====================
Command-line utility that converts **any existing project folder** into a
DSS-compliant repository *structure first* (deterministic) so that
`llm_tasks.py` can subsequently generate human-facing docs & diagrams.

Usage
-----
```bash
python meta/convert_to_dss.py --source ~/old_repo --dest ./dss_repo \
       [--config meta/dss_config.yml] [--force] [--normalize-names]
```

After running the converter, simply execute:
```bash
python meta/llm_tasks.py --mode all
```
to populate READMEs, INDEX.md, Canvas diagrams, etc.

Key features
~~~~~~~~~~~~
* **Deterministic** - No LLM calls; fast, cheap, re-entrant.
* **Config-driven** - Folder mapping, tagging rules, ignored patterns live
  in a YAML file so the workflow adapts without code edits.
* **Idempotent** - Will not overwrite edited files unless `--force`.
* **Manifest** - Emits `meta/manifest.json` for `llm_tasks.py` to consume.
* **Name Normalization** - Optional LLM-optimized filename transformations.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    # dotenv is optional
    pass

try:
    import yaml  # PyYAML
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Default DSS skeleton – can be overridden in YAML config
# ---------------------------------------------------------------------------
DEFAULT_SKELETON = [
    "data",
    "src",
    "docs",
    "canvas",
    "meta",
    "tests",
]

# Default classification: extension → category
DEFAULT_CLASS_MAP = {
    # code
    ".py": "src",
    ".ipynb": "src",
    ".r": "src",
    ".js": "src",
    ".ts": "src",
    ".cpp": "src",
    # markdown / docs
    ".md": "docs",
    ".rst": "docs",
    # data
    ".csv": "data",
    ".json": "data",
    ".parquet": "data",
    ".xlsx": "data",
}

# Binary patterns that we do *not* try to open / read (used as a fallback check)
BINARY_RE = re.compile(r"\.(png|jp(e?)g|gif|pdf|zip|gz|tar|tgz|exe|dll|so|dylib)$", re.I)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config(path: Path | None) -> Dict[str, any]:
    if path and path.exists():
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def ensure_skeleton(dest_root: Path, skeleton: List[str]) -> None:
    for sub in skeleton:
        (dest_root / sub).mkdir(parents=True, exist_ok=True)


def classify(file_path: Path, class_map: Dict[str, str]) -> str:
    return class_map.get(file_path.suffix.lower(), "misc")


def copy_file(src: Path, dest: Path, overwrite: bool = False) -> None:
    if dest.exists() and not overwrite:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def inject_metadata(fp: Path, category: str, tag_rules: Dict[str, str], binary_patterns: List[str]) -> None:
    """Prepend YAML front‑matter for .md, .py, .ipynb, etc.
    Respects binary patterns from config.
    """
    # Check against configured binary patterns
    rel_path_from_root = fp.relative_to(fp.parent.parent)
    for pattern in binary_patterns:
        if rel_path_from_root.match(pattern):
            # print(f"[DEBUG] Skipping binary file '{rel_path_from_root}' based on config pattern '{pattern}'") # Debugging line
            return  # skip if matches configured binary pattern

    # Existing fallback checks (extension regex and decode error)
    if BINARY_RE.search(fp.name):
        # print(f"[DEBUG] Skipping binary file '{fp.name}' based on extension regex") # Debugging line
        return  # skip binaries based on extension regex

    tag = tag_rules.get(category, category)
    front_matter = {
        "tags": [tag],
        "category": category,
        "description": f"Auto‑imported {fp.name} into DSS repo",
    }

    try:
        original = fp.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return  # binary-ish text; skip

    # Avoid double‑injection
    if original.lstrip().startswith("---"):
        return

    yaml_block = "---\n" + yaml.safe_dump(front_matter, sort_keys=False) + "---\n\n"

    if fp.suffix == ".py":
        yaml_block = f'"""\n{yaml_block}"""\n\n'

    fp.write_text(yaml_block + original, encoding="utf-8")


def create_stub_readme(folder: Path) -> None:
    rd = folder / "README.md"
    if not rd.exists():
        rd.write_text(f"# {folder.name}\n\n*This README was auto‑generated as part of the DSS conversion.*\n", encoding="utf-8")


def generate_manifest(dest_root: Path) -> Dict[str, any]:
    manifest = {}
    for path in dest_root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(dest_root).as_posix()
            manifest.setdefault(path.parent.as_posix(), []).append(rel)
    return manifest


# ---------------------------------------------------------------------------
# Filename normalization for LLM-optimized naming conventions
# ---------------------------------------------------------------------------

def transform_filename(path: Path, rules: Dict[str, any]) -> str:
    """Apply naming convention rules to a filename, following LLM-optimized naming conventions.
    
    Args:
        path: The path of the file to transform
        rules: Dictionary of naming rules from dss_config.yml
        
    Returns:
        Transformed filename following the specified conventions
    """
    if not rules:
        return path.name  # No rules, return original name
        
    # Extract file stem and extension
    stem = path.stem
    suffix = path.suffix.lower()
    
    # Check if this file should be ignored
    rel_path_str = path.as_posix()
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
    
    if transformed.lower() in generic_terms and path.parent.name in domain_prefixes:
        prefix = domain_prefixes[path.parent.name]
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

def normalize_names(files: Dict[str, Path], dest_root: Path, rules: Dict[str, any]) -> Dict[str, Path]:
    """Apply naming convention rules to all files in the destination.
    
    Args:
        files: Dictionary of original path -> destination path
        dest_root: Root of the destination directory
        rules: Naming rules from config
        
    Returns:
        Updated dictionary with normalized filenames
    """
    if not rules:
        return files  # No rules, return original mapping
    
    naming_rules = rules.get('naming_rules', {})
    if not naming_rules:
        return files  # No naming rules, return original mapping
    
    normalized_files = {}
    
    for orig_path, dest_path in files.items():
        # Get the normalized filename
        new_name = transform_filename(dest_path, naming_rules)
        
        if new_name != dest_path.name:
            # Create new destination path with normalized name
            new_dest = dest_path.parent / new_name
            print(f"Normalizing: {dest_path.name} -> {new_name}")
            
            # Rename the file if it exists
            if dest_path.exists():
                # Create parent directories if they don't exist
                new_dest.parent.mkdir(parents=True, exist_ok=True)
                
                # Ensure we don't overwrite existing files
                if new_dest.exists() and new_dest != dest_path:
                    print(f"Warning: Cannot rename {dest_path.name} to {new_name} as it already exists")
                    normalized_files[orig_path] = dest_path
                else:
                    # Rename the file
                    shutil.move(dest_path, new_dest)
                    normalized_files[orig_path] = new_dest
            else:
                # File doesn't exist yet, just update the mapping
                normalized_files[orig_path] = new_dest
        else:
            # Keep the original mapping
            normalized_files[orig_path] = dest_path
    
    return normalized_files


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def convert(source: Path, dest: Path, cfg: Dict[str, any], force: bool = False) -> None:
    skeleton = cfg.get("skeleton", DEFAULT_SKELETON)
    class_map = {**DEFAULT_CLASS_MAP, **cfg.get("class_map", {})}
    tag_rules = cfg.get("tags", {})
    ignored = set(cfg.get("ignore", []))
    binary_patterns = cfg.get("patterns", {}).get("binary", []) # Load binary patterns from config

    ensure_skeleton(dest, skeleton)

    # 1. Walk source repo ----------------------------------------------------
    # TODO: meta/TODO.md - Update to respect config 'ignore' patterns
    for src_file in source.rglob("*"):
        if src_file.is_dir():
            continue

        # Check if the file path matches any of the ignored patterns from config
        rel_src_path = src_file.relative_to(source)
        should_ignore = False
        for pattern in ignored:
            if rel_src_path.match(pattern):
                should_ignore = True
                break

        # Also keep skipping dot files/directories explicitly
        if should_ignore or any(part.startswith(".") for part in src_file.parts):
            continue

        category = classify(src_file, class_map)
        # Fallback to misc folder inside meta if unknown
        dst_folder = dest / (category if category in skeleton else "meta/misc")
        dst_path = dst_folder / src_file.name

        if category not in skeleton:
            print(f"[△] Warning: File '{rel_src_path}' classified as '{category}' (not in skeleton). Moving to '{dst_path.relative_to(dest)}'.")

        copy_file(src_file, dst_path, overwrite=force)
        inject_metadata(dst_path, category, tag_rules, binary_patterns) # Pass binary_patterns

    # 2. Create READMEs ------------------------------------------------------
    for sub in skeleton:
        create_stub_readme(dest / sub)

    # 3. Manifest ------------------------------------------------------------
    manifest = generate_manifest(dest)
    manifest_path = dest / "meta/manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[✓] Wrote manifest to {manifest_path}")

    # 4. Root README if absent ----------------------------------------------
    root_readme = dest / "README.md"
    if not root_readme.exists():
        root_readme.write_text(
            """# DSS Converted Repository\n\nThis project was converted automatically using `convert_to_dss.py`.\n\nNext step: run\n```bash\npython meta/llm_tasks.py --mode all\n```\nto generate rich documentation.\n""",
            encoding="utf-8",
        )

    print("[✓] DSS conversion complete. You can now run llm_tasks.py.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Convert an existing repo into DSS structure")
    parser.add_argument("--source", type=Path, required=True, help="Path to the original repository/folder")
    parser.add_argument("--dest", type=Path, required=True, help="Destination path for the DSS repo")
    parser.add_argument("--config", type=Path, default=None, help="Optional YAML config file overriding defaults")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in dest")
    parser.add_argument("--normalize-names", action="store_true", help="Apply LLM-optimized naming conventions")

    args = parser.parse_args(argv)

    if not args.source.exists():
        sys.exit("Source folder does not exist")

    if args.dest.exists() and any(args.dest.iterdir()) and not args.force:
        sys.exit("Destination is not empty – use --force to overwrite")

    cfg = load_config(args.config)

    # Add handling for normalize-names flag
    if args.normalize_names:
        print("Applying LLM-optimized naming conventions...")
        # Create a mapping of files first, then normalize the names
        file_mapping = {}
        # Code to populate file_mapping with source -> destination paths
        
        # Apply name normalization
        file_mapping = normalize_names(file_mapping, args.dest, cfg)
        
        # Use the updated mapping for the conversion process
    
    convert(args.source, args.dest, cfg, force=args.force)


if __name__ == "__main__":
    main()
