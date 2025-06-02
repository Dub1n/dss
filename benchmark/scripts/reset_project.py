#!/usr/bin/env python3
"""
Reset benchmark project to clean state while preserving results.
This script cleans up files created during benchmark testing and archives rules.
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

def generate_archive_name() -> str:
    """Generate a unique archive name with current timestamp."""
    now = datetime.now()
    # Use kebab-case format: v{counter}_{dd-mm-yy}
    date_str = now.strftime("%d-%m-%y")
    
    # Find next version number by checking existing archives
    repo_root = Path.cwd()
    rules_store = repo_root / "rules_store"
    existing_versions = []
    
    if rules_store.exists():
        for item in rules_store.iterdir():
            if item.is_dir() and item.name.startswith("v") and "_" in item.name:
                try:
                    version_part = item.name.split("_")[0][1:]  # Remove 'v' prefix
                    existing_versions.append(int(version_part))
                except (ValueError, IndexError):
                    continue
    
    next_version = max(existing_versions, default=0) + 1
    return f"v{next_version}_{date_str}"

def is_result_file(path: Path) -> bool:
    """Check if a file is a benchmark result file that should be preserved."""
    return (path.is_file() and 
            path.name.startswith('task_') and 
            path.suffix in ['.json', '.md'])

def organize_rules_before_archive() -> Optional[str]:
    """Organize rules directory structure before archiving."""
    repo_root = Path.cwd()
    cursor_rules = repo_root / ".cursor" / "rules"
    
    if not cursor_rules.exists():
        return None
        
    contents = list(cursor_rules.iterdir())
    # Filter out result files (task_*_scores.json, task_*_report.md)
    non_result_contents = [item for item in contents if not is_result_file(item)]
    
    # Case 1: Loose files/folders (config, guidelines, workflows, etc.)
    if any(item.name in ['config', 'guidelines', 'workflows'] or 
           (item.is_file() and item.suffix == '.mdc') 
           for item in non_result_contents):
        return wrap_loose_rules(cursor_rules, non_result_contents)
    
    # Case 2: Single folder named "rules"
    elif (len(non_result_contents) == 1 and 
          non_result_contents[0].is_dir() and 
          non_result_contents[0].name == "rules"):
        return rename_generic_rules_folder(cursor_rules, non_result_contents[0])
    
    # Case 3 & 4: Already properly organized (unique name or same as rules_store)
    return None

def wrap_loose_rules(cursor_rules: Path, non_result_contents: List[Path]) -> str:
    """Wrap loose rule files in a properly named folder."""
    new_name = generate_archive_name()
    new_folder = cursor_rules / new_name
    
    # Create new folder
    new_folder.mkdir(exist_ok=True)
    
    # Move all non-result items into the new folder
    for item in non_result_contents:
        dest_path = new_folder / item.name
        if item.is_dir():
            shutil.move(str(item), str(dest_path))
        else:
            shutil.move(str(item), str(dest_path))
    
    return f"Wrapped loose rules in folder: {new_name}"

def rename_generic_rules_folder(cursor_rules: Path, rules_folder: Path) -> str:
    """Rename 'rules' folder to proper archive name."""
    new_name = generate_archive_name()
    new_path = cursor_rules / new_name
    
    # Rename the folder
    rules_folder.rename(new_path)
    
    return f"Renamed 'rules' folder to: {new_name}"

def archive_current_rules() -> Optional[str]:
    """Archive current rules to rules_store with proper naming."""
    repo_root = Path.cwd()
    current_rules_dir = repo_root / ".cursor" / "rules"
    rules_store = repo_root / "rules_store"
    
    if not current_rules_dir.exists():
        print("⚠️  No current rules directory found - skipping archive")
        return None
    
    # Generate unique archive name
    archive_name = generate_archive_name()
    archive_path = rules_store / archive_name
    
    # Create rules_store if it doesn't exist
    rules_store.mkdir(exist_ok=True)
    
    # Handle the naming convention logic from TODO
    rules_contents = list(current_rules_dir.iterdir())
    
    # Check if the current rules directory structure needs reorganization
    if len(rules_contents) == 1 and rules_contents[0].is_dir() and rules_contents[0].name != "rules":
        # Case: folder INSIDE .cursor/rules has a name other than "rules" (and is unique)
        # Create new folder inside it called "rules" and move all contents inside that
        unique_folder = rules_contents[0]
        archive_path.mkdir(exist_ok=True)
        
        # Copy the unique folder to archive
        unique_archive_path = archive_path / unique_folder.name
        shutil.copytree(unique_folder, unique_archive_path)
        
        # Create rules subfolder and move contents
        rules_subfolder = unique_archive_path / "rules"
        rules_subfolder.mkdir(exist_ok=True)
        
        for item in unique_archive_path.iterdir():
            if item.name != "rules":
                shutil.move(item, rules_subfolder / item.name)
                
    else:
        # Case: folder is just called "rules" or multiple items
        # Place folder inside another one with unique name
        archive_path.mkdir(exist_ok=True)
        rules_archive_path = archive_path / "rules"
        shutil.copytree(current_rules_dir, rules_archive_path)
    
    print(f"📦 Archived current rules to: rules_store/{archive_name}")
    return archive_name

def collect_recent_results() -> List[Dict]:
    """Collect recent benchmark results for the archived rules."""
    repo_root = Path.cwd()
    
    # Check .cursor/rules/ for result files (no subfolder)
    results_dir = repo_root / ".cursor" / "rules"
    
    results = []
    # Look for recent result files (from last 7 days)
    cutoff_time = datetime.now().timestamp() - (7 * 24 * 60 * 60)
    
    if not results_dir.exists():
        return results
        
    # Look for score and report files directly in .cursor/rules/
    for result_file in results_dir.glob("task_*_scores.json"):
        try:
            if result_file.stat().st_mtime > cutoff_time:
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                    results.append({
                        'file': result_file.name,
                        'source_path': result_file,
                        'data': result_data
                    })
        except (json.JSONDecodeError, FileNotFoundError):
            continue
    
    # Also look for .md report files
    for result_file in results_dir.glob("task_*_report.md"):
        try:
            if result_file.stat().st_mtime > cutoff_time:
                results.append({
                    'file': result_file.name,
                    'source_path': result_file,
                    'data': {'type': 'report'}  # Simple marker for report files
                })
        except FileNotFoundError:
            continue
    
    return results

def update_comparison_table(archive_name: str, results: List[Dict]) -> None:
    """Update or create benchmark comparison table."""
    repo_root = Path.cwd()
    comparison_file = repo_root / "BENCHMARK_COMPARISON.md"
    
    # Calculate summary stats from results
    total_score = 0
    task_count = 0
    rule_variant = "unknown"
    task_scores = {}  # Task ID -> score mapping
    task_summaries = {}  # Task ID -> executive summary mapping
    
    for result in results:
        data = result['data']
        if 'total_score' in data:
            total_score += data['total_score']
            task_count += 1
            
            # Extract task ID and score for table
            if 'benchmark_run' in data and 'task_id' in data['benchmark_run']:
                task_id = data['benchmark_run']['task_id']
                task_scores[task_id] = data['total_score']
        
        # Extract executive summary from report files
        if data.get('type') == 'report' and result['file'].endswith('_report.md'):
            task_id = extract_task_id_from_filename(result['file'])
            if task_id:
                executive_summary = extract_executive_summary(result['source_path'])
                if executive_summary:
                    task_summaries[task_id] = executive_summary
        
        if 'benchmark_run' in data and 'rules_variant' in data['benchmark_run']:
            rule_variant = data['benchmark_run']['rules_variant']
    
    avg_score = total_score / task_count if task_count > 0 else 0
    
    # Read existing content
    if not comparison_file.exists():
        print("⚠️  BENCHMARK_COMPARISON.md not found - creating new file")
        return
    
    with open(comparison_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update performance table
    content = update_performance_table(content, archive_name, task_scores, avg_score)
    
    # Build benchmarking notes with executive summaries
    benchmarking_notes = "*[To be filled manually - notable observations from testing]*\n"
    if task_summaries:
        benchmarking_notes = ""
        for task_id in sorted(task_summaries.keys()):
            summary = task_summaries[task_id]
            benchmarking_notes += f"**{task_id}:** {summary}\n"
        benchmarking_notes += "\n*[Add additional manual observations as needed]*"
    
    # Prepare new detailed entry
    date_str = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"""
## {archive_name} ({rule_variant})

**Date:** {date_str}  
**Average Score:** {avg_score:.1f}/100 ({task_count} tasks)  
**Rules Location:** [rules_store/{archive_name}/](mdc:rules_store/{archive_name}/)

### Key Differences
*[To be filled manually - describe what's different in this version]*

### Benchmarking Notes  
{benchmarking_notes}

**Detailed Results:**
"""
    
    for result in results:
        data = result['data']
        if 'total_score' in data:  # Only include score files, not report files
            task_id = data.get('benchmark_run', {}).get('task_id', 'unknown')
            score = data.get('total_score', 0)
            new_entry += f"- [{task_id}](mdc:rules_store/{archive_name}/{result['file']}): {score}/100\n"
    
    new_entry += "\n---\n"
    
    # Find insertion point for detailed entry (after table, before first ## section)
    if "---\n\n## " in content:
        parts = content.split("---\n\n## ", 1)
        header = parts[0] + "---\n"
        rest = "\n## " + parts[1] if len(parts) > 1 else ""
        content = header + new_entry + rest
    else:
        # Append to end if no sections found
        content = content + new_entry
    
    # Write updated content
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📊 Updated benchmark comparison table: BENCHMARK_COMPARISON.md")

def extract_task_id_from_filename(filename: str) -> Optional[str]:
    """Extract task ID from report filename (e.g., 'task_06_report.md' -> 'task-06')."""
    import re
    match = re.match(r'task_(\d+)_report\.md', filename)
    if match:
        task_num = match.group(1)
        return f"task-{task_num.lstrip('0')}"  # Remove leading zeros
    return None

def extract_executive_summary(report_file_path: Path) -> Optional[str]:
    """Extract the Executive Summary section from a task report file."""
    try:
        with open(report_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find Executive Summary section
        summary_start = content.find("## Executive Summary")
        if summary_start == -1:
            return None
        
        # Find the start of content (after the heading)
        content_start = content.find("\n", summary_start) + 1
        
        # Find the end (next ## heading or end of file)
        next_section = content.find("\n## ", content_start)
        if next_section == -1:
            summary_content = content[content_start:].strip()
        else:
            summary_content = content[content_start:next_section].strip()
        
        # Clean up the summary - remove extra whitespace and newlines
        summary_content = ' '.join(summary_content.split())
        
        return summary_content if summary_content else None
        
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"⚠️  Could not read executive summary from {report_file_path}: {e}")
        return None

def update_performance_table(content: str, archive_name: str, task_scores: Dict[str, int], avg_score: float) -> str:
    """Update the performance comparison table with new results."""
    import re
    
    # Find the table in the content
    table_start = content.find("| Rules Version |")
    if table_start == -1:
        print("⚠️  Performance table not found in BENCHMARK_COMPARISON.md")
        return content
    
    # Find the end of the table (next section or end of table)
    table_end = content.find("\n*Table shows scores", table_start)
    if table_end == -1:
        table_end = content.find("\n\n", table_start)
        if table_end == -1:
            table_end = len(content)
    
    # Extract existing table
    table_content = content[table_start:table_end]
    
    # Parse existing table to get all task columns
    lines = table_content.strip().split('\n')
    if len(lines) < 2:
        print("⚠️  Invalid table format")
        return content
    
    # Get existing columns from header
    header_line = lines[0]
    existing_tasks = []
    header_parts = [col.strip() for col in header_line.split('|')[1:-1]]  # Remove empty first/last
    
    for part in header_parts:
        if part not in ['Rules Version', 'Average'] and part.startswith('task-'):
            existing_tasks.append(part)
    
    # Add any new tasks from current results
    all_tasks = sorted(set(existing_tasks + list(task_scores.keys())))
    
    # Build new table header
    new_header = "| Rules Version | " + " | ".join(all_tasks) + " | Average |"
    new_separator = "|" + "|".join(["-" * (len(col) + 2) for col in ["Rules Version"] + all_tasks + ["Average"]]) + "|"
    
    # Parse existing rows
    existing_rows = []
    for line in lines[2:]:  # Skip header and separator
        if line.strip() and '|' in line:
            parts = [col.strip() for col in line.split('|')[1:-1]]
            if len(parts) >= 2:  # At least version and one score
                version = parts[0]
                if version != archive_name:  # Don't duplicate if already exists
                    existing_rows.append((version, parts[1:]))
    
    # Build new row for current archive
    new_row_data = []
    for task in all_tasks:
        score = task_scores.get(task, '-')
        new_row_data.append(str(score) if score != '-' else '-')
    
    new_row = f"| {archive_name} | " + " | ".join(new_row_data) + f" | {avg_score:.1f} |"
    
    # Rebuild table
    new_table_lines = [new_header, new_separator]
    
    # Add existing rows (update them to match new column structure)
    for version, old_data in existing_rows:
        row_data = []
        old_tasks_data = {}
        
        # Try to map old data to tasks (this is approximate)
        old_task_index = 0
        for i, col_name in enumerate(header_parts[1:], 1):  # Skip "Rules Version"
            if col_name.startswith('task-') and old_task_index < len(old_data) - 1:  # -1 for average
                old_tasks_data[col_name] = old_data[old_task_index]
                old_task_index += 1
        
        # Build row with all current tasks
        for task in all_tasks:
            row_data.append(old_tasks_data.get(task, '-'))
        
        # Get average (last column from old data)
        old_avg = old_data[-1] if old_data else '-'
        new_table_lines.append(f"| {version} | " + " | ".join(row_data) + f" | {old_avg} |")
    
    # Add new row
    new_table_lines.append(new_row)
    
    # Replace table in content
    new_table = '\n'.join(new_table_lines)
    new_content = content[:table_start] + new_table + content[table_end:]
    
    return new_content

def copy_results_to_archive(archive_name: str, results: List[Dict]) -> None:
    """Copy recent results to the archived rules folder at parent level."""
    repo_root = Path.cwd()
    archive_parent_path = repo_root / "rules_store" / archive_name  # Parent level, not rules subfolder
    
    if not archive_parent_path.exists():
        print(f"⚠️  Archive path {archive_parent_path} not found - skipping results copy")
        return
    
    copied_count = 0
    for result in results:
        source_file = result['source_path']
        if source_file.exists():
            dest_file = archive_parent_path / result['file']  # Place at parent level
            shutil.copy2(source_file, dest_file)
            copied_count += 1
    
    if copied_count > 0:
        print(f"📄 Copied {copied_count} result files to archive parent folder")

def clean_benchmark_files():
    """Remove benchmark test files and restore clean project state."""
    repo_root = Path.cwd()
    
    # Files/directories created during benchmark tasks - relative to repo root
    # DO NOT include results/ - preserve those!
    benchmark_artifacts = [
        "src/auth",
        "src/services", 
        "src/models/profile.py",
        "src/api/profiles.py",
        "src/utils/validation.py",
        "docs/auth.md",
        "docs/auth-api.md", 
        "docs/authentication.md",
        "docs/user-profiles.md",
        "docs/profiles.md",
        "docs/profile-api.md",
        "docs/notifications.md",
        "docs/project-index.md",
        "analysis.md",
        "task-analysis.md",
        "requirements.txt",
        "config.py",
        "task_repos",  # Include task workspace folders for cleanup
    ]
    
    removed_items = []
    
    for pattern in benchmark_artifacts:
        if "*" in pattern:
            # Handle glob patterns
            parent_dir = repo_root / Path(pattern).parent
            if parent_dir.exists():
                pattern_name = Path(pattern).name.replace("*", "")
                for item in parent_dir.iterdir():
                    if pattern_name in item.name.lower():
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                        removed_items.append(str(item.relative_to(repo_root)))
        else:
            # Handle exact paths
            item_path = repo_root / pattern
            if item_path.exists():
                if item_path.is_dir():
                    shutil.rmtree(item_path)
                else:
                    item_path.unlink()
                removed_items.append(str(item_path.relative_to(repo_root)))
    
    # Also clean up any analysis files in root directory
    for analysis_file in repo_root.glob("analysis-*.md"):
        analysis_file.unlink()
        removed_items.append(str(analysis_file.relative_to(repo_root)))
    
    return removed_items

def reset_modified_files(repo_root="."):
    """Reset any files that might have been modified during benchmark tests."""
    repo_root = Path(repo_root)
    
    # Files that might be modified during tests
    potentially_modified = [
        "src/models/user.py",  # Might be extended with profile fields
        "docs/authentication.md",  # Might be updated with cross-references
    ]
    
    # For now, just report which files might need manual checking
    # In a real scenario, you might restore from git or have backup copies
    modified_warnings = []
    
    for file_path in potentially_modified:
        full_path = repo_root / file_path
        if full_path.exists():
            # In a complete implementation, you might check git status
            # or compare with known clean versions
            modified_warnings.append(str(full_path.relative_to(repo_root)))
    
    return modified_warnings

def restore_cursorignore(repo_root="."):
    """Restore .cursorignore to hide evaluation materials for next test."""
    repo_root = Path(repo_root)
    cursorignore_file = repo_root / ".cursorignore"
    
    patterns = [
        "marking-schemes/",
        "*-rubric.md", 
        "*-marking-scheme.md",
        "EVALUATE_BENCHMARK.md",
        "BENCHMARK_COMPARISON.md"
    ]
    
    if not cursorignore_file.exists():
        # Create .cursorignore with evaluation materials hidden
        with open(cursorignore_file, 'w', encoding='utf-8') as f:
            f.write("# DSS Benchmark - Hidden Files During Testing\n")
            f.write("# This file prevents the assistant from seeing evaluation materials during benchmark tests\n")
            f.write("# The benchmark runner will temporarily remove these patterns for evaluation\n\n")
            f.write("# Optional: Hide other evaluation materials if needed\n\n")
            f.write("# USER ADDED CONTENT - This should be preserved\n")
            f.write("#/README.md\n")
            f.write("#/old/**\n")
            f.write("#/rules_store/**\n")
            f.write("#/rules_store\n")
            f.write("#/old\n")
            f.write("#/.vscode\n")
            f.write("#/.venv\n")
            f.write("#/.envrc\n")
            f.write("#/requirements.txt\n\n\n\n")
            f.write("# Hide evaluation materials during testing\n")
            for pattern in patterns:
                f.write(f"{pattern}\n")
        return "created"
    
    # Read current content
    with open(cursorignore_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if all patterns already exist
    missing_patterns = [p for p in patterns if p not in content]
    
    if not missing_patterns:
        return "already_present"
    
    # Add missing evaluation material hiding back
    with open(cursorignore_file, 'a', encoding='utf-8') as f:
        f.write(f"\n# Hide evaluation materials during testing\n")
        for pattern in missing_patterns:
            f.write(f"{pattern}\n")
    
    return "restored"

def main():
    """Main reset function with rules archiving automation."""
    print("🧹 Resetting project state after benchmark completion...")
    print("📊 Preserving benchmark results and archiving rules...")
    
    # Step 0: Organize rules structure first (NEW)
    organization_result = organize_rules_before_archive()
    if organization_result:
        print(f"📁 {organization_result}")
    
    # Step 1: Archive current rules (before any cleanup)
    archive_name = archive_current_rules()
    
    # Step 2: Collect recent results for the archived rules
    results = collect_recent_results()
    
    # Step 3: Copy results to archive and update comparison table
    if archive_name and results:
        copy_results_to_archive(archive_name, results)
        update_comparison_table(archive_name, results)
        print(f"📈 Processed {len(results)} benchmark results for {archive_name}")
    elif archive_name:
        print(f"📦 Archived rules as {archive_name} (no recent results found)")
    
    # Step 4: Clean up benchmark artifacts
    removed = clean_benchmark_files()
    potentially_modified = reset_modified_files()
    cursorignore_status = restore_cursorignore()
    
    if removed:
        print("\n✅ Removed the following created items:")
        for item in removed:
            print(f"   - {item}")
    else:
        print("\n✅ No created files found - project already clean")
    
    if potentially_modified:
        print("\n⚠️  Note: These files may have been modified during testing:")
        for item in potentially_modified:
            print(f"   - {item}")
        print("   Consider reviewing these files for any changes")
    
    # Report cursorignore status
    if cursorignore_status == "created":
        print("\n📝 Created .cursorignore to hide evaluation materials for next test")
    elif cursorignore_status == "restored":
        print("\n📝 Restored .cursorignore to hide evaluation materials for next test")
    elif cursorignore_status == "already_present":
        print("\n✅ .cursorignore already configured to hide evaluation materials")
    
    print("\n🎯 Project reset complete! Ready for next benchmark test.")
    print("📁 Benchmark results preserved in results/")
    print("🔒 Evaluation materials hidden from assistant until evaluation phase")
    
    if archive_name:
        print(f"📚 Rules archived as: rules_store/{archive_name}")
        print("📊 BENCHMARK_COMPARISON.md updated with latest results")
        print("💡 Remember to manually fill in 'Key Differences' and 'Benchmarking Notes' sections")

if __name__ == "__main__":
    main() 