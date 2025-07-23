/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-useless-escape */
import * as vscode from 'vscode';

// Matches optional indentation, blockquote markers ('>'), unordered or ordered list markers
// followed by whitespace. Used to make table detection aware of nesting inside lists or
// blockquotes (indent-aware detection).
const PREFIX_PATTERN = "^\\s*(?:>\\s*)*(?:[-*+]\\s+|\\d+\\.\\s+)?";

/**
 * Strip any nesting prefix (blockquote or list markers) from a line so that
 * downstream validation logic can operate on the pure table syntax.
 */
function stripTablePrefix(line: string): string {
    let result = line.replace(/^\s*>\s*/, '');
    result = result.replace(/^\s*[-*+]\s+/, '');
    result = result.replace(/^\s*\d+\.\s+/, '');
    return result;
}

/**
 * Represents a detected markdown table
 */
export interface TableInfo {
    range: vscode.Range;
    text: string;
}

/**
 * Detect a markdown table at the given cursor position
 * @param document The document to search in
 * @param position The cursor position
 * @returns Table information or null if no table is found
 */
export function detectTableAtCursor(
    document: vscode.TextDocument,
    position: vscode.Position
): TableInfo | null {
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

/**
 * Detect all markdown tables in the document
 * @param document The document to search in
 * @returns Array of table information
 */
export function detectAllTables(document: vscode.TextDocument): TableInfo[] {
    // Use the more robust class-based detector to avoid drift between two implementations.
    const detector = new TableDetection();
    return detector.detectTables(document).map(t => ({ range: t.range, text: t.text }));
}

/**
 * Check if a line is part of a markdown table
 * @param line The line to check
 * @returns true if the line is part of a table
 */
export function isTableLine(line: string): boolean {
    /**
     * Remove optional blockquote/list prefixes so that nested table lines are
     * evaluated correctly.
     */
    const strippedLine = stripTablePrefix(line);

    // Table lines must contain at least one pipe
    const trimmed = strippedLine.trim();

    // Exclude code blocks
    if (trimmed.startsWith('```') || trimmed.endsWith('```')) {
        return false;
    }

    // Exclude horizontal rules
    if (/^[\-=]{3,}$/.test(trimmed)) {
        return false;
    }

    // Empty lines are not table lines
    if (trimmed.length === 0) {
        return false;
    }

    // Line must contain at least one pipe after stripping prefix
    return trimmed.includes('|');
}

/**
 * Check if text represents a valid markdown table
 * @param text The text to check
 * @returns true if the text is a valid table
 */
export function isValidTable(text: string): boolean {
    // Split into lines
    const lines = text.split('\n');
    
    // A table must have at least 2 lines (header and separator)
    if (lines.length < 2) {
        return false;
    }
    
    // Check for separator row (second line)
    // Must contain only |, -, :, and spaces
    const separatorLine = lines[1].trim();
    const validSeparator = /^\|[\s\-:\|]+\|$/.test(separatorLine);
    
    if (!validSeparator) {
        return false;
    }
    
    // Check that all lines have consistent column count
    const columnCount = (lines[0].match(/\|/g) || []).length;
    
    for (const line of lines) {
        const pipeCount = (line.match(/\|/g) || []).length;
        if (pipeCount !== columnCount) {
            return false;
        }
    }
    
    return true;
}

export interface Table {
    text: string;
    range: vscode.Range;
    isValid(): boolean;
}

export class TableDetection {
    // Note: prefixPattern is defined at the module level (see top of file) to avoid using `this` in
    // property initializers which is not allowed in TypeScript.

    // Allow optional leading/trailing pipes and the prefix pattern
    private readonly tableRegex = new RegExp(`${PREFIX_PATTERN}\\|?.+\\|.+\\|?\\s*$`);
    // eslint-disable-next-line no-useless-escape
    private readonly separatorRegex = new RegExp(`${PREFIX_PATTERN}\\|?[-: ]+\\|?[-:| ]*\\|?\\s*$`);

    /**
     * Detect all tables in a document or text
     */
    public detectTables(input: vscode.TextDocument | string): Table[] {
        if (typeof input === 'string') {
            return this.detectTablesFromText(input);
        } else {
            return this.detectTablesFromDocument(input);
        }
    }

    /**
     * Detect table at cursor position
     */
    public detectTableAtCursor(document: vscode.TextDocument, position: vscode.Position): Table | undefined {
        const tables = this.detectTablesFromDocument(document);
        return tables.find(table => table.range.contains(position));
    }

    private detectTablesFromText(text: string): Table[] {
        const lines = text.split('\n');
        const tables: Table[] = [];
        let currentTable: string[] = [];
        let startLine = -1;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            if (this.tableRegex.test(line)) {
                if (currentTable.length === 0) {
                    startLine = i;
                }
                currentTable.push(line);
            } else if (this.separatorRegex.test(line) && currentTable.length > 0) {
                currentTable.push(line);
            } else if (currentTable.length > 0) {
                // End of table
                if (currentTable.length >= 3) { // At least header, separator, and one row
                    const tableText = currentTable.join('\n');
                    const range = new vscode.Range(
                        startLine,
                        0,
                        i - 1,
                        lines[i - 1].length
                    );
                    tables.push(new TableImpl(tableText, range));
                }
                currentTable = [];
                startLine = -1;
            }
        }

        // Check for table at end of text
        if (currentTable.length >= 3) {
            const tableText = currentTable.join('\n');
            const range = new vscode.Range(
                startLine,
                0,
                lines.length - 1,
                lines[lines.length - 1].length
            );
            tables.push(new TableImpl(tableText, range));
        }

        return tables;
    }

    private detectTablesFromDocument(document: vscode.TextDocument): Table[] {
        const tables: Table[] = [];
        let currentTable: string[] = [];
        let startLine = -1;

        for (let i = 0; i < document.lineCount; i++) {
            const line = document.lineAt(i);
            const text = line.text;

            if (this.tableRegex.test(text)) {
                if (currentTable.length === 0) {
                    startLine = i;
                }
                currentTable.push(text);
            } else if (this.separatorRegex.test(text) && currentTable.length > 0) {
                currentTable.push(text);
            } else if (currentTable.length > 0) {
                // End of table
                if (currentTable.length >= 3) { // At least header, separator, and one row
                    const tableText = currentTable.join('\n');
                    const range = new vscode.Range(
                        startLine,
                        0,
                        i - 1,
                        document.lineAt(i - 1).text.length
                    );
                    tables.push(new TableImpl(tableText, range));
                }
                currentTable = [];
                startLine = -1;
            }
        }

        // Check for table at end of document
        if (currentTable.length >= 3) {
            const tableText = currentTable.join('\n');
            const range = new vscode.Range(
                startLine,
                0,
                document.lineCount - 1,
                document.lineAt(document.lineCount - 1).text.length
            );
            tables.push(new TableImpl(tableText, range));
        }

        return tables;
    }
}

class TableImpl implements Table {
    constructor(
        public readonly text: string,
        public readonly range: vscode.Range
    ) {}

    public isValid(): boolean {
        const lines = this.text.split('\n');
        if (lines.length < 3) return false; // Need header, separator, and at least one row

        // Check header
        if (!this.isValidRow(lines[0])) return false;

        // Check separator
        if (!this.isValidSeparator(lines[1])) return false;

        // Check all data rows
        for (let i = 2; i < lines.length; i++) {
            if (!this.isValidRow(lines[i])) return false;
        }

        // Check column count consistency
        const columnCount = this.getColumnCount(lines[0]);
        for (let i = 1; i < lines.length; i++) {
            if (this.getColumnCount(lines[i]) !== columnCount) return false;
        }

        return true;
    }

    private isValidRow(line: string): boolean {
        const stripped = stripTablePrefix(line);
        return /^\s*\|?.+\|.+\|?\s*$/.test(stripped);
    }

    private isValidSeparator(line: string): boolean {
        const stripped = stripTablePrefix(line);
        return /^\s*\|?[-: ]+\|?[-:| ]*\|?\s*$/.test(stripped);
    }

    private getColumnCount(line: string): number {
        const stripped = stripTablePrefix(line);
        const cells = stripped.split('|').map(c => c.trim());
        return cells.filter(c => c !== '').length;
    }
} 