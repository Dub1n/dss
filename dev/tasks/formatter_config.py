from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class FormatterConfig:
    """Configuration settings for the table formatter."""
    # Output settings
    default_output_format: str = "string"
    encoding: str = "utf-8"
    line_ending: str = "\n"
    
    # Progress tracking
    enable_progress_tracking: bool = True
    progress_update_interval: float = 0.1  # seconds
    
    # Error handling
    max_errors: int = 100
    error_log_file: Optional[str] = None
    
    # Performance settings
    buffer_size: int = 8192
    max_memory_usage: int = 1024 * 1024 * 100  # 100MB
    
    # File operations
    create_backup: bool = True
    backup_suffix: str = ".bak"
    output_directory: str = "output"
    preserve_directory_structure: bool = True
    skip_hidden_files: bool = True
    max_file_size: int = 1024 * 1024 * 10  # 10MB
    file_patterns: List[str] = None
    exclude_patterns: List[str] = None
    
    # Text wrapping settings
    wrap_text: bool = False
    wrap_width: int = 80
    
    # Row divider settings
    row_divider_mode: str = "smart"  # Options: "smart", "always", "never"
    row_divider_style: str = "dash"  # Options: "dash", "equals", "custom"
    custom_row_divider: str = "-"  # Used when row_divider_style is "custom"
    row_divider_padding: int = 1  # Number of spaces around row divider
    
    def __post_init__(self):
        """Initialize default values for lists and validate settings."""
        if self.file_patterns is None:
            self.file_patterns = ["*.md"]
        if self.exclude_patterns is None:
            self.exclude_patterns = []
        
        # Validate text wrapping settings
        if self.wrap_width < 1:
            raise ValueError("Wrap width must be positive")
        
        # Validate row divider settings
        if self.row_divider_mode not in ["smart", "always", "never"]:
            raise ValueError(f"Invalid row divider mode: {self.row_divider_mode}")
        if self.row_divider_style not in ["dash", "equals", "custom"]:
            raise ValueError(f"Invalid row divider style: {self.row_divider_style}")
        if self.row_divider_padding < 0:
            raise ValueError("Row divider padding must be non-negative")
        
        # Validate output settings
        if self.default_output_format not in ["string", "stream"]:
            raise ValueError(f"Invalid output format: {self.default_output_format}")
        if self.encoding not in ["utf-8", "ascii", "latin-1"]:
            raise ValueError(f"Invalid encoding: {self.encoding}")
        if self.line_ending not in ["\n", "\r\n", "\r"]:
            raise ValueError(f"Invalid line ending: {self.line_ending}")
        
        # Validate progress tracking settings
        if self.progress_update_interval <= 0:
            raise ValueError("Progress update interval must be positive")
        
        # Validate error handling settings
        if self.max_errors < 0:
            raise ValueError("Max errors must be non-negative")
        
        # Validate performance settings
        if self.buffer_size < 1:
            raise ValueError("Buffer size must be positive")
        if self.max_memory_usage < 1:
            raise ValueError("Max memory usage must be positive")
        
        # Validate file operation settings
        if self.max_file_size < 1:
            raise ValueError("Max file size must be positive")
        if not isinstance(self.file_patterns, list):
            raise ValueError("File patterns must be a list")
        if not isinstance(self.exclude_patterns, list):
            raise ValueError("Exclude patterns must be a list")
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'FormatterConfig':
        """Create a FormatterConfig instance from a dictionary."""
        return cls(**{
            k: v for k, v in config_dict.items()
            if k in cls.__dataclass_fields__
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return {
            field: getattr(self, field)
            for field in self.__dataclass_fields__
        }
    
    def save(self, file_path: str) -> None:
        """Save the configuration to a file."""
        try:
            path = Path(file_path)
            with path.open('w', encoding=self.encoding) as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Configuration saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            raise
    
    @classmethod
    def load(cls, file_path: str) -> 'FormatterConfig':
        """Load configuration from a file."""
        try:
            path = Path(file_path)
            with path.open('r', encoding='utf-8') as f:
                config_dict = json.load(f)
            logger.info(f"Configuration loaded from {file_path}")
            return cls.from_dict(config_dict)
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def validate(self) -> None:
        """Validate the configuration settings."""
        if self.default_output_format not in ["string", "file", "stream"]:
            raise ValueError(f"Invalid output format: {self.default_output_format}")
        
        if self.progress_update_interval <= 0:
            raise ValueError("Progress update interval must be positive")
        
        if self.max_errors < 0:
            raise ValueError("Maximum errors must be non-negative")
        
        if self.buffer_size <= 0:
            raise ValueError("Buffer size must be positive")
        
        if self.max_memory_usage <= 0:
            raise ValueError("Maximum memory usage must be positive")
        
        if self.max_file_size <= 0:
            raise ValueError("Maximum file size must be positive")
        
        if not isinstance(self.file_patterns, list):
            raise ValueError("File patterns must be a list")
        
        if not isinstance(self.exclude_patterns, list):
            raise ValueError("Exclude patterns must be a list")

# Default configuration
DEFAULT_CONFIG = FormatterConfig()

def get_default_config() -> FormatterConfig:
    """Get the default configuration."""
    return DEFAULT_CONFIG 