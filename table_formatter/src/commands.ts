import * as vscode from 'vscode';
import { detectTableAtCursor, detectAllTables } from './tableDetection';
import { PythonBridge } from './pythonBridge';
import { previewAndConfirm } from './preview';
import { promptForFormattingOptions } from './optionsPrompt';

let pythonBridge: PythonBridge | undefined;

function getPythonBridge(): PythonBridge {
    if (!pythonBridge) {
        pythonBridge = new PythonBridge();
    }
    return pythonBridge;
}

/**
 * Format the markdown table at the current cursor position
 */
export async function formatTableAtCursor(): Promise<void> {
    // Get the active text editor
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }

    // Check if the document is markdown
    if (editor.document.languageId !== 'markdown') {
        vscode.window.showInformationMessage('This is not a markdown file');
        return;
    }

    // Detect table at cursor position
    const table = detectTableAtCursor(editor.document, editor.selection.active);
    if (!table) {
        vscode.window.showInformationMessage('No table found at cursor position');
        return;
    }

    try {
        // Get formatting options (interactive prompt)
        const options = await getFormattingOptions();
        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        const enablePreview = config.get<boolean>('enablePreview', true);
        
        // Format the table
        const formattedTable = await getPythonBridge().formatTable(table.text, options);
        
        // Preview and confirm if enabled
        if (enablePreview) {
            const apply = await previewAndConfirm(table.text, formattedTable);
            if (!apply) {
                return; // User cancelled
            }
        }
        
        // Apply the edit
        await editor.edit(editBuilder => {
            editBuilder.replace(table.range, formattedTable);
        });
        
        vscode.window.showInformationMessage('Table formatted successfully');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to format table: ${error.message}`);
    }
}

/**
 * Format all markdown tables in the current document
 */
export async function formatAllTables(): Promise<void> {
    // Get the active text editor
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }

    // Check if the document is markdown
    if (editor.document.languageId !== 'markdown') {
        vscode.window.showInformationMessage('This is not a markdown file');
        return;
    }

    // Detect all tables in the document
    const tables = detectAllTables(editor.document);
    if (tables.length === 0) {
        vscode.window.showInformationMessage('No tables found in document');
        return;
    }

    try {
        // Get formatting options (interactive prompt)
        const options = await getFormattingOptions();
        
        let tablesFormatted = 0;

        // Show progress
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Formatting tables',
            cancellable: true
        }, async (progress, token) => {
            const increment = 100 / tables.length;

            const sorted = [...tables].sort((a, b) => b.range.start.line - a.range.start.line);

            // Collect edits first to avoid position shifts during editing
            const replacements: { range: vscode.Range; content: string }[] = [];

            for (let i = 0; i < sorted.length; i++) {
                if (token.isCancellationRequested) break;

                progress.report({ message: `Table ${i + 1} of ${tables.length}`, increment });

                try {
                    const content = await getPythonBridge().formatTable(sorted[i].text, options);
                    replacements.push({ range: sorted[i].range, content });
                    tablesFormatted++;
                } catch (err: any) {
                    console.error(`Error formatting table ${i + 1}: ${err.message}`);
                }
            }

            if (replacements.length) {
                await editor.edit(editBuilder => {
                    for (const r of replacements) {
                        editBuilder.replace(r.range, r.content);
                    }
                });
            }
        });

        vscode.window.showInformationMessage(`Formatted ${tablesFormatted} of ${tables.length} tables`);
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to format tables: ${error.message}`);
    }
}

/**
 * Format the current selection as a markdown table
 */
export async function formatSelection(): Promise<void> {
    // Get the active text editor
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No active editor');
        return;
    }

    // Check if the document is markdown
    if (editor.document.languageId !== 'markdown') {
        vscode.window.showInformationMessage('This is not a markdown file');
        return;
    }

    // Check if there is a selection
    if (editor.selection.isEmpty) {
        vscode.window.showInformationMessage('No text selected');
        return;
    }

    // Get the selected text
    const selection = editor.selection;
    const text = editor.document.getText(selection);

    // Check if the selection looks like a table
    if (!text.includes('|')) {
        vscode.window.showInformationMessage('Selection does not appear to be a markdown table');
        return;
    }

    try {
        // Get formatting options (interactive prompt)
        const options = await getFormattingOptions();
        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        const enablePreview = config.get<boolean>('enablePreview', true);
        
        // Format the table
        const formattedTable = await getPythonBridge().formatTable(text, options);
        
        if (enablePreview) {
            const apply = await previewAndConfirm(text, formattedTable);
            if (!apply) {
                return;
            }
        }
        
        // Apply the edit
        await editor.edit(editBuilder => {
            editBuilder.replace(selection, formattedTable);
        });
        
        vscode.window.showInformationMessage('Table formatted successfully');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to format table: ${error.message}`);
    }
}

/**
 * Show a dropdown (QuickPick) for formatting options and execute the selected action.
 */
export async function showFormatOptionsDropdown(): Promise<void> {
    const options = [
        {
            label: 'Format Table at Cursor',
            description: 'Format the markdown table at the current cursor position',
            action: formatTableAtCursor
        },
        {
            label: 'Format All Tables in Document',
            description: 'Format all markdown tables in the current document',
            action: formatAllTables
        },
        {
            label: 'Format Selection as Table',
            description: 'Format the currently selected text as a markdown table',
            action: formatSelection
        }
    ];

    const picked = await vscode.window.showQuickPick(options, {
        placeHolder: 'Select a table formatting action',
        matchOnDescription: true
    });

    if (picked && picked.action) {
        await picked.action();
    }
}

/**
 * Get formatting options from VS Code settings
 */
async function getFormattingOptions(): Promise<any> {
    const options = await promptForFormattingOptions();
    if (options) {
        return options;
    }
    // Fallback to workspace settings if the user cancelled or prompt failed
    const config = vscode.workspace.getConfiguration('markdownTableFormatter');
    return {
        template: config.get<string>('defaultTemplate', 'github'),
        maxWidth: config.get<number>('maxTableWidth', 80),
        minPadding: config.get<number>('minPadding', 1),
        preserveCodeBlocks: config.get<boolean>('preserveCodeBlocks', true),
        wrapText: config.get<boolean>('wrapText', true)
    };
} 