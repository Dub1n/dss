"""---
tags: [code, utility, markdown_cleanup]
provides: [simple_markdown_cleanup]
requires: []
---

Simple Markdown cleanup utility.

Removes NUL / control characters and applies two specific newline-pattern
normalisations requested by the user:
    a) "\n\n \n \n"  → "\n\n"
    b) "\n\n"        → " "

Usage:
    python simple_cleanup.py <input_file.md> <output_file.md>
If <output_file.md> is a directory, an output filename will be generated.
"""
import os
import re
import sys
from pathlib import Path


def simple_cleanup(input_path: str, output_path: str) -> None:
    """Apply the minimal cleanup specified by the user."""
    with open(input_path, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    # 1. Remove NULs (and any other non-printable chars below 32 except \n, \t)
    content = "".join(ch for ch in content if ch in ("\n", "\t") or ord(ch) >= 32)

    # --- Preserve real blank-line section breaks ---------------------------------
    # Temporarily tag the pattern we want to keep: "\n\n  \n  \n" (rule a).
    SENTINEL = "<<KEEP_BLANK>>"
    content = re.sub(r"\n\n[ \t]*\n[ \t]*\n", f"\n{SENTINEL}\n", content)

    # Collapse any remaining double-newlines inside paragraphs to single spaces (rule b).
    content = content.replace("\n\n", " ")

    # Restore the preserved blank lines back to "\n\n".
    content = content.replace(SENTINEL, "\n")

    # ------------------------------------------------------------------
    # Additional clean-ups requested by the user
    # ------------------------------------------------------------------

    # 1. Contextual replacements for the "" (U+FFFD) replacement character
    #    a) " 2023" → "© 2023" (common copyright)
    content = re.sub(r"\uFFFD\s*(20\d{2})", r"© \1", content)

    #    b) inside words -> assume apostrophe (can't → can't)
    content = re.sub(r"(?<=\w)\uFFFD(?=\w)", "'", content)

    #    d) If two replacement chars appear on the same line (with any non-newline
    #       chars in between), treat them as a quoting pair: wrap the interior
    #       text with straight double quotes.
    content = re.sub(r"\uFFFD([^\n]*?)\uFFFD", r'"\1"', content)

    #    c) at line start acting as bullet -> convert to '- '
    content = re.sub(r"(?m)^(\s*)\uFFFD\s+", r"\1- ", content)

    #    e) Unmatched closing quote: pattern "\" ..."  or "' ..." within one line.
    #       Replace the trailing replacement char with the corresponding quote mark.
    content = re.sub(r'("[^"\n]*?)\uFFFD', r'\1"', content)
    content = re.sub(r"('[^'\n]*?)\uFFFD", r"\1'", content)

    # 2. Convert any bullet lines starting with '?' into '- '
    content = re.sub(r"(?m)^(\s*)\?(?=\s)", r"\1-", content)

    # 3. Remove page numbers / numerals lines (digits or roman numerals only)
    content = re.sub(r"(?m)^\s*(?:\d+|[ivxlcdmIVXLCDM]+)\s*$\n?", "", content)

    # 4. Remove specific footer lines containing AAMI copyright strings
    content = re.sub(r"(?m)^.*Association for the Advancement of Medical Instrumentation.*\n?", "", content)

    # 5. Join wrapped bullet text:
    #    • First line: bullet (-/*) and some text
    #    • Next line: at least two leading spaces (indented) continuing the text
    bullet_wrap_pattern = re.compile(r"(?m)^(\s*[-*]\s[^\n]+)\n[ \t]{2,}([^\n]+)")
    while True:
        new_content = bullet_wrap_pattern.sub(r"\1 \2", content)
        if new_content == content:
            break
        content = new_content

    # 6. Remove blank lines that contain only whitespace.
    content = re.sub(r"(?m)^\s*$\n", "\n", content)
    # After that, collapse any occurrence of two consecutive blank lines where the
    # second still has stray spaces (edge-case) → single true blank line.
    content = content.replace("\n \n", "\n\n")

    # Write result
    out_path = Path(output_path)
    if out_path.is_dir():
        out_path = out_path / (Path(input_path).stem + "_simple.md")

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"✅ Cleaned file saved to '{out_path}'")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python simple_cleanup.py <input_file.md> <output_file.md|output_dir>")
        sys.exit(1)

    simple_cleanup(sys.argv[1], sys.argv[2]) 