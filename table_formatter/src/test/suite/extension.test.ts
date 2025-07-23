import * as assert from 'assert';
import * as vscode from 'vscode';
import { TableDetection } from '../../tableDetection';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Table Detection', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.strictEqual(tables[0].text, text.trim());
    });

    test('Table Validation', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.strictEqual(tables[0].isValid(), true);
    });

    test('Invalid Table Detection', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
| Cell 1   | Cell 2   |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 0);
    });
}); 