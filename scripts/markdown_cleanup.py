#!/usr/bin/env python3
import re
import sys
import os

# New helper to fix split letters within words

def _merge_letters_within_words(text):
    """
    Detect sequences like 'w o r d' or 'T I R' produced by some PDF →
    Markdown conversions where individual letters are separated by
    single spaces. The function removes those internal spaces while
    preserving normal word boundaries.
    """
    # Accept sequences of **two or more** spaced letters (e.g., "T I R", "w o r d").
    # Using {2,} allows 3-letter acronyms while still preventing accidental merges of
    # short patterns like "e g" which are unlikely to appear in technical prose.
    pattern = re.compile(r'((?:[A-Za-z]\s){2,}[A-Za-z])(?=\s|$)')
    return pattern.sub(lambda m: m.group(0).replace(' ', ''), text)

def fix_markdown_formatting(input_path, output_path):
    """
    Reads a Markdown file with formatting issues (likely from a PDF
    conversion) and writes a corrected, cleaned-up version.

    The script performs several cleaning steps:
    1.  Removes form feed characters and known repetitive footers.
    2.  Normalizes common "smart" punctuation (e.g., fancy quotes, en/em-dashes)
        and other frequently seen Unicode glyphs into plain ASCII so we don't
        lose meaning.
    3.  Corrects strange character spacing (e.g., "w o r d" -> "word") while
        preserving spaces between actual words.
    4.  Fixes paragraph structure by removing unnecessary line breaks and
        normalizing paragraph spacing.
    """
    print(f"Processing '{os.path.basename(input_path)}'...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # --- Step 1: Preliminary Cleaning ---
    # Remove form feed characters (often used for page breaks in plain text)
    content = content.replace('\f', '')

    # Remove embedded NULs and other non-printable control characters that
    # sometimes sneak in during faulty PDF→text conversions. These tend to
    # manifest as NUL-padded ASCII that later renders as CJK when opened with
    # the wrong encoding.
    content = ''.join(ch for ch in content if ch == '\n' or ch == '\t' or 32 <= ord(ch))

    # Filter out known, repetitive lines like copyright footers or page numbers.
    # This part might need adjustment for different documents.
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # A more robust filter for the AAMI copyright line and similar patterns
        line_no_spaces = line.replace(' ', '')
        if '©2023AssociationfortheAdvancementofMedicalInstrumentation' in line_no_spaces:
            continue
        if 'AAMITIR45:2023' in line_no_spaces and len(line_no_spaces) < 30:
             continue
        # Filter for lines that are just page numbers (e.g., 'v i', '9 3')
        if re.match(r'^[ivx\d\s]+$', line.strip()) and len(line.strip().replace(' ', '')) < 4:
            continue
        cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)

    # Replace common typographic Unicode characters with ASCII equivalents ―
    # this keeps the meaning while avoiding a full Unicode dependency.
    unicode_replacements = {
        "\u2018": "'",  # left single quote
        "\u2019": "'",  # right single quote
        "\u201C": '"',  # left double quote
        "\u201D": '"',  # right double quote
        "\u2013": '-',   # en dash
        "\u2014": '-',   # em dash
        "\u2026": '...', # ellipsis
        "\u2022": '-',   # bullet •
        "\u00A0": ' ',   # non-breaking space
    }
    for bad, good in unicode_replacements.items():
        content = content.replace(bad, good)

    # Finally, strip any remaining non-ASCII bytes while keeping newlines/tabs intact.
    content = ''.join(ch if (ch in ('\n', '\t') or 32 <= ord(ch) < 128) else '' for ch in content)
    content = content.replace('some_marker', '')


    # --- Step 2: Fix Character and Word Spacing ---
    # 1. Collapse sequences of multiple spaces/tabs down to a single space.
    content = re.sub(r'[ \t]{2,}', ' ', content)
    
    # 2. Merge letters that were incorrectly split by single spaces
    #    (e.g., "w o r d" -> "word").
    content = _merge_letters_within_words(content)

    # Convert stray '?' characters used as bullet placeholders to real markdown bullets.
    # If a line (possibly indented) begins with a single '?' followed by space or end-of-line → replace with '-'.
    content = re.sub(r'^(\s*)\?(?=\s)', r'\1- ', content, flags=re.MULTILINE)

    # Ensure there's a blank line before any list item ("- " or "* ") so the bullet
    # list remains visually separated after paragraph recombination.
    content = re.sub(r'([^\n])\n(\s*[-*]\s)', r'\1\n\n\2', content)

    # Heuristic: promote single newlines to paragraph breaks *only* when the preceding
    # character clearly ends a sentence (., ! or ?)
    # AND the following line contains at least one lowercase letter. This prevents
    # unwanted breaks before fully-capitalised lines like "RELEASE LAYER".
    content = re.sub(r'([.!?])\n((?=[^\n]*[a-z])[A-Z][^\n]{0,100})', r'\1\n\n\2', content)

    # --- Step 3: Fix Paragraphs and Newlines ---
    # Paragraph boundary = 2 or more consecutive blank lines.
    paragraphs = re.split(r'(?:\n\s*){2,}', content)

    corrected_paragraphs = []
    for para in paragraphs:
        # Join all remaining single/double newlines inside paragraph into spaces
        corrected_para = re.sub(r'\n+', ' ', para).strip()
        if not corrected_para:
            continue

        if corrected_paragraphs:
            prev = corrected_paragraphs[-1]
            ends_with_abbrev = re.search(r'(?:[A-Z]\.){1,3}$', prev) is not None
            prev_ends_sentence = prev[-1] in '.!?:'
            is_allcaps_heading = prev.isupper() and len(prev.split()) <= 8
            is_numbered_heading = bool(re.match(r'^\d+(?:\.\d+)*\s+.+', prev))

            # Merge when the previous chunk doesn't appear to terminate a sentence,
            # **and** it isn't an ALL-CAPS heading. This scoops up orphaned lines like
            # “(e.g., …)” or continuation fragments while preserving genuine headings.
            if ((not prev_ends_sentence and not is_allcaps_heading and not is_numbered_heading) or ends_with_abbrev):
                corrected_paragraphs[-1] = prev + ' ' + corrected_para
                continue

        corrected_paragraphs.append(corrected_para)

    # --- Step 4: Reassemble the Document ---
    # Join the corrected paragraphs with double newlines for standard Markdown.
    final_text = '\n\n'.join(corrected_paragraphs)

    # --- Step 5: Write to Output File ---
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        print(f"Formatting complete. Corrected file saved to '{os.path.basename(output_path)}'")
    except IOError:
        print(f"Error: Could not write to output file at {output_path}")

# --- Main execution block ---
# This allows the script to be run from the command line.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python format_script.py <input_file.md> <output_file.md|output_directory>")
        print("Example (file): python format_script.py 'AAMI TIR45-2023.md' 'AAMI_TIR45_corrected.md'")
        print("Example (directory): python format_script.py 'AAMI TIR45-2023.md' '/path/to/output_dir/'")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # If the provided output path is a directory, generate an output filename
    # using the input file's stem with a '_corrected.md' suffix.
    if os.path.isdir(output_file_path):
        input_stem = os.path.splitext(os.path.basename(input_file_path))[0]
        output_file_path = os.path.join(output_file_path, f"{input_stem}_corrected.md")
    
    fix_markdown_formatting(input_file_path, output_file_path)
