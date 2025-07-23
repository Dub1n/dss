import * as assert from 'assert';
import { TableDetection } from '../tableDetection';

suite('Table Detection Test Suite', () => {
    test('Detect simple table', () => {
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

    test('Detect multiple tables', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

| Header 3 | Header 4 |
|----------|----------|
| Cell 3   | Cell 4   |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 2);
        assert.strictEqual(tables[0].text, text.split('\n\n')[0].trim());
        assert.strictEqual(tables[1].text, text.split('\n\n')[1].trim());
    });

    test('Detect invalid table', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
| Cell 1   | Cell 2   |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 0);
    });

    test('Detect table with inconsistent columns', () => {
        const detector = new TableDetection();
        const text = `
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   | Cell 3 |
`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.strictEqual(tables[0].isValid(), false);
    });

    test('Detect table without trailing pipes', () => {
        const detector = new TableDetection();
        const text = `Header 1 | Header 2\n--- | ---\nCell 1 | Cell 2`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.ok(tables[0].isValid());
    });

    test('Detect table without leading pipes', () => {
        const detector = new TableDetection();
        const text = `Header 1 | Header 2 | Header 3\n--- | --- | ---\nC1 | C2 | C3`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
    });
});

suite('Indent-aware Table Detection', () => {
    test('Detect table nested inside unordered list', () => {
        const detector = new TableDetection();
        const text = `- List item with table\n  | H1 | H2 |\n  | --- | --- |\n  | C1 | C2 |`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.ok(tables[0].isValid());
    });
    
    test('Detect table nested inside blockquote', () => {
        const detector = new TableDetection();
        const text = `> | H1 | H2 |\n> | --- | --- |\n> | C1 | C2 |`;
        const tables = detector.detectTables(text);
        assert.strictEqual(tables.length, 1);
        assert.ok(tables[0].isValid());
    });
}); 