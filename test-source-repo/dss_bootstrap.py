#!/usr/bin/env python3
"""---
tags: [bootstrap, dss, automation, cursor, transformation, improved]
provides: [dss_bootstrap, robust_transformation]
requires: []
---

DSS Bootstrap: Enhanced Repository Transformation

Improvements:
- Cross-platform Unicode handling (Windows/Linux/Mac)
- Better Android/mobile project detection
- Graceful handling of missing remote resources
- Enhanced file organization with meaningful names
- Improved error handling and rollback capabilities
- Better validation and user feedback
- Installation report generation for community feedback
- Iterative versioning for output directories (v2.1.1)

Note: This is the consolidated script that includes all enhancements.
This is the only bootstrap script needed.

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
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from datetime import datetime

__version__ = "2.1.1"

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
    """Enhanced DSS transformation with robust error handling."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.original_path = self.repo_path
        self.dss_path = self._get_versioned_dss_path()
        self.backup_path = self.repo_path.parent / f"{self.repo_path.name}-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.platform = platform.system().lower()
        
        # Installation report data collection
        self.report_data = {
            'start_time': datetime.now(),
            'platform': self.platform,
            'python_version': sys.version,
            'issues': [],
            'warnings': [],
            'optimizations': [],
            'performance_metrics': {},
            'project_info': {},
            'validation_results': {},
            'transformation_method': 'unknown'
        }
        
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
        version = 1.0
        while True:
            versioned_path = self.repo_path.parent / f"{self.repo_path.name}-dss-{version}"
            if not versioned_path.exists():
                return versioned_path
            version += 1.0
            
        # Should never reach here, but just in case
        return base_path
    
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
            print("="*60)
            
            # Step 0: Create backup if requested
            if create_backup and not dry_run:
                self._print_unicode("💾 Step 0: Creating backup...")
                self._create_backup()
            
            # Step 1: Download auto-formatter with fallbacks
            self._print_unicode("📥 Step 1: Downloading DSS auto-formatter...")
            formatter_path = self._download_autoformatter_robust()
            if not formatter_path:
                self._add_report_issue("Failed to download DSS auto-formatter", "critical")
                return False
            
            # Step 2: Enhanced project detection
            self._print_unicode("🔍 Step 2: Analyzing project structure...")
            detection_start = time.time()
            project_info = self._detect_project_type_enhanced()
            self._record_performance_metric("project_detection", time.time() - detection_start)
            self.report_data['project_info'] = project_info
            print(f"   Detected project type: {project_info['type']}")
            print(f"   Key technologies: {', '.join(project_info['technologies'])}")
            
            # Step 3: Run transformation with validation
            self._print_unicode("⚡ Step 3: Running DSS transformation...")
            
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
                except:
                    pass
                
            success = self._run_autoformatter_robust(formatter_path, dest_path, dry_run, project_info)
            if not success:
                return False
            
            # Step 4: Post-process file organization
            if not dry_run:
                self._print_unicode("🎯 Step 4: Optimizing file organization...")
                self._optimize_file_organization(dest_path, project_info)
            
            # Step 5: Install Cursor intelligence with fallbacks
            self._print_unicode("🧠 Step 5: Installing Cursor AI intelligence...")
            self._install_cursor_intelligence_robust(dest_path, project_info)
            
            # Step 6: Create enhanced project documentation
            self._print_unicode("📚 Step 6: Generating project documentation...")
            self._create_enhanced_documentation(dest_path, project_info)
            
            # Step 7: Validate transformation
            self._print_unicode("✅ Step 7: Validating transformation...")
            validation_result = self._validate_transformation(dest_path)
            self.report_data['validation_results'] = validation_result
            
            # Step 8: Offer installation report
            self._print_unicode("📝 Step 8: Installation report...")
            
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
        """Print Unicode text with cross-platform compatibility."""
        try:
            print(text)
        except UnicodeEncodeError:
            # Fallback for systems that can't handle Unicode
            clean_text = text.encode('ascii', 'replace').decode('ascii')
            print(clean_text)
    
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
        
        # If all downloads fail, create a minimal fallback formatter
        print("   ⚠️  All downloads failed, creating fallback formatter...")
        self._add_report_warning("Auto-formatter download failed, using fallback")
        self._add_report_optimization("Improve auto-formatter download reliability", "infrastructure")
        self.report_data['transformation_method'] = 'fallback'
        return self._create_fallback_formatter()
    
    def _create_fallback_formatter(self) -> str:
        """Create a minimal fallback formatter when download fails."""
        fallback_formatter = '''#!/usr/bin/env python3
"""Minimal DSS formatter fallback"""
import os
import sys
import shutil
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
    
    if not args.dry_run:
        # Create basic DSS structure
        dest.mkdir(exist_ok=True)
        for folder in ["src", "docs", "tests", "data", "meta"]:
            (dest / folder).mkdir(exist_ok=True)
        
        # Copy files with basic organization
        for file in source.rglob("*"):
            if file.is_file() and not any(part.startswith('.') for part in file.parts):
                rel_path = file.relative_to(source)
                
                # Basic file routing
                if file.suffix in ['.py', '.kt', '.java', '.js', '.ts']:
                    dest_file = dest / "src" / rel_path
                elif file.suffix in ['.md', '.txt', '.rst']:
                    dest_file = dest / "docs" / rel_path
                elif "test" in file.name.lower():
                    dest_file = dest / "tests" / rel_path
                else:
                    dest_file = dest / "src" / rel_path
                
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest_file)
    
    print("Fallback DSS transformation completed")

if __name__ == "__main__":
    main()
'''
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='_fallback_formatter.py', 
                                       delete=False, encoding='utf-8') as tmp:
            tmp.write(fallback_formatter)
            return tmp.name
    
    def _detect_project_type_enhanced(self) -> Dict:
        """Enhanced project type detection with detailed analysis."""
        files = list(self.repo_path.rglob('*'))
        file_names = [f.name.lower() for f in files if f.is_file()]
        file_extensions = [f.suffix.lower() for f in files if f.is_file()]
        
        # Enhanced counting with more categories
        counts = {
            'python': len([f for f in file_extensions if f == '.py']),
            'kotlin': len([f for f in file_extensions if f == '.kt']),
            'java': len([f for f in file_extensions if f == '.java']),
            'javascript': len([f for f in file_extensions if f in ['.js', '.ts', '.jsx', '.tsx']]),
            'android': len([f for f in file_names if f in ['androidmanifest.xml', 'build.gradle', 'gradle.properties']]),
            'wearos': len([f for f in files if 'wear' in str(f).lower() or 'wearos' in str(f).lower()]),
            'jupyter': len([f for f in file_extensions if f == '.ipynb']),
            'data': len([f for f in file_extensions if f in ['.csv', '.parquet', '.json', '.jsonl', '.xml']]),
            'docs': len([f for f in file_extensions if f in ['.md', '.rst', '.txt']]),
            'web': len([f for f in file_names if f in ['package.json', 'webpack.config.js', 'next.config.js']]),
            'ml': len([f for f in file_names if f in ['requirements.txt', 'environment.yml', 'conda.yml']]),
            'config': len([f for f in file_extensions if f in ['.yml', '.yaml', '.toml', '.ini', '.conf']])
        }
        
        technologies = []
        
        # Determine primary project type and technologies
        if counts['wearos'] > 0 or any('wear' in str(f).lower() for f in files):
            project_type = "android_wearos"
            technologies.extend(["WearOS", "Android"])
            self._add_report_optimization("Consider WearOS-specific DSS templates", "project_type")
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
            'file_count': len(files)
        }
    
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
            
            # Enhanced environment setup
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'
            
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
            
            # Intelligent monitoring parameters
            INACTIVITY_TIMEOUT = 45  # Seconds of no output before considering stalled
            ABSOLUTE_MAX_TIMEOUT = 900  # 15 minutes absolute maximum
            PROGRESS_INDICATORS = [
                "discovered", "classified", "transformation", "planning", 
                "executing", "copying", "moving", "creating", "completed",
                "phase", "step", "processing", "files", "directories"
            ]
            
            start_time = time.time()
            last_activity = start_time
            output_lines = []
            progress_count = 0
            
            print("   📊 Monitoring progress (will timeout after 45s of inactivity or 15min total)...")
            
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
                
                # Check inactivity timeout
                if current_time - last_activity > INACTIVITY_TIMEOUT:
                    print(f"   ❌ No activity for {INACTIVITY_TIMEOUT} seconds - process appears stalled")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
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
                        
                        # Count progress indicators
                        if any(indicator in line.lower() for indicator in PROGRESS_INDICATORS):
                            progress_count += 1
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
                # Show last few lines of output for debugging
                if output_lines:
                    print("   📋 Last few output lines:")
                    for line in output_lines[-5:]:
                        print(f"      {line}")
                        # Collect error details for report
                        if "error" in line.lower() or "failed" in line.lower():
                            self._add_report_issue(f"Formatter output: {line.strip()}", "info")
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
        report.append(f"- **Python Version:** {self.report_data['python_version'].split()[0]}")
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
                "Consider organizing WearOS-specific modules in src/wearos/",
                "Create dedicated documentation for WearOS deployment in docs/wearos/",
                "Set up device-specific testing in tests/devices/"
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
        
        # Based on transformation method
        if self.report_data.get('transformation_method') == 'fallback':
            feedback.append("Auto-formatter download reliability could be improved")
            feedback.append("Fallback formatter functionality could be enhanced")
        
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
    
    def _generate_github_cli_command(self, dest_path: Path, report_content: str, quiet: bool = False):
        """Generate a GitHub CLI command for manual execution.
        
        Args:
            dest_path: Destination path for script files
            report_content: Content of the installation report
            quiet: If True, suppress output messages
        """
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
        title = f"DSS Installation Report: {project_type} project on {platform}{version_info}"
        
        # Create GitHub issue body
        issue_body = self._create_github_issue_body(report_content)
        
        # Create the GitHub CLI command
        gh_command = [
            'gh', 'issue', 'create',
            '--repo', f'{DSS_REPO}',
            '--title', title,
            '--body-file', '-',  # Read from stdin
            '--label', 'installation-report',
            '--label', f'platform-{platform}',
            '--label', f'project-{project_type}'
        ]
        
        # Save command and body to files for easy use
        command_file = dest_path / "meta" / "github_issue_command.sh"
        body_file = dest_path / "meta" / "github_issue_body.md"
        
        # Create platform-specific scripts
        if self.platform == "windows":
            # Create PowerShell script for Windows
            ps_script = fr"""# PowerShell script to submit DSS installation report

Write-Host "Submitting DSS installation report to GitHub..." -ForegroundColor Cyan
Write-Host "Repository: {DSS_REPO}" -ForegroundColor Cyan
Write-Host "Title: {title}" -ForegroundColor Cyan
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
        --label "installation-report" `
        --label "platform-{platform}" `
        --label "project-{project_type}"
    
    Write-Host ""
    Write-Host "Issue submitted! Thank you for helping improve DSS." -ForegroundColor Green
}} catch {{
    Write-Host "Error submitting issue: $_" -ForegroundColor Red
    Write-Host "Please try manually submitting the report from {body_file.name}" -ForegroundColor Yellow
}} 
"""
            ps_file = dest_path / "meta" / "github_issue_command.ps1"
            ps_file.write_text(ps_script, encoding='utf-8')
            
        # Create bash script for all platforms (Unix & Windows with Git Bash)
        shell_script = fr"""#!/bin/bash
# Generated GitHub CLI command to submit DSS installation report

echo "Submitting DSS installation report to GitHub..."
echo "Repository: {DSS_REPO}"
echo "Title: {title}"
echo ""

# Submit the issue using GitHub CLI
cat "{body_file.name}" | {' '.join(f'"{arg}"' if ' ' in arg else arg for arg in gh_command)}

echo ""
echo "Issue submitted! Thank you for helping improve DSS."
"""
        
        command_file.write_text(shell_script, encoding='utf-8')
        body_file.write_text(issue_body, encoding='utf-8')
        
        # Make shell script executable on Unix-like systems
        try:
            import stat
            command_file.chmod(command_file.stat().st_mode | stat.S_IEXEC)
        except:
            pass
        
        if not quiet:
            print(f"\n✅ GitHub submission files created:")
            print(f"   📄 Issue body: {body_file}")
            print(f"   🚀 Command script: {command_file}")
            
            if self.platform == "windows":
                ps_file = dest_path / "meta" / "github_issue_command.ps1"
                print(f"   🔷 PowerShell script: {ps_file}")
                print(f"\nTo submit the issue (Windows):")
                print(f"   1. Ensure GitHub CLI is installed: https://cli.github.com/")
                print(f"   2. Authenticate: gh auth login")
                print(f"   3. Run in PowerShell: {ps_file}")
                print(f"   Or in Command Prompt: powershell -ExecutionPolicy Bypass -File {ps_file}")
            else:
                print(f"\nTo submit the issue:")
                print(f"   1. Ensure GitHub CLI is installed: https://cli.github.com/")
                print(f"   2. Authenticate: gh auth login")
                print(f"   3. Run: {command_file}")
                
            print(f"\nOr manually run:")
            print(f"   cd {dest_path}")
            print(f"   cat {body_file.name} | {' '.join(gh_command)}")
    
    # The following method is not used in the current implementation but kept for reference
    def _auto_submit_github_issue(self, dest_path: Path, report_content: str):
        """Attempt to automatically submit the GitHub issue."""
        try:
            # Check if GitHub CLI is available
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("   ❌ GitHub CLI not found. Please install from: https://cli.github.com/")
                print("   Falling back to manual command generation...")
                self._generate_github_cli_command(dest_path, report_content)
                return
            
            print("   ✅ GitHub CLI found")
            
            # Check authentication
            auth_result = subprocess.run(['gh', 'auth', 'status'], 
                                       capture_output=True, text=True, timeout=10)
            if auth_result.returncode != 0:
                print("   ❌ GitHub CLI not authenticated.")
                print("   Please run: gh auth login")
                print("   Falling back to manual command generation...")
                self._generate_github_cli_command(dest_path, report_content)
                return
            
            print("   ✅ GitHub CLI authenticated")
            
            # Create issue title and body
            project_type = self.report_data['project_info'].get('type', 'unknown')
            platform = self.report_data['platform']
            title = f"DSS Installation Report: {project_type} project on {platform}"
            issue_body = self._create_github_issue_body(report_content)
            
            # Submit the issue
            print("   🚀 Submitting GitHub issue...")
            
            cmd = [
                'gh', 'issue', 'create',
                '--repo', DSS_REPO,
                '--title', title,
                '--body', issue_body,
                '--label', 'installation-report',
                '--label', f'platform-{platform}',
                '--label', f'project-{project_type}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                issue_url = result.stdout.strip()
                print(f"   ✅ Issue created successfully!")
                print(f"   🔗 Issue URL: {issue_url}")
                print(f"   🙏 Thank you for helping improve DSS!")
            else:
                print(f"   ❌ Failed to create issue: {result.stderr}")
                print("   Falling back to manual command generation...")
                self._generate_github_cli_command(dest_path, report_content)
                
        except subprocess.TimeoutExpired:
            print("   ❌ GitHub CLI command timed out")
            self._generate_github_cli_command(dest_path, report_content)
        except Exception as e:
            print(f"   ❌ Auto-submission failed: {e}")
            print("   Falling back to manual command generation...")
            self._generate_github_cli_command(dest_path, report_content)
    
    def _create_github_issue_body(self, report_content: str) -> str:
        """Create a GitHub issue body from the installation report."""
        # Extract key sections for the GitHub issue
        project_info = self.report_data['project_info']
        
        issue_body = fr"""## DSS Installation Report

**Auto-generated installation report from DSS Bootstrap v{__version__}**

### Quick Summary
- **Project Type**: {project_info.get('type', 'unknown')}
- **Technologies**: {', '.join(project_info.get('technologies', []))}
- **Platform**: {self.report_data['platform']}
- **Duration**: {self.report_data.get('total_duration', 0):.1f} seconds
- **Transformation Method**: {self.report_data.get('transformation_method', 'unknown')}

### Issues Encountered
"""
        
        if self.report_data['issues']:
            for issue in self.report_data['issues']:
                severity_emoji = {"critical": "🔴", "error": "🟠", "warning": "🟡"}.get(issue['severity'], "ℹ️")
                issue_body += f"- {severity_emoji} **{issue['severity'].title()}**: {issue['description']}\n"
        else:
            issue_body += "- ✅ No issues encountered\n"
        
        issue_body += "\n### Optimization Suggestions\n"
        
        if self.report_data['optimizations']:
            for opt in self.report_data['optimizations']:
                issue_body += f"- **{opt['category'].title()}**: {opt['suggestion']}\n"
        else:
            issue_body += "- No specific optimizations suggested\n"
        
        issue_body += fr"""
### Validation Results
"""
        
        passed = sum(1 for v in self.report_data['validation_results'].values() if v)
        total = len(self.report_data['validation_results'])
        issue_body += f"- **Validation Score**: {passed}/{total} checks passed\n"
        
        for check, status in self.report_data['validation_results'].items():
            status_emoji = "✅" if status else "❌"
            issue_body += f"- {status_emoji} {check}\n"
        
        issue_body += fr"""

### Performance Metrics
- **Total Duration**: {self.report_data.get('total_duration', 0):.2f} seconds
"""
        
        for metric, data in self.report_data['performance_metrics'].items():
            issue_body += f"- **{metric.replace('_', ' ').title()}**: {data['value']:.2f} {data['unit']}\n"
        
        issue_body += fr"""

---

<details>
<summary>Full Installation Report</summary>

```markdown
{report_content}
```

</details>

**Note**: This report contains no sensitive data or file contents, only structural and performance information to help improve DSS.
"""
        
        return issue_body

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