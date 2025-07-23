import unittest
from table_formatter.core.table_parser import TableParser
from table_formatter.core.table_analyzer import TableAnalyzer
from table_formatter.core.table_formatter import TableFormatter

class TestTableFormatter(unittest.TestCase):
    def setUp(self):
        self.parser = TableParser()
        self.analyzer = TableAnalyzer()
        self.formatter = TableFormatter()

    def _format(self, markdown: str) -> str:
        parsed, diag = self.parser.parse_table(markdown.strip())
        analysis = self.analyzer.analyze_table(parsed, diag)
        return self.formatter.format_table(parsed, diag, analysis)

    def _normalize(self, markdown: str):
        parsed, _ = self.parser.parse_table(markdown)
        # strip spaces in cells
        return [[c.strip() for c in row] for row in parsed]

    def test_format_simple_table(self):
        input_table = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""
        formatted = self._format(input_table)
        expected_cells = self._normalize(input_table.strip())
        result_cells = self._normalize(formatted)
        self.assertEqual(result_cells, expected_cells)

    def test_format_uneven_table(self):
        input_table = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   | Cell 5 |
"""
        formatted = self._format(input_table)
        expected_cells = self._normalize(input_table.strip())
        result_cells = self._normalize(formatted)
        self.assertEqual(result_cells, expected_cells)

    def test_validate_valid_table(self):
        input_table = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
        parsed, diag = self.parser.parse_table(input_table.strip())
        self.assertTrue(diag.is_valid)

    def test_code_block_preservation(self):
        input_table = """
| Header | Code |
|--------|------|
| Row 1  | `print('hi')` |
"""
        formatted = self._format(input_table)
        self.assertIn("`print('hi')`", formatted)

    def test_header_divider_matches_column_width(self):
        input_table = """
| H1      | H2 |
|---------|----|
| a       | b  |
| longer1 | c  |
"""
        parsed, diag = self.parser.parse_table(input_table.strip())
        analysis = self.analyzer.analyze_table(parsed, diag)
        self.formatter.format_table(parsed, diag, analysis)
        lines = self.formatter.format_table(parsed, diag, analysis).strip().split('\n')
        separator = lines[1]
        sep_cells = [cell for cell in separator.split('|')[1:-1]]
        for fmt, s in zip(self.formatter.column_formats, sep_cells):
            self.assertEqual(len(s), fmt.width, f"Separator '{s}' should be width {fmt.width} (got {len(s)})")

if __name__ == '__main__':
    unittest.main() 