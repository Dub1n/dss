"""convert_to_dss.py
====================
Command-line utility that converts **any existing project folder** into a
DSS-compliant repository *structure first* (deterministic) so that
`llm_tasks.py` can subsequently generate human-facing docs & diagrams.

Usage
-----
```bash
python meta/convert_to_dss.py --source ~/old_repo --dest ./dss_repo \
       [--config meta/dss_config.yml] [--force]
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
from pathlib import Path, dotenv
dotenv.load_dotenv(Path(__file__).parent.parent / ".env")

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

# Binary patterns that we do *not* try to open / read
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


def inject_metadata(fp: Path, category: str, tag_rules: Dict[str, str]) -> None:
    """Prepend YAML front‑matter for .md, .py, .ipynb, etc."""
    if BINARY_RE.search(fp.name):
        return  # skip binaries

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
# Main logic
# ---------------------------------------------------------------------------

def convert(source: Path, dest: Path, cfg: Dict[str, any], force: bool = False) -> None:
    skeleton = cfg.get("skeleton", DEFAULT_SKELETON)
    class_map = {**DEFAULT_CLASS_MAP, **cfg.get("class_map", {})}
    tag_rules = cfg.get("tags", {})
    ignored = set(cfg.get("ignore", []))

    ensure_skeleton(dest, skeleton)

    # 1. Walk source repo ----------------------------------------------------
    for src_file in source.rglob("*"):
        if src_file.is_dir():
            continue
        if src_file.name in ignored or any(part.startswith(".") for part in src_file.parts):
            continue  # skip dot files & ignored patterns

        category = classify(src_file, class_map)
        # Fallback to misc folder inside meta if unknown
        dst_folder = dest / (category if category in skeleton else "meta/misc")
        dst_path = dst_folder / src_file.name

        copy_file(src_file, dst_path, overwrite=force)
        inject_metadata(dst_path, category, tag_rules)

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

    args = parser.parse_args(argv)

    if not args.source.exists():
        sys.exit("Source folder does not exist")

    if args.dest.exists() and any(args.dest.iterdir()) and not args.force:
        sys.exit("Destination is not empty – use --force to overwrite")

    cfg = load_config(args.config)

    convert(args.source, args.dest, cfg, force=args.force)


if __name__ == "__main__":
    main()
