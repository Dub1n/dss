#!/usr/bin/env python3
"""
Dev Tasks Table Generator
Scans dev/ folder and creates a Markdown table view of tasks with their frontmatter
"""

import os
import re
import yaml
import argparse
from pathlib import Path
from datetime import datetime

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match frontmatter pattern
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {}

def scan_dev_tasks():
    """Scan dev/ folder for markdown files and extract metadata"""
    dev_path = Path("dev")
    tasks = []
    
    for md_file in dev_path.glob("**/*.md"):
        if md_file.name == "README.md" or "dev_table_output" in md_file.name:
            continue
            
        frontmatter = extract_frontmatter(md_file)
        
        # Get relative path for display
        rel_path = str(md_file.relative_to(dev_path))
        
        task = {
            'file': rel_path,
            'filename': md_file.stem,  # Just the filename without extension
            'status': frontmatter.get('status', 'N/A'),
            'tags': ', '.join(frontmatter.get('tags', [])),
            'provides': ', '.join(frontmatter.get('provides', [])),
            'requires': ', '.join(frontmatter.get('requires', []))
        }
        tasks.append(task)
    
    return tasks

def calculate_display_width(link_text):
    """
    Calculate the display width of an MDC link in Cursor.
    Cursor shows MDC links as @filename, so width is filename length + 1
    """
    # Extract the filename from the MDC link [filename](mdc:path)
    match = re.match(r'\[(.*?)\]', link_text)
    if match:
        filename = match.group(1)
        # Cursor shows as @filename
        return len(filename) + 1  # +1 for the @ symbol
    return len(link_text)  # Fallback if not a link

def pad_link_cell(link_text, cell_width):
    """
    Add the right amount of padding after a link to ensure consistent cell width
    regardless of the displayed link length in Cursor.
    """
    display_width = calculate_display_width(link_text)
    # Calculate how many spaces needed after the link to reach cell_width
    # For the longest entry (cell_width == display_width), add no extra space
    padding = max(0, cell_width - display_width)
    return link_text + " " * padding

def sort_tasks(tasks, sort_key='status'):
    """Sort tasks by the specified key"""
    # Custom sorting order for status
    status_order = {
        'IN PROGRESS': 0,
        'active': 0,
        'BLOCKED': 1, 
        'NOT STARTED': 2,
        'N/A': 3,
        'DEFERRED': 4,
        'COMPLETED': 5
    }
    
    if sort_key == 'status':
        return sorted(tasks, key=lambda x: (
            status_order.get(x['status'], 99),  # Sort by status order first
            x['filename'].lower()                # Then alphabetically by filename
        ))
    else:
        # Default to sort by filename
        return sorted(tasks, key=lambda x: x['filename'].lower())

def generate_markdown_table(tasks, sort_by='status', extra_columns=None):
    """Generate a Markdown table from tasks data"""
    if extra_columns is None:
        extra_columns = []
        
    # Sort tasks
    sorted_tasks = sort_tasks(tasks, sort_by)
    
    lines = []
    
    # Add frontmatter with proper YAML formatting
    lines.append("---")
    lines.append("tags: [dev_overview, generated, table]")
    lines.append("provides: [dev_tasks_overview]")
    lines.append("requires: []")
    lines.append(f"generated: '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")
    lines.append("---")
    lines.append("")
    lines.append("# Dev Tasks Overview")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total tasks: {len(tasks)}")
    if sort_by:
        lines.append(f"Sorted by: {sort_by}")
    lines.append("")
    
    # First, calculate the maximum display width needed for the filename column
    max_filename_display_width = 0
    for task in tasks:
        filename = task['filename']
        file_path = task['file'].replace('\\', '/')
        filename_link = f"[{filename}](mdc:dev/{file_path})"
        display_width = calculate_display_width(filename_link)
        max_filename_display_width = max(max_filename_display_width, display_width)
    
    # Define column widths - adjust File header to match content exactly
    file_col_width = max_filename_display_width  # Exact width needed, no extra padding
    col_widths = [file_col_width, 10, 40]  # [File, Status, Tags]
    
    # Add extra columns if specified
    headers = ["File", "Status", "Tags"]
    if "provides" in extra_columns:
        headers.append("Provides")
        col_widths.append(30)
    if "requires" in extra_columns:
        headers.append("Requires")
        col_widths.append(30)
    
    # Create header row
    header_parts = []
    for i, header in enumerate(headers):
        header_parts.append(header.ljust(col_widths[i]))
    header_row = "| " + " | ".join(header_parts) + " |"
    lines.append(header_row)
    
    # Add separator row
    separator_parts = []
    for width in col_widths:
        separator_parts.append("-".ljust(width, "-"))
    separator_row = "| " + " | ".join(separator_parts) + " |"
    lines.append(separator_row)
    
    # Group tasks by status for visual separation if sorting by status
    current_status = None
    status_headers = []
    
    # Add rows with careful formatting and consistent cell padding
    for task in sorted_tasks:
        # Add status header if this is a new status group
        if sort_by == 'status' and task['status'] != current_status:
            current_status = task['status']
            if current_status != 'N/A':
                status_headers.append(len(lines))  # Remember position for later styling
            
        # Create the MDC link for the filename
        filename = task['filename']
        file_path = task['file'].replace('\\', '/')
        filename_link = f"[{filename}](mdc:dev/{file_path})"
        
        # Pad the filename cell to have consistent visual width
        padded_filename = pad_link_cell(filename_link, max_filename_display_width)
        
        # Prepare row cells
        row_cells = [padded_filename, task['status'].ljust(col_widths[1])]
        
        # Handle tags
        tags = task['tags']
        if len(tags) > col_widths[2] - 3:
            tags = tags[:col_widths[2]-6] + "..."
        row_cells.append(tags.ljust(col_widths[2]))
        
        # Add extra columns if specified
        if "provides" in extra_columns:
            provides = task['provides']
            if len(provides) > col_widths[3] - 3:
                provides = provides[:col_widths[3]-6] + "..."
            row_cells.append(provides.ljust(col_widths[3]))
        
        if "requires" in extra_columns:
            requires = task['requires']
            if len(requires) > col_widths[4] - 3:
                requires = requires[:col_widths[4]-6] + "..."
            row_cells.append(requires.ljust(col_widths[4]))
        
        # Build the row
        row = "| " + " | ".join(row_cells) + " |"
        lines.append(row)
    
    # Add a bit of space after the table
    lines.append("")
    
    # Add status legend if sorting by status
    if sort_by == 'status' and status_headers:
        lines.append("## Status Groups")
        lines.append("")
        # Add legend for status groups
        statuses_seen = []
        for task in sorted_tasks:
            if task['status'] not in statuses_seen and task['status'] != 'N/A':
                statuses_seen.append(task['status'])
                lines.append(f"- **{task['status']}**: Tasks currently in {task['status'].lower()} state")
        lines.append("")
    
    lines.append("## Details Reference")
    lines.append("")
    
    # Add detailed reference
    for task in sorted_tasks:
        # Normalize path with forward slashes
        file_path = task['file'].replace('\\', '/')
        
        # Create short MDC link
        lines.append(f"### [{task['filename']}](mdc:dev/{file_path})")
        lines.append(f"- **Path**: `{task['file']}`")
        lines.append(f"- **Status**: {task['status']}")
        lines.append(f"- **Tags**: {task['tags']}")
        if task['provides']:
            lines.append(f"- **Provides**: {task['provides']}")
        if task['requires']:
            lines.append(f"- **Requires**: {task['requires']}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*This file is auto-generated. Run `python dev/dev_table.py` to update.*")
    lines.append("*For more columns, run with `--extra-columns provides requires`*")
    
    return '\n'.join(lines)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a table of dev tasks')
    parser.add_argument('--sort', choices=['status', 'filename'], default='status',
                        help='Sort by status (default) or filename')
    parser.add_argument('--extra-columns', nargs='+', choices=['provides', 'requires'],
                        help='Additional columns to include')
    parser.add_argument('--output', default='dev/dev_table_output.mdc',
                        help='Output file path (default: dev/dev_table_output.mdc)')
    
    args = parser.parse_args()
    
    print("🔧 Generating Dev Tasks Overview...")
    
    tasks = scan_dev_tasks()
    
    if not tasks:
        print("No tasks found in dev/ folder")
        return
    
    # Generate markdown content
    markdown_content = generate_markdown_table(
        tasks, 
        sort_by=args.sort, 
        extra_columns=args.extra_columns
    )
    
    # Write to file with .mdc extension for Cursor-specific features
    output_file = Path(args.output)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Table written to: {output_file}")
    print(f"📊 Total tasks: {len(tasks)}")
    print(f"🔄 Sorted by: {args.sort}")
    if args.extra_columns:
        print(f"➕ Extra columns: {', '.join(args.extra_columns)}")
    
    print("\nOpen the output file in Cursor to view your tasks table!")

if __name__ == "__main__":
    main() 