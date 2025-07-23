import * as vscode from 'vscode';

/**
 * Initialize the status bar item for the extension
 * @param context The extension context
 * @returns The status bar item
 */
export function initializeStatusBar(context: vscode.ExtensionContext): vscode.StatusBarItem {
    // Create status bar item
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = '$(table) Table';
    statusBar.tooltip = 'Markdown Table Formatter';
    statusBar.command = 'markdownTableFormatter.formatTable';
    
    // Show the status bar item only for markdown files
    const documentChangeSubscription = vscode.window.onDidChangeActiveTextEditor(updateStatusBarVisibility);
    context.subscriptions.push(documentChangeSubscription);
    
    // Initial update
    updateStatusBarVisibility(vscode.window.activeTextEditor);
    
    return statusBar;
}

/**
 * Update the visibility of the status bar item based on the active editor
 * @param editor The active text editor
 */
function updateStatusBarVisibility(editor: vscode.TextEditor | undefined): void {
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    
    if (editor && editor.document.languageId === 'markdown') {
        statusBar.show();
    } else {
        statusBar.hide();
    }
}

/**
 * Show a progress indicator in the status bar
 * @param message The message to display
 * @returns A function to clear the progress indicator
 */
export function showProgress(message: string): () => void {
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = `$(sync~spin) ${message}`;
    statusBar.show();
    
    return () => {
        statusBar.dispose();
    };
}

/**
 * Show a temporary message in the status bar
 * @param message The message to display
 * @param timeout The timeout in milliseconds
 */
export function showTemporaryMessage(message: string, timeout = 3000): void {
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = message;
    statusBar.show();
    
    setTimeout(() => {
        statusBar.dispose();
    }, timeout);
} 