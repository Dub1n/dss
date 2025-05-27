#!/usr/bin/env python3
"""---
tags: [automation, github_integration, self_development, issue_processing]
provides: [github_issues_processor, automated_analysis, pattern_detection]
requires: [meta/assistant_workflows/github_issues_integration.md]
---

GitHub Issues Processor for DSS Self-Development

This script automates the processing of GitHub Issues to support the DSS self-development
workflow. It fetches issues, performs pattern analysis, and generates development tasks.

Usage:
    python meta/scripts/github_issues_processor.py --analyze-reports
    python meta/scripts/github_issues_processor.py --generate-tasks
    python meta/scripts/github_issues_processor.py --update-priorities
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class IssueData:
    """Structured representation of a GitHub Issue."""
    number: int
    title: str
    body: str
    labels: List[str]
    created_at: str
    updated_at: str
    state: str
    reporter_type: str  # 'bootstrap-user', 'manual-user', 'maintainer'
    platform: Optional[str] = None
    project_type: Optional[str] = None
    severity: Optional[str] = None
    component: Optional[str] = None

@dataclass
class IssuePattern:
    """Represents a detected pattern across multiple issues."""
    pattern_id: str
    description: str
    frequency: int
    affected_platforms: List[str]
    severity_distribution: Dict[str, int]
    sample_issues: List[int]
    root_cause: Optional[str] = None
    proposed_solution: Optional[str] = None

@dataclass
class DevelopmentTask:
    """Represents a generated development task."""
    task_id: str
    title: str
    description: str
    task_type: str  # 'bug_fix', 'enhancement', 'documentation', 'optimization'
    priority: str  # 'high', 'medium', 'low'
    effort: str  # 'small', 'medium', 'large'
    source_issues: List[int]
    success_criteria: List[str]
    affected_components: List[str]
    estimated_completion: Optional[str] = None

class GitHubIssuesProcessor:
    """Main processor for GitHub Issues analysis and task generation."""
    
    def __init__(self, repo: str = "Dub1n/dss", data_dir: Path = None):
        """Initialize the processor.
        
        Args:
            repo: GitHub repository in format "owner/repo"
            data_dir: Directory to store analysis data (defaults to meta/development_queue)
        """
        self.repo = repo
        self.data_dir = data_dir or (project_root / "meta" / "development_queue")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern detection rules
        self.pattern_rules = self._load_pattern_rules()
        
        # Task generation rules
        self.task_rules = self._load_task_generation_rules()
    
    def fetch_issues(self, days_back: int = 30, labels: List[str] = None) -> List[IssueData]:
        """Fetch issues from GitHub repository.
        
        Args:
            days_back: Number of days to look back for issues
            labels: Specific labels to filter by
            
        Returns:
            List of IssueData objects
        """
        try:
            # Build GitHub CLI command
            cmd = [
                'gh', 'issue', 'list',
                '--repo', self.repo,
                '--limit', '100',
                '--json', 'number,title,body,labels,createdAt,updatedAt,state',
                '--state', 'all'
            ]
            
            # Add label filter if specified
            if labels:
                for label in labels:
                    cmd.extend(['--label', label])
            
            # Execute command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"Error fetching issues: {result.stderr}")
                return []
            
            # Parse JSON response
            issues_json = json.loads(result.stdout)
            issues = []
            
            # Convert to IssueData objects
            for issue_data in issues_json:
                # Extract labels
                labels_list = [label['name'] for label in issue_data.get('labels', [])]
                
                # Classify reporter type
                reporter_type = self._classify_reporter_type(issue_data, labels_list)
                
                # Extract metadata from labels
                platform = self._extract_platform(labels_list)
                project_type = self._extract_project_type(labels_list)
                severity = self._extract_severity(labels_list)
                component = self._extract_component(labels_list)
                
                issue = IssueData(
                    number=issue_data['number'],
                    title=issue_data['title'],
                    body=issue_data.get('body', ''),
                    labels=labels_list,
                    created_at=issue_data['createdAt'],
                    updated_at=issue_data['updatedAt'],
                    state=issue_data['state'],
                    reporter_type=reporter_type,
                    platform=platform,
                    project_type=project_type,
                    severity=severity,
                    component=component
                )
                
                # Filter by date if specified
                if days_back:
                    created_date = datetime.fromisoformat(issue.created_at.replace('Z', '+00:00'))
                    cutoff_date = datetime.now().replace(tzinfo=created_date.tzinfo) - timedelta(days=days_back)
                    
                    if created_date >= cutoff_date:
                        issues.append(issue)
                else:
                    issues.append(issue)
            
            return issues
            
        except subprocess.TimeoutExpired:
            print("Timeout fetching issues from GitHub")
            return []
        except json.JSONDecodeError:
            print("Error parsing GitHub response")
            return []
        except Exception as e:
            print(f"Unexpected error fetching issues: {e}")
            return []
    
    def analyze_patterns(self, issues: List[IssueData]) -> List[IssuePattern]:
        """Analyze issues to detect patterns.
        
        Args:
            issues: List of issues to analyze
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Group issues by various dimensions for pattern detection
        
        # 1. Installation report patterns
        installation_reports = [i for i in issues if 'installation-report' in i.labels]
        if installation_reports:
            patterns.extend(self._analyze_installation_patterns(installation_reports))
        
        # 2. Platform-specific patterns
        platform_groups = defaultdict(list)
        for issue in issues:
            if issue.platform:
                platform_groups[issue.platform].append(issue)
        
        for platform, platform_issues in platform_groups.items():
            if len(platform_issues) >= 3:  # Need at least 3 issues to identify a pattern
                patterns.extend(self._analyze_platform_patterns(platform, platform_issues))
        
        # 3. Component-specific patterns
        component_groups = defaultdict(list)
        for issue in issues:
            if issue.component:
                component_groups[issue.component].append(issue)
        
        for component, component_issues in component_groups.items():
            if len(component_issues) >= 2:
                patterns.extend(self._analyze_component_patterns(component, component_issues))
        
        # 4. Text-based pattern detection (common error messages, etc.)
        patterns.extend(self._analyze_text_patterns(issues))
        
        return patterns
    
    def generate_tasks(self, patterns: List[IssuePattern], issues: List[IssueData]) -> List[DevelopmentTask]:
        """Generate development tasks based on detected patterns and issues.
        
        Args:
            patterns: Detected issue patterns
            issues: Original issues
            
        Returns:
            List of generated development tasks
        """
        tasks = []
        
        for pattern in patterns:
            # Calculate priority based on pattern characteristics
            priority = self._calculate_task_priority(pattern, issues)
            
            # Determine task type and effort
            task_type = self._determine_task_type(pattern)
            effort = self._estimate_effort(pattern)
            
            # Generate task
            task = DevelopmentTask(
                task_id=f"task_{pattern.pattern_id}_{datetime.now().strftime('%Y%m%d')}",
                title=f"Address {pattern.description}",
                description=self._generate_task_description(pattern),
                task_type=task_type,
                priority=priority,
                effort=effort,
                source_issues=pattern.sample_issues,
                success_criteria=self._generate_success_criteria(pattern),
                affected_components=self._identify_affected_components(pattern)
            )
            
            tasks.append(task)
        
        # Also generate tasks for high-priority individual issues that don't fit patterns
        individual_tasks = self._generate_individual_tasks(issues, patterns)
        tasks.extend(individual_tasks)
        
        return tasks
    
    def save_analysis(self, issues: List[IssueData], patterns: List[IssuePattern], 
                     tasks: List[DevelopmentTask]):
        """Save analysis results to files.
        
        Args:
            issues: Analyzed issues
            patterns: Detected patterns
            tasks: Generated tasks
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw issues data
        issues_file = self.data_dir / f"issues_analysis_{timestamp}.json"
        with open(issues_file, 'w') as f:
            json.dump([asdict(issue) for issue in issues], f, indent=2, default=str)
        
        # Save patterns analysis
        patterns_file = self.data_dir / f"patterns_analysis_{timestamp}.md"
        self._write_patterns_report(patterns, patterns_file)
        
        # Save generated tasks
        self._distribute_tasks_by_priority(tasks)
        
        # Update summary files
        self._update_summary_files(issues, patterns, tasks)
    
    def _classify_reporter_type(self, issue_data: Dict, labels: List[str]) -> str:
        """Classify the type of issue reporter."""
        if 'installation-report' in labels:
            return 'bootstrap-user'
        
        # Could add more sophisticated logic here
        # e.g., checking if reporter is a maintainer, frequent contributor, etc.
        return 'manual-user'
    
    def _extract_platform(self, labels: List[str]) -> Optional[str]:
        """Extract platform from labels."""
        platform_labels = [l for l in labels if l.startswith('platform-')]
        return platform_labels[0].replace('platform-', '') if platform_labels else None
    
    def _extract_project_type(self, labels: List[str]) -> Optional[str]:
        """Extract project type from labels."""
        project_labels = [l for l in labels if l.startswith('project-')]
        return project_labels[0].replace('project-', '') if project_labels else None
    
    def _extract_severity(self, labels: List[str]) -> Optional[str]:
        """Extract severity from labels."""
        severity_labels = ['critical', 'high-priority', 'medium-priority', 'low-priority']
        for label in labels:
            if label in severity_labels:
                return label
        return None
    
    def _extract_component(self, labels: List[str]) -> Optional[str]:
        """Extract component from labels."""
        component_labels = ['bootstrap', 'cursor-integration', 'file-organization', 'documentation']
        for label in labels:
            if label in component_labels:
                return label
        return None
    
    def _analyze_installation_patterns(self, reports: List[IssueData]) -> List[IssuePattern]:
        """Analyze patterns in installation reports."""
        patterns = []
        
        # Pattern: Platform-specific installation failures
        platform_failures = defaultdict(list)
        for report in reports:
            if 'fail' in report.title.lower() or 'error' in report.body.lower():
                platform_failures[report.platform or 'unknown'].append(report)
        
        for platform, failures in platform_failures.items():
            if len(failures) >= 2:
                pattern = IssuePattern(
                    pattern_id=f"install_fail_{platform}",
                    description=f"Installation failures on {platform}",
                    frequency=len(failures),
                    affected_platforms=[platform],
                    severity_distribution={'high': len(failures)},
                    sample_issues=[f.number for f in failures[:3]]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _analyze_platform_patterns(self, platform: str, issues: List[IssueData]) -> List[IssuePattern]:
        """Analyze patterns specific to a platform."""
        patterns = []
        
        # Look for common keywords in platform-specific issues
        common_keywords = self._extract_common_keywords([i.title + ' ' + i.body for i in issues])
        
        if common_keywords:
            pattern = IssuePattern(
                pattern_id=f"platform_{platform}_common",
                description=f"Common {platform} issues: {', '.join(common_keywords[:3])}",
                frequency=len(issues),
                affected_platforms=[platform],
                severity_distribution=self._count_severities(issues),
                sample_issues=[i.number for i in issues[:3]]
            )
            patterns.append(pattern)
        
        return patterns
    
    def _analyze_component_patterns(self, component: str, issues: List[IssueData]) -> List[IssuePattern]:
        """Analyze patterns for a specific component."""
        patterns = []
        
        if len(issues) >= 2:
            pattern = IssuePattern(
                pattern_id=f"component_{component}",
                description=f"{component.title()} component issues",
                frequency=len(issues),
                affected_platforms=list(set(i.platform for i in issues if i.platform)),
                severity_distribution=self._count_severities(issues),
                sample_issues=[i.number for i in issues]
            )
            patterns.append(pattern)
        
        return patterns
    
    def _analyze_text_patterns(self, issues: List[IssueData]) -> List[IssuePattern]:
        """Analyze text patterns across issue titles and bodies."""
        patterns = []
        
        # Look for common error messages
        error_patterns = [
            r'timeout.*expired',
            r'permission.*denied',
            r'file.*not.*found',
            r'unicode.*error',
            r'connection.*failed'
        ]
        
        for error_pattern in error_patterns:
            matching_issues = []
            for issue in issues:
                text = (issue.title + ' ' + issue.body).lower()
                if re.search(error_pattern, text):
                    matching_issues.append(issue)
            
            if len(matching_issues) >= 2:
                pattern = IssuePattern(
                    pattern_id=f"error_{error_pattern.replace('.*', '_').replace('[', '').replace(']', '')}",
                    description=f"Common error pattern: {error_pattern}",
                    frequency=len(matching_issues),
                    affected_platforms=list(set(i.platform for i in matching_issues if i.platform)),
                    severity_distribution=self._count_severities(matching_issues),
                    sample_issues=[i.number for i in matching_issues[:3]]
                )
                patterns.append(pattern)
        
        return patterns
    
    def _calculate_task_priority(self, pattern: IssuePattern, issues: List[IssueData]) -> str:
        """Calculate task priority based on pattern characteristics."""
        # Simple priority calculation
        score = 0
        
        # Frequency weight
        score += pattern.frequency * 2
        
        # Platform diversity bonus
        score += len(pattern.affected_platforms) * 1.5
        
        # Severity weight
        severity_weights = {'critical': 10, 'high-priority': 7, 'medium-priority': 4, 'low-priority': 1}
        for severity, count in pattern.severity_distribution.items():
            score += count * severity_weights.get(severity, 1)
        
        if score >= 20:
            return 'high'
        elif score >= 10:
            return 'medium'
        else:
            return 'low'
    
    def _determine_task_type(self, pattern: IssuePattern) -> str:
        """Determine the type of task needed for a pattern."""
        if 'fail' in pattern.description.lower() or 'error' in pattern.description.lower():
            return 'bug_fix'
        elif 'install' in pattern.description.lower():
            return 'enhancement'
        elif 'document' in pattern.description.lower():
            return 'documentation'
        else:
            return 'enhancement'
    
    def _estimate_effort(self, pattern: IssuePattern) -> str:
        """Estimate effort required for addressing a pattern."""
        if pattern.frequency >= 10 or len(pattern.affected_platforms) >= 3:
            return 'large'
        elif pattern.frequency >= 5 or len(pattern.affected_platforms) >= 2:
            return 'medium'
        else:
            return 'small'
    
    def _generate_task_description(self, pattern: IssuePattern) -> str:
        """Generate a detailed task description."""
        return f"""
## Problem Statement
{pattern.description} affecting {pattern.frequency} reported cases across platforms: {', '.join(pattern.affected_platforms)}.

## Impact Analysis
- **Frequency**: {pattern.frequency} occurrences
- **Platform Distribution**: {', '.join(pattern.affected_platforms)}
- **Severity Breakdown**: {pattern.severity_distribution}

## Pattern Details
{pattern.root_cause or 'Root cause analysis needed'}

## Proposed Approach
{pattern.proposed_solution or 'Solution approach to be determined during investigation'}
"""
    
    def _generate_success_criteria(self, pattern: IssuePattern) -> List[str]:
        """Generate success criteria for a task."""
        criteria = [
            f"Reduce occurrence frequency by at least 50%",
            f"Address root cause identified in pattern analysis"
        ]
        
        if len(pattern.affected_platforms) > 1:
            criteria.append("Ensure fix works across all affected platforms")
        
        return criteria
    
    def _identify_affected_components(self, pattern: IssuePattern) -> List[str]:
        """Identify which components are affected by a pattern."""
        components = []
        
        if 'install' in pattern.description.lower():
            components.append('meta/scripts/dss_bootstrap.py')
        if 'cursor' in pattern.description.lower():
            components.append('meta/cursor/')
        if 'document' in pattern.description.lower():
            components.append('docs/')
        
        return components
    
    def _generate_individual_tasks(self, issues: List[IssueData], patterns: List[IssuePattern]) -> List[DevelopmentTask]:
        """Generate tasks for high-priority individual issues not covered by patterns."""
        tasks = []
        
        # Issues already covered by patterns
        covered_issue_numbers = set()
        for pattern in patterns:
            covered_issue_numbers.update(pattern.sample_issues)
        
        # Find high-priority individual issues
        for issue in issues:
            if (issue.number not in covered_issue_numbers and 
                issue.severity in ['critical', 'high-priority']):
                
                task = DevelopmentTask(
                    task_id=f"individual_{issue.number}_{datetime.now().strftime('%Y%m%d')}",
                    title=f"Address issue #{issue.number}: {issue.title[:50]}...",
                    description=f"Individual high-priority issue:\n\n{issue.body[:200]}...",
                    task_type=self._classify_issue_type(issue),
                    priority='high' if issue.severity == 'critical' else 'medium',
                    effort='small',
                    source_issues=[issue.number],
                    success_criteria=[f"Resolve issue #{issue.number}"],
                    affected_components=self._guess_affected_components(issue)
                )
                tasks.append(task)
        
        return tasks
    
    def _classify_issue_type(self, issue: IssueData) -> str:
        """Classify an individual issue type."""
        if 'bug' in issue.labels:
            return 'bug_fix'
        elif 'enhancement' in issue.labels:
            return 'enhancement'
        elif 'documentation' in issue.labels:
            return 'documentation'
        else:
            return 'enhancement'
    
    def _guess_affected_components(self, issue: IssueData) -> List[str]:
        """Guess which components are affected by an issue."""
        components = []
        text = (issue.title + ' ' + issue.body).lower()
        
        if any(word in text for word in ['bootstrap', 'install', 'setup']):
            components.append('meta/scripts/dss_bootstrap.py')
        if any(word in text for word in ['cursor', 'assistant', 'ai']):
            components.append('meta/cursor/')
        if any(word in text for word in ['document', 'readme', 'guide']):
            components.append('docs/')
        
        return components
    
    def _extract_common_keywords(self, texts: List[str], min_frequency: int = 2) -> List[str]:
        """Extract common keywords from a list of texts."""
        # Simple keyword extraction
        words = []
        for text in texts:
            # Basic text cleaning and word extraction
            clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
            words.extend(clean_text.split())
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Filter out common stop words and short words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'cannot', 'this', 'that', 'these', 'those'}
        
        common_keywords = []
        for word, count in word_counts.most_common():
            if (count >= min_frequency and 
                len(word) > 3 and 
                word not in stop_words):
                common_keywords.append(word)
        
        return common_keywords[:10]  # Return top 10
    
    def _count_severities(self, issues: List[IssueData]) -> Dict[str, int]:
        """Count severity distribution in a list of issues."""
        severity_counts = defaultdict(int)
        for issue in issues:
            severity = issue.severity or 'unknown'
            severity_counts[severity] += 1
        return dict(severity_counts)
    
    def _write_patterns_report(self, patterns: List[IssuePattern], output_file: Path):
        """Write patterns analysis to a markdown file."""
        with open(output_file, 'w') as f:
            f.write(f"# GitHub Issues Pattern Analysis\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Total Patterns Detected**: {len(patterns)}\n\n")
            
            for pattern in patterns:
                f.write(f"## Pattern: {pattern.description}\n\n")
                f.write(f"- **Pattern ID**: {pattern.pattern_id}\n")
                f.write(f"- **Frequency**: {pattern.frequency} occurrences\n")
                f.write(f"- **Affected Platforms**: {', '.join(pattern.affected_platforms)}\n")
                f.write(f"- **Severity Distribution**: {pattern.severity_distribution}\n")
                f.write(f"- **Sample Issues**: #{', #'.join(map(str, pattern.sample_issues))}\n")
                
                if pattern.root_cause:
                    f.write(f"- **Root Cause**: {pattern.root_cause}\n")
                if pattern.proposed_solution:
                    f.write(f"- **Proposed Solution**: {pattern.proposed_solution}\n")
                
                f.write("\n")
    
    def _distribute_tasks_by_priority(self, tasks: List[DevelopmentTask]):
        """Distribute tasks into priority-based files."""
        priority_files = {
            'high': self.data_dir / 'high_priority_tasks.md',
            'medium': self.data_dir / 'medium_priority_tasks.md',
            'low': self.data_dir / 'low_priority_tasks.md'
        }
        
        # Group tasks by priority
        priority_groups = defaultdict(list)
        for task in tasks:
            priority_groups[task.priority].append(task)
        
        # Write to files
        for priority, task_list in priority_groups.items():
            if priority in priority_files:
                self._append_tasks_to_file(task_list, priority_files[priority])
    
    def _append_tasks_to_file(self, tasks: List[DevelopmentTask], file_path: Path):
        """Append tasks to a priority file."""
        # Read existing content
        existing_content = ""
        if file_path.exists():
            existing_content = file_path.read_text()
        
        # Append new tasks
        with open(file_path, 'w') as f:
            if not existing_content:
                f.write(f"# {file_path.stem.replace('_', ' ').title()}\n\n")
                f.write(f"Generated and updated by GitHub Issues Processor\n\n")
            else:
                f.write(existing_content)
                if not existing_content.endswith('\n\n'):
                    f.write('\n\n')
            
            f.write(f"## Tasks Added: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for task in tasks:
                f.write(f"### {task.title}\n\n")
                f.write(f"**Task ID**: {task.task_id}\n")
                f.write(f"**Type**: {task.task_type}\n")
                f.write(f"**Effort**: {task.effort}\n")
                f.write(f"**Source Issues**: #{', #'.join(map(str, task.source_issues))}\n\n")
                f.write(f"{task.description}\n\n")
                f.write(f"**Success Criteria**:\n")
                for criteria in task.success_criteria:
                    f.write(f"- [ ] {criteria}\n")
                f.write("\n")
                f.write(f"**Affected Components**: {', '.join(task.affected_components)}\n\n")
                f.write("---\n\n")
    
    def _update_summary_files(self, issues: List[IssueData], patterns: List[IssuePattern], tasks: List[DevelopmentTask]):
        """Update summary files with latest analysis."""
        summary_file = self.data_dir / 'analysis_summary.md'
        
        with open(summary_file, 'w') as f:
            f.write("# DSS Development Queue Summary\n\n")
            f.write(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Recent Analysis\n\n")
            f.write(f"- **Issues Analyzed**: {len(issues)}\n")
            f.write(f"- **Patterns Detected**: {len(patterns)}\n")
            f.write(f"- **Tasks Generated**: {len(tasks)}\n\n")
            
            # Task summary by priority
            priority_counts = Counter(task.priority for task in tasks)
            f.write("## Task Distribution\n\n")
            for priority in ['high', 'medium', 'low']:
                count = priority_counts.get(priority, 0)
                f.write(f"- **{priority.title()} Priority**: {count} tasks\n")
            
            f.write("\n## Top Patterns\n\n")
            # Sort patterns by frequency
            sorted_patterns = sorted(patterns, key=lambda p: p.frequency, reverse=True)
            for pattern in sorted_patterns[:5]:
                f.write(f"- **{pattern.description}**: {pattern.frequency} occurrences\n")
    
    def _load_pattern_rules(self) -> Dict:
        """Load pattern detection rules (placeholder for future configuration)."""
        return {}
    
    def _load_task_generation_rules(self) -> Dict:
        """Load task generation rules (placeholder for future configuration)."""
        return {}


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process GitHub Issues for DSS self-development")
    parser.add_argument('--repo', default='Dub1n/dss', help='GitHub repository (owner/repo)')
    parser.add_argument('--days-back', type=int, default=30, help='Days to look back for issues')
    parser.add_argument('--labels', nargs='*', help='Filter by specific labels')
    parser.add_argument('--analyze-reports', action='store_true', help='Focus on installation reports')
    parser.add_argument('--generate-tasks', action='store_true', help='Generate development tasks')
    parser.add_argument('--output-dir', help='Output directory for results')
    
    args = parser.parse_args()
    
    # Initialize processor
    output_dir = Path(args.output_dir) if args.output_dir else None
    processor = GitHubIssuesProcessor(repo=args.repo, data_dir=output_dir)
    
    # Determine labels to filter by
    labels = args.labels or []
    if args.analyze_reports:
        labels.append('installation-report')
    
    print(f"Fetching issues from {args.repo}...")
    issues = processor.fetch_issues(days_back=args.days_back, labels=labels)
    print(f"Found {len(issues)} issues")
    
    if not issues:
        print("No issues found to analyze")
        return
    
    print("Analyzing patterns...")
    patterns = processor.analyze_patterns(issues)
    print(f"Detected {len(patterns)} patterns")
    
    tasks = []
    if args.generate_tasks:
        print("Generating development tasks...")
        tasks = processor.generate_tasks(patterns, issues)
        print(f"Generated {len(tasks)} tasks")
    
    print("Saving analysis results...")
    processor.save_analysis(issues, patterns, tasks)
    
    print(f"Analysis complete! Results saved to {processor.data_dir}")
    
    # Print summary
    if patterns:
        print("\nTop patterns detected:")
        for pattern in sorted(patterns, key=lambda p: p.frequency, reverse=True)[:3]:
            print(f"  - {pattern.description}: {pattern.frequency} occurrences")
    
    if tasks:
        priority_counts = Counter(task.priority for task in tasks)
        print(f"\nTasks generated:")
        for priority in ['high', 'medium', 'low']:
            count = priority_counts.get(priority, 0)
            if count > 0:
                print(f"  - {priority.title()} priority: {count} tasks")


if __name__ == '__main__':
    main() 