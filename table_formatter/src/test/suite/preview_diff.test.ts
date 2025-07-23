import * as assert from 'assert';
import * as vscode from 'vscode';
import { previewAndConfirm } from '../../preview';

suite('Diff Preview Tests', () => {
    test('Uses diff editor when previewMode is diff', async () => {
        const originalGetConfig = vscode.workspace.getConfiguration;
        (vscode.workspace as any).getConfiguration = () => {
            return {
                get: (key: string, def: any) => {
                    if (key === 'previewMode') return 'diff';
                    if (key === 'enablePreview') return true;
                    return def;
                }
            };
        };

        let diffCalled = false;
        const originalDiff = vscode.commands.executeCommand;
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        (vscode.commands as any).executeCommand = async (cmd: string, ..._args: any[]) => {
            if (cmd === 'vscode.diff') diffCalled = true;
            return undefined;
        };

        // Stub modal
        const originalShowInfo = vscode.window.showInformationMessage;
        (vscode.window as any).showInformationMessage = async () => 'Apply';

        try {
            const result = await previewAndConfirm('| a |', '| b |');
            assert.ok(diffCalled, 'Expected vscode.diff to be invoked');
            assert.strictEqual(result, true);
        } finally {
            (vscode.workspace as any).getConfiguration = originalGetConfig;
            (vscode.commands as any).executeCommand = originalDiff;
            (vscode.window as any).showInformationMessage = originalShowInfo;
        }
    });
}); 