"""
Table Formatter Main Module

Entry point for the DSS table formatting pipeline. Orchestrates the different
phases of table processing: parsing, analysis, and formatting.

Key responsibilities:
- Coordinate between different processing phases
- Handle command-line interface
- Manage input/output operations
- Provide progress feedback

Integration points:
- Input: Markdown files or direct table text
- Output: Formatted markdown tables
- Uses: Core processing modules for each phase
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

from core.table_parser import TableParser, TableDiagnostics
from core.table_analyzer import TableAnalyzer, TableAnalysis, ContentType
from core.table_formatter import TableFormatter, FormatConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('table_formatter.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

def parse_args() -> Dict[str, Any]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Format markdown tables with consistent alignment and padding."
    )
    
    # Input/Output arguments
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read table from stdin"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write formatted table to stdout"
    )
    parser.add_argument(
        "--template",
        choices=["github", "technical", "minimal"],
        default="github",
        help="Template to use for formatting"
    )
    
    # Formatting options
    parser.add_argument(
        "--max-width",
        type=int,
        default=80,
        help="Maximum width for tables"
    )
    parser.add_argument(
        "--min-padding",
        type=int,
        default=1,
        help="Minimum padding between cell content and borders"
    )
    parser.add_argument(
        "--preserve-code-blocks",
        type=bool,
        default=True,
        help="Preserve code blocks in table cells"
    )
    parser.add_argument(
        "--wrap-text",
        type=bool,
        default=True,
        help="Wrap text in table cells"
    )
    
    return vars(parser.parse_args())

def create_format_config(args: Dict[str, Any]) -> FormatConfig:
    """Create formatting configuration from arguments."""
    return FormatConfig(
        max_width=args['max_width'],
        min_padding=args['min_padding'],
        padding=args['min_padding'],  # unify
        preserve_code_blocks=args['preserve_code_blocks'],
        wrap_text=args['wrap_text']
    )

def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()
        
        # Create formatter components
        parser = TableParser()
        analyzer = TableAnalyzer()
        formatter = TableFormatter(create_format_config(args))
        # Apply chosen template early
        formatter.apply_template(args['template'])
        
        # Read input
        if args['stdin']:
            table_text = sys.stdin.read()
        else:
            logger.error("No input source specified. Use --stdin to read from stdin.")
            sys.exit(1)
        
        # Process table
        parsed_table, diagnostics = parser.parse_table(table_text)
        analysis = analyzer.analyze_table(parsed_table, diagnostics)
        formatted_table = formatter.format_table(parsed_table, diagnostics, analysis)
        
        # Write output
        if args['stdout']:
            print(formatted_table)
        else:
            logger.error("No output destination specified. Use --stdout to write to stdout.")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 