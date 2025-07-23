from typing import List, Generator, Optional, Dict, Any
from pathlib import Path
import os
import shutil
import logging
from dataclasses import dataclass
import time
from formatter_config import FormatterConfig

logger = logging.getLogger(__name__)

@dataclass
class FileStats:
    """Statistics about file operations."""
    total_files: int
    processed_files: int
    skipped_files: int
    failed_files: int
    total_size: int
    processing_time: float
    errors: List[str]

class FileOperationsManager:
    """Manages file system operations for the table formatter."""
    
    def __init__(self, config: FormatterConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.stats = FileStats(0, 0, 0, 0, 0, 0.0, [])
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate the file operations configuration."""
        if not os.path.exists(self.config.output_directory):
            os.makedirs(self.config.output_directory)
    
    def process_directory(self, directory: str) -> Dict[str, Any]:
        """Process all markdown files in a directory."""
        start_time = time.time()
        stats = {
            "files_processed": 0,
            "files_skipped": 0,
            "errors": 0,
            "processing_time": 0.0
        }
        
        if not os.path.isdir(directory):
            stats["errors"] += 1
            stats["processing_time"] = time.time() - start_time
            return stats
        
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if self._should_process_file(file):
                        file_path = os.path.join(root, file)
                        # Compute output file path
                        rel_path = os.path.relpath(file_path, directory)
                        output_file = os.path.join(self.config.output_directory, rel_path)
                        os.makedirs(os.path.dirname(output_file), exist_ok=True)
                        try:
                            self.process_file(file_path, output_file)
                            stats["files_processed"] += 1
                        except Exception as e:
                            stats["errors"] += 1
                            self.logger.error(f"Error processing {file_path}: {str(e)}")
                    else:
                        stats["files_skipped"] += 1
        except Exception as e:
            self.logger.error(f"Error processing directory {directory}: {str(e)}")
            raise
        
        stats["processing_time"] = time.time() - start_time
        return stats
    
    def process_file(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Process a single markdown file."""
        input_path = Path(input_file)
        output_path = Path(output_file)
        
        # Validate input file
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Create backup if enabled
        if self.config.create_backup and output_path.exists():
            backup_path = output_path.with_suffix(output_path.suffix + self.config.backup_suffix)
            shutil.copy2(output_path, backup_path)
        
        # Read file content
        with input_path.open('r', encoding=self.config.encoding) as f:
            content = f.read()
        
        # Get file stats
        file_size = input_path.stat().st_size
        
        return {
            "status": "success",
            "input_file": str(input_path),
            "output_file": str(output_path),
            "file_size": file_size,
            "content": content
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get file operation statistics."""
        return {
            "total_files": self.stats.total_files,
            "processed_files": self.stats.processed_files,
            "skipped_files": self.stats.skipped_files,
            "failed_files": self.stats.failed_files,
            "total_size": self.stats.total_size,
            "processing_time": self.stats.processing_time,
            "errors": self.stats.errors
        }
    
    def validate_file(self, file_path: str) -> bool:
        """Validate a file for processing."""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            if not path.is_file():
                return False
            if path.suffix.lower() != '.md':
                return False
            if not os.access(file_path, os.R_OK):
                return False
            return True
        except Exception:
            return False
    
    def create_backup(self, file_path: str) -> Optional[str]:
        """Create a backup of a file."""
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            backup_path = path.with_suffix(path.suffix + self.config.backup_suffix)
            shutil.copy2(path, backup_path)
            return str(backup_path)
        except Exception as e:
            logger.error(f"Failed to create backup of {file_path}: {str(e)}")
            return None
    
    def cleanup_backups(self, directory: str) -> int:
        """Clean up backup files in a directory."""
        try:
            backup_count = 0
            for backup_file in Path(directory).rglob(f"*{self.config.backup_suffix}"):
                backup_file.unlink()
                backup_count += 1
            return backup_count
        except Exception as e:
            logger.error(f"Failed to cleanup backups in {directory}: {str(e)}")
            return 0
    
    def _should_process_file(self, filename: str) -> bool:
        """Determine if a file should be processed based on patterns and config."""
        import fnmatch
        if self.config.skip_hidden_files and filename.startswith('.'):
            return False
        for pattern in self.config.file_patterns:
            if fnmatch.fnmatch(filename, pattern):
                for exclude in self.config.exclude_patterns:
                    if fnmatch.fnmatch(filename, exclude):
                        return False
                return True
        return False 