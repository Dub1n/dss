"""
Core table formatting modules.

This package contains the core functionality for table parsing,
analysis, and formatting.

Contains the main processing modules for each phase of table handling:
- table_parser.py: Basic table parsing and diagnostics
- table_analyzer.py: Content analysis and pattern detection
- core/table_formatter.py: Table formatting and output
"""

from .table_parser import TableParser, TableDiagnostics
from .table_analyzer import (
    TableAnalyzer,
    TableAnalysis,
    ColumnAnalysis,
    ContentType
)
from .table_formatter import TableFormatter

__all__ = [
    'TableParser',
    'TableDiagnostics',
    'TableAnalyzer',
    'TableAnalysis',
    'ColumnAnalysis',
    'ContentType',
    'TableFormatter'
] 