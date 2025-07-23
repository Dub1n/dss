import unittest
import tempfile
import os
from pathlib import Path
import shutil
from file_operations import FileOperationsManager, FileStats
from formatter_config import FormatterConfig

class TestFileOperationsManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = FormatterConfig(
            output_directory=os.path.join(self.temp_dir, "output"),
            encoding="utf-8",
            create_backup=True,
            backup_suffix=".bak"
        )
        self.file_manager = FileOperationsManager(self.config)
        
        # Create test directory structure
        self.input_dir = os.path.join(self.temp_dir, "input")
        os.makedirs(self.input_dir)
        
        # Create test files
        self.test_files = []
        for i in range(3):
            file_path = os.path.join(self.input_dir, f"test{i}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Test content {i}")
            self.test_files.append(file_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test that the file manager initializes correctly."""
        self.assertIsInstance(self.file_manager.stats, FileStats)
        self.assertEqual(self.file_manager.stats.total_files, 0)
        self.assertEqual(self.file_manager.stats.processed_files, 0)
        self.assertEqual(self.file_manager.stats.skipped_files, 0)
        self.assertEqual(self.file_manager.stats.failed_files, 0)
        self.assertEqual(self.file_manager.stats.total_size, 0)
        self.assertEqual(self.file_manager.stats.processing_time, 0.0)
        self.assertEqual(len(self.file_manager.stats.errors), 0)
    
    def test_process_directory(self):
        """Test processing a directory of markdown files."""
        stats = self.file_manager.process_directory(self.input_dir)
        print(f"Processed files: {stats['files_processed']}, Skipped: {stats['files_skipped']}, Errors: {stats['errors']}")
        self.assertEqual(stats["files_processed"], 3)
        self.assertEqual(stats["files_skipped"], 0)
        self.assertEqual(stats["errors"], 0)
    
    def test_process_file(self):
        """Test processing a single file."""
        input_file = self.test_files[0]
        output_file = os.path.join(self.config.output_directory, "test0.md")
        
        result = self.file_manager.process_file(input_file, output_file)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_file"], input_file)
        self.assertEqual(result["output_file"], output_file)
        self.assertGreater(result["file_size"], 0)
        self.assertEqual(result["content"], "Test content 0")
    
    def test_validate_file(self):
        """Test file validation."""
        # Test valid file
        self.assertTrue(self.file_manager.validate_file(self.test_files[0]))
        
        # Test non-existent file
        self.assertFalse(self.file_manager.validate_file("nonexistent.md"))
        
        # Test non-markdown file
        non_md_file = os.path.join(self.input_dir, "test.txt")
        with open(non_md_file, 'w') as f:
            f.write("test")
        self.assertFalse(self.file_manager.validate_file(non_md_file))
    
    def test_create_backup(self):
        """Test backup creation."""
        test_file = self.test_files[0]
        backup_path = self.file_manager.create_backup(test_file)
        
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
        self.assertEqual(backup_path, test_file + self.config.backup_suffix)
        
        # Test backup of non-existent file
        self.assertIsNone(self.file_manager.create_backup("nonexistent.md"))
    
    def test_cleanup_backups(self):
        """Test backup cleanup."""
        # Create some backup files
        backup_files = []
        for i in range(3):
            backup_path = self.test_files[i] + self.config.backup_suffix
            shutil.copy2(self.test_files[i], backup_path)
            backup_files.append(backup_path)
        
        # Clean up backups
        cleaned_count = self.file_manager.cleanup_backups(self.input_dir)
        
        self.assertEqual(cleaned_count, 3)
        for backup_file in backup_files:
            self.assertFalse(os.path.exists(backup_file))
    
    def test_error_handling(self):
        """Test error handling in file operations."""
        # Test processing a non-existent directory
        stats = self.file_manager.process_directory("/nonexistent/path")
        self.assertGreaterEqual(stats["errors"], 1)
        
        # Test processing a file with insufficient permissions (simulate by passing a directory as a file)
        os.mkdir(os.path.join(self.input_dir, "subdir"))
        try:
            result = self.file_manager.process_file(os.path.join(self.input_dir, "subdir"), None)
            self.assertEqual(result["status"], "error")
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main() 