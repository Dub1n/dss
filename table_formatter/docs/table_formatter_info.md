---
tags: [automation, markdown, formatting, tables]
provides: [markdown_table_formatting, table_content_wrapping, advanced_table_formatting]
requires: []
---

Enhanced Markdown Table Formatter - Architecture & Dataflow Overview

This script processes Markdown files to find, parse, and reformat tables with consistent alignment, padding, and advanced features (e.g., code block preservation, multi-line cells).

# High-Level Dataflow

1. Input Handling & Validation ✓
   - Input: Command-line arguments (list of Markdown file paths, optional max-width, output directory, timeout, debug flag)
   - Output: Validated configuration object and list of file paths to process
   - Parameters: max-width (default: 80), output directory (default: 'tables/test_results'), timeout (default: 5 seconds), debug-whitespace (boolean)
   - Process:
     a. Validate all input parameters (check file existence, directory permissions, numeric ranges) ✓
     b. Create configuration object with validated parameters ✓
     c. Initialize logging with appropriate level based on debug flag ✓
     d. Set up error tracking and recovery state ✓
   - Error Handling:
     - Invalid parameters: Log error and exit with usage instructions ✓
     - File access issues: Log error and skip file ✓
     - Directory issues: Create directory if missing, log warning if permissions insufficient ✓

2. File Processing & Buffering ✓
   - Input: List of file paths, configuration object
   - Output: Generator yielding (file_path, content_chunks)
   - Parameters: chunk_size (default: 8192 bytes)
   - Process:
     a. For each file:
        - Open file in binary mode ✓
        - Read in chunks to manage memory ✓
        - Decode chunks to UTF-8 with error handling ✓
        - Yield (file_path, chunk) pairs ✓
   - Error Handling:
     - File read errors: Log error, skip to next file ✓
     - Decode errors: Log warning, use replacement character ✓
     - Memory issues: Log error, reduce chunk size ✓

3. Table Detection & Validation ✓
   - Input: Content chunk (string), file context (path, line numbers)
   - Output: List of validated table blocks with metadata
   - Parameters: min_table_lines (default: 3), max_table_width (default: 1000)
   - Process:
     a. Scan chunk for table markers (pipes, dashes) ✓
     b. For each potential table:
        - Validate structure (header, separator, at least one row) ✓
        - Check column consistency ✓
        - Detect code blocks and nested structures ✓
        - Record table boundaries and metadata ✓
     c. Handle tables split across chunks ✓
   - Error Handling:
     - Malformed tables: Log warning, attempt recovery ✓
     - Inconsistent columns: Log error, skip table ✓
     - Nested structures: Log warning, preserve structure ✓

4. Table Parsing & State Management ✓
   - Input: Table block with metadata
   - Output: Parsed table object with headers, data, alignments, and state
   - Parameters: None
   - Process:
     a. Initialize table state object ✓
     b. Parse header row:
        - Split by pipe, handle escaped pipes ✓
        - Validate header content ✓
        - Store header state ✓
     c. Parse separator row:
        - Extract alignment information ✓
        - Validate separator format ✓
        - Store alignment state ✓
     d. Parse data rows:
        - Handle code blocks and nested structures ✓
        - Track row state and column counts ✓
        - Validate cell content ✓
     e. Update table state with parsing results ✓
   - Error Handling:
     - Parse errors: Log error, attempt recovery ✓
     - State inconsistencies: Log warning, reset state ✓
     - Memory issues: Log error, clear state ✓

5. Table Analysis & Validation ✓
   - Input: Parsed table object, diagnostics
   - Output: TableAnalysis object with column analyses, statistics, and issues
   - Parameters: thresholds for content consistency, unique value ratio, etc.
   - Process:
     a. Analyze each column for content type, patterns, and statistics ✓
     b. Validate content consistency and unique value ratios ✓
     c. Report issues such as mixed content, low/high variety, empty cells, etc. ✓
   - Error Handling:
     - Analysis errors: Log error, skip problematic columns ✓
     - Validation errors: Log warning, include in issues ✓

6. Basic Formatting ✓
   - Input: Parsed and analyzed table object, configuration
   - Output: Formatted table string
   - Parameters: max-width, alignment, padding
   - Process:
     a. Calculate optimal column widths ✓
     b. Format headers, separators, and data rows ✓
     c. Apply alignment and padding rules ✓
     d. Preserve code blocks and special characters ✓
   - Error Handling:
     - Formatting errors: Log warning, use fallback format ✓
     - Width issues: Log warning, adjust formatting ✓

7. Advanced Features (Completed ✓)
   - Code block detection and preservation ✓
   - Multi-line cell handling ✓
   - Cell wrapping and line breaks ✓
   - Advanced alignment and padding ✓
   - Maximum width constraints ✓
   - Special character handling ✓
   - Style template system ✓
   - Priority-based rule application ✓

# Style Template System

## Overview

The style template system allows users to apply predefined sets of formatting rules and configuration options to tables. This enables quick switching between common table styles (e.g., GitHub, technical documentation, minimal) and ensures consistent formatting across different use cases.

## How It Works

- **Templates** are collections of formatting rules and configuration values (e.g., padding, alignment, code block handling).
- The formatter can apply a template by name, which replaces the current rules/config with those from the template.
- Users can also combine templates with custom rules for advanced scenarios.
- Built-in templates include:
  - **GitHub**: Mimics GitHub-flavored markdown tables, preserving inline code and links.
  - **Technical**: Optimized for technical docs, with extra math/code formatting.
  - **Minimal**: Strips most formatting for compact tables.

## Template Configuration

Each template includes:

- Complete FormatConfig settings
- Priority-based rule set
- Template-specific formatting rules
- Inheritance from default rules

## Integration in the Pipeline

- Templates are initialized in the formatter and can be applied or removed at any time.
- When a template is active, its rules/config override the defaults.
- The template system is compatible with the custom rule system, allowing for flexible combinations.
- Rules are applied in priority order, with template rules taking precedence.

## Example Usage

```python
# Apply GitHub style
formatter.apply_template('github')

# Apply technical style with custom rules
formatter.apply_template('technical')
formatter.add_rule(custom_rule)

# Revert to default style
formatter.remove_template()
```

8. Output Generation (In Progress)
   - Input: Formatted table string, output configuration
   - Output: Formatted markdown file or string
   - Process:
     a. Generate output in specified format
       - String output: Basic implementation complete ✓
       - File output: Basic implementation with backup support ✓
       - Stream output: Basic implementation with progress tracking ✓
       - Custom output handlers: Framework in place ✓
     b. Apply final formatting and cleanup
     c. Write to file or return string
   - Error Handling:
     - Output errors: Log error, attempt recovery ✓
     - Format issues: Log warning, use fallback format ✓
     - File system errors: Log error, skip file ✓
     - Permission issues: Log error, skip file ✓
   - Progress Tracking:
     - Table processing status: Implemented ✓
     - Formatting progress: Implemented ✓
     - Error reporting: Implemented ✓
   - Configuration:
     - Output format settings: Implemented ✓
     - File operation settings: Implemented ✓
     - Progress tracking settings: Implemented ✓
     - Error handling settings: Implemented ✓

9. File Operations (In Progress)
   - Input: List of input files, output configuration
   - Output: Processed files in output directory
   - Process:
     a. Create output directory structure ✓
     b. Process each input file ✓
     c. Write formatted output ✓
   - Error Handling:
     - File system errors: Log error, skip file ✓
     - Permission issues: Log error, skip file ✓
     - Disk space issues: Log error, stop processing ✓
   - Features:
     - Directory traversal ✓
     - File pattern matching ✓
     - Backup creation ✓
     - Progress tracking ✓
     - Statistics generation ✓
     - Error reporting ✓

# Current Known Issues / Edge Cases

- **Unique Value Ratio Reporting:**
  - For columns with all identical values, the analyzer reports "All numeric values are identical" but does not always include "Low variety of values". The test suite expects both issues to be reported for such columns. This is an edge case in the validation logic and is being addressed.

- **Padding Configuration:**
  - The padding system has been updated to support variable padding configurations per column
  - Tests have been updated to validate different padding scenarios
  - Edge cases for padding with code blocks and multiline content are being addressed

# Development Roadmap

### Phase 1: Core Functionality (Completed ✓)

- [x] Basic table detection and parsing
- [x] Content type analysis
- [x] Basic formatting rules
- [x] Error handling and recovery
- [x] Test suite for core functionality

### Phase 2: Advanced Features (Completed ✓)

- [x] Code block detection and preservation
- [x] Multi-line cell handling
- [x] Cell wrapping
- [x] Advanced alignment and padding
- [x] Custom formatting rules
  - [x] Rule system with conditions and formatters
  - [x] Priority-based rule application
  - [x] Default rule set
  - [x] Rule management (add/remove)
  - [x] Rule combinations and edge cases
- [x] Style templates
  - [x] Template configuration system
  - [x] Built-in templates (GitHub, Technical, Minimal)
  - [x] Template inheritance
  - [x] Template management
- [x] Real-world test suite with sample data
  - [x] Test data directory structure
  - [x] GitHub README style tables
  - [x] Technical documentation tables
  - [x] Complex edge case tables
  - [x] Additional real-world examples
  - [x] Performance benchmarks
  - [x] Memory usage tests

### Phase 3: Output Generation (Completed ✓)

- [x] Formatted output options
  - [x] String output
  - [x] File output
  - [x] Stream output
  - [x] Custom output handlers
- [x] Progress indicators
  - [x] Table processing status
  - [x] Formatting progress
  - [x] Error reporting
- [x] Summary reports
  - [x] Processing statistics
  - [x] Formatting changes
  - [x] Error summaries
- [x] Error reports
  - [x] Detailed error messages
  - [x] Error categorization
  - [x] Recovery suggestions
- [x] Statistics generation
  - [x] Table metrics
  - [x] Formatting metrics
  - [x] Performance metrics

### Phase 4: File Operations (Completed ✓)

- [x] File reading and writing
  - [x] Basic file operations
  - [x] Directory traversal
  - [x] File pattern matching
  - [x] Backup creation
- [x] Directory traversal
  - [x] Recursive directory scanning
  - [x] Pattern-based file filtering
  - [x] Hidden file handling
- [x] Backup creation
  - [x] Automatic backup generation
  - [x] Backup cleanup
  - [x] Backup restoration
- [x] File validation
  - [x] File existence checks
  - [x] Permission validation
  - [x] Size limits
  - [x] Pattern matching
- [x] Progress reporting
  - [x] File processing status
  - [x] Directory traversal progress
  - [x] Error tracking
  - [x] Statistics generation

### Phase 5: CLI Implementation (Completed ✓)

- [x] Command-line interface
  - [x] Argument parsing
  - [x] Option validation
  - [x] Help documentation
  - [x] Error handling
- [x] Batch processing
  - [x] Multiple file handling
  - [x] Directory traversal
  - [x] Pattern matching
- [x] Integration with core modules
  - [x] Connecting parser, analyzer, and formatter
  - [x] Configuration mapping
  - [x] Error propagation
- [x] Usability enhancements
  - [x] Helper scripts (batch/shell)
  - [x] Test script
  - [x] Usage examples
  - [x] Documentation

### Phase 6: VS Code Extension (Planned)

- [ ] Extension architecture
  - [ ] Project setup
  - [ ] Extension manifest
  - [ ] Activation events
  - [ ] Command registration
- [ ] Core functionality
  - [ ] Table detection in active document
  - [ ] Format table command
  - [ ] Format all tables command
  - [ ] Format selection command
- [ ] User interface
  - [ ] Template selection dropdown
  - [ ] Configuration UI
  - [ ] Status bar indicator
  - [ ] Progress notification
- [ ] Integration with formatter
  - [ ] Node.js interop with Python
  - [ ] Configuration mapping
  - [ ] Error handling
  - [ ] Output processing
- [ ] Extension packaging
  - [ ] Build process
  - [ ] Documentation
  - [ ] Marketplace publishing
  - [ ] Version management

# Module Structure

```text
table_formatter/
├── __init__.py                  # Package initialization
├── main.py                     # CLI entry point and orchestration
├── README.md                   # User-facing documentation
├── requirements.txt            # Package dependencies
├── format_tables.bat           # Windows helper script
├── format_tables.sh            # Unix helper script
├── core/                       # Core functionality
│   ├── __init__.py             # Core module exports
│   ├── table_parser.py         # Table parsing
│   ├── table_analyzer.py       # Table analysis
│   ├── core/table_formatter.py      # Table formatting
│   └── code_block_info.py      # Code block handling
├── tests/                      # Test suite
│   ├── __init__.py             # Test package initialization
│   ├── test_formatter.py       # Formatter test script
│   └── test_data/              # Test data
│       └── sample_tables.md    # Sample tables for testing
├── docs/                       # Documentation
│   ├── SUMMARY.md              # Project summary
│   ├── current_state.md        # Development status
│   └── table_formatter_info.md # Developer documentation
└── vscode-extension/           # VS Code extension
    ├── package.json            # Extension manifest
    ├── tsconfig.json           # TypeScript configuration
    ├── src/                    # Extension source code
    │   └── extension.ts        # Extension entry point
    ├── node_modules/           # Node.js dependencies
    └── out/                    # Compiled output
```

# VS Code Extension Development Plan

## Overview

The VS Code extension will integrate the markdown table formatter into Visual Studio Code, providing commands to format tables within markdown documents. The extension will leverage the existing Python implementation through a Node.js wrapper.

## Architecture

1. **Extension Layer** (TypeScript)
   - Extension activation
   - Command registration
   - UI components
   - Configuration management
   - Document handling

2. **Bridge Layer** (Node.js)
   - Communication with Python script
   - Process management
   - Error handling
   - Configuration mapping

3. **Formatter Layer** (Python)
   - Existing table formatter implementation
   - CLI adapter for extension use
   - Response formatting for extension

## Key Components

1. **Commands**
   - `markdownTableFormatter.formatTable`: Format the table at cursor
   - `markdownTableFormatter.formatAllTables`: Format all tables in the document
   - `markdownTableFormatter.formatSelection`: Format selection as a table

2. **Configuration**
   - Template selection
   - Formatting options
   - Auto-format settings

3. **UI Elements**
   - Status bar item
   - Quick pick for templates
   - Configuration UI
   - Progress notification

4. **Integration**
   - Python environment detection
   - Extension installation validation
   - Table detection algorithm
   - Range-based editing

## Development Roadmap

### Phase 1: Project Setup and Basic Structure

1. Initialize VS Code extension project
   - Create extension scaffold with Yeoman generator
   - Set up TypeScript configuration
   - Define extension manifest
   - Configure build process

2. Implement basic extension activation
   - Register activation events
   - Set up logging and error handling
   - Initialize configuration
   - Register commands

### Phase 2: Core Functionality

1. Implement table detection
   - Detect tables in active document
   - Find table at cursor position
   - Find all tables in document
   - Handle selection range

2. Implement bridge to Python formatter
   - Set up child process execution
   - Handle command-line argument mapping
   - Process output parsing
   - Error handling and recovery

3. Implement formatting commands
   - Format table at cursor
   - Format all tables
   - Format selection

### Phase 3: User Interface

1. Implement status bar integration
   - Show formatter status
   - Quick access to commands
   - Template selection

2. Implement configuration UI
   - Extension settings
   - Template configuration
   - Advanced options

3. Implement progress and notification
   - Show formatting progress
   - Display results summary
   - Error notifications

### Phase 4: Testing and Packaging

1. Implement test suite
   - Unit tests for extension functions
   - Integration tests with VS Code API
   - End-to-end tests with real documents

2. Package extension
   - Create VSIX package
   - Write marketplace documentation
   - Prepare screenshots and examples
   - Set up publishing workflow

3. Publish extension
   - Publish to VS Code Marketplace
   - Set up update mechanism
   - Gather initial feedback

## Implementation Details

### Extension Entry Point

```typescript
// extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Register commands
    const formatTableCmd = vscode.commands.registerCommand(
        'markdownTableFormatter.formatTable',
        formatTableAtCursor
    );
    
    const formatAllTablesCmd = vscode.commands.registerCommand(
        'markdownTableFormatter.formatAllTables',
        formatAllTables
    );
    
    const formatSelectionCmd = vscode.commands.registerCommand(
        'markdownTableFormatter.formatSelection',
        formatSelection
    );
    
    // Register disposables
    context.subscriptions.push(formatTableCmd);
    context.subscriptions.push(formatAllTablesCmd);
    context.subscriptions.push(formatSelectionCmd);
    
    // Initialize status bar
    initializeStatusBar(context);
    
    // Log activation
    console.log('Markdown Table Formatter is now active');
}

export function deactivate() {
    // Clean up resources
}
```

### Python Bridge

```typescript
// pythonBridge.ts
import * as cp from 'child_process';
import * as vscode from 'vscode';

export async function formatTable(tableText: string, options: any): Promise<string> {
    return new Promise((resolve, reject) => {
        // Get Python path from configuration
        const pythonPath = vscode.workspace.getConfiguration('markdownTableFormatter')
            .get('pythonPath', 'python');
        
        // Get formatter script path
        const formatterPath = getFormatterPath();
        
        // Build command-line arguments
        const args = buildCommandLineArgs(options);
        
        // Execute formatter
        const process = cp.spawn(pythonPath, [formatterPath, ...args]);
        
        // Collect output
        let stdout = '';
        let stderr = '';
        
        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        process.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve(stdout);
            } else {
                reject(new Error(`Formatter failed with code ${code}: ${stderr}`));
            }
        });
        
        // Send table text to formatter
        process.stdin.write(tableText);
        process.stdin.end();
    });
}
```

### Table Detection

```typescript
// tableDetection.ts
import * as vscode from 'vscode';

export function detectTableAtCursor(
    document: vscode.TextDocument,
    position: vscode.Position
): { range: vscode.Range, text: string } | null {
    // Get the line at cursor position
    const line = document.lineAt(position.line).text;
    
    // Check if the line is part of a table
    if (!isTableLine(line)) {
        return null;
    }
    
    // Find table start
    let startLine = position.line;
    while (startLine > 0 && isTableLine(document.lineAt(startLine - 1).text)) {
        startLine--;
    }
    
    // Find table end
    let endLine = position.line;
    while (endLine < document.lineCount - 1 && isTableLine(document.lineAt(endLine + 1).text)) {
        endLine++;
    }
    
    // Create range and extract text
    const range = new vscode.Range(
        new vscode.Position(startLine, 0),
        new vscode.Position(endLine, document.lineAt(endLine).text.length)
    );
    
    const text = document.getText(range);
    
    return { range, text };
}

function isTableLine(line: string): boolean {
    // Simple check for table line: contains at least one pipe
    return line.trim().startsWith('|') && line.trim().endsWith('|');
}
```

### Formatting Command Implementation

```typescript
// commands.ts
import * as vscode from 'vscode';
import { detectTableAtCursor } from './tableDetection';
import { formatTable } from './pythonBridge';

export async function formatTableAtCursor() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }
    
    const table = detectTableAtCursor(editor.document, editor.selection.active);
    if (!table) {
        vscode.window.showInformationMessage('No table found at cursor position');
        return;
    }
    
    try {
        // Get formatting options
        const options = getFormattingOptions();
        
        // Format the table
        const formattedTable = await formatTable(table.text, options);
        
        // Apply the edit
        await editor.edit(editBuilder => {
            editBuilder.replace(table.range, formattedTable);
        });
        
        vscode.window.showInformationMessage('Table formatted successfully');
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to format table: ${error.message}`);
    }
}
```

## Next Steps

The detailed roadmap provides a clear path forward for developing the VS Code extension. The key is to maintain the modular architecture and leverage the existing Python implementation while providing a seamless integration with VS Code.

Each phase of the roadmap should be approached incrementally, with testing at each step to ensure functionality works as expected.

# Update Protocol

- Update this section whenever the script's architecture or dataflow changes.
- Use this as a reference for all future development and debugging.

## Current Implementation Status

- **Core functionality**: Completed ✓
- **Advanced features**: Completed ✓
- **Output generation**: Completed ✓
- **File operations**: Completed ✓
- **CLI Implementation**: Completed ✓
- **VS Code Extension**: Planned ◯

## Packaging & Distribution (2025-07-15)
The VS Code `.vsix` bundle now includes:
- `main.py`, `bg_server.py`, `core/` modules
- `requirements.txt` for offline install
`package.json files[]` updated accordingly.

## Error UX Improvements
- Missing Python executable or bad path → extension shows a clear VS Code error with action to open settings.
- Background server stderr is piped to console for quick diagnosis.
