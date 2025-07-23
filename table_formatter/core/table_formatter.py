"""
Table Formatter Module

Handles the formatting of parsed and analyzed markdown tables, focusing on
consistent alignment, padding, and width calculations. This is the third phase
of table processing in the DSS table formatting pipeline.

Key responsibilities:
- Calculate optimal column widths based on content and code blocks
- Apply alignment rules with support for left, center, and right alignment
- Handle cell padding with configurable minimum and maximum values
- Preserve and format code blocks (both inline and fenced)
- Generate formatted output with consistent styling
- Apply custom formatting rules with priority-based execution
- Support style templates (GitHub, Technical, Minimal)

Features:
- Robust code block detection and preservation
- Configurable text wrapping with soft/hard options
- Support for multiline cell content
- Customizable padding and alignment per column
- Template-based styling with inheritance
- Priority-based rule application
- Diagnostic output for code blocks

Integration points:
- Input: Parsed table data and analysis results
- Output: Formatted markdown table
- Used by: Main script for final output

Style Templates:
- GitHub: Optimized for GitHub markdown rendering
- Technical: Enhanced for technical documentation
- Minimal: Simplified formatting for basic tables

Configuration:
- Column width constraints
- Padding rules
- Text wrapping behavior
- Code block handling
- Line break preservation
- Template selection
"""

from typing import Dict, List, Tuple, Optional, Any, Set, Union, Callable
from dataclasses import dataclass
import re
from .table_parser import TableParser, TableDiagnostics, CodeBlockInfo
from enum import Enum
from .table_analyzer import TableAnalysis, ContentType, ColumnAnalysis
import textwrap

class ContentType(Enum):
    """Content type enumeration."""
    EMPTY = "empty"
    TEXT = "text"
    NUMBER = "number"
    CODE = "code"
    URL = "url"
    EMAIL = "email"
    DATE = "date"
    BOOLEAN = "boolean"
    MIXED = "mixed"

@dataclass
class ColumnFormat:
    """
    Formatting information for a table column.
    """
    width: int
    alignment: str
    padding: int
    content_type: ContentType
    code_blocks: List[CodeBlockInfo]
    has_code_blocks: bool = False
    has_multiline: bool = False

@dataclass
class FormatRule:
    """A custom formatting rule for table cells."""
    name: str
    description: str
    condition: Callable[[str, ContentType, List[CodeBlockInfo], 'ColumnFormat'], bool]
    formatter: Callable[[str, 'ColumnFormat'], str]
    priority: int = 0  # Higher priority rules are applied first

@dataclass
class FormatConfig:
    """Configuration for table formatting."""
    min_width: int = 3
    max_width: int = 80
    min_padding: int = 1
    max_padding: int = 3
    code_block_padding: int = 2
    preserve_code_blocks: bool = True
    wrap_text: bool = True
    wrap_width: int = 40
    show_code_blocks: bool = False
    code_block_indent: int = 2
    preserve_indentation: bool = True
    wrap_style: str = 'soft'  # 'soft' for word wrap, 'hard' for character wrap
    wrap_indent: int = 0
    preserve_line_breaks: bool = True  # Whether to preserve explicit line breaks
    max_lines_per_cell: int = 10  # Maximum number of lines per cell before truncation
    padding: int = 1
    alignment: str = 'left'
    rules: List[FormatRule] = None  # Custom formatting rules

@dataclass
class StyleTemplate:
    """A predefined set of formatting rules and configurations."""
    name: str
    description: str
    config: FormatConfig
    rules: List[FormatRule]
    priority: int = 0  # Higher priority templates are applied first

class TableFormatter:
    """
    Formats markdown tables with consistent alignment and padding.
    
    Flow: Parsed table → Width calculation → Alignment → Padding → Rules → Style → Output
    """
    
    def __init__(self, config: Optional[FormatConfig] = None):
        """
        Initialize the table formatter.
        
        Args:
            config: Optional formatting configuration
        """
        self.config = config or FormatConfig()
        self.column_formats = []
        # Match both inline code and fenced code blocks, with support for nested blocks
        self._code_block_pattern = re.compile(
            r'(?P<inline>`{1,3})(?P<inline_content>[^`]*?)(?P=inline)'  # Inline code
            r'|(?P<fence>```)(?P<language>\w*)\n(?P<fence_content>[\s\S]*?)(?<=\n)(?P=fence)',  # Fenced code block
            re.DOTALL
        )
        
        # Initialize default rules if none provided
        if self.config.rules is None:
            self.config.rules = self._get_default_rules()
            
        # Initialize style templates
        self.style_templates = self._get_default_templates()
        self.active_template = None
        
    def _get_default_rules(self) -> List[FormatRule]:
        """Get default formatting rules."""
        return [
            FormatRule(
                name="code_blocks",
                description="Format code blocks",
                condition=lambda content, content_type, code_blocks, col_format: bool(code_blocks),
                formatter=lambda content, col_format: self._preserve_code_blocks(content, col_format.code_blocks),
                priority=100
            ),
            FormatRule(
                name="multiline",
                description="Format multiline content",
                condition=lambda content, content_type, code_blocks, col_format: '\n' in content,
                formatter=lambda content, col_format: self._format_multiline_cell(content, col_format),
                priority=90
            ),
            FormatRule(
                name="wrapping",
                description="Wrap long content",
                condition=lambda content, content_type, code_blocks, col_format: len(content) > (col_format.width - 2 * self.config.padding),
                formatter=lambda content, col_format: self._wrap_cell_content(content, col_format),
                priority=80
            ),
            FormatRule(
                name="padding",
                description="Apply padding",
                condition=lambda content, content_type, code_blocks, col_format: True,
                formatter=lambda content, col_format: self._apply_padding(content, col_format),
                priority=70
            )
        ]
        
    def add_rule(self, rule: FormatRule) -> None:
        """
        Add a custom formatting rule.
        
        Args:
            rule: The FormatRule to add
        """
        self.config.rules.append(rule)
        # Sort rules by priority (highest first)
        self.config.rules.sort(key=lambda r: r.priority, reverse=True)
        
    def remove_rule(self, rule_name: str) -> None:
        """
        Remove a formatting rule by name.
        
        Args:
            rule_name: Name of the rule to remove
        """
        self.config.rules = [r for r in self.config.rules if r.name != rule_name]
        
    def _apply_rules(
        self,
        content: str,
        col_format: 'ColumnFormat'
    ) -> str:
        """
        Apply formatting rules to cell content.
        Args:
            content: Cell content
            col_format: Column formatting information
        Returns:
            Formatted cell content
        """
        # Apply rules in order of priority
        for rule in self.config.rules:
            if rule.condition(content, col_format.content_type, col_format.code_blocks, col_format):
                content = rule.formatter(content, col_format)
        return content

    def _normalize_table(self, parsed_table, diagnostics):
        """
        Ensure all rows have the same number of columns as the header.
        Extend diagnostics.alignments if needed.
        """
        if not parsed_table:
            return parsed_table, diagnostics
        num_cols = len(parsed_table[0])
        # Pad all rows
        for i, row in enumerate(parsed_table):
            if len(row) < num_cols:
                row.extend([''] * (num_cols - len(row)))
            elif len(row) > num_cols:
                parsed_table[i] = row[:num_cols]
        # Pad alignments
        if hasattr(diagnostics, 'alignments'):
            if len(diagnostics.alignments) < num_cols:
                diagnostics.alignments.extend(['left'] * (num_cols - len(diagnostics.alignments)))
            elif len(diagnostics.alignments) > num_cols:
                diagnostics.alignments = diagnostics.alignments[:num_cols]
        return parsed_table, diagnostics

    def format_table(
        self,
        parsed_table: List[List[str]],
        diagnostics: Any,
        analysis: Any
    ) -> str:
        """
        Format a parsed table with consistent styling.
        """
        # Normalize table and diagnostics
        parsed_table, diagnostics = self._normalize_table(parsed_table, diagnostics)
        if not parsed_table or len(parsed_table) < 2:
            raise ValueError("Invalid table data for formatting")
            
        # Calculate column formats
        self.column_formats = self._calculate_column_formats(
            parsed_table,
            diagnostics,
            analysis
        )
        
        # Format header
        header = self._format_row(parsed_table[0], self.column_formats, is_header=True)
        
        # Format separator
        separator = self._format_separator()
        
        # Format data rows
        data_rows = [
            self._format_row(row, self.column_formats, is_header=False)
            for row in parsed_table[1:]
        ]
        
        # Combine all rows
        formatted = '\n'.join([header, separator] + data_rows)
        
        # Show code block information if requested
        if self.config.show_code_blocks:
            formatted += '\n\n' + self._format_code_block_info()
            
        return formatted
    
    def _calculate_column_formats(
        self,
        table: List[List[str]],
        diagnostics: TableDiagnostics,
        analysis: TableAnalysis
    ) -> List[ColumnFormat]:
        """
        Calculate formatting information for each column.
        Args:
            table: Parsed table data
            diagnostics: Table diagnostics
            analysis: Table analysis
        Returns:
            List of column formats
        """
        column_formats = []
        for col_idx in range(len(table[0])):
            # Initialize column format with default values
            col_format = ColumnFormat(
                width=0,
                alignment='left',
                padding=1,
                content_type=ContentType.TEXT,
                code_blocks=[]
            )
            
            # Calculate width based on content
            for row in table:
                if col_idx < len(row):
                    content = row[col_idx]
                    # Detect code blocks
                    code_blocks = self._detect_code_blocks(content)
                    col_format.code_blocks.extend(code_blocks)
                    col_format.has_code_blocks = bool(code_blocks)
                    
                    # Calculate width considering code blocks
                    if code_blocks:
                        # For code blocks, use the raw content length
                        width = len(content) + 2 * col_format.padding
                    else:
                        width = len(content) + 2 * col_format.padding
                    col_format.width = max(col_format.width, width)
            
            # Apply alignment from diagnostics
            if col_idx < len(diagnostics.alignments):
                col_format.alignment = diagnostics.alignments[col_idx]
            
            # Apply content type from analysis
            if col_idx < len(analysis.column_analyses):
                col_format.content_type = analysis.column_analyses[col_idx].content_type
            
            # Ensure width is within bounds
            col_format.width = max(
                self.config.min_width,
                min(col_format.width, self.config.max_width)
            )
            
            column_formats.append(col_format)
            
        return column_formats
    
    def _detect_code_blocks(self, content: str) -> List[CodeBlockInfo]:
        """
        Detect code blocks (inline and fenced) in the given content string.
        Args:
            content: The string content to search for code blocks.
        Returns:
            List of CodeBlockInfo objects.
        """
        code_blocks = []
        # Fenced code blocks first
        fenced_matches = list(re.finditer(r'```(\w*)\n([\s\S]*?)```', content))
        fenced_spans = [(m.start(), m.end()) for m in fenced_matches]
        for match in fenced_matches:
            code_blocks.append(CodeBlockInfo(
                start=match.start(),
                end=match.end(),
                content=match.group(2),
                language=match.group(1) if match.group(1) else None,
                is_fenced=True
            ))
        # Inline code blocks only outside fenced blocks
        def is_outside_fenced(pos):
            return not any(start <= pos < end for start, end in fenced_spans)
        for match in re.finditer(r'`{1,3}([^`]+)`{1,3}', content):
            if is_outside_fenced(match.start()):
                code_blocks.append(CodeBlockInfo(
                    start=match.start(),
                    end=match.end(),
                    content=match.group(1),
                    language=None,
                    is_fenced=False
                ))
        code_blocks.sort(key=lambda x: x.start)
        return code_blocks

    def _preserve_code_blocks(self, content: str, code_blocks: List[CodeBlockInfo]) -> str:
        """Preserve code blocks during formatting."""
        if not self.config.preserve_code_blocks:
            # Remove code block markers
            content = re.sub(r'`{1,3}([^`]+)`{1,3}', r'\1', content)
            content = re.sub(r'```\w*\n(.*?)```', r'\1', content, flags=re.DOTALL)
            return content
            
        # Sort blocks by start position to handle nested blocks
        code_blocks.sort(key=lambda x: x.start)
        
        # Process blocks from end to start to avoid position shifts
        for block in reversed(code_blocks):
            if block.is_fenced:
                # Preserve fenced block with language
                lang = block.language or ''
                content = content[:block.start] + f"```{lang}\n{block.content}```" + content[block.end:]
            else:
                # Preserve inline block
                content = content[:block.start] + f"`{block.content}`" + content[block.end:]
                
        return content
    
    def _calculate_column_width(
        self,
        content: List[str],
        col_format: 'ColumnFormat',
        header: str,
        code_blocks: List[CodeBlockInfo]
    ) -> int:
        """
        Calculate the width of a column.
        Args:
            content: List of cell contents
            col_format: Column formatting information
            header: Header text
            code_blocks: List of code blocks in the column
        Returns:
            Calculated column width
        """
        # Start with header width
        width = len(header)

        # Check content width
        for cell in content:
            cell_width = len(cell)
            if cell_width > width:
                width = cell_width

        # Add padding
        width += 2 * self.config.padding

        # Ensure width is within bounds
        width = max(self.config.min_width, min(width, self.config.max_width))

        return width
    
    def _calculate_padding(self, analysis: Any) -> int:
        """
        Calculate padding for a column based on content type.
        
        Args:
            analysis: ColumnAnalysis object
            
        Returns:
            Number of padding spaces
        """
        if analysis.content_type == ContentType.CODE:
            return self.config.code_block_padding
        elif analysis.content_type == ContentType.NUMBER:
            return self.config.min_padding
        else:
            return self.config.min_padding
    
    def _format_row(
        self,
        row: List[str],
        column_formats: List[ColumnFormat],
        is_header: bool = False
    ) -> str:
        """
        Format a single row of the table.
        Args:
            row: List of cell contents
            column_formats: List of column formats
            is_header: Whether this is a header row
        Returns:
            Formatted row string
        """
        formatted_cells = []
        for cell, col_format in zip(row, column_formats):
            # Apply rules to cell content
            formatted_cell = self._apply_rules(cell, col_format)
            # Apply padding
            padded_cell = self._apply_padding(formatted_cell, col_format.padding)
            # Apply alignment
            aligned_cell = self._apply_alignment(padded_cell, col_format)
            # Ensure total width matches or exceeds expected width
            total_width = col_format.width + 2 * col_format.padding
            if len(aligned_cell) < total_width:
                aligned_cell = aligned_cell.ljust(total_width)
            formatted_cells.append(aligned_cell)
        # Join cells with pipes and spaces
        return '| ' + ' | '.join(formatted_cells) + ' |'
    
    def _format_multiline_cell(self, content: str, col_format: 'ColumnFormat') -> str:
        """Format a multiline cell."""
        if not self.config.preserve_line_breaks:
            return content.replace('\n', ' ')
            
        lines = content.split('\n')
        if not self.config.wrap_text:
            return content
            
        # Wrap each line if needed
        wrapped_lines = []
        for line in lines:
            if len(line) > col_format.width - 2 * self.config.padding:
                wrapped = textwrap.wrap(
                    line,
                    width=col_format.width - 2 * self.config.padding,
                    break_long_words=True,
                    break_on_hyphens=False
                )
                wrapped_lines.extend(wrapped)
            else:
                wrapped_lines.append(line)
                
        # Apply max lines limit if configured
        if len(wrapped_lines) > self.config.max_lines_per_cell:
            wrapped_lines = wrapped_lines[:self.config.max_lines_per_cell]
            wrapped_lines.append('...')
            
        return '\n'.join(wrapped_lines)
    
    def _wrap_cell_content(
        self,
        content: str,
        col_format: ColumnFormat
    ) -> str:
        """
        Wrap cell content to fit column width.

        Args:
            content: Cell content
            col_format: Column formatting information

        Returns:
            Wrapped cell content
        """
        if not content:
            return content
        
        # Calculate available width
        available_width = col_format.width - (2 * col_format.padding)
        
        # Handle code blocks
        if col_format.has_code_blocks:
            code_blocks = self._detect_code_blocks(content)
            if code_blocks:
                # Don't wrap code blocks
                return content
        
        # Handle multi-line content
        if '\n' in content:
            lines = content.split('\n')
            wrapped_lines = []
            for line in lines:
                wrapped = self._wrap_line(line, available_width)
                wrapped_lines.extend(wrapped)
            return '\n'.join(wrapped_lines)
        else:
            return '\n'.join(self._wrap_line(content, available_width))
    
    def _wrap_line(
        self,
        line: str,
        width: int
    ) -> List[str]:
        """
        Wrap a single line of text.

        Args:
            line: Line to wrap
            width: Maximum width

        Returns:
            List of wrapped lines
        """
        if len(line) <= width:
            return [line]
        
        if self.config.wrap_style == 'hard':
            # Character-based wrapping
            return [line[i:i+width] for i in range(0, len(line), width)]
        else:
            # Word-based wrapping
            words = line.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) + 1 <= width:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            return lines
    
    def _apply_padding(
        self,
        content: Union[str, List[str]],
        col_format: Union['ColumnFormat', int]
    ) -> str:
        """
        Apply padding to cell content.
        Args:
            content: Cell content
            col_format: Column formatting information or padding value
        Returns:
            Padded cell content
        """
        if isinstance(content, list):
            content = '\n'.join(content)
            
        # Handle both ColumnFormat objects and direct padding values
        padding = col_format.padding if isinstance(col_format, ColumnFormat) else col_format
        
        # Apply padding to each line
        lines = content.split('\n')
        padded_lines = []
        for line in lines:
            # Only add padding if it's not already padded
            if not line.startswith(' ') and not line.endswith(' '):
                padded_lines.append(' ' * padding + line + ' ' * padding)
            else:
                padded_lines.append(line)
            
        return '\n'.join(padded_lines)

    def _apply_alignment(
        self,
        content: str,
        col_format: 'ColumnFormat'
    ) -> str:
        """
        Apply alignment to cell content.
        Args:
            content: Cell content
            col_format: Column formatting information
        Returns:
            Aligned cell content
        """
        # Calculate width excluding padding since padding is handled separately
        width = col_format.width
        
        # Remove any existing padding before alignment
        content = content.strip()
        
        if col_format.alignment == 'center':
            return content.center(width)
        elif col_format.alignment == 'right':
            return content.rjust(width)
        else:  # left
            return content.ljust(width)
    
    def _format_separator(self) -> str:
        """
        Format the separator row so that each cell matches the actual width and alignment of the corresponding column, using per-column padding and width from ColumnFormat.
        Returns:
            Formatted separator string
        """
        separator_cells = []
        for fmt in self.column_formats:
            total_width = fmt.width  # fmt.width already includes padding
            if fmt.alignment == 'left':
                sep = '-' * total_width
            elif fmt.alignment == 'right':
                sep = '-' * (total_width - 1) + ':' if total_width > 1 else ':'
            else:  # center
                sep = ':' + '-' * (total_width - 2) + ':' if total_width > 2 else '::'
            separator_cells.append(sep)
        return '|' + '|'.join(separator_cells) + '|'
        
    def _format_code_block_info(self) -> str:
        """
        Format code block information for diagnostic output.
        
        Returns:
            Formatted code block information
        """
        info = ["Code Block Information:"]
        
        for i, fmt in enumerate(self.column_formats):
            if fmt.has_code_blocks:
                info.append(f"\nColumn {i + 1}:")
                for j, block in enumerate(fmt.code_blocks):
                    info.append(f"  Block {j + 1}:")
                    info.append(f"    Type: {'Fenced' if block.is_fenced else 'Inline'}")
                    if block.language:
                        info.append(f"    Language: {block.language}")
                    info.append(f"    Content: {block.content[:50]}...")
                    
        return '\n'.join(info)
    
    def _get_default_templates(self) -> Dict[str, StyleTemplate]:
        """Get default style templates."""
        return {
            'github': StyleTemplate(
                name="github",
                description="GitHub-style markdown formatting",
                config=FormatConfig(
                    min_width=3,
                    max_width=80,
                    min_padding=1,
                    max_padding=3,
                    code_block_padding=2,
                    preserve_code_blocks=True,
                    wrap_text=True,
                    wrap_width=40,
                    show_code_blocks=False,
                    code_block_indent=2,
                    preserve_indentation=True,
                    wrap_style='soft',
                    wrap_indent=0,
                    preserve_line_breaks=True,
                    max_lines_per_cell=10,
                    padding=1,
                    alignment='left'
                ),
                rules=[
                    FormatRule(
                        name="github_code_blocks",
                        description="Format code blocks in GitHub style",
                        condition=lambda content, content_type, code_blocks, col_format: bool(code_blocks),
                        formatter=lambda content, col_format: self._format_github_code_blocks(content, col_format.code_blocks),
                        priority=100
                    ),
                    FormatRule(
                        name="github_links",
                        description="Format links in GitHub style",
                        condition=lambda content, content_type, code_blocks, col_format: '[' in content and ']' in content,
                        formatter=lambda content, col_format: self._format_github_links(content),
                        priority=90
                    )
                ],
                priority=100
            ),
            'technical': StyleTemplate(
                name="technical",
                description="Technical documentation style",
                config=FormatConfig(
                    min_width=3,
                    max_width=100,
                    min_padding=2,
                    max_padding=4,
                    code_block_padding=3,
                    preserve_code_blocks=True,
                    wrap_text=True,
                    wrap_width=60,
                    show_code_blocks=True,
                    code_block_indent=4,
                    preserve_indentation=True,
                    wrap_style='soft',
                    wrap_indent=2,
                    preserve_line_breaks=True,
                    max_lines_per_cell=20,
                    padding=2,
                    alignment='left'
                ),
                rules=[
                    FormatRule(
                        name="technical_code_blocks",
                        description="Format code blocks in technical style",
                        condition=lambda content, content_type, code_blocks, col_format: bool(code_blocks),
                        formatter=lambda content, col_format: self._format_technical_code_blocks(content, col_format.code_blocks),
                        priority=100
                    ),
                    FormatRule(
                        name="technical_math",
                        description="Format math expressions in technical style",
                        condition=lambda content, content_type, code_blocks, col_format: '$' in content,
                        formatter=lambda content, col_format: self._format_technical_math(content),
                        priority=90
                    )
                ],
                priority=90
            ),
            'minimal': StyleTemplate(
                name="minimal",
                description="Minimal formatting style",
                config=FormatConfig(
                    min_width=3,
                    max_width=60,
                    min_padding=1,
                    max_padding=2,
                    code_block_padding=1,
                    preserve_code_blocks=False,
                    wrap_text=False,
                    wrap_width=40,
                    show_code_blocks=False,
                    code_block_indent=0,
                    preserve_indentation=False,
                    wrap_style='hard',
                    wrap_indent=0,
                    preserve_line_breaks=False,
                    max_lines_per_cell=5,
                    padding=1,
                    alignment='left'
                ),
                rules=[
                    FormatRule(
                        name="minimal_formatting",
                        description="Minimal formatting",
                        condition=lambda content, content_type, code_blocks, col_format: True,
                        formatter=lambda content, col_format: content,
                        priority=50
                    )
                ],
                priority=50
            )
        }
        
    def apply_template(self, template_name: str) -> None:
        """
        Apply a style template to the formatter.
        
        Args:
            template_name: Name of the template to apply
        """
        if template_name not in self.style_templates:
            raise ValueError(f"Unknown template: {template_name}")
            
        template = self.style_templates[template_name]
        self.active_template = template
        
        # Update configuration
        self.config = template.config
        
        # Update rules
        self.config.rules = template.rules + self._get_default_rules()
        # Sort rules by priority
        self.config.rules.sort(key=lambda r: r.priority, reverse=True)
        
    def remove_template(self) -> None:
        """Remove the currently applied template."""
        self.active_template = None
        self.config = FormatConfig()
        self.config.rules = self._get_default_rules()
        
    def _format_technical_code_blocks(
        self,
        content: str,
        code_blocks: List[CodeBlockInfo]
    ) -> str:
        """Format code blocks in technical documentation style."""
        # Technical docs often use more indentation and language highlighting
        for block in code_blocks:
            if block.is_fenced and block.language:
                # Add extra indentation for fenced blocks
                content = content.replace(
                    f"```{block.language}\n{block.content}```",
                    f"```{block.language}\n{block.content}\n```"
                )
        return content

    def _format_github_code_blocks(
        self,
        content: str,
        code_blocks: List[CodeBlockInfo]
    ) -> str:
        """Format code blocks in GitHub style."""
        # GitHub style often uses more indentation and language highlighting
        for block in code_blocks:
            if block.is_fenced and block.language:
                # Add extra indentation for fenced blocks
                content = content.replace(
                    f"```{block.language}\n{block.content}```",
                    f"```{block.language}\n{block.content}\n```"
                )
        return content

    def _format_github_links(self, content: str) -> str:
        """Format links in GitHub style."""
        # GitHub style often uses more indentation and language highlighting
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
            link = match.group(2)
            text = match.group(1)
            content = content.replace(
                f"[{text}]({link})",
                f"[{text}]({link})"
            )
        return content

    def _format_technical_math(self, content: str) -> str:
        """Format math expressions in technical style."""
        # Technical style often uses more indentation and language highlighting
        for match in re.finditer(r'\$(.*?)\$', content):
            expression = match.group(1)
            content = content.replace(
                f"${expression}$",
                f"${expression}$"
            )
        return content