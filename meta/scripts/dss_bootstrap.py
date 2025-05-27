#!/usr/bin/env python3
"""---
tags: [bootstrap, dss, automation, cursor, transformation]
provides: [dss_bootstrap, instant_transformation]
requires: []
---

DSS Bootstrap: One-File Repository Transformation

Drop this file into any repository root and run:
    python dss_bootstrap.py

Or use in Cursor by asking:
    "Format this repo with DSS" 
    "Transform this repository to DSS structure"
    "Apply DSS formatting"

This script will:
1. Download the DSS auto-formatter
2. Transform the repository to DSS structure  
3. Install Cursor AI assistant intelligence
4. Set up project-specific context and templates
"""

import os
import sys
import json
import subprocess
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Optional

__version__ = "1.0.0"

# DSS Repository Configuration
DSS_REPO = "Dub1n/dss"
DSS_BASE_URL = f"https://raw.githubusercontent.com/{DSS_REPO}/main"

class DSSBootstrap:
    """One-click DSS transformation for any repository."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.original_path = self.repo_path
        self.dss_path = self.repo_path.parent / f"{self.repo_path.name}-dss"
        
    def run_transformation(self, in_place: bool = False, dry_run: bool = False) -> bool:
        """Run the complete DSS transformation process."""
        try:
            print("🚀 DSS Bootstrap: Transforming Repository")
            print("="*50)
            
            # Step 1: Download auto-formatter
            print("📥 Step 1: Downloading DSS auto-formatter...")
            formatter_path = self._download_autoformatter()
            if not formatter_path:
                return False
            
            # Step 2: Detect project type
            print("🔍 Step 2: Analyzing project structure...")
            project_type = self._detect_project_type()
            print(f"   Detected project type: {project_type}")
            
            # Step 3: Run transformation
            print("⚡ Step 3: Running DSS transformation...")
            dest_path = self.repo_path if in_place else self.dss_path
            success = self._run_autoformatter(formatter_path, dest_path, dry_run)
            if not success:
                return False
            
            # Step 4: Install Cursor intelligence
            print("🧠 Step 4: Installing Cursor AI intelligence...")
            self._install_cursor_intelligence(dest_path, project_type)
            
            # Step 5: Create bootstrap commands
            print("🎯 Step 5: Setting up voice commands...")
            self._setup_cursor_commands(dest_path)
            
            print("\n" + "="*50)
            print("✅ DSS Transformation Complete!")
            
            if not in_place:
                print(f"📁 New DSS repository: {dest_path}")
                print(f"💡 Original repository preserved: {self.repo_path}")
            else:
                print(f"📁 Repository transformed in place: {self.repo_path}")
            
            print("\n🎉 Next steps:")
            print("   1. Open the DSS repository in Cursor")
            print("   2. Try saying: 'Create a new analysis notebook'")
            print("   3. The AI assistant now understands DSS conventions!")
            
            return True
            
        except Exception as e:
            print(f"❌ Bootstrap failed: {e}")
            return False
        
        finally:
            # Cleanup
            if 'formatter_path' in locals():
                try:
                    Path(formatter_path).unlink()
                except:
                    pass
    
    def _download_autoformatter(self) -> Optional[str]:
        """Download the DSS auto-formatter script."""
        try:
            url = f"{DSS_BASE_URL}/meta/scripts/dss_autoformat.py"
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix='_dss_autoformat.py', delete=False) as tmp:
                print(f"   Downloading from: {url}")
                with urllib.request.urlopen(url) as response:
                    content = response.read().decode()
                tmp.write(content)
                tmp_path = tmp.name
            
            print(f"   ✅ Downloaded to: {tmp_path}")
            return tmp_path
            
        except urllib.error.URLError as e:
            print(f"   ❌ Download failed: {e}")
            print("   💡 Check internet connection and GitHub access")
            return None
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return None
    
    def _detect_project_type(self) -> str:
        """Detect the project type for optimal DSS configuration."""
        files = list(self.repo_path.rglob('*'))
        file_names = [f.name.lower() for f in files if f.is_file()]
        file_extensions = [f.suffix.lower() for f in files if f.is_file()]
        
        # Count different file types
        counts = {
            'python': len([f for f in file_extensions if f == '.py']),
            'jupyter': len([f for f in file_extensions if f == '.ipynb']),
            'javascript': len([f for f in file_extensions if f in ['.js', '.ts', '.jsx', '.tsx']]),
            'data': len([f for f in file_extensions if f in ['.csv', '.parquet', '.json', '.jsonl']]),
            'docs': len([f for f in file_extensions if f in ['.md', '.rst', '.txt']]),
            'web': len([f for f in file_names if f in ['package.json', 'webpack.config.js', 'next.config.js']]),
            'ml': len([f for f in file_names if f in ['requirements.txt', 'environment.yml', 'conda.yml']])
        }
        
        # Data science indicators
        if counts['jupyter'] > 2 or (counts['data'] > 3 and counts['python'] > 3):
            return "data_science"
        
        # Web application indicators  
        if counts['web'] > 0 or counts['javascript'] > 5:
            return "web_application"
        
        # Python package indicators
        if any(name in file_names for name in ['setup.py', 'pyproject.toml']) and counts['python'] > 5:
            return "python_package"
        
        # Documentation project
        if counts['docs'] > len(files) * 0.4:
            return "documentation"
        
        # Machine learning project
        if counts['ml'] > 0 and (counts['python'] > 5 or counts['jupyter'] > 1):
            return "data_science"
        
        return "general"
    
    def _run_autoformatter(self, formatter_path: str, dest_path: Path, dry_run: bool = False) -> bool:
        """Run the DSS auto-formatter."""
        try:
            cmd = [
                sys.executable, formatter_path,
                "--source", str(self.repo_path),
                "--dest", str(dest_path)
            ]
            
            if dry_run:
                cmd.append("--dry-run")
                print("   🔍 Running in dry-run mode (preview only)")
            
            # Set environment variables for better experience
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=False, text=True, env=env)
            
            if result.returncode == 0:
                print("   ✅ Auto-formatter completed successfully")
                return True
            else:
                print(f"   ❌ Auto-formatter failed with code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"   ❌ Failed to run auto-formatter: {e}")
            return False
    
    def _install_cursor_intelligence(self, dest_path: Path, project_type: str):
        """Install Cursor AI intelligence."""
        try:
            # Download cursor rules manager
            url = f"{DSS_BASE_URL}/meta/scripts/cursor_rules_manager.py"
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix='_cursor_manager.py', delete=False) as tmp:
                with urllib.request.urlopen(url) as response:
                    content = response.read().decode()
                tmp.write(content)
                tmp_path = tmp.name
            
            # Run cursor rules installation
            cmd = [
                sys.executable, tmp_path, "install",
                "--project-type", project_type,
                "--repo-root", str(dest_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=dest_path)
            
            # Cleanup
            Path(tmp_path).unlink()
            
            if result.returncode == 0:
                print("   ✅ Cursor intelligence installed")
            else:
                print(f"   ⚠️  Cursor installation warning: {result.stderr}")
                
        except Exception as e:
            print(f"   ⚠️  Could not install Cursor intelligence: {e}")
    
    def _setup_cursor_commands(self, dest_path: Path):
        """Set up Cursor voice commands for DSS operations."""
        try:
            cursor_rules_dir = dest_path / ".cursor" / "rules"
            cursor_rules_dir.mkdir(parents=True, exist_ok=True)
            
            # Create DSS bootstrap commands file
            bootstrap_commands = """# DSS Bootstrap Commands

## Voice Commands for DSS Operations

You can use these voice commands in Cursor to interact with your DSS repository:

### Repository Management
- "Format this repo" / "Apply DSS formatting" → Run DSS transformation
- "Create new analysis notebook" → Generate Jupyter notebook with DSS frontmatter
- "Add new Python module" → Create .py file with proper DSS structure
- "Generate documentation" → Create comprehensive docs using DSS templates

### File Operations
- "Create data processing script" → New Python script in src/ with DSS metadata
- "Add dataset documentation" → New README in data/ directory
- "Create test file" → New test file in tests/ with proper structure

### Documentation  
- "Update project index" → Refresh INDEX.md with current structure
- "Generate module docs" → Create documentation for Python modules
- "Create project overview" → Generate comprehensive project documentation

## Assistant Behavior

The AI assistant now understands:
- DSS folder structure and conventions
- Proper frontmatter formatting for all file types
- Template usage from meta/templates/
- Project-specific context and requirements
- Cross-referencing between modules and documentation

## Custom Commands

To add custom voice commands, edit this file and restart Cursor.

<!-- DSS_BOOTSTRAP_COMMANDS: This enables voice command recognition -->
"""
            
            (cursor_rules_dir / "dss_bootstrap_commands.mdc").write_text(bootstrap_commands)
            
            # Create quick reference
            quick_ref = """# DSS Quick Reference

## Common Voice Commands
- "Format this repo" - Transform to DSS structure
- "Create analysis notebook" - New Jupyter notebook  
- "Add Python module" - New .py file with frontmatter
- "Generate docs" - Create documentation
- "Update index" - Refresh INDEX.md

## File Structure  
- src/ - Source code and executable logic
- data/ - Datasets and data files
- docs/ - Documentation
- meta/ - Scripts, config, automation
- tests/ - Test files

## Frontmatter Template
```yaml
---
tags: [category, specific_tags]
provides: [what_this_file_provides]
requires: [dependencies]
---
```

The AI assistant automatically applies DSS conventions!
"""
            
            (cursor_rules_dir / "dss_quick_reference.mdc").write_text(quick_ref)
            
            print("   ✅ Voice commands configured")
            
        except Exception as e:
            print(f"   ⚠️  Could not set up voice commands: {e}")

def main():
    """Main entry point for DSS bootstrap."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DSS Bootstrap: One-click repository transformation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dss_bootstrap.py                    # Transform current directory
  python dss_bootstrap.py --in-place        # Transform in place (backup first!)
  python dss_bootstrap.py --dry-run         # Preview changes only
  python dss_bootstrap.py --help            # Show this help
  
Voice Commands (in Cursor):
  "Format this repo"                        # Trigger transformation
  "Apply DSS structure"                     # Alternative command
  "Transform to DSS"                        # Another option
        """
    )
    
    parser.add_argument('--repo-path', default='.', 
                        help='Repository path to transform (default: current directory)')
    parser.add_argument('--in-place', action='store_true',
                        help='Transform repository in place (CAUTION: backup first!)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without making them')
    parser.add_argument('--version', action='version', version=f'DSS Bootstrap v{__version__}')
    
    args = parser.parse_args()
    
    # Validate repository path
    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"❌ Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Safety check for in-place transformation
    if args.in_place and not args.dry_run:
        print("⚠️  WARNING: In-place transformation will modify your current repository!")
        print("   It's recommended to backup or commit your changes first.")
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Transformation cancelled.")
            sys.exit(0)
    
    # Run bootstrap
    bootstrap = DSSBootstrap(repo_path)
    success = bootstrap.run_transformation(in_place=args.in_place, dry_run=args.dry_run)
    
    if not success:
        print("\n❌ DSS Bootstrap failed. See errors above.")
        sys.exit(1)
    
    print(f"\n🎯 DSS Bootstrap v{__version__} completed successfully!")

if __name__ == '__main__':
    main() 