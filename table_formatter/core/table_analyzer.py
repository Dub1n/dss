"""
Table Analyzer Module

Handles the analysis of parsed markdown tables, focusing on content analysis,
pattern recognition, and statistical analysis. This is the second phase of
table processing in the DSS table formatting pipeline.

Key responsibilities:
- Analyze column content types
- Detect content patterns
- Generate statistical analysis
- Validate content consistency

Integration points:
- Input: Parsed table data from TableParser
- Output: Content analysis and statistics
- Used by: Table formatter for optimal formatting
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass
import re
from enum import Enum
from collections import Counter
import statistics
from .table_parser import TableParser, TableDiagnostics

class ContentType(Enum):
    """Content type enumeration."""
    TEXT = 'text'
    NUMBER = 'number'
    CODE = 'code'
    DATE = "date"
    BOOLEAN = "boolean"
    URL = "url"
    EMAIL = "email"
    EMPTY = 'empty'
    MIXED = "mixed"
    NUMERIC = 'numeric'  # Added for numeric content

@dataclass
class ColumnAnalysis:
    """Analysis results for a single column."""
    content_type: ContentType
    patterns: List[str]
    statistics: Dict[str, Any]
    consistency_score: float
    issues: List[str]

@dataclass
class TableAnalysis:
    """Complete analysis of a table's content."""
    column_analyses: List[ColumnAnalysis]
    overall_consistency: float
    content_patterns: Dict[str, int]
    issues: List[str]

class TableAnalyzer:
    """
    Analyzes parsed table content for patterns, types, and statistics.
    
    Flow: Parsed table → Content analysis → Pattern detection → Statistics → Validation
    """
    
    def __init__(self):
        """Initialize the table analyzer with default settings."""
        self.analysis = None
        self._pattern_regexes = {
            'url': r'https?://\S+',
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'date': r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}',
            'code': r'`[^`]+`|```[\s\S]+?```',
            'number': r'^-?\d*\.?\d+$',
            'boolean': r'^(true|false|yes|no|1|0)$'
        }
        
        # Validation thresholds
        self._thresholds = {
            'empty_cell_ratio': 0.2,  # 20% empty cells is too high
            'mixed_content_ratio': 0.2,  # 20% mixed content is too high
            'min_unique_ratio': 0.2,  # At least 20% unique values
            'max_unique_ratio': 0.95,  # No more than 95% unique values
            'min_word_count': 2,  # Minimum words per cell for text
            'max_word_count': 100  # Maximum words per cell for text
        }
    
    def analyze_table(
        self,
        parsed_table: List[List[str]],
        diagnostics: TableDiagnostics
    ) -> TableAnalysis:
        """
        Analyze a parsed table's content.
        
        Args:
            parsed_table: List of rows, each as a list of cell contents
            diagnostics: TableDiagnostics object from parser
            
        Returns:
            TableAnalysis object with content analysis results
        """
        if not parsed_table:
            # Handle empty table case
            return TableAnalysis(
                column_analyses=[],
                overall_consistency=1.0,
                content_patterns={},
                issues=["Empty table"]
            )
            
        # Analyze each column
        column_analyses = []
        for col_idx in range(diagnostics.column_count):
            column_data = [row[col_idx] for row in parsed_table[1:]]  # Skip header
            analysis = self._analyze_column(column_data)
            column_analyses.append(analysis)
            
        # Generate overall analysis
        self.analysis = self._generate_analysis(column_analyses)
        return self.analysis
    
    def _analyze_column(self, column_data: List[str]) -> ColumnAnalysis:
        """
        Analyze a single column's content.
        
        Args:
            column_data: List of cell contents for the column
            
        Returns:
            ColumnAnalysis object with content analysis
        """
        # Detect content type
        content_type = self._detect_content_type(column_data)
        
        # Find patterns
        patterns = self._detect_patterns(column_data)
        
        # Calculate statistics
        stats = self._calculate_statistics(column_data, content_type)
        
        # Check consistency
        consistency_score = self._calculate_consistency(column_data, content_type)
        
        # Identify issues
        issues = self._identify_issues(column_data, content_type, patterns, stats)
        
        return ColumnAnalysis(
            content_type=content_type,
            patterns=patterns,
            statistics=stats,
            consistency_score=consistency_score,
            issues=issues
        )
    
    def _detect_content_type(self, column_data: List[str]) -> ContentType:
        """
        Detect the primary content type of a column.
        
        Args:
            column_data: List of cell contents
            
        Returns:
            ContentType enum value
        """
        type_counts = Counter()
        
        for cell in column_data:
            if not cell.strip():
                type_counts[ContentType.EMPTY] += 1
                continue
                
            # Check each pattern
            for type_name, pattern in self._pattern_regexes.items():
                if re.search(pattern, cell, re.IGNORECASE):
                    type_counts[ContentType(type_name)] += 1
                    break
            else:
                type_counts[ContentType.TEXT] += 1
        
        # Determine primary type
        if not type_counts:
            return ContentType.EMPTY
            
        most_common = type_counts.most_common(1)[0]
        if most_common[1] / len(column_data) >= 0.8:  # 80% threshold
            return most_common[0]
        return ContentType.MIXED
    
    def _detect_patterns(self, column_data: List[str]) -> List[str]:
        """
        Detect common patterns in column content.
        
        Args:
            column_data: List of cell contents
            
        Returns:
            List of detected pattern names
        """
        if not column_data:
            return []
            
        patterns = []
        for pattern_name, regex in self._pattern_regexes.items():
            matches = sum(1 for cell in column_data if re.search(regex, cell, re.IGNORECASE))
            if matches / len(column_data) >= 0.2:  # 20% threshold
                patterns.append(pattern_name)
        return patterns
    
    def _calculate_statistics(
        self,
        column_data: List[str],
        content_type: ContentType
    ) -> Dict[str, Any]:
        """
        Calculate statistics for a column based on its content type.
        
        Args:
            column_data: List of cell contents
            content_type: Detected content type
            
        Returns:
            Dictionary of statistical measures
        """
        stats = {
            'total_cells': len(column_data),
            'empty_cells': sum(1 for cell in column_data if not cell.strip()),
            'unique_values': len(set(column_data))
        }
        
        # Calculate unique value ratio
        if len(column_data) > 0:
            stats['unique_ratio'] = stats['unique_values'] / len(column_data)
        else:
            stats['unique_ratio'] = 0.0
        
        if content_type == ContentType.NUMBER:
            try:
                numbers = [float(cell) for cell in column_data if cell.strip()]
                if numbers:
                    stats.update({
                        'min': min(numbers),
                        'max': max(numbers),
                        'mean': statistics.mean(numbers),
                        'median': statistics.median(numbers),
                        'std_dev': statistics.stdev(numbers) if len(numbers) > 1 else 0
                    })
            except ValueError:
                pass
                
        elif content_type == ContentType.TEXT:
            # Calculate text statistics
            word_counts = []
            char_counts = []
            for cell in column_data:
                if cell.strip():
                    words = cell.split()
                    word_counts.append(len(words))
                    char_counts.append(len(cell))
            
            if word_counts:
                stats.update({
                    'min_words': min(word_counts),
                    'max_words': max(word_counts),
                    'avg_words': statistics.mean(word_counts),
                    'min_chars': min(char_counts),
                    'max_chars': max(char_counts),
                    'avg_chars': statistics.mean(char_counts)
                })
        
        return stats
    
    def _calculate_consistency(
        self,
        column_data: List[str],
        content_type: ContentType
    ) -> float:
        """
        Calculate consistency score for a column.
        
        Args:
            column_data: List of cell contents
            content_type: Detected content type
            
        Returns:
            Float between 0 and 1 indicating consistency
        """
        if not column_data:
            return 1.0
            
        # Count content types
        type_counts = Counter()
        for cell in column_data:
            if not cell.strip():
                type_counts[ContentType.EMPTY] += 1
                continue
                
            # Check each pattern
            for type_name, pattern in self._pattern_regexes.items():
                if re.search(pattern, cell, re.IGNORECASE):
                    type_counts[ContentType(type_name)] += 1
                    break
            else:
                type_counts[ContentType.TEXT] += 1
        
        # Calculate consistency as ratio of most common type
        if not type_counts:
            return 1.0
            
        most_common = type_counts.most_common(1)[0]
        return most_common[1] / len(column_data)
    
    def _identify_issues(
        self,
        column_data: List[str],
        content_type: ContentType,
        patterns: List[str],
        stats: Dict[str, Any]
    ) -> List[str]:
        """
        Identify potential issues in column content.
        
        Args:
            column_data: List of cell contents
            content_type: Detected content type
            patterns: List of detected patterns
            stats: Statistical measures
            
        Returns:
            List of issue descriptions
        """
        issues = []
        
        # Check empty cells
        if stats['total_cells'] > 0:
            empty_ratio = stats['empty_cells'] / stats['total_cells']
            if empty_ratio >= self._thresholds['empty_cell_ratio']:
                issues.append("High ratio of empty cells")
        
        # Check content type consistency
        if content_type == ContentType.MIXED:
            issues.append("Column contains mixed content types")
        
        # Check unique values (high variety)
        unique_ratio = stats['unique_ratio']
        if unique_ratio > self._thresholds['max_unique_ratio']:
            issues.append(f"Very high variety of values ({unique_ratio:.1%} unique)")
        
        # Check text length
        if content_type == ContentType.TEXT and 'avg_words' in stats:
            avg_words = stats['avg_words']
            if avg_words < self._thresholds['min_word_count']:
                issues.append("Very short text content")
            elif avg_words > self._thresholds['max_word_count']:
                issues.append("Very long text content")
        
        # Check patterns
        if len(patterns) > 1:
            issues.append("Multiple content patterns detected")
            
        # Check for identical numbers
        if content_type == ContentType.NUMBER and 'std_dev' in stats:
            if stats['std_dev'] == 0 and stats['total_cells'] > 1:
                issues.append("All numeric values are identical")
        
        # FINAL: Always check low variety at the very end
        if unique_ratio < self._thresholds['min_unique_ratio'] and "Low variety of values" not in issues:
            issues.append("Low variety of values")
        
        return issues
    
    def _generate_analysis(self, column_analyses: List[ColumnAnalysis]) -> TableAnalysis:
        """
        Generate overall table analysis from column analyses.
        
        Args:
            column_analyses: List of ColumnAnalysis objects
            
        Returns:
            TableAnalysis object with overall results
        """
        if not column_analyses:
            return TableAnalysis(
                column_analyses=[],
                overall_consistency=1.0,
                content_patterns={},
                issues=["Empty table"]
            )
        
        # Calculate overall consistency
        consistency_scores = [analysis.consistency_score for analysis in column_analyses]
        overall_consistency = statistics.mean(consistency_scores)
        
        # Collect all patterns
        content_patterns = Counter()
        for analysis in column_analyses:
            content_patterns.update(analysis.patterns)
        
        # Collect all issues
        issues = []
        for analysis in column_analyses:
            issues.extend(analysis.issues)
        
        return TableAnalysis(
            column_analyses=column_analyses,
            overall_consistency=overall_consistency,
            content_patterns=dict(content_patterns),
            issues=issues
        ) 