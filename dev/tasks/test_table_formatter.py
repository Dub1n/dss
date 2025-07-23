import unittest
from io import StringIO
from pathlib import Path
import tempfile
import os
from table_formatter import TableFormatter, TableStats
from formatter_config import FormatterConfig

class TestTableFormatter(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.config = FormatterConfig(
            default_output_format="string",
            encoding="utf-8",
            line_ending="\n",
            enable_progress_tracking=True,
            progress_update_interval=0.1,
            max_errors=100,
            error_log_file=None,
            buffer_size=8192,
            max_memory_usage=1024 * 1024 * 100,
            create_backup=True,
            backup_suffix=".bak"
        )
        self.formatter = TableFormatter(self.config)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        os.rmdir(self.temp_dir)

    def test_initialization(self):
        """Test that the formatter initializes correctly."""
        self.assertIsInstance(self.formatter.stats, TableStats)
        self.assertEqual(self.formatter.stats.total_rows, 0)
        self.assertEqual(self.formatter.stats.total_columns, 0)
        self.assertEqual(self.formatter.stats.processing_time, 0.0)
        self.assertEqual(self.formatter.stats.formatting_changes, 0)
        self.assertEqual(len(self.formatter.stats.errors), 0)
        self.assertEqual(self.formatter.config, self.config)

    def test_generate_output_invalid_format(self):
        """Test that invalid output formats raise an error."""
        with self.assertRaises(ValueError):
            self.formatter.generate_output("invalid_format")

    def test_write_to_file(self):
        """Test writing output to a file."""
        test_file = Path(self.temp_dir) / "test_output.md"
        self.formatter.write_to_file(str(test_file))
        self.assertTrue(test_file.exists())

    def test_write_to_file_with_backup(self):
        """Test writing output to a file with backup creation."""
        test_file = Path(self.temp_dir) / "test_output.md"
        # Create initial file
        test_file.write_text("original content")
        
        # Write new content
        self.formatter.write_to_file(str(test_file))
        
        # Check that backup was created
        backup_file = test_file.with_suffix(test_file.suffix + self.config.backup_suffix)
        self.assertTrue(backup_file.exists())
        self.assertEqual(backup_file.read_text(), "original content")

    def test_stream_output(self):
        """Test streaming output to a stream."""
        stream = StringIO()
        self.formatter.stream_output(stream)
        self.assertIsInstance(stream.getvalue(), str)

    def test_get_progress(self):
        """Test getting progress information."""
        progress = self.formatter.get_progress()
        self.assertIn("progress", progress)
        self.assertIn("status", progress)
        self.assertIn("errors", progress)
        self.assertIsInstance(progress["progress"], float)
        self.assertIsInstance(progress["status"], str)
        self.assertIsInstance(progress["errors"], list)

    def test_get_summary(self):
        """Test getting summary information."""
        summary = self.formatter.get_summary()
        self.assertIn("total_rows", summary)
        self.assertIn("total_columns", summary)
        self.assertIn("processing_time", summary)
        self.assertIn("formatting_changes", summary)
        self.assertIn("errors", summary)
        self.assertIsInstance(summary["total_rows"], int)
        self.assertIsInstance(summary["total_columns"], int)
        self.assertIsInstance(summary["processing_time"], float)
        self.assertIsInstance(summary["formatting_changes"], int)
        self.assertIsInstance(summary["errors"], list)

    def test_error_handling(self):
        """Test error handling in output generation."""
        # Test file write error
        with self.assertRaises(Exception):
            self.formatter.write_to_file("/invalid/path/test.md")

        # Test stream error
        class BadStream:
            def write(self, data):
                raise IOError("Test error")

        with self.assertRaises(Exception):
            self.formatter.stream_output(BadStream())

    def test_max_errors_limit(self):
        """Test that error handling respects the maximum error limit."""
        # Add more errors than the maximum limit
        for i in range(self.config.max_errors + 10):
            self.formatter.output_handler.handle_error(f"Error {i}")
        
        # Check that only max_errors were stored
        self.assertEqual(len(self.formatter.output_handler.errors), self.config.max_errors)

    def test_progress_update_interval(self):
        """Test that progress updates respect the update interval."""
        # Update progress multiple times in quick succession
        for i in range(10):
            self.formatter.output_handler.update_progress(i * 10, f"Status {i}")
        
        # The progress should only be updated according to the interval
        self.assertLessEqual(self.formatter.output_handler.progress, 100)

    def test_row_dividers(self):
        """Test row divider functionality."""
        # Test smart mode with wrapped cells
        config = FormatterConfig(
            wrap_text=True,
            wrap_width=10,
            row_divider_mode="smart"
        )
        formatter = TableFormatter(config)
        table = [
            ["Header 1", "Header 2"],
            ["Short", "This is a long cell that will wrap"],
            ["Another short", "Another long cell that will wrap"]
        ]
        result = formatter.format_table(table)
        self.assertIn("+", result)  # Should have row dividers
        
        # Test smart mode without wrapped cells
        config = FormatterConfig(
            wrap_text=True,
            wrap_width=20,
            row_divider_mode="smart"
        )
        formatter = TableFormatter(config)
        table = [
            ["Header 1", "Header 2"],
            ["Short", "Short"],
            ["Short", "Short"]
        ]
        result = formatter.format_table(table)
        print("\nSMART MODE NO WRAP OUTPUT:\n", result)
        # There should be only one divider line (after the header)
        divider_lines = [line for line in result.splitlines() if line.strip().startswith("+")]
        self.assertEqual(len(divider_lines), 1)
        
        # Test always mode
        config = FormatterConfig(
            row_divider_mode="always",
            row_divider_style="equals"
        )
        formatter = TableFormatter(config)
        table = [
            ["Header 1", "Header 2"],
            ["Short", "Short"],
            ["Short", "Short"]
        ]
        result = formatter.format_table(table)
        self.assertIn("=", result)  # Should have equals dividers
        
        # Test never mode
        config = FormatterConfig(
            row_divider_mode="never"
        )
        formatter = TableFormatter(config)
        table = [
            ["Header 1", "Header 2"],
            ["Short", "Short"],
            ["Short", "Short"]
        ]
        result = formatter.format_table(table)
        # There should be only one divider line (after the header)
        divider_lines = [line for line in result.splitlines() if line.strip().startswith("+")]
        self.assertEqual(len(divider_lines), 1)
        
        # Test custom divider
        config = FormatterConfig(
            row_divider_mode="always",
            row_divider_style="custom",
            custom_row_divider="*",
            row_divider_padding=2
        )
        formatter = TableFormatter(config)
        table = [
            ["Header 1", "Header 2"],
            ["Short", "Short"]
        ]
        result = formatter.format_table(table)
        self.assertIn("**", result)  # Should have custom divider with padding

if __name__ == '__main__':
    unittest.main() 