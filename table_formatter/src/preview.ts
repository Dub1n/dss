/* eslint-disable @typescript-eslint/no-inferrable-types */
import * as vscode from 'vscode';

/**
 * Show a preview of the formatted text in a temporary editor and ask the user to confirm applying the change.
 * If the user chooses Apply, returns true; otherwise false.
 */
export async function previewAndConfirm(_originalText: string, formattedText: string, language: string = 'markdown'): Promise<boolean> {
    const config = vscode.workspace.getConfiguration('markdownTableFormatter');
    const previewMode = config.get<string>('previewMode', 'diff');

    let choice: string | undefined;

    if (previewMode === 'webview') {
        await showWebviewPreview(_originalText, formattedText);
        choice = await vscode.window.showInformationMessage('Apply formatted changes?', { modal: true }, 'Apply', 'Cancel');
    } else if (previewMode === 'diff') {
        // Create two untitled documents for diff view
        const originalDoc = await vscode.workspace.openTextDocument({ language, content: _originalText });
        const formattedDoc = await vscode.workspace.openTextDocument({ language, content: formattedText });

        // Show diff editor
        await vscode.commands.executeCommand(
            'vscode.diff',
            originalDoc.uri,
            formattedDoc.uri,
            'Table Format Preview'
        );

        choice = await vscode.window.showInformationMessage('Preview: Apply formatted changes?', { modal: true }, 'Apply', 'Cancel');

        // Close the diff editors
        await vscode.commands.executeCommand('workbench.action.closeAllEditors');
    } else {
        // Fallback to side-by-side static preview
        const formattedDoc = await vscode.workspace.openTextDocument({ language, content: formattedText });
        await vscode.window.showTextDocument(formattedDoc, { preview: true, viewColumn: vscode.ViewColumn.Beside });

        choice = await vscode.window.showInformationMessage('Preview: Apply formatted changes?', { modal: true }, 'Apply', 'Cancel');

        // Close the preview editor
        await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    }

    return choice === 'Apply';
}

async function showWebviewPreview(original: string, formatted: string): Promise<void> {
    const panel = vscode.window.createWebviewPanel(
        'tablePreview',
        'Table Format Preview',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    const style = `<style>
        body { font-family: var(--vscode-editor-font-family, monospace); padding: 1rem; }
        textarea { width: 45%; height: 80vh; white-space: pre; font-family: inherit; }
        #container { display: flex; gap: 1rem; }
        h2 { margin: 0.5rem 0; }
    </style>`;

    panel.webview.html = `${style}
    <h2>Original vs Formatted</h2>
    <div id="container">
        <textarea readonly>${original.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</textarea>
        <textarea readonly>${formatted.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</textarea>
    </div>`;

    // Focus webview until user closes or switches.
    await new Promise<void>(resolve => {
        const listener = panel.onDidDispose(() => {
            listener.dispose();
            resolve();
        });
    });
} 