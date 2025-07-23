import unittest
import tempfile
import os
from pathlib import Path
from formatter_config import FormatterConfig, get_default_config

class TestFormatterConfig(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = FormatterConfig()
    
    def tearDown(self):
        """Clean up test fixtures."""
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration values."""
        self.assertEqual(self.config.default_output_format, "string")
        self.assertEqual(self.config.encoding, "utf-8")
        self.assertEqual(self.config.line_ending, "\n")
        self.assertTrue(self.config.enable_progress_tracking)
        self.assertEqual(self.config.progress_update_interval, 0.1)
        self.assertEqual(self.config.max_errors, 100)
        self.assertIsNone(self.config.error_log_file)
        self.assertEqual(self.config.buffer_size, 8192)
        self.assertEqual(self.config.max_memory_usage, 1024 * 1024 * 100)
        self.assertTrue(self.config.create_backup)
        self.assertEqual(self.config.backup_suffix, ".bak")
        self.assertEqual(self.config.output_directory, "output")
        self.assertTrue(self.config.preserve_directory_structure)
        self.assertTrue(self.config.skip_hidden_files)
        self.assertEqual(self.config.max_file_size, 1024 * 1024 * 10)
        self.assertEqual(self.config.file_patterns, ["*.md"])
        self.assertEqual(self.config.exclude_patterns, [])
    
    def test_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "default_output_format": "string",
            "encoding": "utf-8",
            "line_ending": "\n",
            "enable_progress_tracking": True,
            "progress_update_interval": 0.2,
            "max_errors": 10,
            "error_log_file": None,
            "buffer_size": 4096,
            "max_memory_usage": 1024 * 1024 * 10,
            "create_backup": False,
            "backup_suffix": ".backup",
            "output_directory": "out",
            "preserve_directory_structure": False,
            "skip_hidden_files": False,
            "max_file_size": 1024 * 1024,
            "file_patterns": ["*.md"],
            "exclude_patterns": ["*.tmp"],
            "wrap_text": True,
            "wrap_width": 40,
            "row_divider_mode": "always",
            "row_divider_style": "equals",
            "custom_row_divider": "*",
            "row_divider_padding": 2
        }
        config = FormatterConfig.from_dict(config_dict)
        self.assertEqual(config.default_output_format, "string")
        self.assertEqual(config.encoding, "utf-8")
        self.assertEqual(config.line_ending, "\n")
        self.assertTrue(config.enable_progress_tracking)
        self.assertEqual(config.progress_update_interval, 0.2)
        self.assertEqual(config.max_errors, 10)
        self.assertIsNone(config.error_log_file)
        self.assertEqual(config.buffer_size, 4096)
        self.assertEqual(config.max_memory_usage, 1024 * 1024 * 10)
        self.assertFalse(config.create_backup)
        self.assertEqual(config.backup_suffix, ".backup")
        self.assertEqual(config.output_directory, "out")
        self.assertFalse(config.preserve_directory_structure)
        self.assertFalse(config.skip_hidden_files)
        self.assertEqual(config.max_file_size, 1024 * 1024)
        self.assertEqual(config.file_patterns, ["*.md"])
        self.assertEqual(config.exclude_patterns, ["*.tmp"])
        self.assertTrue(config.wrap_text)
        self.assertEqual(config.wrap_width, 40)
        self.assertEqual(config.row_divider_mode, "always")
        self.assertEqual(config.row_divider_style, "equals")
        self.assertEqual(config.custom_row_divider, "*")
        self.assertEqual(config.row_divider_padding, 2)
    
    def test_to_dict(self):
        """Test converting config to dictionary."""
        config_dict = self.config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["default_output_format"], "string")
        self.assertEqual(config_dict["encoding"], "utf-8")
        self.assertEqual(config_dict["line_ending"], "\n")
        self.assertTrue(config_dict["enable_progress_tracking"])
        self.assertEqual(config_dict["progress_update_interval"], 0.1)
        self.assertEqual(config_dict["max_errors"], 100)
        self.assertIsNone(config_dict["error_log_file"])
        self.assertEqual(config_dict["buffer_size"], 8192)
        self.assertEqual(config_dict["max_memory_usage"], 1024 * 1024 * 100)
        self.assertTrue(config_dict["create_backup"])
        self.assertEqual(config_dict["backup_suffix"], ".bak")
        self.assertEqual(config_dict["output_directory"], "output")
        self.assertTrue(config_dict["preserve_directory_structure"])
        self.assertTrue(config_dict["skip_hidden_files"])
        self.assertEqual(config_dict["max_file_size"], 1024 * 1024 * 10)
        self.assertEqual(config_dict["file_patterns"], ["*.md"])
        self.assertEqual(config_dict["exclude_patterns"], [])
    
    def test_save_and_load(self):
        """Test saving and loading configuration."""
        config_file = Path(self.temp_dir) / "config.json"
        self.config.save(str(config_file))
        self.assertTrue(config_file.exists())
        
        loaded_config = FormatterConfig.load(str(config_file))
        self.assertEqual(loaded_config.default_output_format, self.config.default_output_format)
        self.assertEqual(loaded_config.encoding, self.config.encoding)
        self.assertEqual(loaded_config.line_ending, self.config.line_ending)
        self.assertEqual(loaded_config.enable_progress_tracking, self.config.enable_progress_tracking)
        self.assertEqual(loaded_config.progress_update_interval, self.config.progress_update_interval)
        self.assertEqual(loaded_config.max_errors, self.config.max_errors)
        self.assertEqual(loaded_config.error_log_file, self.config.error_log_file)
        self.assertEqual(loaded_config.buffer_size, self.config.buffer_size)
        self.assertEqual(loaded_config.max_memory_usage, self.config.max_memory_usage)
        self.assertEqual(loaded_config.create_backup, self.config.create_backup)
        self.assertEqual(loaded_config.backup_suffix, self.config.backup_suffix)
        self.assertEqual(loaded_config.output_directory, self.config.output_directory)
        self.assertEqual(loaded_config.preserve_directory_structure, self.config.preserve_directory_structure)
        self.assertEqual(loaded_config.skip_hidden_files, self.config.skip_hidden_files)
        self.assertEqual(loaded_config.max_file_size, self.config.max_file_size)
        self.assertEqual(loaded_config.file_patterns, self.config.file_patterns)
        self.assertEqual(loaded_config.exclude_patterns, self.config.exclude_patterns)
    
    def test_validation(self):
        """Test configuration validation."""
        # Test invalid output format
        with self.assertRaises(ValueError):
            FormatterConfig(default_output_format="invalid")
        
        # Test invalid encoding
        with self.assertRaises(ValueError):
            FormatterConfig(encoding="invalid")
        
        # Test invalid line ending
        with self.assertRaises(ValueError):
            FormatterConfig(line_ending="invalid")
        
        # Test invalid progress interval
        with self.assertRaises(ValueError):
            FormatterConfig(progress_update_interval=0)
        
        # Test invalid max errors
        with self.assertRaises(ValueError):
            FormatterConfig(max_errors=-1)
        
        # Test invalid buffer size
        with self.assertRaises(ValueError):
            FormatterConfig(buffer_size=0)
        
        # Test invalid max memory usage
        with self.assertRaises(ValueError):
            FormatterConfig(max_memory_usage=0)
        
        # Test invalid max file size
        with self.assertRaises(ValueError):
            FormatterConfig(max_file_size=0)
        
        # Test invalid row divider mode
        with self.assertRaises(ValueError):
            FormatterConfig(row_divider_mode="invalid")
        
        # Test invalid row divider style
        with self.assertRaises(ValueError):
            FormatterConfig(row_divider_style="invalid")
        
        # Test invalid row divider padding
        with self.assertRaises(ValueError):
            FormatterConfig(row_divider_padding=-1)
        
        # Test invalid wrap width
        with self.assertRaises(ValueError):
            FormatterConfig(wrap_width=0)
        
        # Test invalid file patterns
        with self.assertRaises(ValueError):
            FormatterConfig(file_patterns="*.md")
        
        # Test invalid exclude patterns
        with self.assertRaises(ValueError):
            FormatterConfig(exclude_patterns="*.tmp")
        
        # Test valid row divider settings
        config = FormatterConfig(
            row_divider_mode="always",
            row_divider_style="equals",
            custom_row_divider="*",
            row_divider_padding=2
        )
        self.assertEqual(config.row_divider_mode, "always")
        self.assertEqual(config.row_divider_style, "equals")
        self.assertEqual(config.custom_row_divider, "*")
        self.assertEqual(config.row_divider_padding, 2)
    
    def test_get_default_config(self):
        """Test getting default configuration."""
        default_config = get_default_config()
        self.assertIsInstance(default_config, FormatterConfig)
        self.assertEqual(default_config.default_output_format, "string")
        self.assertEqual(default_config.encoding, "utf-8")

if __name__ == '__main__':
    unittest.main() 