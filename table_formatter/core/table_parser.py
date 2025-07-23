"""
Table Parser Module

Handles the parsing of markdown tables into structured data.
This is the second phase of table processing in the DSS table
formatting pipeline.

Key responsibilities:
- Split tables into rows and cells
- Validate table structure
- Detect column alignments
- Generate diagnostics

Integration points:
- Input: Raw markdown table text
- Output: Structured table data and diagnostics
- Used by: Table analyzer for content analysis
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from .code_block_info import CodeBlockInfo

@dataclass
class TableDiagnostics:
    """Diagnostic information about a parsed table."""
    row_count: int
    column_count: int
    alignments: List[str]
    has_header: bool
    has_separator: bool
    is_valid: bool
    errors: List[str]

class TableParser:
    """
    Parses markdown tables into structured data with diagnostics.
    
    Flow: Raw text → Row splitting → Cell extraction → Validation → Output
    """
    
    def __init__(self):
        """Initialize the table parser."""
        self.diagnostics = None
        
    def parse_table(
        self,
        table_text: str | List[List[str]]
    ) -> Tuple[List[List[str]], TableDiagnostics]:
        """
        Parse a markdown table into structured data with diagnostics.

        Flow:
        1. Split into rows
        2. Validate header structure
        3. Detect column alignments
        4. Generate diagnostics

        Args:
            table_text: Raw markdown table text or pre-split table data

        Returns:
            Tuple containing:
            - List of rows, each as a list of cell contents
            - TableDiagnostics object with structural information

        Raises:
            ValueError: If table structure is invalid
        """
        # Handle pre-split table data
        if isinstance(table_text, list):
            # If already a list of lists, assume it's parsed
            if all(isinstance(row, list) for row in table_text):
                parsed_rows = table_text
                header_cells = parsed_rows[0]
                alignments = ['left'] * len(header_cells)
                self.diagnostics = TableDiagnostics(
                    row_count=len(parsed_rows),
                    column_count=len(header_cells),
                    alignments=alignments,
                    has_header=True,
                    has_separator=True,
                    is_valid=len(parsed_rows) >= 2,
                    errors=[]
                )
                return parsed_rows, self.diagnostics
            # Otherwise, treat as list of strings
            rows = table_text
        else:
            rows = [row.strip() for row in table_text.strip().split('\n') if row.strip()]
        if not rows:
            raise ValueError("Empty table")
        header = rows[0]
        separator = rows[1] if len(rows) > 1 else None
        data_rows = rows[2:] if len(rows) > 2 else []
        header_cells = self._parse_row(header)
        if not header_cells:
            raise ValueError("Invalid header row")
        alignments = []
        if separator:
            separator_cells = self._parse_row(separator)
            if not separator_cells:
                raise ValueError("Invalid separator row")
            alignments = self._detect_alignments(separator_cells)
        else:
            alignments = ['left'] * len(header_cells)
        parsed_rows = [header_cells]
        for row in data_rows:
            cells = self._parse_row(row)
            if cells:
                if len(cells) != len(header_cells):
                    # Record mismatch
                    if 'errors' not in locals():
                        mismatch_errors = []
                    mismatch_errors.append(
                        f"Row {len(parsed_rows)} has {len(cells)} cells (expected {len(header_cells)})"
                    )
                    # Normalize by padding or trimming
                    if len(cells) < len(header_cells):
                        cells.extend([''] * (len(header_cells) - len(cells)))
                    else:
                        cells = cells[:len(header_cells)]
                parsed_rows.append(cells)
        errors = locals().get('mismatch_errors', [])
        self.diagnostics = TableDiagnostics(
            row_count=len(parsed_rows),
            column_count=len(header_cells),
            alignments=alignments,
            has_header=True,
            has_separator=bool(separator),
            is_valid=len(parsed_rows) >= 2 and not errors,
            errors=errors
        )
        return parsed_rows, self.diagnostics
        
    def _parse_row(self, row: str | List[str]) -> List[str]:
        """
        Parse a table row into cells.
        
        Args:
            row: Raw row text or pre-split row data
            
        Returns:
            List of cell contents
        """
        if isinstance(row, list):
            return row
        if not row.startswith('|'):
            row = '|' + row
        if not row.endswith('|'):
            row = row + '|'
            
        # Split by pipe and clean cells
        cells = [cell.strip() for cell in row.split('|')[1:-1]]
        return cells
        
    def _detect_alignments(self, separator_cells: List[str]) -> List[str]:
        """
        Detect column alignments from separator row.
        
        Args:
            separator_cells: List of separator cell contents
            
        Returns:
            List of alignment strings ('left', 'center', 'right')
        """
        alignments = []
        for cell in separator_cells:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')
        return alignments 