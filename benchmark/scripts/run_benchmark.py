#!/usr/bin/env python3
"""
DSS Cursor Rules Benchmark Runner
Helps manage rule switching and benchmark execution for testing Cursor rule effectiveness.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class BenchmarkRunner:
    """Manages DSS Cursor rules benchmarking process."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.rules_dir = self.repo_root / ".cursor" / "rules"
        self.variations_dir = self.repo_root / ".cursor" / "test-variations"
        self.results_dir = self.repo_root / "results"
        self.tasks_dir = self.repo_root / "tasks"
        self.cursorignore_file = self.repo_root / ".cursorignore"
        
    def hide_evaluation_materials(self) -> bool:
        """Ensure marking schemes and evaluation guide are hidden in .cursorignore."""
        patterns = [
            "marking-schemes/",
            "*-rubric.md",
            "*-marking-scheme.md",
            "EVALUATE_BENCHMARK.md",
            "BENCHMARK_COMPARISON.md"
        ]
        
        if not self.cursorignore_file.exists():
            # Create .cursorignore with evaluation materials hidden
            with open(self.cursorignore_file, 'w', encoding='utf-8') as f:
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
            print(f"📝 Created .cursorignore to hide evaluation materials")
            return True
        
        # Check if patterns already exist
        with open(self.cursorignore_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        missing_patterns = [p for p in patterns if p not in content]
        
        if not missing_patterns:
            print(f"✅ Evaluation materials already hidden in .cursorignore")
            return True
            
        # Add missing patterns to existing file
        with open(self.cursorignore_file, 'a', encoding='utf-8') as f:
            f.write(f"\n# Hide evaluation materials during testing\n")
            for pattern in missing_patterns:
                f.write(f"{pattern}\n")
        print(f"📝 Added evaluation material hiding to .cursorignore")
        return True
        
    def reveal_evaluation_materials(self) -> bool:
        """Temporarily reveal evaluation materials by removing from .cursorignore."""
        if not self.cursorignore_file.exists():
            print(f"✅ No .cursorignore file - evaluation materials already visible")
            return True
            
        # Read current content
        with open(self.cursorignore_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter out evaluation material patterns
        filtered_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Skip evaluation material related lines
            if ("marking-schemes" in line_stripped or 
                "*-rubric.md" in line_stripped or 
                "*-marking-scheme.md" in line_stripped or
                "EVALUATE_BENCHMARK.md" in line_stripped):
                continue
            # Skip comment lines about evaluation materials
            if ("Hide marking schemes" in line or 
                "Hide evaluation materials" in line or
                "Hide any backup" in line):
                continue
                
            filtered_lines.append(line)
        
        # Write back filtered content
        with open(self.cursorignore_file, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)
        
        print(f"🔓 Temporarily revealed evaluation materials for scoring")
        return True
    
    def list_rule_variations(self) -> List[str]:
        """List available rule variations."""
        if not self.variations_dir.exists():
            return []
        
        variations = []
        for item in self.variations_dir.iterdir():
            if item.is_dir() and item.name.startswith("rules-"):
                variant_name = item.name.replace("rules-", "")
                variations.append(variant_name)
        
        return sorted(variations)
    
    def switch_rules(self, variant: str) -> bool:
        """Switch to specified rule variant."""
        source_dir = self.variations_dir / f"rules-{variant}"
        
        if not source_dir.exists():
            print(f"❌ Rule variant '{variant}' not found at {source_dir}")
            return False
        
        # Backup current rules
        if self.rules_dir.exists():
            backup_dir = self.rules_dir.parent / f"rules-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            shutil.move(self.rules_dir, backup_dir)
            print(f"📦 Backed up current rules to {backup_dir}")
        
        # Copy new rules
        try:
            shutil.copytree(source_dir, self.rules_dir)
            print(f"✅ Switched to rule variant: {variant}")
            return True
        except Exception as e:
            print(f"❌ Failed to switch rules: {e}")
            return False
    
    def list_tasks(self) -> List[Dict]:
        """List available benchmark tasks."""
        tasks = []
        
        if not self.tasks_dir.exists():
            return tasks
        
        for task_file in self.tasks_dir.glob("task-*.md"):
            try:
                # Parse basic task info from frontmatter
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if content.startswith('---'):
                    # Extract frontmatter
                    end_idx = content.find('---', 3)
                    if end_idx != -1:
                        frontmatter = content[3:end_idx].strip()
                        task_info = {'file': task_file.name}
                        
                        # Parse basic fields
                        for line in frontmatter.split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                key = key.strip()
                                value = value.strip().strip('"\'')
                                task_info[key] = value
                        
                        tasks.append(task_info)
                        
            except Exception as e:
                print(f"⚠️ Error reading task {task_file}: {e}")
        
        return sorted(tasks, key=lambda x: x.get('file', ''))
    
    def create_results_template(self, variant: str, task_id: str) -> Path:
        """Create a template results file for manual scoring."""
        self.results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_file = self.results_dir / f"{timestamp}_{variant}_{task_id}.json"
        
        template = {
            "benchmark_run": {
                "timestamp": datetime.now().isoformat(),
                "rules_variant": variant,
                "task_id": task_id,
                "evaluator": "manual"
            },
            "scores": {
                "file_placement": {"score": 0, "max": 25, "notes": ""},
                "frontmatter_quality": {"score": 0, "max": 20, "notes": ""},
                "code_structure": {"score": 0, "max": 20, "notes": ""},
                "documentation": {"score": 0, "max": 15, "notes": ""},
                "dss_integration": {"score": 0, "max": 10, "notes": ""},
                "technical_accuracy": {"score": 0, "max": 10, "notes": ""}
            },
            "total_score": 0,
            "notes": "",
            "files_created": [],
            "files_modified": [],
            "observations": ""
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2)
        
        print(f"📊 Created results template: {results_file}")
        return results_file
    
    def compare_results(self, file1: Path, file2: Path) -> None:
        """Compare two benchmark result files."""
        try:
            with open(file1) as f:
                results1 = json.load(f)
            with open(file2) as f:
                results2 = json.load(f)
            
            variant1 = results1["benchmark_run"]["rules_variant"]
            variant2 = results2["benchmark_run"]["rules_variant"]
            
            total1 = results1.get("total_score", 0)
            total2 = results2.get("total_score", 0)
            
            print(f"\n🔍 Benchmark Comparison: {variant1} vs {variant2}")
            print("=" * 60)
            print(f"{'Category':<20} {'':>8} {'':>8} {'Change':>10}")
            print(f"{'':^20} {variant1:^8} {variant2:^8} {'':^10}")
            print("-" * 60)
            
            for category, data1 in results1["scores"].items():
                data2 = results2["scores"].get(category, {"score": 0})
                score1 = data1["score"]
                score2 = data2["score"]
                change = score2 - score1
                change_str = f"{change:+.1f}" if change != 0 else "0.0"
                
                print(f"{category:<20} {score1:>8} {score2:>8} {change_str:>10}")
            
            print("-" * 60)
            total_change = total2 - total1
            total_change_str = f"{total_change:+.1f}" if total_change != 0 else "0.0"
            print(f"{'TOTAL':<20} {total1:>8} {total2:>8} {total_change_str:>10}")
            
            if total_change > 0:
                print(f"\n✅ {variant2} performed better by {total_change:.1f} points")
            elif total_change < 0:
                print(f"\n❌ {variant2} performed worse by {abs(total_change):.1f} points")
            else:
                print(f"\n➖ Performance was equivalent")
                
        except Exception as e:
            print(f"❌ Error comparing results: {e}")

def main():
    parser = argparse.ArgumentParser(description='DSS Cursor Rules Benchmark Runner')
    parser.add_argument('--repo-root', default='.', help='Repository root directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List variations command
    list_parser = subparsers.add_parser('list-rules', help='List available rule variations')
    
    # Switch rules command
    switch_parser = subparsers.add_parser('switch', help='Switch to rule variant')
    switch_parser.add_argument('variant', help='Rule variant name (e.g., baseline, experimental)')
    
    # List tasks command
    tasks_parser = subparsers.add_parser('list-tasks', help='List available benchmark tasks')
    
    # Start benchmark command
    start_parser = subparsers.add_parser('start', help='Start benchmark session')
    start_parser.add_argument('variant', help='Rule variant to test')
    start_parser.add_argument('task', help='Task ID to run')
    
    # Compare results command
    compare_parser = subparsers.add_parser('compare', help='Compare two result files')
    compare_parser.add_argument('file1', help='First results file')
    compare_parser.add_argument('file2', help='Second results file')
    
    # Reveal marking schemes command
    reveal_parser = subparsers.add_parser('reveal-schemes', help='Reveal marking schemes for evaluation')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    runner = BenchmarkRunner(args.repo_root)
    
    if args.command == 'list-rules':
        variations = runner.list_rule_variations()
        if variations:
            print("📋 Available rule variations:")
            for variant in variations:
                print(f"  - {variant}")
        else:
            print("❌ No rule variations found in .cursor/test-variations/")
    
    elif args.command == 'switch':
        runner.switch_rules(args.variant)
    
    elif args.command == 'list-tasks':
        tasks = runner.list_tasks()
        if tasks:
            print("📋 Available benchmark tasks:")
            for task in tasks:
                task_id = task.get('task_id', 'unknown')
                category = task.get('category', 'unknown')
                difficulty = task.get('difficulty', 'unknown')
                print(f"  - {task_id} ({category}, {difficulty})")
        else:
            print("❌ No benchmark tasks found")
    
    elif args.command == 'start':
        print(f"🚀 Starting benchmark session:")
        print(f"   Rule variant: {args.variant}")
        print(f"   Task: {args.task}")
        
        # Hide marking schemes before testing
        runner.hide_evaluation_materials()
        
        # Switch to specified rules
        if runner.switch_rules(args.variant):
            # Create results template
            results_file = runner.create_results_template(args.variant, args.task)
            
            print(f"\n📝 Instructions:")
            print(f"1. Open the task file: tasks/{args.task}.md")
            print(f"2. Complete the task following the instructions")
            print(f"3. Run 'python scripts/run_benchmark.py reveal-schemes' to access evaluation materials")
            print(f"4. Open the evaluation guide: EVALUATE_BENCHMARK.md")
            print(f"5. Open the benchmark comparison: BENCHMARK_COMPARISON.md")
            print(f"6. Open the marking scheme: marking-schemes/{args.task}-rubric.md")
            print(f"7. Score your work using the rubric")
            print(f"8. Update the results file: {results_file}")
            print(f"9. Run comparison when you have multiple results")
    
    elif args.command == 'reveal-schemes':
        print("🔓 Revealing evaluation materials for scoring...")
        runner.reveal_evaluation_materials()
        print("📊 You can now access:")
        print("   - Marking schemes in marking-schemes/")
        print("   - Evaluation guide: EVALUATE_BENCHMARK.md")
        print("   - Benchmark comparison: BENCHMARK_COMPARISON.md")
        print("⚠️  Remember: Do not show these to the assistant during testing!")
    
    elif args.command == 'compare':
        runner.compare_results(Path(args.file1), Path(args.file2))

if __name__ == '__main__':
    main() 