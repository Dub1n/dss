from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import json
from pathlib import Path
import logging
import time
from formatter_config import FormatterConfig, get_default_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='table_formatter.log'
)
logger = logging.getLogger(__name__)

@dataclass
class TableStats:
    """Statistics about the table processing."""
    total_rows: int
    total_columns: int
    processing_time: float
    formatting_changes: int
    errors: List[str]

class OutputHandler:
    """Base class for output handlers."""
    def __init__(self, config: FormatterConfig):
        self.config = config
        self.progress = 0.0
        self.status = "initialized"
        self.errors = []
        self.last_update = time.time()

    def update_progress(self, progress: float, status: str):
        """Update the progress and status."""
        current_time = time.time()
        if (current_time - self.last_update) >= self.config.progress_update_interval:
            self.progress = float(progress)
            self.status = status
            self.last_update = current_time
            logger.info(f"Progress: {progress}% - Status: {status}")

    def handle_error(self, error: str):
        """Handle an error during processing."""
        if len(self.errors) < self.config.max_errors:
            self.errors.append(error)
            logger.error(f"Error: {error}")
        else:
            logger.error("Maximum error limit reached")

class TableFormatter:
    """Main class for formatting markdown tables."""
    
    def __init__(self, config: Optional[FormatterConfig] = None):
        self.config = config or get_default_config()
        self.stats = TableStats(0, 0, 0.0, 0, [])
        self.output_handler = OutputHandler(self.config)
        self._validate_config()

    def _validate_config(self):
        """Validate the formatter configuration."""
        self.config.validate()

    def generate_output(self, format_type: Optional[str] = None) -> str:
        """Generate formatted output based on the specified type."""
        format_type = format_type or self.config.default_output_format
        self.output_handler.update_progress(0, "Starting output generation")
        try:
            if format_type == "string":
                return self._generate_string_output()
            elif format_type == "file":
                return self._generate_file_output()
            elif format_type == "stream":
                return self._generate_stream_output()
            else:
                raise ValueError(f"Unsupported output format: {format_type}")
        except Exception as e:
            self.output_handler.handle_error(str(e))
            raise

    def write_to_file(self, file_path: str) -> None:
        """Write the formatted table to a file."""
        self.output_handler.update_progress(0, "Starting file write")
        try:
            path = Path(file_path)
            
            # Create backup if enabled
            if self.config.create_backup and path.exists():
                backup_path = path.with_suffix(path.suffix + self.config.backup_suffix)
                path.rename(backup_path)
            
            with path.open('w', encoding=self.config.encoding) as f:
                f.write(self.generate_output("string"))
            self.output_handler.update_progress(100, "File write complete")
        except Exception as e:
            self.output_handler.handle_error(f"Failed to write to file: {str(e)}")
            raise

    def stream_output(self, stream) -> None:
        """Stream the formatted output to the provided stream."""
        self.output_handler.update_progress(0, "Starting stream output")
        try:
            output = self.generate_output("string")
            stream.write(output)
            self.output_handler.update_progress(100, "Stream output complete")
        except Exception as e:
            self.output_handler.handle_error(f"Failed to stream output: {str(e)}")
            raise

    def get_progress(self) -> Dict[str, Any]:
        """Get the current progress information."""
        return {
            "progress": float(self.output_handler.progress),
            "status": self.output_handler.status,
            "errors": self.output_handler.errors
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the processing results."""
        return {
            "total_rows": self.stats.total_rows,
            "total_columns": self.stats.total_columns,
            "processing_time": self.stats.processing_time,
            "formatting_changes": self.stats.formatting_changes,
            "errors": self.stats.errors
        }

    def _generate_string_output(self) -> str:
        """Generate string output."""
        # TODO: Implement string output generation
        return ""

    def _generate_file_output(self) -> str:
        """Generate file output."""
        # TODO: Implement file output generation
        return ""

    def _generate_stream_output(self) -> str:
        """Generate stream output."""
        # TODO: Implement stream output generation
        return ""

    def _calculate_column_widths(self, table: List[List[str]]) -> List[int]:
        """Calculate the maximum width for each column."""
        num_columns = max(len(row) for row in table)
        widths = [0] * num_columns
        for row in table:
            for i, cell in enumerate(row):
                cell_lines = cell.split("\n")
                max_line_length = max(len(line) for line in cell_lines)
                widths[i] = max(widths[i], max_line_length)
        # Optionally, apply wrap_width if wrap_text is enabled
        if self.config.wrap_text:
            widths = [min(w, self.config.wrap_width) for w in widths]
        return widths

    def _format_row(self, row: List[str], column_widths: List[int]) -> str:
        """Format a single row with proper padding and alignment."""
        formatted_cells = []
        for cell, width in zip(row, column_widths):
            # Handle text wrapping if enabled
            if self.config.wrap_text:
                wrapped_lines = self._wrap_text(cell, width)
                formatted_cell = "\n".join(wrapped_lines)
            else:
                formatted_cell = cell.ljust(width)
            formatted_cells.append(formatted_cell)
        
        return "| " + " | ".join(formatted_cells) + " |"
    
    def _should_add_row_divider(self, row: List[str], column_widths: List[int]) -> bool:
        """Determine if a row divider should be added based on configuration and content."""
        if self.config.row_divider_mode == "always":
            return True
        if self.config.row_divider_mode == "never":
            return False
        
        # Smart mode: check if any cell needs wrapping
        if self.config.wrap_text:
            for cell, width in zip(row, column_widths):
                if len(cell) > width:
                    return True
        return False
    
    def _create_row_divider(self, column_widths: List[int]) -> str:
        """Create a row divider based on configuration settings."""
        if self.config.row_divider_style == "equals":
            divider_char = "="
        elif self.config.row_divider_style == "custom":
            divider_char = self.config.custom_row_divider
        else:  # dash
            divider_char = "-"
        
        padding = " " * self.config.row_divider_padding
        divider = f"+{padding}{divider_char * (sum(column_widths) + 2 * (len(column_widths) - 1))}{padding}+"
        return divider
    
    def format_table(self, table: List[List[str]]) -> str:
        """Format a table with proper alignment and spacing."""
        if not table:
            return ""
            
        # Calculate column widths
        column_widths = self._calculate_column_widths(table)
        
        # Format header
        formatted_rows = []
        header = table[0]
        formatted_rows.append(self._format_row(header, column_widths))
        
        # Add header separator
        formatted_rows.append(self._create_row_divider(column_widths))
        
        # Format data rows
        for row in table[1:]:
            # Add row divider if needed
            if self._should_add_row_divider(row, column_widths):
                formatted_rows.append(self._create_row_divider(column_widths))
            formatted_rows.append(self._format_row(row, column_widths))
        
        return "\n".join(formatted_rows)

    def _wrap_text(self, text: str, width: int) -> list:
        """Wrap text to the specified width."""
        import textwrap
        return textwrap.wrap(text, width=width) 