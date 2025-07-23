import * as assert from 'assert';
import * as vscode from 'vscode';
import { previewAndConfirm } from '../../preview';

suite('Webview Preview Tests', () => {
    test('Creates webview panel when previewMode is webview', async () => {
        // Stub configuration to force webview mode
        const originalGetConfig = vscode.workspace.getConfiguration;
        (vscode.workspace as any).getConfiguration = () => {
            return {
                get: (key: string, def: any) => {
                    if (key === 'previewMode') return 'webview';
                    if (key === 'enablePreview') return true;
                    return def;
                }
            };
        };

        let panelCreated = false;
        const originalCreatePanel = vscode.window.createWebviewPanel;
        (vscode.window as any).createWebviewPanel = (
            _viewType: string,
            _title: string,
            _showColumn: vscode.ViewColumn,
            _options: vscode.WebviewPanelOptions
        ) => {
            panelCreated = true;
            let disposeCallback: () => void;
            return {
                webview: { html: '' } as any,
                onDidDispose: (cb: () => void) => {
                    disposeCallback = cb;
                    // Immediately dispose so the preview promise resolves
                    setTimeout(() => disposeCallback(), 0);
                    // eslint-disable-next-line @typescript-eslint/no-empty-function
                    return { dispose: () => {} } as any;
                }
            } as unknown as vscode.WebviewPanel;
        };

        // Stub showInformationMessage to auto-apply
        const originalShowInfo = vscode.window.showInformationMessage;
        (vscode.window as any).showInformationMessage = async () => 'Apply';

        try {
            const result = await previewAndConfirm('a | b', 'a | b');
            assert.ok(panelCreated, 'Expected createWebviewPanel to be called');
            assert.strictEqual(result, true, 'Expected Apply to be returned');
        } finally {
            // Restore stubs
            (vscode.workspace as any).getConfiguration = originalGetConfig;
            (vscode.window as any).createWebviewPanel = originalCreatePanel;
            (vscode.window as any).showInformationMessage = originalShowInfo;
        }
    });
}); 