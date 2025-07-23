import * as vscode from 'vscode';
import { formatTableAtCursor, formatAllTables, formatSelection, showFormatOptionsDropdown } from './commands';
import { initializeStatusBar } from './statusBar';

/**
 * This method is called when the extension is activated.
 * The extension is activated the first time the command is executed.
 */
export function activate(context: vscode.ExtensionContext) {
    // Log activation
    console.log('Markdown Table Formatter is now active');

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

    // Register the dropdown command for context menu
    const formatDropdownCmd = vscode.commands.registerCommand(
        'markdownTableFormatter.formatDropdown',
        showFormatOptionsDropdown
    );

    // Initialize the status bar
    const statusBar = initializeStatusBar(context);

    // ────────────────────────────────────────────────────────────
    // First-run onboarding toast (shown once per machine)
    // ────────────────────────────────────────────────────────────
    const firstRunKey = 'markdownTableFormatter.welcomeShown';
    if (!context.globalState.get<boolean>(firstRunKey, false)) {
        vscode.window.showInformationMessage(
            'Markdown Table Formatter installed!  Right-click → “Table Formatting Options…” or press Ctrl+Alt+T to format tables.',
            'Open README'
        ).then(selection => {
            if (selection === 'Open README') {
                const ext = vscode.extensions.getExtension('dss-tools.markdown-table-formatter');
                if (ext) {
                    const readme = vscode.Uri.joinPath(ext.extensionUri, 'README.md');
                    vscode.commands.executeCommand('markdown.showPreview', readme);
                }
            }
        });
        void context.globalState.update(firstRunKey, true);
    }

    // Register save event listener for format-on-save
    const onSaveDisposable = vscode.workspace.onWillSaveTextDocument(event => {
        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        const formatOnSave = config.get<boolean>('formatOnSave', false);

        if (formatOnSave && event.document.languageId === 'markdown') {
            formatAllTables();
        }
    });

    // Add all disposables to the context
    context.subscriptions.push(
        formatTableCmd,
        formatAllTablesCmd,
        formatSelectionCmd,
        formatDropdownCmd,
        statusBar,
        onSaveDisposable
    );
}

/**
 * This method is called when the extension is deactivated
 */
export function deactivate() {
    // Clean up resources
    console.log('Markdown Table Formatter is now deactivated');
} 