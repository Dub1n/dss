# Markdown Table Formatter

Format markdown tables with consistent alignment, padding, and advanced features directly in Visual Studio Code.

## Features

- Format markdown tables with consistent column widths, alignment, and padding
- Preserve code blocks, inline code, and special formatting
- Support for multi-line cells and text wrapping
- Smart detection of content types
- Predefined style templates (GitHub, Technical, Minimal)
- **Background Python bridge** (optional) eliminates process-spawn overhead
- **First-run toast** with quick links to docs & commands
- Status bar integration for quick access
- Format on save option

## Usage

### Commands & Context Menu

The extension now provides a **single entry point** that makes table formatting more discoverable:

- **Table Formatting Options…** (`markdownTableFormatter.formatDropdown`)
  - Opens a Quick Pick dropdown where you can choose:
    - *Format Table at Cursor*
    - *Format All Tables in Document*
    - *Format Selection as Table*

After choosing an action, an **interactive prompt** lets you adjust formatting parameters (template, width, padding, wrap, etc.).  You can reuse the previous choices or persist them as your new defaults.  When *Preview* is enabled you’ll see either a diff view or a side-by-side **Webview panel** (`markdownTableFormatter.previewMode = diff | webview`).

> Legacy keybindings (`Ctrl+Alt+T`, `Ctrl+Alt+A`) are still available and mapped internally to the same underlying commands.

Right-clicking inside a Markdown document shows the *Table Formatting Options…* item in the context menu, keeping the editor surface uncluttered while still giving quick access.

### Status Bar

Click the "Table" button in the status bar to format the table at the current cursor position.

## Command-Line Usage

The same formatter can be run head-less from a terminal (useful for CI or batch scripts):

```bash
# Read a table from stdin and write to stdout using the technical template
cat myTable.md | python -m table_formatter.main \
    --stdin --stdout \
    --template technical \
    --max-width 100 \
    --min-padding 1 \
    --preserve-code-blocks true \
    --wrap-text true
```

CLI flags map 1-to-1 onto `FormatConfig` fields. The VS Code extension simply spawns this CLI with the same set of flags, ensuring **one unified configuration path** across editor and scripts.

---

## Implementation Details

The core table formatting logic is implemented in `core/table_formatter.py`. All formatting features, templates, and configuration options are provided by this module. The VS Code extension and any CLI tools use this core module for all formatting operations.

## Configuration

All settings are available in **Settings UI** or `settings.json`:

| Setting | Description | Default |
|---------|-------------|---------|
| `pythonPath` | Path to Python executable | `python` |
| `formatterPath` | Custom path to `main.py` (empty = bundled) | `""` |
| `enableBackgroundFormatter` | Keep a background formatter process | `false` |
| `defaultTemplate` | `github`, `technical`, `minimal`, `smart`, `none` | `github` |
| `formatOnSave` | Auto-format on save | `false` |
| `maxTableWidth` | Max width (chars) | `80` |
| `minPadding` | Spaces between borders & text | `1` |
| `preserveCodeBlocks` | Don’t alter fenced code blocks | `true` |
| `wrapText` | Wrap long cell text | `true` |
| `enablePreview` | Show diff/webview before apply | `true` |
| `previewMode` | `diff` or `webview` | `diff` |

## Requirements

- Visual Studio Code 1.60.0 or higher
- Python 3.6 or higher

## Installation

1. Install the extension from the VS Code Marketplace
2. Ensure Python is installed and available in your PATH
3. Restart VS Code

## Examples

### Before Formatting

```markdown
| Column 1 | Column 2 | Column 3 |
|---|---|---|
| Data 1 | Data 2 | Data 3 |
| More data | More | And more |
```

### After Formatting (GitHub Template)

```markdown
| Column 1   | Column 2 | Column 3  |
|------------|----------|-----------|
| Data 1     | Data 2   | Data 3    |
| More data  | More     | And more  |
```

## Known Issues

- Large tables may take longer to format
- Tables within code blocks are not detected

## Release Notes

### 0.1.0

- Initial release
- Basic table formatting
- Template support
- Status bar integration

## Packaging & Distribution

The VS Code marketplace package now bundles **all Python assets** required to run the formatter offline:

```text
main.py          # CLI entry-point
bg_server.py     # background JSON-RPC server
core/            # formatter library modules
requirements.txt # pinned versions (vendored by VSCE)
```

`package.json → files[]` ensures these items are included in the `.vsix` build produced by `vsce package`.

---
