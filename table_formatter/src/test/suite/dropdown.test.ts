import * as assert from 'assert';
import * as vscode from 'vscode';
import { showFormatOptionsDropdown } from '../../commands';

suite('Dropdown QuickPick Tests', () => {
    test('Selected action is executed', async () => {
        let executed = false;

        // Fake action we expect to be called
        const fakeAction = async () => { executed = true; };

        // Stub showQuickPick
        const original = vscode.window.showQuickPick;
        (vscode.window as any).showQuickPick = async () => {
            return { label: 'stub', description: '', action: fakeAction } as any;
        };

        try {
            await showFormatOptionsDropdown();
            assert.ok(executed, 'The selected QuickPick action should have been executed');
        } finally {
            // Restore original implementation to avoid side-effects on other tests
            (vscode.window as any).showQuickPick = original;
        }
    });
}); 