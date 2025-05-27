"""---
tags: [code, automation, documentation]
provides: [dss_overview_sync]
requires: [meta/DSS_GUIDE.md]
---

sync_dss_mdc.py

Watches the DSS overview source file (docs/DSS_OVERVIEW.md) and only updates
.cursor/rules/dss-overview.mdc when the generated content differs.
"""

from pathlib import Path
import re
import hashlib
import time

# --- Config ---
SOURCE_FILE = Path("meta/DSS_GUIDE.md")
DEST_FILE = Path(".cursor/rules/dss-overview.mdc")
CHECK_INTERVAL = 2  # seconds

# --- Extraction helpers ---
def extract_section_content(text, header_to_match, next_header_to_match=None):
    """Extracts content between header_to_match and next_header_to_match or end of text."""
    pattern = rf"(?<=\n{re.escape(header_to_match)}\n)(.*?)(?=(\n{re.escape(next_header_to_match)})|\Z)"
    if next_header_to_match is None:
         pattern = rf"(?<=\n{re.escape(header_to_match)}\n)(.*)"

    match = re.search(pattern, "\n" + text + "\n", flags=re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        return ""

def generate_output(text):
    out = []
    out.append("## DSS Summary for LLM Context (Cursor Prompt Injection)\n")
    out.append("<!-- This file is injected into every prompt by Cursor. It provides LLMs with a compressed understanding of DSS and how to behave inside its structure. -->\n")

    # Extract initial content before the first ### header (Purpose)
    match_intro = re.search(r'(.*?)(^### Purpose)', text, flags=re.DOTALL | re.MULTILINE)
    if match_intro:
        intro_content = match_intro.group(1).strip()
        # Filter out frontmatter and just keep the main title and principles section
        intro_lines = intro_content.splitlines()
        filtered_intro = []
        for line in intro_lines:
            if line.strip() and not line.strip().startswith('---'): # Exclude empty lines and separators
                 filtered_intro.append(line)
        if filtered_intro:
            out.extend(filtered_intro)
            out.append("\n---\n")

    # Define sections to extract and their desired output headers in order
    sections_config = [
        {"match": "### Purpose", "output": "### 🧭 Purpose\n"},
        {"match": "### 📁 Project Structure", "output": "### 📁 Folder Structure\n"},
        {"match": "### 🔄 Key Workflows", "output": "### 🪚 Primary LLM Workflows\n"},
        {"match": "### 🧠 Behavioral Conventions", "output": "### 🤖 LLM Behavior Guidelines\n"},
    ]

    # Extract and add sections based on the defined order
    for i, section in enumerate(sections_config):
        header_to_match = section["match"]
        output_header = section["output"]
        next_header_to_match = sections_config[i+1]["match"] if i + 1 < len(sections_config) else None

        content = extract_section_content(text, header_to_match, next_header_to_match)
        if content:
            out.append(output_header)
            out.append(content)
            out.append("\n---\n")

    out.append("> DSS is a structured system for building structured systems. Your job is to assist its evolution by making intelligent, metadata-aware, structure-preserving suggestions that integrate cleanly with its design.\n")
    out.append("\n<!-- End of LLM-facing rules -->\n")
    return "\n".join(out)

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# --- Watch loop ---
def sync_once():
    print(f"Attempting to sync {str(SOURCE_FILE)} to {str(DEST_FILE)}...")
    try:
        text = SOURCE_FILE.read_text(encoding="utf-8")
        generated = generate_output(text)
        current_hash = hash_text(generated)

        old_content = DEST_FILE.read_text(encoding="utf-8") if DEST_FILE.exists() else ""
        old_hash = hash_text(old_content)

        if current_hash != old_hash:
            DEST_FILE.parent.mkdir(parents=True, exist_ok=True)
            DEST_FILE.write_text(generated, encoding="utf-8")
            print(f"✔ Successfully updated {str(DEST_FILE)} from {str(SOURCE_FILE)}")
        else:
            print(f"File {str(DEST_FILE)} is already in sync with {str(SOURCE_FILE)}. No update needed.")

    except FileNotFoundError:
        print(f"❌ Error: Source file not found at {str(SOURCE_FILE)}")
    except Exception as e:
        print(f"❌ An error occurred during sync: {e}")

if __name__ == "__main__":
    sync_once()

# Referenced By
# - docs/automated_formatting - Listed in automation documentation table
# - meta/guidelines/backlink_conventions.md - Used as an example for backlink implementation
