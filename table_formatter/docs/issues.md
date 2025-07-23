### 1. Fix header divider length

- **Problem:** The formatted table's header divider (the row of dashes) doesn't match the column widths and alignment.
- **Likely Cause:** The code that calculates the divider length is probably not accounting for the actual rendered width of each column, or is using a static length.
- **Next Step:** Inspect the logic in `table_formatter.py` (or the TypeScript equivalent if formatting is done in the extension) that generates the divider row. Add tests for tables with varying column widths.

### 2. Refactor right-click menu

- **Problem:** The context menu for formatting is not a dropdown, so users can't choose the formatting style.
- **Likely Cause:** The extension is registering multiple context menu commands instead of a single command with a submenu or quick pick.
- **Next Step:** Refactor the VSCode extension's `package.json` and command registration to use a single context menu entry that opens a dropdown (QuickPick) for formatting options.

### 3. Preview before apply

- **Problem:** Formatting commands don't show a preview before applying changes.
- **Likely Cause:** The extension applies formatting directly without a preview step.
- **Next Step:** Implement a preview feature using a webview or VSCode's diff/preview API, allowing users to see the formatted table before confirming.

### 4. Interactive options prompt

- **Problem:** No way to customize formatting options; only the default is used.
- **Likely Cause:** The command handler doesn't prompt for options or expose configuration.
- **Next Step:** Add a step in the command handler to prompt the user for formatting options (e.g., alignment, padding), with an option to use defaults.

### 5. Format-all loop

- **Problem:** The command/option that should format all tables only formats the first one.
- **Likely Cause:** The code that finds tables in the document is stopping after the first match, or the loop is broken.
- **Next Step:** Review the table detection and formatting loop. Ensure it iterates over all matches, not just the first.

### 6. Robust table detection

- **Problem:** The detection logic misses some tables.
- **Likely Cause:** The regex or parser for finding tables is too restrictive or buggy.
- **Next Step:** Test the detection logic with a variety of markdown tables, including edge cases (e.g., tables with extra whitespace, missing pipes, or unusual formatting). Expand the regex/parser and add tests.

### 7. Dropdown integration tests

- **Problem:** The VSCode extension's QuickPick actions are not properly mapped to the command handler.
- **Likely Cause:** The extension's `package.json` and command registration might not be correctly configured to handle QuickPick selections.
- **Next Step:** Add tests to verify that the QuickPick options (e.g., "Align Left", "Align Center", "Align Right") correctly trigger the corresponding formatting commands.

### 8. Background Python bridge

- **Problem:** The Python formatter is spawned for each command, causing delays for batch operations.
- **Likely Cause:** The extension spawns a new Python process for each command, which can be slow.
- **Next Step:** Keep a single formatter process alive to speed up batch operations.

### 9. Indent-aware detection

- **Problem:** The table detection logic doesn't handle tables nested inside lists or blockquotes.
- **Likely Cause:** The regex or parser for finding tables doesn't account for leading whitespace or list markers.
- **Next Step:** Extend the table detection logic to handle tables nested inside lists or blockquotes.

### 10. Alignment metadata

- **Problem:** The table detection logic doesn't capture alignment (`:---:`) and pass it to the Python formatter.
- **Likely Cause:** The table detection logic doesn't parse separator cells for `:^?-+:?` patterns.
- **Next Step:** Parse separator cells for `:^?-+:?` patterns and pass `align=["left","center",…]` array to Python CLI.

### 11. Settings UI parity

- **Problem:** Not all promptable options are surfaced in VS Code settings.json schema.
- **Likely Cause:** The extension's settings.json schema doesn't include all promptable options.
- **Next Step:** Add all promptable options to the extension's settings.json schema.

### 12. CI pipeline

- **Problem:** There is no CI pipeline for the extension.
- **Likely Cause:** The extension doesn't have a CI pipeline.
- **Next Step:** Add a CI pipeline that runs `npm test && pytest` on push / PR.

### 13. Packaging polish

- **Problem:** The Python formatter and dependencies are not bundled or clearly documented.
- **Likely Cause:** The extension doesn't bundle the Python formatter and dependencies.
- **Next Step:** Ensure Python formatter + deps bundled or clearly documented.

### 14. Error UX

- **Problem:** The extension doesn't handle errors gracefully.
- **Likely Cause:** The extension doesn't handle errors gracefully.
- **Next Step:** Handle errors gracefully, e.g. show friendly messages for missing Python / bad path, avoid closing unrelated editors.

### 15. First-run onboarding

- **Problem:** The extension doesn't have first-run onboarding.
- **Likely Cause:** The extension doesn't have first-run onboarding.
- **Next Step:** Show a toast notification explaining commands & keybindings on first run.

---
tags: [roadmap, project_management, table_formatter]
provides: [table_formatter_roadmap]
requires: [table_formatter, vscode_extension]
status: active
priority: high
---

# Roadmap: Table Formatter & VSCode Extension Improvements

A structured plan for addressing core issues in the table formatter and its VSCode extension, following DSS guidelines for incremental, testable, and well-documented improvements.

## Overview

This roadmap outlines the steps to resolve known issues with the table formatter and its VSCode extension, focusing on correctness, usability, and maintainability. Each task is aligned with DSS workflows and documentation standards.

## Prerequisites

- Familiarity with Python and TypeScript
- Understanding of VSCode extension development
- Access to the DSS codebase and test suite
- Review of [table_formatter_info.md](mdc:table_formatter/docs/table_formatter_info.md)

## Task Breakdown

| # | Task | Description | Status |
|---|------|-------------|--------|
| 1 | Fix header divider length | Ensure the markdown table header divider matches column widths and alignment | **Completed** |
| 2 | Refactor right-click menu | Consolidate multiple commands into a single QuickPick dropdown | **Completed** |
| 3 | Preview before apply | Provide diff-view or webview preview | **Completed** |
| 4 | Interactive options prompt | Gather formatting options with session cache + settings persistence | **Completed** |
| 5 | Format-all loop | Process every table without position drift | **Completed** |
| 6 | Robust table detection | Handle missing leading/trailing pipes & improved column counting | **Completed** |
| 7 | Dropdown integration tests | CI-ready tests for QuickPick mapping | **Completed** |
| 8 | **Background Python bridge** | Keep a single formatter process alive to speed up batch operations | **Completed** |
| 9 | **Indent-aware detection** | Detect tables nested inside lists / blockquotes | **Completed** |
| 10 | **Alignment metadata** | Capture alignment (`:---:`) and pass to Python formatter | **Completed** |
| 11 | **Settings UI parity** | Surface all promptable options in VS Code settings.json schema | **Completed** |
| 12 | **CI pipeline** | GitHub Action: `npm test && pytest` on push / PR | **Completed** |
| 13 | **Packaging polish** | Ensure Python formatter + deps bundled or clearly documented | Pending |
| 14 | **Error UX** | Friendlier messages for missing Python / bad path, avoid closing unrelated editors | Pending |
| 15 | **First-run onboarding** | Toast notification explaining commands & keybindings | **Completed** |
