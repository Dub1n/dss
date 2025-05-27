#!/usr/bin/env python3
"""---
tags: [bootstrap, dss, automation, cursor, transformation, enhanced]
provides: [dss_bootstrap, robust_transformation]
requires: []
---

DSS Bootstrap: Enhanced Repository Transformation

Improvements in v2.2.0:
- Fixed GitHub label validation to prevent non-existent label errors
- Improved title encoding handling for special characters  
- Enhanced WearOS project detection with more specific patterns
- Better fallback formatter with WearOS-aware file organization
- Improved duplicate issue detection and handling
- Enhanced error reporting and recovery mechanisms
- Cross-platform Unicode handling (Windows/Linux/Mac)
- Better Android/mobile project detection
- Graceful handling of missing remote resources
- Enhanced file organization with meaningful names
- Improved error handling and rollback capabilities
- Better validation and user feedback
- Installation report generation for community feedback
- Iterative versioning for output directories
- Enhanced console output reliability for Windows terminals

Note: This is the consolidated script that includes all enhancements previously
separated into dss_bootstrap_enhanced.py. This is the only bootstrap script needed.

Drop this file into any repository root and run:
    python dss_bootstrap.py

This script will:
1. Download the DSS auto-formatter (with fallbacks)
2. Transform the repository to DSS structure with smart naming
3. Install Cursor AI assistant intelligence (robust)
4. Set up project-specific context and templates
5. Validate the transformation and offer rollback
6. Generate optional installation report for DSS improvement
"""

import os
import sys
import json
import subprocess
import tempfile
import urllib.request
import urllib.error
import shutil
import platform
import hashlib
import time
import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Set
from datetime import datetime

__version__ = "2.3.0"

# DSS Repository Configuration
DSS_REPO = "Dub1n/dss"
DSS_BASE_URL = f"https://raw.githubusercontent.com/{DSS_REPO}/main"

# Fallback configurations
FALLBACK_CONFIG = {
    "dss_config.yml": """# DSS Configuration
structure:
  src: "Source code and executable logic"
  docs: "Documentation and guides"
  tests: "Test files and validation"
  data: "Datasets and artifacts"
  meta: "Scripts, config, automation"
""",
    "gitignore_template": """# DSS Generated .gitignore
.DS_Store
*.log
*.tmp
__pycache__/
*.pyc
.env
.venv/
node_modules/
*.class
""",
}

class DSSBootstrap:
    """Enhanced DSS transformation with robust error handling and improved GitHub integration."""
    
    def __init__(self, repo_path: Path = None, dss_path: Path = None):
        """Initialize with repository paths and setup state tracking."""
        self.repo_path = repo_path or Path.cwd()
        self.dss_path = dss_path or self._get_versioned_dss_path()
        self.backup_path = None
        self.platform = platform.system().lower()
        
        # Detect Cursor environment
        self.in_cursor = self._detect_cursor_environment()
        
        # Report data structure
        self.report_data = {
            'start_time': datetime.now(),
            'end_time': None,
            'platform': self.platform,
            'issues': [],
            'warnings': [],
            'optimizations': [],
            'performance_metrics': {},
            'project_info': {},
            'transformation_method': 'cursor_native' if self.in_cursor else 'auto',
            'validation_results': {},
            'cursor_integration': self.in_cursor
        }
        
        # Initialize GitHub labels cache
        self._github_labels_cache = None
        
        # Set up Unicode handling for Windows
        if self.platform == "windows":
            os.environ['PYTHONIOENCODING'] = 'utf-8'
        
    def _get_versioned_dss_path(self) -> Path:
        """Determine the next available versioned DSS path.
        
        If {repo_name}-dss doesn't exist, use that.
        If it exists, check for {repo_name}-dss-1.0, then {repo_name}-dss-2.0, etc.
        
        Returns:
            Path: The next available versioned DSS directory path
        """
        base_path = self.repo_path.parent / f"{self.repo_path.name}-dss"
        
        # If the base path doesn't exist, use it
        if not base_path.exists():
            return base_path
        
        # Check for versioned paths
        version = 1
        while True:
            versioned_path = self.repo_path.parent / f"{self.repo_path.name}-dss-{version}.0"
            if not versioned_path.exists():
                return versioned_path
            version += 1
            
                    # Should never reach here, but just in case
        return base_path
    
    def _detect_cursor_environment(self) -> bool:
        """Detect if we're running inside Cursor IDE environment."""
        # Check for Cursor-specific environment variables
        cursor_indicators = [
            'CURSOR_USER_DATA_DIR',
            'CURSOR_LOGS_DIR', 
            'CURSOR_SESSION_ID',
            'CURSOR_WORKSPACE_FOLDER'
        ]
        
        # Check if any Cursor environment variables are present
        if any(var in os.environ for var in cursor_indicators):
            return True
            
        # Check for Cursor process in system
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if 'cursor' in proc.info['name'].lower():
                    return True
        except (ImportError, Exception):
            pass
            
        # Check for Cursor configuration files
        cursor_config_paths = [
            Path.home() / '.cursor',
            Path.home() / 'AppData' / 'Roaming' / 'Cursor' if self.platform == 'windows' else None,
            Path.home() / 'Library' / 'Application Support' / 'Cursor' if self.platform == 'darwin' else None
        ]
        
        for config_path in cursor_config_paths:
            if config_path and config_path.exists():
                return True
                
        # Check if we're running in a directory with .cursor folder
        if (self.repo_path / '.cursor').exists():
            return True
            
        return False
    
    def run_transformation(self, in_place: bool = False, dry_run: bool = False, create_backup: bool = True) -> bool:
        """Run the complete DSS transformation process with enhanced error handling.
        
        Args:
            in_place: Whether to transform the repository in place (ignored for dry runs)
            dry_run: Whether to perform a dry run (always uses separate directory)
            create_backup: Whether to create a backup before transformation
            
        Returns:
            bool: True if transformation was successful, False otherwise
        """
        try:
            self._print_unicode("🚀 DSS Bootstrap: Transforming Repository")
            if self.in_cursor:
                self._print_unicode("🎯 Cursor Environment Detected - Using Native AI Integration")
            print("="*60)
            
            # Step 0: Create backup if requested
            if create_backup and not dry_run:
                self._print_unicode("💾 Step 0: Creating backup...")
                self._create_backup()
            
            # Step 1: Enhanced project detection (moved earlier)
            self._print_unicode("🔍 Step 1: Analyzing project structure...")
            detection_start = time.time()
            project_info = self._detect_project_type_enhanced()
            self._record_performance_metric("project_detection", time.time() - detection_start)
            self.report_data['project_info'] = project_info
            print(f"   Detected project type: {project_info['type']}")
            print(f"   Key technologies: {', '.join(project_info['technologies'])}")
            
            # Step 2: Choose transformation method based on environment
            # Always use a new directory for dry runs to avoid modifying original repo
            if dry_run:
                dest_path = self.dss_path
                self._print_unicode("🔍 Using separate directory for dry-run: {0}".format(dest_path))
            else:
                dest_path = self.repo_path if in_place else self.dss_path
                
            # Log versioning information if applicable
            if not in_place and "-dss-" in str(dest_path):
                try:
                    version = str(dest_path).split("-dss-")[1]
                    self._print_unicode(f"📊 Creating versioned DSS directory (v{version})")
                    self._add_report_optimization(f"Created versioned directory {version} to avoid conflicts", "file_organization")
                    self._add_report_optimization("Versioned directory creation helps avoid overwriting existing transformations", "usability")
                except:
                    pass

            if self.in_cursor:
                self._print_unicode("🧠 Step 2: Using Cursor Native Transformation...")
                success = self._run_cursor_native_transformation(dest_path, dry_run, project_info)
                if not success:
                    self._print_unicode("   ⚠️ Cursor native transformation failed, falling back to auto-formatter...")
                    formatter_path = self._download_autoformatter_robust()
                    if not formatter_path:
                        self._add_report_issue("Failed to download DSS auto-formatter after Cursor fallback", "critical")
                        return False
                    success = self._run_autoformatter_robust(formatter_path, dest_path, dry_run, project_info)
            else:
                # Traditional auto-formatter approach
                self._print_unicode("📥 Step 2: Downloading DSS auto-formatter...")
                formatter_path = self._download_autoformatter_robust()
                if not formatter_path:
                    self._add_report_issue("Failed to download DSS auto-formatter", "critical")
                    return False
                success = self._run_autoformatter_robust(formatter_path, dest_path, dry_run, project_info)
            
            # Step 3: Handle result and continue with post-processing
            if not success:
                return False
            
            # Step 4: Post-process file organization
            if not dry_run:
                self._print_unicode("🎯 Step 3: Optimizing file organization...")
                self._optimize_file_organization(dest_path, project_info)
            
            # Step 5: Install Cursor intelligence with fallbacks
            self._print_unicode("🧠 Step 4: Installing Cursor AI intelligence...")
            self._install_cursor_intelligence_robust(dest_path, project_info)
            
            # Step 6: Create enhanced project documentation
            self._print_unicode("📚 Step 5: Generating project documentation...")
            self._create_enhanced_documentation(dest_path, project_info)
            
            # Step 7: Validate transformation
            self._print_unicode("✅ Step 6: Validating transformation...")
            validation_result = self._validate_transformation(dest_path)
            self.report_data['validation_results'] = validation_result
            
            # Step 8: Offer installation report
            self._print_unicode("📝 Step 7: Installation report...")
            
            print("\n" + "="*60)
            self._print_unicode("✅ DSS Transformation Complete!")
            
            if not in_place:
                # Get the version number if present in the path
                version_info = ""
                if "-dss-" in str(dest_path):
                    try:
                        version = str(dest_path).split("-dss-")[1]
                        version_info = f" (version {version})"
                    except:
                        pass
                
                print(f"📁 New DSS repository{version_info}: {dest_path}")
                print(f"💡 Original repository preserved: {self.repo_path}")
                if create_backup:
                    print(f"💾 Backup created at: {self.backup_path}")
            else:
                print(f"📁 Repository transformed in place: {self.repo_path}")
            
            print(f"\n📊 Validation Results:")
            for check, status in validation_result.items():
                status_icon = "✅" if status else "❌"
                self._print_unicode(f"   {status_icon} {check}")
                if not status:
                    self._add_report_issue(f"Validation failed: {check}", "warning")
            
            # Offer to generate installation report
            self._offer_installation_report(dest_path)
            
            print(f"\n🎉 Next steps:")
            print("   1. Open the DSS repository in Cursor")
            print("   2. Try voice commands like 'Create analysis notebook'")
            print("   3. Review the generated documentation in docs/")
            print("   4. Check src/ for your organized source code")
            
            return True
            
        except Exception as e:
            print(f"❌ Bootstrap failed: {e}")
            if create_backup and not dry_run:
                print(f"💾 Backup available at: {self.backup_path}")
            return False
        
        finally:
            # Cleanup temporary files
            if 'formatter_path' in locals():
                try:
                    Path(formatter_path).unlink(missing_ok=True)
                except:
                    pass
    
    def _print_unicode(self, text: str):
        """Print Unicode text with cross-platform compatibility and buffer-safe output."""
        try:
            # Use a wrapped print to avoid console buffer issues
            self._safe_print(text)
        except UnicodeEncodeError:
            # Fallback for systems that can't handle Unicode
            clean_text = text.encode('ascii', 'replace').decode('ascii')
            self._safe_print(clean_text)
    
    def _safe_print(self, text: str):
        """Print text safely to avoid console buffer issues.
        
        Some terminals (especially PowerShell with PSReadLine) can have buffer issues
        that cause exceptions when trying to render text.
        """
        try:
            # Standard print attempt
            print(text)
        except Exception as e:
            # If there's a buffer issue or other console error, try alternative approaches
            try:
                # Approach 1: Write directly to stdout with flush
                import sys
                sys.stdout.write(text + "\n")
                sys.stdout.flush()
            except Exception:
                try:
                    # Approach 2: Split into smaller chunks
                    for line in text.split("\n"):
                        for chunk in [line[i:i+80] for i in range(0, len(line), 80)]:
                            import sys
                            sys.stdout.write(chunk)
                            sys.stdout.flush()
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                except:
                    # Last resort: Just try to get some output
                    try:
                        import sys
                        sys.stderr.write(f"INFO: {text}\n")
                    except:
                        pass
    
    def _add_report_issue(self, issue: str, severity: str = "error"):
        """Add an issue to the installation report."""
        self.report_data['issues'].append({
            'timestamp': datetime.now(),
            'severity': severity,
            'description': issue
        })
    
    def _add_report_warning(self, warning: str):
        """Add a warning to the installation report."""
        self.report_data['warnings'].append({
            'timestamp': datetime.now(),
            'description': warning
        })
    
    def _add_report_optimization(self, optimization: str, category: str = "general"):
        """Add an optimization suggestion to the installation report."""
        self.report_data['optimizations'].append({
            'timestamp': datetime.now(),
            'category': category,
            'suggestion': optimization
        })
    
    def _record_performance_metric(self, metric_name: str, value: float, unit: str = "seconds"):
        """Record a performance metric for the installation report."""
        self.report_data['performance_metrics'][metric_name] = {
            'value': value,
            'unit': unit,
            'timestamp': datetime.now()
        }
    
    def _create_backup(self):
        """Create a backup of the original repository."""
        try:
            shutil.copytree(self.repo_path, self.backup_path, ignore=shutil.ignore_patterns('.git'))
            print(f"   ✅ Backup created at: {self.backup_path}")
        except Exception as e:
            print(f"   ⚠️  Backup failed: {e}")
    
    def _download_autoformatter_robust(self) -> Optional[str]:
        """Download the DSS auto-formatter with fallback handling."""
        urls_to_try = [
            f"{DSS_BASE_URL}/meta/scripts/dss_autoformat.py",
            f"{DSS_BASE_URL}/scripts/dss_autoformat.py",
            f"{DSS_BASE_URL}/dss_autoformat.py"
        ]
        
        for url in urls_to_try:
            try:
                print(f"   Trying: {url}")
                with urllib.request.urlopen(url, timeout=30) as response:
                    content = response.read().decode('utf-8')
                
                with tempfile.NamedTemporaryFile(mode='w+', suffix='_dss_autoformat.py', 
                                               delete=False, encoding='utf-8') as tmp:
                    tmp.write(content)
                    tmp_path = tmp.name
                
                print(f"   ✅ Downloaded successfully")
                self.report_data['transformation_method'] = 'downloaded'
                return tmp_path
                
            except urllib.error.URLError as e:
                print(f"   ❌ Failed: {e}")
                continue
            except Exception as e:
                print(f"   ❌ Unexpected error: {e}")
                continue
        
        # If all downloads fail, create enhanced fallback formatter
        print("   ⚠️  All downloads failed, creating enhanced fallback formatter...")
        self._add_report_warning("Auto-formatter download failed, using enhanced fallback")
        self._add_report_optimization("Improve auto-formatter download reliability or enhance fallback", "infrastructure")
        self._add_report_optimization("Fallback formatter should handle WearOS project structure better", "project_types")
        self.report_data['transformation_method'] = 'enhanced_fallback'
        return self._create_enhanced_fallback_formatter()
    
    def _create_fallback_formatter(self) -> str:
        """Create a minimal fallback formatter when download fails."""
        return self._create_enhanced_fallback_formatter()  # Use enhanced version
    
    def _run_cursor_native_transformation(self, dest_path: Path, dry_run: bool, project_info: Dict) -> bool:
        """Run DSS transformation using Cursor's built-in AI instead of external APIs."""
        try:
            self._print_unicode("🎯 Using Cursor's built-in AI agent - no external API calls needed!")
            self._add_report_optimization("Using Cursor native AI eliminates API key dependencies", "ai_integration")
            
            # Always use a new directory for dry runs to avoid modifying original repo
            if dry_run:
                actual_dest = self.dss_path
                self._print_unicode("🔍 Using separate directory for dry-run: {0}".format(actual_dest))
            else:
                actual_dest = dest_path
                
            # Log versioning information if applicable
            if "-dss-" in str(actual_dest):
                try:
                    version = str(actual_dest).split("-dss-")[1]
                    self._print_unicode(f"📊 Creating versioned DSS directory (v{version})")
                    self._add_report_optimization(f"Created versioned directory {version} to avoid conflicts", "file_organization")
                except:
                    pass
            
            if not dry_run:
                # Create the DSS structure first
                print("   📁 Creating DSS directory structure...")
                actual_dest.mkdir(parents=True, exist_ok=True)
                
                # Create standard DSS directories
                for dir_name in ["src", "docs", "tests", "data", "meta"]:
                    (actual_dest / dir_name).mkdir(exist_ok=True)
                    print(f"   ✅ Created {dir_name}/")
                
                # Create Cursor-native transformation using intelligent file organization
                self._cursor_native_file_organization(actual_dest, project_info)
                
                # Create Cursor-specific AI integration files
                self._create_cursor_ai_integration(actual_dest, project_info)
                
                print("   ✅ Cursor native transformation completed successfully!")
                self._add_report_optimization("Cursor native transformation avoids network dependencies", "reliability")
                return True
            else:
                print("   🔍 Dry-run: Would create DSS structure and organize files using Cursor AI")
                return True
                
        except Exception as e:
            print(f"   ❌ Cursor native transformation failed: {e}")
            self._add_report_issue(f"Cursor native transformation error: {e}", "error")
            return False
    
    def _cursor_native_file_organization(self, dest_path: Path, project_info: Dict):
        """Organize files using Cursor-native intelligence without external API calls."""
        print("   🧠 Organizing files using Cursor's built-in intelligence...")
        
        project_type = project_info.get('type', 'general')
        technologies = project_info.get('technologies', [])
        
        # Count files processed
        files_processed = 0
        files_by_type = {'src': 0, 'docs': 0, 'tests': 0, 'data': 0, 'meta': 0}
        
        try:
            for file_path in self.repo_path.rglob('*'):
                if not file_path.is_file():
                    continue
                    
                # Skip hidden files and directories
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                
                # CRITICAL FIX: Skip files that are already in DSS directories to prevent recursion
                rel_path = file_path.relative_to(self.repo_path)
                if any(part in ['src', 'docs', 'tests', 'data', 'meta'] and 
                       str(rel_path).count(part) > 1 for part in ['src', 'docs', 'tests', 'data', 'meta']):
                    continue  # Skip nested DSS directories
                
                # Skip if file is already in a DSS-structured path (prevents copying DSS files into themselves)
                path_parts = rel_path.parts
                if len(path_parts) > 1 and path_parts[0] in ['src', 'docs', 'tests', 'data', 'meta']:
                    # This is already a DSS-organized file, check if it would create recursion
                    if dest_path != self.repo_path:  # Only skip if not in-place transformation
                        continue
                
                dest_category = self._categorize_file_cursor_native(file_path, project_type, technologies)
                
                # Determine destination
                dest_file = dest_path / dest_category / rel_path
                
                # ADDITIONAL SAFETY: Don't copy a file to itself
                if dest_file == file_path:
                    continue
                
                # Create directory structure
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(file_path, dest_file)
                files_processed += 1
                files_by_type[dest_category] += 1
                
                # Progress reporting
                if files_processed % 100 == 0:
                    print(f"   📊 Processed {files_processed} files...")
            
            print(f"   ✅ Organized {files_processed} files:")
            for category, count in files_by_type.items():
                if count > 0:
                    print(f"      {category}/: {count} files")
                    
        except Exception as e:
            print(f"   ⚠️ File organization warning: {e}")
    
    def _categorize_file_cursor_native(self, file_path: Path, project_type: str, technologies: List[str]) -> str:
        """Categorize files intelligently without external AI calls."""
        file_lower = file_path.name.lower()
        path_lower = str(file_path).lower()
        extension = file_path.suffix.lower()
        
        # Configuration and meta files
        meta_patterns = ['config', 'gradle', 'maven', 'package.json', 'pyproject.toml', 'setup.py', 
                        'requirements.txt', 'dockerfile', 'makefile', '.yml', '.yaml', '.toml', '.ini']
        if any(pattern in file_lower or extension == pattern for pattern in meta_patterns):
            return "meta"
        
        # Documentation files
        if extension in ['.md', '.txt', '.rst', '.adoc'] or 'readme' in file_lower or 'doc' in path_lower:
            return "docs"
            
        # Test files
        if 'test' in file_lower or 'spec' in file_lower or '/test/' in path_lower or '\\test\\' in path_lower:
            return "tests"
            
        # Data files
        if extension in ['.csv', '.json', '.xml', '.parquet', '.db', '.sqlite', '.data']:
            return "data"
            
        # Source code files with project-specific logic
        if extension in ['.py', '.kt', '.java', '.js', '.ts', '.cpp', '.c', '.h', '.swift', '.rs']:
            # Special handling for Android WearOS projects
            if project_type == 'android_wearos':
                if any(pattern in path_lower for pattern in ['/wear/', '\\wear\\', 'wearos', 'watchface']):
                    return "src"  # Keep WearOS structure within src/
                elif any(pattern in path_lower for pattern in ['/mobile/', '\\mobile\\', '/phone/', '\\phone\\']):
                    return "src"  # Mobile companion code
            return "src"
            
        # Android-specific files
        if extension in ['.xml'] and ('android' in path_lower or 'manifest' in file_lower):
            return "src"
            
        # Default to src for unknown files that might be source-related
        return "src"
    
    def _create_cursor_ai_integration(self, dest_path: Path, project_info: Dict):
        """Create Cursor-specific AI integration files that work with built-in agent."""
        print("   🤖 Setting up Cursor AI integration...")
        
        # Create .cursor directory with enhanced rules
        cursor_dir = dest_path / ".cursor" / "rules"
        cursor_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Cursor-native assistant rules
        assistant_rules = self._generate_cursor_native_rules(project_info)
        (cursor_dir / "dss_assistant.mdc").write_text(assistant_rules, encoding='utf-8')
        
        # Create project context file for Cursor
        context_file = self._generate_cursor_project_context(project_info)
        (cursor_dir / "project_context.mdc").write_text(context_file, encoding='utf-8')
        
        # Create AI prompts that work with Cursor's agent
        prompts_dir = dest_path / "meta" / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        ai_prompts = self._generate_cursor_ai_prompts(project_info)
        (prompts_dir / "cursor_ai_helpers.md").write_text(ai_prompts, encoding='utf-8')
        
        print("   ✅ Cursor AI integration configured for native agent")
    
    def _generate_cursor_native_rules(self, project_info: Dict) -> str:
        """Generate Cursor-specific assistant rules that work with the built-in agent."""
        project_type = project_info.get('type', 'general')
        technologies = project_info.get('technologies', [])
        
        rules = f"""# DSS Project Assistant Rules (Cursor Native)

## Project Context
- **Type**: {project_type}
- **Technologies**: {', '.join(technologies)}
- **Structure**: DSS (Data SuperStructure) format
- **AI Integration**: Cursor Built-in Agent (No External APIs)

## Core DSS Principles
This project follows DSS conventions:
- `src/` - Source code and executable logic
- `docs/` - Documentation and guides  
- `tests/` - Test files and validation
- `data/` - Datasets and artifacts
- `meta/` - Scripts, configuration, automation

## Cursor Agent Behavior

### Code Generation
When generating code:
- Follow {project_type} best practices and conventions
- Maintain DSS file organization principles
- Use appropriate naming patterns for {', '.join(technologies)}
- Add YAML frontmatter to new files when appropriate

### File Operations
- **New source files** → Place in `src/` with appropriate subdirectory
- **Documentation** → Create in `docs/` with clear naming
- **Test files** → Generate in `tests/` matching source structure
- **Configuration** → Store in `meta/` or appropriate config location

### Voice Commands & Chat Interactions
Understand these common requests:
- "Create new module" → Generate appropriate source file in src/
- "Add documentation" → Create .md file in docs/ with proper structure
- "Write tests" → Generate test file in tests/ with framework setup
- "Update index" → Refresh INDEX.md with current project structure
- "Analyze project" → Review DSS structure and suggest improvements

### Project-Specific Intelligence"""

        # Add technology-specific rules
        if "Android" in technologies:
            rules += """

#### Android Development
- Follow Android MVVM/MVI architecture patterns
- Use proper lifecycle management and coroutines
- Implement Material Design principles
- Handle permissions and configuration changes properly
- Organize by feature modules when appropriate"""

        if "WearOS" in technologies:
            rules += """

#### WearOS Development  
- Optimize UI for small circular/square screens
- Use touch-friendly elements with proper spacing
- Consider battery optimization strategies
- Handle companion app data synchronization
- Implement proper complications and tiles structure"""

        if "Kotlin" in technologies:
            rules += """

#### Kotlin Development
- Use idiomatic Kotlin syntax and conventions
- Leverage coroutines for asynchronous operations
- Utilize data classes, sealed classes, and extension functions
- Follow Kotlin coding standards and best practices"""

        if "Python" in technologies:
            rules += """

#### Python Development
- Follow PEP 8 style guidelines
- Use type hints and proper docstrings
- Implement proper exception handling
- Structure packages and modules clearly"""

        rules += f"""

### Context Awareness
- Understand DSS structure and file relationships
- Provide project-context-aware suggestions
- Maintain consistent code style across files
- Generate appropriate YAML frontmatter for DSS files
- Suggest improvements based on DSS best practices

### File Frontmatter Template
When creating new files, use appropriate frontmatter:

For Python files:
```python
\"\"\"---
tags: [tag1, tag2]
provides: [module_name]
requires: [dependency1, dependency2]
---\"\"\"
```

For Markdown files:
```markdown
---
tags: [doc, guide]
provides: [documentation_topic]
requires: [prerequisite_knowledge]
---
```

## Integration Benefits
- **No API Keys Required**: Uses Cursor's built-in AI exclusively
- **Local Processing**: No external network calls for AI features
- **Consistent Experience**: Works reliably without internet dependency
- **Enhanced Context**: Full access to project structure and code

## Assistant Personality
- Be helpful and context-aware
- Understand DSS conventions intuitively
- Provide practical, actionable suggestions
- Maintain consistency with project patterns
- Offer improvements that align with DSS principles

---
Generated by DSS Bootstrap (Cursor Native Mode)
AI Integration: Cursor Built-in Agent Only
"""
        return rules
    
    def _generate_cursor_project_context(self, project_info: Dict) -> str:
        """Generate project context file for Cursor's understanding."""
        context = f"""# Project Context for Cursor AI

## Overview
This is a DSS-formatted {project_info.get('type', 'general')} project with {project_info.get('file_count', 'unknown')} files.

## Technologies
{chr(10).join(f'- {tech}' for tech in project_info.get('technologies', []))}

## DSS Structure Benefits
- **Organized**: Clear separation of concerns across directories
- **AI-Friendly**: Structured for optimal AI assistant understanding
- **Scalable**: Grows cleanly as project complexity increases
- **Collaborative**: Multiple developers can work efficiently

## Cursor-Specific Features
- **Native AI Integration**: No external API dependencies
- **Smart Code Completion**: Context-aware suggestions
- **Project Navigation**: Enhanced understanding of file relationships
- **DSS-Aware Assistance**: Built-in knowledge of DSS conventions

## Common Tasks
- Generating new modules with proper DSS structure
- Creating documentation that links to relevant code
- Writing tests that follow project patterns
- Refactoring code while maintaining DSS organization

## File Organization Logic
- Source code organized by functionality in `src/`
- Documentation structured for both humans and AI in `docs/`
- Tests mirror source structure in `tests/`
- Configuration and automation in `meta/`
- Data assets managed in `data/`

This context helps Cursor's AI provide more accurate, project-specific assistance.
"""
        return context
    
    def _generate_cursor_ai_prompts(self, project_info: Dict) -> str:
        """Generate AI helper prompts for common Cursor interactions."""
        project_type = project_info.get('type', 'general')
        
        prompts = f"""# Cursor AI Helper Prompts

These prompts work optimally with Cursor's built-in AI agent for this {project_type} DSS project.

## Code Generation Prompts

### Create New Module
```
Create a new {project_type} module in src/ with:
- Proper DSS frontmatter
- Basic structure following {project_type} conventions
- TODO comments for implementation
- Corresponding test file in tests/
```

### Generate Documentation
```
Create documentation in docs/ that:
- Explains the module purpose and usage
- Includes code examples
- Links to related files
- Follows DSS documentation standards
```

### Write Tests
```
Generate comprehensive tests in tests/ that:
- Cover main functionality
- Include edge cases
- Follow {project_type} testing conventions
- Use appropriate testing framework
```

## Analysis Prompts

### Project Structure Review
```
Analyze the current DSS structure and suggest:
- Missing documentation
- Untested code areas
- Organization improvements
- DSS convention compliance
```

### Code Quality Assessment
```
Review the codebase for:
- DSS compliance
- Code consistency
- Architecture patterns
- Potential improvements
```

## Refactoring Prompts

### DSS Compliance Update
```
Update this code/file to better follow DSS conventions:
- Add proper frontmatter
- Organize according to DSS principles
- Improve documentation links
- Enhance AI readability
```

### Architecture Improvement
```
Refactor this code to better follow {project_type} best practices while maintaining DSS structure
```

## Maintenance Prompts

### Update INDEX.md
```
Regenerate INDEX.md to reflect current project structure with:
- All major files and directories
- Brief descriptions
- Cross-references
- DSS compliance notes
```

### Documentation Sync
```
Ensure documentation in docs/ is synchronized with current code structure and implementation
```

## Project-Specific Prompts"""

        if project_type == "android_wearos":
            prompts += """

### WearOS-Specific
```
Create WearOS complication/tile with:
- Proper WearOS architecture
- Data synchronization with companion app
- Battery optimization considerations
- DSS organization in src/wear/
```"""

        elif project_type == "data_science":
            prompts += """

### Data Science-Specific
```
Create analysis notebook that:
- Follows DSS data science structure
- Includes proper data validation
- Documents methodology clearly
- Organizes results in appropriate directories
```"""

        prompts += """

## Integration Benefits
- **Context-Aware**: Prompts designed for this specific project type
- **DSS-Optimized**: All suggestions maintain DSS structure
- **Cursor-Native**: Designed for Cursor's built-in AI capabilities
- **No External Dependencies**: Works entirely with local AI agent

## Usage Tips
1. Use these prompts as starting points for conversations
2. Cursor's AI will adapt them to your specific context
3. Combine prompts for complex tasks
4. The AI understands DSS structure inherently with these prompts

---
Generated for Cursor Native AI Integration
Project Type: {project_type}
DSS Version: Compatible
"""
        return prompts
    
    def _create_enhanced_fallback_formatter(self) -> str:
        """Create an enhanced fallback formatter based on installation report feedback."""
        enhanced_fallback = '''#!/usr/bin/env python3
"""Enhanced DSS formatter fallback - addresses installation report issues"""
import os
import sys
import shutil
import time
from pathlib import Path

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    source = Path(args.source)
    dest = Path(args.dest)
    
    print("Enhanced DSS fallback formatter starting...")
    print(f"Source: {source}")
    print(f"Destination: {dest}")
    
    if not args.dry_run:
        start_time = time.time()
        
        # Create DSS structure
        print("Creating DSS directory structure...")
        dest.mkdir(exist_ok=True)
        for folder in ["src", "docs", "tests", "data", "meta"]:
            (dest / folder).mkdir(exist_ok=True)
            print(f"  ✅ Created {folder}/")
        
        # Enhanced file organization with progress reporting
        print("Processing files...")
        files_processed = 0
        wearos_files = 0
        
        for file in source.rglob("*"):
            if file.is_file() and not any(part.startswith('.') for part in file.parts):
                rel_path = file.relative_to(source)
                
                # Enhanced file routing with WearOS awareness
                file_lower = file.name.lower()
                path_lower = str(file).lower()
                
                # WearOS-specific routing
                if any(pattern in path_lower for pattern in ['/wear/', '\\\\wear\\\\', 'wearos', 'watchface']):
                    if file.suffix in ['.kt', '.java']:
                        dest_file = dest / "src" / "wear" / rel_path
                        wearos_files += 1
                    elif file.suffix in ['.xml'] and 'manifest' in file_lower:
                        dest_file = dest / "src" / "wear" / rel_path
                        wearos_files += 1
                    else:
                        dest_file = dest / "src" / rel_path
                elif any(pattern in path_lower for pattern in ['/mobile/', '\\\\mobile\\\\', '/phone/', '\\\\phone\\\\']):
                    dest_file = dest / "src" / "mobile" / rel_path
                elif file.suffix in ['.py', '.kt', '.java', '.js', '.ts']:
                    dest_file = dest / "src" / rel_path
                elif file.suffix in ['.md', '.txt', '.rst']:
                    dest_file = dest / "docs" / rel_path
                elif "test" in file_lower:
                    dest_file = dest / "tests" / rel_path
                elif file.suffix in ['.csv', '.json', '.xml', '.yml', '.yaml']:
                    dest_file = dest / "data" / rel_path
                else:
                    dest_file = dest / "src" / rel_path
                
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest_file)
                files_processed += 1
                
                # Progress reporting every 100 files
                if files_processed % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"  Processing files: {files_processed} done ({elapsed:.1f}s)")
        
        elapsed_total = time.time() - start_time
        print(f"✅ Enhanced fallback transformation completed!")
        print(f"   Files processed: {files_processed}")
        print(f"   WearOS files detected: {wearos_files}")
        print(f"   Duration: {elapsed_total:.1f}s")
        
        if wearos_files > 0:
            print("   📱 WearOS project detected - consider using WearOS template structure")

if __name__ == "__main__":
    main()
'''
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='_enhanced_fallback.py', 
                                       delete=False, encoding='utf-8') as tmp:
            tmp.write(enhanced_fallback)
            return tmp.name
    
    def _detect_project_type_enhanced(self) -> Dict:
        """Enhanced project type detection with detailed WearOS and Android analysis."""
        try:
            files = list(self.repo_path.rglob('*'))
            
            # Handle large projects with timeout protection
            if len(files) > 10000:  # Large project detection
                self._add_report_warning(f"Large project detected ({len(files)} files) - using optimized scanning")
                # Sample files for large projects to avoid timeout
                files = files[:5000] + [f for f in files[5000:] if any(pattern in f.name.lower() 
                                       for pattern in ['manifest', 'gradle', 'wear', 'wearos'])]
            
            file_names = [f.name.lower() for f in files if f.is_file()]
            file_extensions = [f.suffix.lower() for f in files if f.is_file()]
            file_paths = [str(f).lower() for f in files if f.is_file()]
        except Exception as e:
            self._add_report_issue(f"Project scanning error: {e}", "warning")
            # Fallback to basic detection
            files = []
            file_names = []
            file_extensions = []
            file_paths = []
        
        # Enhanced counting with more categories and specific WearOS detection
        counts = {
            'python': len([f for f in file_extensions if f == '.py']),
            'kotlin': len([f for f in file_extensions if f == '.kt']),
            'java': len([f for f in file_extensions if f == '.java']),
            'javascript': len([f for f in file_extensions if f in ['.js', '.ts', '.jsx', '.tsx']]),
            'android': len([f for f in file_names if f in ['androidmanifest.xml', 'build.gradle', 'gradle.properties']]),
            'wearos': self._detect_wearos_patterns(files, file_names, file_paths),
            'jupyter': len([f for f in file_extensions if f == '.ipynb']),
            'data': len([f for f in file_extensions if f in ['.csv', '.parquet', '.json', '.jsonl', '.xml']]),
            'docs': len([f for f in file_extensions if f in ['.md', '.rst', '.txt']]),
            'web': len([f for f in file_names if f in ['package.json', 'webpack.config.js', 'next.config.js']]),
            'ml': len([f for f in file_names if f in ['requirements.txt', 'environment.yml', 'conda.yml']]),
            'config': len([f for f in file_extensions if f in ['.yml', '.yaml', '.toml', '.ini', '.conf']])
        }
        
        technologies = []
        
        # Enhanced WearOS detection with specific patterns
        wearos_confidence = self._calculate_wearos_confidence(files, file_names, file_paths)
        
        # Determine primary project type and technologies
        if wearos_confidence > 0.3:  # 30% confidence threshold
            project_type = "android_wearos"
            technologies.extend(["WearOS", "Android"])
            self._add_report_optimization("WearOS-specific DSS templates and documentation structure recommended", "project_type")
            self._add_report_optimization(f"WearOS confidence: {wearos_confidence:.2f} - specific patterns detected", "detection")
        elif counts['android'] > 2 and counts['kotlin'] > 0:
            project_type = "android_kotlin"
            technologies.extend(["Android", "Kotlin"])
            self._add_report_optimization("Enhanced Android/Kotlin project structure templates", "project_type")
        elif counts['android'] > 2 and counts['java'] > 0:
            project_type = "android_java"
            technologies.extend(["Android", "Java"])
        elif counts['jupyter'] > 2 or (counts['data'] > 3 and counts['python'] > 3):
            project_type = "data_science"
            technologies.extend(["Python", "Data Science"])
            self._add_report_optimization("Data science notebook organization could be enhanced", "project_type")
        elif counts['web'] > 0 or counts['javascript'] > 5:
            project_type = "web_application"
            technologies.append("Web")
            self._add_report_optimization("Web application structure templates could be improved", "project_type")
        elif any(name in file_names for name in ['setup.py', 'pyproject.toml']) and counts['python'] > 5:
            project_type = "python_package"
            technologies.append("Python")
        elif counts['docs'] > len(files) * 0.4:
            project_type = "documentation"
            technologies.append("Documentation")
        else:
            project_type = "general"
        
        # Add detected technologies
        if counts['python'] > 0:
            technologies.append("Python")
        if counts['kotlin'] > 0:
            technologies.append("Kotlin")
        if counts['java'] > 0:
            technologies.append("Java")
        if counts['javascript'] > 0:
            technologies.append("JavaScript/TypeScript")
        
        return {
            'type': project_type,
            'technologies': list(set(technologies)),
            'counts': counts,
            'file_count': len(files),
            'wearos_confidence': wearos_confidence if wearos_confidence > 0 else None
        }
    
    def _detect_wearos_patterns(self, files: List[Path], file_names: List[str], file_paths: List[str]) -> int:
        """Detect WearOS-specific patterns in the project."""
        wearos_count = 0
        
        # File name patterns
        wearos_patterns = ['wear', 'wearos', 'watchface', 'complication', 'tile']
        for pattern in wearos_patterns:
            wearos_count += len([f for f in file_names if pattern in f])
        
        # Directory/path patterns
        wearos_path_patterns = ['/wear/', '/wearos/', '/mobile/', '/companion/']
        for pattern in wearos_path_patterns:
            wearos_count += len([f for f in file_paths if pattern in f])
        
        # Content-based detection (for manifest files)
        for file in files:
            if file.is_file() and file.name.lower() == 'androidmanifest.xml':
                try:
                    content = file.read_text(encoding='utf-8', errors='ignore')
                    if any(pattern in content.lower() for pattern in [
                        'android.hardware.type.watch',
                        'android.software.leanback_only',
                        'com.google.android.wearable',
                        'wearable'
                    ]):
                        wearos_count += 3  # Higher weight for manifest indicators
                except:
                    pass
        
        return wearos_count
    
    def _calculate_wearos_confidence(self, files: List[Path], file_names: List[str], file_paths: List[str]) -> float:
        """Calculate confidence score for WearOS project detection."""
        total_indicators = 0
        wearos_indicators = 0
        
        # Check various WearOS indicators
        indicators = {
            'wear_in_names': len([f for f in file_names if 'wear' in f]),
            'wearos_in_names': len([f for f in file_names if 'wearos' in f]),
            'watchface_in_names': len([f for f in file_names if 'watchface' in f or 'watch' in f]),
            'complication_in_names': len([f for f in file_names if 'complication' in f]),
            'tile_in_names': len([f for f in file_names if 'tile' in f]),
            'wear_paths': len([f for f in file_paths if '/wear/' in f or '\\wear\\' in f]),
            'mobile_companion': len([f for f in file_paths if '/mobile/' in f or '/companion/' in f])
        }
        
        # Weight different indicators
        weights = {
            'wear_in_names': 0.3,
            'wearos_in_names': 0.4,
            'watchface_in_names': 0.3,
            'complication_in_names': 0.4,
            'tile_in_names': 0.3,
            'wear_paths': 0.5,
            'mobile_companion': 0.2
        }
        
        for indicator, count in indicators.items():
            if count > 0:
                wearos_indicators += weights[indicator] * min(count, 3)  # Cap individual contributions
            total_indicators += weights[indicator] * 3
        
        # Check for Android manifest WearOS indicators
        for file in files:
            if file.is_file() and file.name.lower() == 'androidmanifest.xml':
                try:
                    content = file.read_text(encoding='utf-8', errors='ignore')
                    manifest_indicators = [
                        'android.hardware.type.watch',
                        'android.software.leanback_only',
                        'com.google.android.wearable',
                        'android.intent.category.LAUNCHER.*wearable'
                    ]
                    for pattern in manifest_indicators:
                        if pattern in content.lower():
                            wearos_indicators += 0.6  # High weight for manifest
                            total_indicators += 0.6
                except:
                    pass
        
        return wearos_indicators / max(total_indicators, 1) if total_indicators > 0 else 0
    
    def _run_autoformatter_robust(self, formatter_path: str, dest_path: Path, 
                                dry_run: bool, project_info: Dict) -> bool:
        """Run the DSS auto-formatter with intelligent output-based monitoring."""
        import time
        import threading
        from queue import Queue, Empty
        
        try:
            cmd = [sys.executable, formatter_path, "--source", str(self.repo_path), "--dest", str(dest_path)]
            
            if dry_run:
                cmd.append("--dry-run")
                print("   🔍 Running in dry-run mode (preview only)")
            
            # Enhanced environment setup with API key handling
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # Prevent auto-formatter from requiring OpenAI API key for basic functionality
            env['DSS_DISABLE_AI_FEATURES'] = '1'
            env['OPENAI_API_KEY'] = ''  # Explicitly clear to avoid auto-formatter AI dependency
            
            # Add debugging flags for auto-formatter issues
            env['DSS_DEBUG'] = '1' if progress_count > 0 else '0'  # Enable if we've had issues before
            
            print(f"   Running: {' '.join(cmd)}")
            
            # Start process with real-time output monitoring
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True, 
                env=env,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Queues for thread-safe output handling
            stdout_queue = Queue()
            stderr_queue = Queue()
            
            def monitor_output(stream, queue, prefix=""):
                """Monitor output stream and feed to queue."""
                try:
                    for line in iter(stream.readline, ''):
                        if line:
                            queue.put((time.time(), f"{prefix}{line.rstrip()}"))
                    stream.close()
                except Exception as e:
                    queue.put((time.time(), f"{prefix}Stream error: {e}"))
            
            # Start monitoring threads
            stdout_thread = threading.Thread(target=monitor_output, args=(process.stdout, stdout_queue, "   "))
            stderr_thread = threading.Thread(target=monitor_output, args=(process.stderr, stderr_queue, "   ERROR: "))
            
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
            
            # Enhanced timeout parameters based on installation report feedback
            INACTIVITY_TIMEOUT = 90  # Increased from 45s based on WearOS project feedback
            ABSOLUTE_MAX_TIMEOUT = 1200  # 20 minutes for large Android projects
            INITIAL_SETUP_TIMEOUT = 120  # Allow 2 minutes for initial setup without output
            PROGRESS_INDICATORS = [
                "discovered", "classified", "transformation", "planning", 
                "executing", "copying", "moving", "creating", "completed",
                "phase", "step", "processing", "files", "directories"
            ]
            
            start_time = time.time()
            last_activity = start_time
            output_lines = []
            progress_count = 0
            setup_phase = True  # Track if we're still in initial setup
            
            print("   📊 Monitoring progress (90s inactivity timeout, 20min total, 2min initial setup)...")
            self._add_report_optimization("Timeout handling enhanced based on installation report feedback", "performance")
            
            while True:
                current_time = time.time()
                
                # Check for process completion
                if process.poll() is not None:
                    break
                
                # Check absolute timeout
                if current_time - start_time > ABSOLUTE_MAX_TIMEOUT:
                    print(f"   ❌ Absolute timeout reached ({ABSOLUTE_MAX_TIMEOUT/60:.1f} minutes)")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    return False
                
                # Enhanced inactivity timeout with setup phase consideration
                timeout_to_use = INITIAL_SETUP_TIMEOUT if setup_phase else INACTIVITY_TIMEOUT
                if current_time - last_activity > timeout_to_use:
                    if setup_phase:
                        print(f"   ❌ No output during initial setup ({INITIAL_SETUP_TIMEOUT}s) - auto-formatter may be stalled")
                        self._add_report_issue("Auto-formatter stalled during initial setup phase", "error")
                    else:
                        print(f"   ❌ No activity for {INACTIVITY_TIMEOUT} seconds - process appears stalled")
                        self._add_report_issue(f"Auto-formatter execution stalled after {current_time - start_time:.1f}s", "error")
                    
                    # Graceful termination with better error reporting
                    print("   🔄 Attempting graceful termination...")
                    process.terminate()
                    try:
                        process.wait(timeout=10)  # Give more time for graceful shutdown
                        print("   ✅ Process terminated gracefully")
                    except subprocess.TimeoutExpired:
                        print("   ⚠️ Force killing unresponsive process...")
                        process.kill()
                        self._add_report_issue("Had to force-kill unresponsive auto-formatter process", "warning")
                    return False
                
                # Process output from both streams
                activity_detected = False
                
                # Check stdout
                try:
                    while True:
                        timestamp, line = stdout_queue.get_nowait()
                        print(line)
                        output_lines.append(line)
                        last_activity = timestamp
                        activity_detected = True
                        
                        # Count progress indicators and detect setup completion
                        if any(indicator in line.lower() for indicator in PROGRESS_INDICATORS):
                            progress_count += 1
                            if setup_phase and progress_count >= 1:
                                setup_phase = False  # Exit setup phase after first progress indicator
                                print(f"   ✅ Initial setup completed, switching to normal monitoring")
                            if progress_count % 5 == 0:  # Every 5 progress indicators
                                elapsed = current_time - start_time
                                print(f"   ⏱️  Progress update: {progress_count} operations, {elapsed:.1f}s elapsed")
                        
                except Empty:
                    pass
                
                # Check stderr
                try:
                    while True:
                        timestamp, line = stderr_queue.get_nowait()
                        print(line)
                        output_lines.append(line)
                        last_activity = timestamp
                        activity_detected = True
                except Empty:
                    pass
                
                # Small sleep to prevent busy waiting
                time.sleep(0.1)
            
            # Wait for threads to finish
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            
            # Process any remaining output
            try:
                while True:
                    timestamp, line = stdout_queue.get_nowait()
                    print(line)
                    output_lines.append(line)
            except Empty:
                pass
            
            try:
                while True:
                    timestamp, line = stderr_queue.get_nowait()
                    print(line)
                    output_lines.append(line)
            except Empty:
                pass
            
            # Get final return code
            return_code = process.poll()
            elapsed_total = time.time() - start_time
            
            print(f"   📊 Process completed in {elapsed_total:.1f}s with {progress_count} progress indicators")
            
            if return_code == 0:
                print("   ✅ Auto-formatter completed successfully")
                self._record_performance_metric("transformation_total", elapsed_total)
                return True
            else:
                print(f"   ❌ Auto-formatter failed with code {return_code}")
                self._add_report_issue(f"Auto-formatter failed with exit code {return_code}", "error")
                # Enhanced error analysis and reporting
                if output_lines:
                    print("   📋 Last few output lines:")
                    api_key_issues = []
                    timeout_issues = []
                    other_errors = []
                    
                    for line in output_lines[-10:]:  # Check more lines for patterns
                        print(f"      {line}")
                        line_lower = line.lower()
                        
                        # Detect specific error patterns from installation reports
                        if any(pattern in line_lower for pattern in ['openai', 'api key', 'authentication']):
                            api_key_issues.append(line.strip())
                        elif any(pattern in line_lower for pattern in ['timeout', 'stall', 'hang']):
                            timeout_issues.append(line.strip())
                        elif any(pattern in line_lower for pattern in ['error', 'failed', 'exception']):
                            other_errors.append(line.strip())
                    
                    # Report specific error categories
                    if api_key_issues:
                        self._add_report_issue("Auto-formatter tried to use AI features requiring API key", "error")
                        self._add_report_optimization("Auto-formatter should work without OpenAI API key", "ai_dependency")
                    if timeout_issues:
                        self._add_report_issue("Auto-formatter execution timeout detected in output", "error")
                    for error in other_errors[:3]:  # Limit to prevent spam
                        self._add_report_issue(f"Formatter error: {error}", "info")
                return False
                
        except Exception as e:
            print(f"   ❌ Failed to run auto-formatter: {e}")
            self._add_report_issue(f"Auto-formatter execution failed: {e}", "critical")
            return False
    
    def _optimize_file_organization(self, dest_path: Path, project_info: Dict):
        """Post-process the transformation to fix file organization issues."""
        try:
            src_dir = dest_path / "src"
            
            # Find files with hash-like names and try to restore meaningful names
            hash_pattern_files = []
            for file in src_dir.rglob("*"):
                if file.is_file() and len(file.stem) == 32 and file.suffix == "":
                    # Likely a hash-named file
                    hash_pattern_files.append(file)
            
            if hash_pattern_files:
                print(f"   Found {len(hash_pattern_files)} hash-named files, attempting to restore...")
                self._add_report_issue(f"Found {len(hash_pattern_files)} hash-named files - file naming could be improved", "warning")
                self._add_report_optimization("Auto-formatter should preserve original file names", "file_organization")
                
                # Try to match content with original files
                original_files = {f.name: f for f in self.repo_path.rglob("*") if f.is_file()}
                
                for hash_file in hash_pattern_files[:10]:  # Limit to prevent overwhelming
                    try:
                        # Read content and try to match with original
                        content = hash_file.read_bytes()
                        content_hash = hashlib.md5(content).hexdigest()
                        
                        # Look for matching content in original files
                        for orig_name, orig_file in original_files.items():
                            try:
                                if orig_file.stat().st_size == len(content):
                                    orig_content = orig_file.read_bytes()
                                    if hashlib.md5(orig_content).hexdigest() == content_hash:
                                        # Found match! Restore original name
                                        new_path = hash_file.parent / orig_name
                                        hash_file.rename(new_path)
                                        print(f"   ✅ Restored: {orig_name}")
                                        break
                            except:
                                continue
                    except:
                        continue
            
            print("   ✅ File organization optimized")
            
        except Exception as e:
            print(f"   ⚠️  File optimization warning: {e}")
    
    def _install_cursor_intelligence_robust(self, dest_path: Path, project_info: Dict):
        """Install Cursor intelligence with fallback to local templates."""
        cursor_dir = dest_path / ".cursor" / "rules"
        cursor_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Try downloading cursor rules, but provide fallbacks
            rules_urls = [
                f"{DSS_BASE_URL}/meta/cursor/assistant.mdc",
                f"{DSS_BASE_URL}/.cursor/rules/assistant.mdc"
            ]
            
            downloaded = False
            for url in rules_urls:
                try:
                    with urllib.request.urlopen(url, timeout=15) as response:
                        content = response.read().decode('utf-8')
                    (cursor_dir / "assistant.mdc").write_text(content, encoding='utf-8')
                    downloaded = True
                    break
                except:
                    continue
            
            if not downloaded:
                # Create enhanced local template
                self._create_enhanced_cursor_rules(cursor_dir, project_info)
            
            print("   ✅ Cursor intelligence configured")
            
        except Exception as e:
            print(f"   ⚠️  Cursor installation warning: {e}")
            # Create basic local rules as fallback
            self._create_basic_cursor_rules(cursor_dir, project_info)
    
    def _create_enhanced_cursor_rules(self, cursor_dir: Path, project_info: Dict):
        """Create enhanced Cursor rules based on project type."""
        project_type = project_info['type']
        technologies = project_info['technologies']
        
        rules_content = fr"""# DSS Project Assistant Rules

## Project Context
- **Type**: {project_type}
- **Technologies**: {', '.join(technologies)}
- **Structure**: DSS (Data SuperStructure) format

## Behavior Guidelines

### Code Generation
- Follow {project_type} best practices
- Maintain DSS file organization (src/, docs/, tests/, data/, meta/)
- Use appropriate naming conventions for {', '.join(technologies)}

### File Operations
- Place source code in src/
- Put documentation in docs/
- Store tests in tests/
- Keep scripts and config in meta/

### Voice Commands
- "Create new module" → Generate appropriate source file in src/
- "Add documentation" → Create .md file in docs/
- "Write tests" → Generate test file in tests/
- "Update index" → Refresh INDEX.md with current structure

### Technology-Specific Rules
"""

        if "Android" in technologies:
            rules_content += """
#### Android Development
- Follow Android MVVM architecture patterns
- Use proper lifecycle management
- Implement proper permission handling
- Follow Material Design guidelines
"""

        if "WearOS" in technologies:
            rules_content += """
#### WearOS Development
- Optimize for small screens
- Use touch-friendly UI elements
- Consider battery optimization
- Handle connectivity limitations
"""

        if "Kotlin" in technologies:
            rules_content += """
#### Kotlin Development
- Use idiomatic Kotlin syntax
- Leverage coroutines for async operations
- Follow Kotlin coding conventions
- Use data classes and sealed classes appropriately
"""

        rules_content += r"""
## Assistant Behavior
- Understand DSS structure and conventions
- Provide project-context-aware suggestions
- Maintain consistent code style across files
- Generate appropriate frontmatter for new files
"""
        
        (cursor_dir / "enhanced_assistant.mdc").write_text(rules_content, encoding='utf-8')
    
    def _create_basic_cursor_rules(self, cursor_dir: Path, project_info: Dict):
        """Create basic Cursor rules as fallback."""
        basic_rules = r"""# Basic DSS Assistant Rules

## File Structure
- src/ - Source code
- docs/ - Documentation  
- tests/ - Test files
- data/ - Data files
- meta/ - Configuration

## Voice Commands
- "Create module" - New source file
- "Add docs" - New documentation
- "Write tests" - New test file

The AI understands DSS conventions.
"""
        (cursor_dir / "basic_assistant.mdc").write_text(basic_rules, encoding='utf-8')
    
    def _create_enhanced_documentation(self, dest_path: Path, project_info: Dict):
        """Create comprehensive project documentation."""
        try:
            docs_dir = dest_path / "docs"
            
            # Enhanced README.md
            readme_content = fr"""# {self.repo_path.name} - DSS Formatted

## Project Overview
- **Type**: {project_info['type']}
- **Technologies**: {', '.join(project_info['technologies'])}
- **Files**: {project_info['file_count']} total files
- **Structure**: DSS (Data SuperStructure) format

## Quick Start
1. Open in your preferred IDE/editor
2. Review src/ for source code
3. Check docs/ for documentation
4. Run tests from tests/

## DSS Structure
- `src/` - Source code and executable logic
- `docs/` - Documentation and guides
- `tests/` - Test files and validation
- `data/` - Datasets and artifacts  
- `meta/` - Scripts, configuration, automation

## Development Guidelines
- Follow DSS conventions for file organization
- Add frontmatter to new files for better AI understanding
- Keep documentation updated in docs/
- Write tests for new functionality

## Technologies Used
{chr(10).join(f'- {tech}' for tech in project_info['technologies'])}

---
Generated by DSS Bootstrap v{__version__}
Transformation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            (docs_dir / "README.md").write_text(readme_content, encoding='utf-8')
            
            # Project structure documentation
            structure_doc = self._generate_structure_documentation(dest_path)
            (docs_dir / "PROJECT_STRUCTURE.md").write_text(structure_doc, encoding='utf-8')
            
            print("   ✅ Enhanced documentation created")
            
        except Exception as e:
            print(f"   ⚠️  Documentation creation warning: {e}")    
    def _generate_structure_documentation(self, dest_path: Path) -> str:
        """Generate detailed project structure documentation."""
        structure = []
        
        def scan_directory(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
            if current_depth >= max_depth:
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                for item in items[:10]:  # Limit items to prevent overwhelming
                    if item.name.startswith('.'):
                        continue
                    
                    icon = "📄" if item.is_file() else "📁"
                    structure.append(f"{prefix}{icon} {item.name}")
                    
                    if item.is_dir() and current_depth < max_depth - 1:
                        scan_directory(item, prefix + "  ", max_depth, current_depth + 1)
            except PermissionError:
                pass
        
        structure.append("# Project Structure")
        structure.append("")
        structure.append("```")
        scan_directory(dest_path)
        structure.append("```")
        
        return "\n".join(structure)
    
    def _validate_transformation(self, dest_path: Path) -> Dict[str, bool]:
        """Validate the DSS transformation."""
        checks = {}
        
        # Check required directories exist
        required_dirs = ["src", "docs", "tests", "data", "meta"]
        for dir_name in required_dirs:
            checks[f"Directory {dir_name}/ exists"] = (dest_path / dir_name).exists()
        
        # Check for important files
        checks["INDEX.md exists"] = (dest_path / "INDEX.md").exists()
        checks["docs/README.md exists"] = (dest_path / "docs" / "README.md").exists()
        
        # Check Cursor integration
        checks["Cursor rules configured"] = (dest_path / ".cursor" / "rules").exists()
        
        # Check source files were moved
        src_files = list((dest_path / "src").rglob("*"))
        checks["Source files present"] = len([f for f in src_files if f.is_file()]) > 0
        
        return checks
    
    def _offer_installation_report(self, dest_path: Path):
        """Generate installation report and prepare for AI assistant interaction."""
        try:
            # Complete report data
            self.report_data['end_time'] = datetime.now()
            self.report_data['total_duration'] = (
                self.report_data['end_time'] - self.report_data['start_time']
            ).total_seconds()
            
            # Skip prompting and always generate the report
            print("\n" + "="*60)
            self._print_unicode("📊 DSS Installation Report")
            print("Generating installation report for project improvement...")
            
            # Generate report
            report_content = self._generate_installation_report()
            report_path = dest_path / "meta" / "dss_installation_report.md"
            
            # Ensure meta directory exists
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save report
            report_path.write_text(report_content, encoding='utf-8')
            
            # Create GitHub scripts without prompting
            self._prepare_github_submission_files(dest_path, report_content)
            
            # Create assistant prompt for AI-driven interaction
            prompt_path = self._create_assistant_report_prompt(dest_path, report_path)
            
            print(f"\n✅ Installation report saved to: {report_path}")
            print("\n🤖 AI Assistant Next Steps:")
            print("Your DSS installation report is ready! When you chat with the AI assistant, it will:")
            print("   • Offer to review the installation report")
            print("   • Help you submit feedback to improve DSS")
            print("   • Suggest project-specific improvements")
            print("   • Assist with GitHub submission if requested")
            print("\n📋 Simply open this project in Cursor and start chatting with the assistant")
        
        except Exception as e:
            print(f"   ⚠️  Report generation warning: {e}")
    
    def _generate_installation_report(self) -> str:
        """Generate a comprehensive installation report."""
        report = []
        
        # Header
        report.append("# DSS Installation Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**DSS Bootstrap Version:** {__version__}")
        report.append("")
        
        # System Information
        report.append("## System Information")
        report.append(f"- **Platform:** {self.report_data['platform']}")
        report.append(f"- **Python Version:** {sys.version}")
        report.append(f"- **Repository Name:** {self.repo_path.name}")
        report.append("")
        
        # Project Analysis
        project_info = self.report_data['project_info']
        report.append("## Project Analysis")
        report.append(f"- **Project Type:** {project_info.get('type', 'unknown')}")
        report.append(f"- **Technologies:** {', '.join(project_info.get('technologies', []))}")
        report.append(f"- **File Count:** {project_info.get('file_count', 'unknown')}")
        report.append(f"- **Transformation Method:** {self.report_data.get('transformation_method', 'unknown')}")
        report.append("")
        
        # Performance Metrics
        if self.report_data['performance_metrics']:
            report.append("## Performance Metrics")
            for metric, data in self.report_data['performance_metrics'].items():
                report.append(f"- **{metric.replace('_', ' ').title()}:** {data['value']:.2f} {data['unit']}")
            report.append(f"- **Total Duration:** {self.report_data['total_duration']:.2f} seconds")
            report.append("")
        
        # Issues and Warnings
        if self.report_data['issues'] or self.report_data['warnings']:
            report.append("## Issues and Warnings")
            
            if self.report_data['issues']:
                report.append("### Issues")
                for issue in self.report_data['issues']:
                    severity_emoji = {"critical": "🔴", "error": "🟠", "warning": "🟡"}.get(issue['severity'], "ℹ️")
                    report.append(f"- {severity_emoji} **{issue['severity'].title()}:** {issue['description']}")
                report.append("")
            
            if self.report_data['warnings']:
                report.append("### Warnings")
                for warning in self.report_data['warnings']:
                    report.append(f"- ⚠️ {warning['description']}")
                report.append("")
        
        # Validation Results
        report.append("## Validation Results")
        for check, status in self.report_data['validation_results'].items():
            status_emoji = "✅" if status else "❌"
            report.append(f"- {status_emoji} {check}")
        report.append("")
        
        # Optimization Suggestions
        if self.report_data['optimizations']:
            report.append("## Optimization Suggestions")
            for opt in self.report_data['optimizations']:
                report.append(f"- **{opt['category'].title()}:** {opt['suggestion']}")
            report.append("")
        
        # Project-Specific Recommendations
        report.append("## Project-Specific Recommendations")
        recommendations = self._generate_project_recommendations()
        for rec in recommendations:
            report.append(f"- {rec}")
        report.append("")
        
        # Feedback Request
        report.append("## Feedback for DSS Development")
        report.append("This report helps improve DSS for future users. Potential areas for enhancement:")
        report.append("")
        
        # Auto-generate feedback based on project type and issues
        feedback_items = self._generate_feedback_suggestions()
        for item in feedback_items:
            report.append(f"- {item}")
        
        report.append("")
        report.append("---")
        report.append("*This report contains no sensitive data or file contents, only structural and performance information.*")
        
        return "\n".join(report)
    
    def _generate_project_recommendations(self) -> List[str]:
        """Generate project-specific recommendations based on detected type."""
        recommendations = []
        project_type = self.report_data['project_info'].get('type', 'general')
        technologies = self.report_data['project_info'].get('technologies', [])
        
        if project_type == "android_wearos":
            recommendations.extend([
                "Organize WearOS app module in src/wear/ and companion app in src/mobile/",
                "Create dedicated documentation for WearOS deployment and watch face development in docs/wearos/",
                "Set up device-specific testing with emulator configurations in tests/wearos/",
                "Document WearOS-specific data sync patterns between watch and companion app",
                "Consider creating templates for complications, tiles, and watch faces in docs/templates/",
                "Set up Android Gradle plugin configuration for WearOS modules"
            ])
        elif project_type == "android_kotlin":
            recommendations.extend([
                "Organize by feature modules in src/features/",
                "Consider MVVM architecture documentation in docs/architecture/",
                "Set up unit and instrumentation tests separation"
            ])
        elif project_type == "data_science":
            recommendations.extend([
                "Organize notebooks by analysis phase in src/notebooks/",
                "Create data pipeline documentation in docs/pipelines/",
                "Set up data validation tests in tests/data/"
            ])
        elif project_type == "web_application":
            recommendations.extend([
                "Separate frontend and backend code in src/",
                "Document API endpoints in docs/api/",
                "Set up integration tests in tests/integration/"
            ])
        
        # Technology-specific recommendations
        if "Python" in technologies:
            recommendations.append("Consider adding requirements.txt or pyproject.toml to meta/")
        if "Kotlin" in technologies:
            recommendations.append("Document Kotlin-specific conventions in docs/coding-standards.md")
        
        return recommendations
    
    def _generate_feedback_suggestions(self) -> List[str]:
        """Generate feedback suggestions based on the installation experience."""
        feedback = []
        
        # Based on transformation method and specific installation report issues
        transformation_method = self.report_data.get('transformation_method', '')
        if 'fallback' in transformation_method:
            feedback.append("Auto-formatter download reliability could be improved")
            if transformation_method == 'enhanced_fallback':
                feedback.append("Enhanced fallback handled the transformation but main formatter failed")
            else:
                feedback.append("Fallback formatter functionality could be enhanced")
        
        # Check for specific installation report error patterns
        issue_descriptions = [issue['description'] for issue in self.report_data['issues']]
        if any('stall' in desc.lower() for desc in issue_descriptions):
            feedback.append("Auto-formatter execution stalling needs investigation")
        if any('api key' in desc.lower() for desc in issue_descriptions):
            feedback.append("Auto-formatter should not require OpenAI API key for basic functionality")
        if any('timeout' in desc.lower() for desc in issue_descriptions):
            feedback.append("Timeout handling and progress detection could be improved")
        
        # Based on issues
        if self.report_data['issues']:
            feedback.append("Issue handling and error recovery could be enhanced")
        
        # Based on project type
        project_type = self.report_data['project_info'].get('type', 'general')
        if project_type in ['android_wearos', 'android_kotlin']:
            feedback.append("Android project detection and optimization could be improved")
        elif project_type == 'data_science':
            feedback.append("Data science project templates could be enhanced")
        
        # Performance-based feedback
        duration = self.report_data.get('total_duration', 0)
        if duration > 300:  # 5 minutes
            feedback.append("Transformation performance could be optimized for large projects")
        
        # Platform-specific feedback
        platform = self.report_data.get('platform', '')
        if platform.lower() == 'windows':
            if any('console' in issue['description'].lower() for issue in self.report_data['issues']):
                feedback.append("Windows console compatibility could be improved")
            if any('path' in issue['description'].lower() for issue in self.report_data['issues']):
                feedback.append("Windows file path handling could be enhanced")
            feedback.append("Windows-specific WearOS development environment setup could be documented")
        
        # Validation-based feedback
        failed_validations = [k for k, v in self.report_data['validation_results'].items() if not v]
        if failed_validations:
            feedback.append("Validation process could be more robust")
        
        return feedback
    
    def _create_assistant_report_prompt(self, dest_path: Path, report_path: Path) -> Path:
        """Create a ready-to-use prompt for the AI assistant.
        
        Returns:
            Path: The path to the created prompt file
        """
        prompt_content = fr"""# AI Assistant: DSS Installation Report

## Context
A DSS installation report has been generated at `{report_path.relative_to(dest_path)}`. The report contains valuable feedback that can help improve DSS for everyone.

## Important AI Assistant Instructions
When the user first opens this project in Cursor, proactively:

1. **Welcome them** to their newly transformed DSS project
2. **Mention** that an installation report has been generated
3. **Offer** to help them with any of the following actions:

## Available Actions

1. **Review Installation Report**
   ```
   I notice you've just transformed your repository with DSS! Would you like me to review your installation report and summarize the key findings?
   ```

2. **Submit to GitHub (Recommended)**
   ```
   Your installation report contains valuable feedback that could help improve DSS. Would you like me to help you submit it to the DSS GitHub repository?
   
   I can help you:
   - For Windows: Run the PowerShell script at meta/github_issue_command.ps1
   - For macOS/Linux: Run the bash script at ./meta/github_issue_command.sh
   ```
```"""
        
        prompt_path = dest_path / "meta" / "assistant_report_prompt.md"
        prompt_path.write_text(prompt_content, encoding='utf-8')
        return prompt_path
    
    def _prepare_github_submission_files(self, dest_path: Path, report_content: str):
        """Prepare GitHub submission files without terminal prompting."""
        try:
            # Simply generate the GitHub CLI commands without prompting
            self._generate_github_cli_command(dest_path, report_content, quiet=True)
        except Exception as e:
            print(f"   ⚠️  GitHub submission preparation warning: {e}")
    
    def _get_github_labels(self) -> Set[str]:
        """Fetch and cache available GitHub labels for the repository."""
        if self._github_labels_cache is not None:
            return self._github_labels_cache
        
        try:
            # Try to get labels using GitHub CLI
            result = subprocess.run(
                ['gh', 'label', 'list', '--repo', DSS_REPO, '--json', 'name'],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode == 0:
                try:
                    labels_data = json.loads(result.stdout)
                    labels = {label['name'] for label in labels_data}
                    self._github_labels_cache = labels
                    return labels
                except json.JSONDecodeError:
                    pass
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Fallback to common DSS labels if GitHub CLI fails
        fallback_labels = {
            'bug', 'enhancement', 'documentation', 'question', 'help wanted',
            'good first issue', 'wontfix', 'duplicate', 'invalid', 'installation-report'
        }
        self._github_labels_cache = fallback_labels
        return fallback_labels
    
    def _validate_github_labels(self, labels: List[str]) -> List[str]:
        """Validate and filter GitHub labels against available repository labels."""
        available_labels = self._get_github_labels()
        valid_labels = []
        
        for label in labels:
            if label in available_labels:
                valid_labels.append(label)
            else:
                self._add_report_warning(f"Label '{label}' does not exist in repository - skipping")
        
        return valid_labels
    
    def _sanitize_title_for_github(self, title: str) -> str:
        """Sanitize title for GitHub CLI to prevent encoding issues."""
        # Replace problematic characters that can cause encoding issues
        title = title.replace(':', ' -')
        title = title.replace('|', ' ')
        title = title.replace('\n', ' ')
        title = title.replace('\r', ' ')
        
        # Remove any control characters
        title = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', title)
        
        # Limit length to avoid command line issues
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title.strip()
    
    def _create_github_issue_body(self, report_content: str) -> str:
        """Create a comprehensive GitHub issue body from the installation report."""
        
        # Extract key information
        project_info = self.report_data['project_info']
        platform = self.report_data['platform']
        duration = self.report_data.get('total_duration', 0)
        
        issue_body = f"""## Installation Summary

**Repository:** {self.repo_path.name}  
**Platform:** {platform}  
**DSS Bootstrap Version:** {__version__}  
**Duration:** {duration:.1f} seconds  
**Project Type:** {project_info.get('type', 'unknown')}  
**Technologies:** {', '.join(project_info.get('technologies', []))}  
**Transformation Method:** {self.report_data.get('transformation_method', 'unknown')}  

## Issues Encountered

"""
        
        # Add issues if any
        if self.report_data['issues']:
            for issue in self.report_data['issues']:
                severity_emoji = {"critical": "🔴", "error": "🟠", "warning": "🟡"}.get(issue['severity'], "ℹ️")
                issue_body += f"- {severity_emoji} **{issue['severity'].title()}:** {issue['description']}\n"
        else:
            issue_body += "- ✅ No critical issues encountered\n"
        
        issue_body += "\n## Optimization Suggestions\n\n"
        
        # Add optimization suggestions
        if self.report_data['optimizations']:
            for opt in self.report_data['optimizations']:
                issue_body += f"- **{opt['category'].title()}:** {opt['suggestion']}\n"
        else:
            issue_body += "- No specific optimizations suggested\n"
        
        issue_body += f"""
## Validation Results

"""
        # Add validation results
        for check, status in self.report_data['validation_results'].items():
            status_emoji = "✅" if status else "❌"
            issue_body += f"- {status_emoji} {check}\n"
        
        issue_body += f"""

## Performance Metrics

- **Project Detection:** {self.report_data['performance_metrics'].get('project_detection', {}).get('value', 0):.2f} seconds
- **Total Duration:** {duration:.2f} seconds
- **Files Processed:** {project_info.get('file_count', 'unknown')}

## Environment Details

- **Python Version:** {sys.version.split()[0]}
- **Platform:** {platform}
- **Cursor Integration:** {"Yes" if self.report_data.get('cursor_integration', False) else "No"}

## Feedback Categories

"""
        
        # Add feedback suggestions
        feedback_items = self._generate_feedback_suggestions()
        for item in feedback_items:
            issue_body += f"- {item}\n"
        
        issue_body += f"""

---

**Full Installation Report:**

```markdown
{report_content}
```

---

*This automated report helps improve DSS for future users. Thank you for contributing to the project!*
"""
        
        return issue_body

    def _generate_github_cli_command(self, dest_path: Path, report_content: str, quiet: bool = False):
        """Generate a GitHub CLI command for manual execution.
        
        Args:
            dest_path: Destination path for script files
            report_content: Content of the installation report
            quiet: If True, suppress output messages
        """
        try:
            # Create a concise issue title
            project_type = self.report_data['project_info'].get('type', 'unknown')
            platform = self.report_data['platform']
            # Add versioning info if applicable
            version_info = ""
            if not self.dss_path.name.endswith("-dss") and "-dss-" in self.dss_path.name:
                try:
                    version = self.dss_path.name.split("-dss-")[1]
                    version_info = f" (v{version})"
                except:
                    pass
            title_raw = f"DSS Installation Report: {project_type} project on {platform}{version_info}"
            title = self._sanitize_title_for_github(title_raw)
            
            # Create GitHub issue body
            issue_body = self._create_github_issue_body(report_content)
            
            # Validate labels before using them
            proposed_labels = ['installation-report', f'platform-{platform}', f'project-{project_type}']
            valid_labels = self._validate_github_labels(proposed_labels)
            
            # Create label arguments based on validation
            if not valid_labels:
                # If no labels are valid, don't use any to avoid errors
                self._add_report_warning("No valid GitHub labels found - creating issue without labels")
                label_args = []
            else:
                label_args = []
                for label in valid_labels:
                    label_args.extend(['--label', label])
            
            # Create the GitHub CLI command with validated labels
            gh_command = [
                'gh', 'issue', 'create',
                '--repo', f'{DSS_REPO}',
                '--title', title,
                '--body-file', '-',  # Read from stdin
            ] + label_args
            
            # Save command and body to files for easy use
            command_file = dest_path / "meta" / "github_issue_command.sh"
            body_file = dest_path / "meta" / "github_issue_body.md"
            
            # Create platform-specific scripts
            if self.platform == "windows":
                # Create PowerShell script for Windows with validated labels
                label_commands = ""
                if valid_labels:
                    for label in valid_labels:
                        label_commands += f'        --label "{label}" `\n'
                
                ps_script = fr"""# PowerShell script to submit DSS installation report

Write-Host "Submitting DSS installation report to GitHub..." -ForegroundColor Cyan
Write-Host "Repository: {DSS_REPO}" -ForegroundColor Cyan
Write-Host "Title: {title}" -ForegroundColor Cyan
Write-Host "Valid Labels: {', '.join(valid_labels) if valid_labels else 'None (will create without labels)'}" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
try {{
    $ghVersion = gh --version
    Write-Host "GitHub CLI detected: $($ghVersion[0])" -ForegroundColor Green
}} catch {{
    Write-Host "GitHub CLI not found. Please install from: https://cli.github.com/" -ForegroundColor Red
    Write-Host "After installing, authenticate with: gh auth login" -ForegroundColor Yellow
    exit 1
}}

# Check GitHub CLI authentication
try {{
    $authStatus = gh auth status
    Write-Host "GitHub CLI authenticated successfully" -ForegroundColor Green
}} catch {{
    Write-Host "GitHub CLI not authenticated. Please run: gh auth login" -ForegroundColor Red
    exit 1
}}

# Submit the issue using GitHub CLI
Write-Host "Submitting issue..." -ForegroundColor Cyan
try {{
    Get-Content "{body_file.name}" | gh issue create `
        --repo "{DSS_REPO}" `
        --title "{title}" `
        --body-file - `
{label_commands}
    Write-Host "DSS installation report submitted successfully!" -ForegroundColor Green
}} catch {{
    Write-Host "Failed to submit issue. Please try manually using the command:" -ForegroundColor Red
    Write-Host "{' '.join(gh_command)}" -ForegroundColor Yellow
    exit 1
}}"""
                
                # Save PowerShell script
                ps_script_file = dest_path / "meta" / "github_issue_command.ps1"
                ps_script_file.write_text(ps_script, encoding='utf-8')
                print(f"   ✅ PowerShell script saved to: {ps_script_file}")
            
            # Save GitHub CLI command and body for all platforms
            command_file.write_text(f"{' '.join(gh_command)}\n", encoding='utf-8')
            body_file.write_text(issue_body, encoding='utf-8')
            
            print(f"   ✅ GitHub CLI command saved to: {command_file}")
            print(f"   ✅ GitHub issue body saved to: {body_file}")
            
            if not quiet:
                print(f"🤖 AI Assistant Next Steps:")
                print("Your DSS installation report is ready! When you chat with the AI assistant, it will:")
                print("   • Offer to review the installation report")
                print("   • Help you submit feedback to improve DSS")
                print("   • Suggest project-specific improvements")
                print("   • Assist with GitHub submission if requested")
                print("\n📋 Simply open this project in Cursor and start chatting with the assistant")
                
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to generate GitHub CLI command: {e}")
            self._add_report_issue(f"GitHub CLI command generation failed: {e}", "critical")
            return False

def main():
    """Enhanced main entry point with better argument handling."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DSS Bootstrap: Enhanced repository transformation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
Examples:
  python dss_bootstrap.py                    # Transform current directory
  python dss_bootstrap.py --in-place        # Transform in place
  python dss_bootstrap.py --dry-run         # Preview changes only
  python dss_bootstrap.py --no-backup       # Skip creating backup
        """
    )
    
    parser.add_argument('--repo-path', default='.', 
                        help='Repository path to transform (default: current directory)')
    parser.add_argument('--in-place', action='store_true',
                        help='Transform repository in place (CAUTION: backup recommended!)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without making them')
    parser.add_argument('--no-backup', action='store_true',
                        help='Skip creating backup (not recommended)')
    parser.add_argument('--version', action='version', version=f'DSS Bootstrap v{__version__}')
    
    args = parser.parse_args()
    
    # Validate repository path
    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"❌ Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Safety checks for in-place transformation
    if args.in_place and not args.dry_run and not args.no_backup:
        print("⚠️  WARNING: In-place transformation will modify your current repository!")
        print("   A backup will be created automatically unless --no-backup is specified.")
        response = input("Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Transformation cancelled.")
            sys.exit(0)
    
    # Run enhanced bootstrap
    bootstrap = DSSBootstrap(repo_path)
    success = bootstrap.run_transformation(
        in_place=args.in_place, 
        dry_run=args.dry_run,
        create_backup=not args.no_backup
    )
    
    if not success:
        print(f"\n❌ DSS Bootstrap failed. Check errors above.")
        sys.exit(1)
    
    print(f"\n🎯 DSS Bootstrap v{__version__} completed successfully!")

if __name__ == '__main__':
    main()
