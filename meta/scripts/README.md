---
module: "scripts"
status: active
tags: [meta, script, Documentation, Markdown, Tables]
provides: [Script_Documentation, Table_Formatter_Documentation]
requires: [meta/scripts/format_markdown_tables.py, meta/scripts/format_markdown_tables_enhanced.py]
---

# Scripts for DSS Maintenance

This directory contains utility scripts for maintaining and working with DSS repositories.

## Files

| File                               | Purpose                                                  |
|------------------------------------|----------------------------------------------------------|
| format_markdown_tables.py          | Basic markdown table formatter                           |
|------------------------------------|----------------------------------------------------------|
| format_markdown_tables_enhanced.py | Enhanced markdown table formatter with advanced features |
|------------------------------------|----------------------------------------------------------|
| generate_docs.py                   | Documentation generator (TBD)                            |
|------------------------------------|----------------------------------------------------------|
| update_links.py                    | Link updater for file renames (TBD)                      |

# Markdown Table Formatters

## Basic Formatter

The basic formatter provides simple markdown table formatting with consistent column widths and content wrapping.

```bash
python meta/scripts/format_markdown_tables.py path/to/file.md
```

Options:

* `--padding N` - Number of spaces on each side of cell content (default: 1)
* `--max-width N` - Maximum width for the entire table (default: 140)

## Enhanced Formatter

The enhanced formatter extends the basic formatter with additional features for more professional-looking tables.

```bash
python meta/scripts/format_markdown_tables_enhanced.py path/to/file.md
```

Options:

* `--padding N` - Number of spaces on each side of cell content (default: 1)
* `--max-width N` - Maximum width for the entire table (default: 120)
* `--row-separators` - Add separator lines between rows (default: enabled)
* `--no-row-separators` - Do not add separator lines between rows
* `--smart-separators` - Only add separators for rows with wrapped content (default: enabled)
* `--no-smart-separators` - Add separators for all rows (when row separators are enabled)
* `--end-row` - Add a final separator at the bottom of the table (default: disabled)
* `--uniform-height` - Make all cells in a row (or table) the same height (default: enabled)
* `--vertical-align [top|middle|bottom]` - Vertical alignment for cell content (default: middle)

### Settings File

The enhanced formatter can load settings from a settings.json file. The script looks for this file in:

1. Current directory
2. User's home directory (`~/.markdown_tables/settings.json`)
3. Script directory

Example settings.json:

```json
{
    "padding": 1,
    "max_line_length": 120,
    "use_row_separators": true,
    "smart_separators": true,
    "end_row": false,
    "uniform_cell_height": true,
    "vertical_align": "middle"
}
```

## Recommended Usage

For most documentation tables, the enhanced formatter with default settings (smart separators) provides a good balance between readability and space efficiency:

```bash
python meta/scripts/format_markdown_tables_enhanced.py path/to/file.md
```

For tables with minimal content (no wrapped text), use the no row separators option:

```bash
python meta/scripts/format_markdown_tables_enhanced.py path/to/file.md --no-row-separators
```

For a more formal presentation with consistent separators throughout, use the no smart separators option:

```bash
python meta/scripts/format_markdown_tables_enhanced.py path/to/file.md --no-smart-separators
```

To add a final separator at the bottom of tables for visual completeness:

```bash
python meta/scripts/format_markdown_tables_enhanced.py path/to/file.md --end-row
```

## Examples

See example tables in the `tables/` directory:

* `tables/test_enhanced_table.md` - Various table formatting examples
* `tables/recommended_table_format.md` - Recommended formatting style

## Integration with Other Tools

These scripts can be integrated with:

* Text editors (via plugins/extensions)
* Git hooks (for pre-commit formatting)
* CI/CD pipelines (for automated formatting)
* Documentation generation tools

## Future Enhancements

* Notes on potential further enhancements:
* Column-specific wrapping rules (wrap certain columns but not others)
* Support for custom row separators (user-defined separator styles)
* Support for cell background colors (via HTML output option)
* Table of contents generation from tables
* Multi-line header support with proper alignment
* Span support (rowspan, colspan) with pseudo-markdown syntax
* Conditional formatting based on cell content
* Theme support with predefined styles
* Interactive table editor (with web UI)
* Export to various formats (HTML, CSV, JSON, etc.)
* Import from various formats (HTML, CSV, JSON, etc.)
* Integration with version control systems
* Diff highlighting for table changes
* Table pagination for very large tables
* Cell content validation and formatting (dates, numbers, etc.) 

## Test File Organization (2024+)

* **Test input files** should be placed in the `@/preformat_tables` directory.
* **Test output files** should be written to the `@/test_results` directory.
* The `tables/` directory is deprecated and will be removed.

All documentation and usage information for table formatter scripts is now consolidated here. See below for usage, options, and integration guidance.