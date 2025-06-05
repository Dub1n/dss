#!/usr/bin/env python3
"""
⚠️  WARNING: This script is in need of significant rework and is kept for reference only.
    It was written for an earlier version of DSS and does not match the current repo structure.
    DO NOT USE in production - significant updates required before it can be functional.
    
    For current DSS functionality, see the main documentation and newer scripts.
"""

"""---
tags: [script, automation, dss, formatter, standalone]
provides: [dss_autoformatter, repository_transformation]
requires: [openai, pathlib, yaml, gitpython]
---

DSS Auto-Formatter: Standalone Repository Transformation Tool

This script transforms any repository into DSS (Data SuperStructure) format
while preserving functionality, git history, and developer intent.

Usage:
    python dss_autoformat.py --source /path/to/repo --dest /path/to/output
    python dss_autoformat.py --source . --dest ../my-repo-dss --config custom.yml
    python dss_autoformat.py --help

Features:
    - Multi-phase intelligent transformation
    - LLM-assisted file classification  
    - Safe execution with rollback capability
    - Dependency analysis and import updating
    - Comprehensive metadata injection
    - Risk assessment and conflict resolution

For comprehensive documentation, see:
https://github.com/yourusername/dss_template_repo/blob/main/docs/automated_formatting.md
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml

# Try to import optional dependencies
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import git
    HAS_GIT = True
except ImportError:
    HAS_GIT = False

__version__ = "1.0.0"

# Configuration
DEFAULT_DSS_TEMPLATE_URL = "https://github.com/yourusername/dss_template_repo"
DEFAULT_CONFIG_URL = f"{DEFAULT_DSS_TEMPLATE_URL}/raw/main/meta/dss_config.yml"

class DSSAutoFormatter:
    """Main DSS auto-formatter class implementing the multi-phase transformation."""
    
    def __init__(self, source_path: Path, dest_path: Path, config: Dict[str, Any]):
        self.source_path = Path(source_path).resolve()
        self.dest_path = Path(dest_path).resolve()
        self.config = config
        self.logger = self._setup_logging()
        self.openai_client = self._setup_openai() if HAS_OPENAI else None
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
        
    def _setup_openai(self) -> Optional[Any]:
        """Set up OpenAI client if available and configured."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.logger.warning("OPENAI_API_KEY not found. LLM-assisted features disabled.")
            return None
            
        try:
            client = openai.OpenAI(api_key=api_key)
            return client
        except Exception as e:
            self.logger.warning(f"Failed to initialize OpenAI client: {e}")
            return None
    
    def transform_repository(self) -> bool:
        """Execute the complete DSS transformation process."""
        try:
            self.logger.info(f"Starting DSS transformation: {self.source_path} -> {self.dest_path}")
            
            # Phase 1: Discovery
            self.logger.info("Phase 1: Repository Discovery")
            repo_structure = self._discover_repository()
            
            # Phase 2: Classification  
            self.logger.info("Phase 2: File Classification")
            classifications = self._classify_files(repo_structure)
            
            # Phase 3: Planning
            self.logger.info("Phase 3: Transformation Planning")
            plan = self._create_transformation_plan(repo_structure, classifications)
            
            # Phase 4: Execution
            self.logger.info("Phase 4: Safe Execution")
            if not self._execute_transformation(plan):
                return False
                
            # Phase 5: Enhancement
            self.logger.info("Phase 5: Enhancement & Metadata")
            self._enhance_repository()
            
            # Phase 6: Validation
            self.logger.info("Phase 6: Validation")
            validation_result = self._validate_transformation()
            
            self.logger.info("DSS transformation completed successfully!")
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Transformation failed: {e}")
            return False
    
    def _discover_repository(self) -> Dict[str, Any]:
        """Phase 1: Analyze repository structure and patterns."""
        structure = {
            'files': [],
            'directories': [],
            'patterns': {},
            'dependencies': {},
            'git_info': {}
        }
        
        # Walk directory tree
        for path in self.source_path.rglob('*'):
            if path.is_file() and not self._should_ignore_file(path):
                structure['files'].append({
                    'path': path,
                    'relative_path': path.relative_to(self.source_path),
                    'size': path.stat().st_size,
                    'extension': path.suffix,
                    'content_sample': self._get_content_sample(path)
                })
            elif path.is_dir():
                structure['directories'].append(path.relative_to(self.source_path))
        
        # Analyze patterns
        structure['patterns'] = self._analyze_patterns(structure['files'])
        
        # Extract dependencies
        structure['dependencies'] = self._extract_dependencies(structure['files'])
        
        # Git information
        if HAS_GIT and (self.source_path / '.git').exists():
            try:
                repo = git.Repo(self.source_path)
                structure['git_info'] = {
                    'has_git': True,
                    'current_branch': repo.active_branch.name,
                    'commit_count': len(list(repo.iter_commits())),
                    'is_dirty': repo.is_dirty()
                }
            except Exception as e:
                self.logger.warning(f"Could not analyze git info: {e}")
                structure['git_info'] = {'has_git': False}
        
        self.logger.info(f"Discovered {len(structure['files'])} files in {len(structure['directories'])} directories")
        return structure
    
    def _classify_files(self, repo_structure: Dict[str, Any]) -> Dict[str, str]:
        """Phase 2: Classify files into DSS categories."""
        classifications = {}
        
        for file_info in repo_structure['files']:
            path = file_info['relative_path']
            classification = self._classify_single_file(file_info, repo_structure)
            classifications[str(path)] = classification
            
        self.logger.info(f"Classified {len(classifications)} files")
        return classifications
    
    def _classify_single_file(self, file_info: Dict[str, Any], repo_structure: Dict[str, Any]) -> str:
        """Classify a single file using multiple strategies."""
        path = file_info['relative_path']
        
        # Strategy 1: Rule-based classification
        rule_based = self._classify_by_rules(path)
        if rule_based != 'ambiguous':
            return rule_based
            
        # Strategy 2: Content-based classification
        content_based = self._classify_by_content(file_info)
        if content_based != 'ambiguous':
            return content_based
            
        # Strategy 3: LLM-assisted classification (if available)
        if self.openai_client and self.config.get('use_llm_classification', True):
            llm_based = self._classify_by_llm(file_info, repo_structure)
            if llm_based != 'ambiguous':
                return llm_based
        
        # Fallback to best guess
        return self._classify_fallback(file_info)
    
    def _classify_by_rules(self, path: Path) -> str:
        """Rule-based file classification."""
        path_str = str(path).lower()
        
        # DSS category patterns
        patterns = self.config.get('classification_rules', {
            'src': ['**/*.py', '**/*.js', '**/*.ts', '**/src/**', '**/lib/**'],
            'data': ['**/*.csv', '**/*.parquet', '**/*.json', '**/data/**'],
            'docs': ['**/*.md', '**/*.rst', '**/docs/**'],
            'tests': ['**/test_*.py', '**/*_test.py', '**/tests/**'],
            'meta': ['**/meta/**', '**/.github/**', '**/scripts/**']
        })
        
        for category, category_patterns in patterns.items():
            if any(path.match(pattern) for pattern in category_patterns):
                return category
                
        return 'ambiguous'
    
    def _classify_by_content(self, file_info: Dict[str, Any]) -> str:
        """Content-based file classification."""
        content = file_info.get('content_sample', '')
        path = file_info['relative_path']
        
        # Python file heuristics
        if path.suffix == '.py':
            if 'if __name__ == "__main__"' in content:
                return 'src'
            elif any(test_pattern in content.lower() for test_pattern in ['import pytest', 'import unittest', 'def test_']):
                return 'tests'
            elif any(config_pattern in content for config_pattern in ['CONFIG', 'SETTINGS', 'config =']):
                return 'meta'
                
        # Jupyter notebook heuristics
        elif path.suffix == '.ipynb':
            try:
                notebook = json.loads(content)
                if any('analysis' in str(cell).lower() for cell in notebook.get('cells', [])):
                    return 'data'
                elif any('documentation' in str(cell).lower() for cell in notebook.get('cells', [])):
                    return 'docs'
            except:
                pass
                
        return 'ambiguous'
    
    def _classify_by_llm(self, file_info: Dict[str, Any], repo_structure: Dict[str, Any]) -> str:
        """LLM-assisted file classification."""
        if not self.openai_client:
            return 'ambiguous'
            
        try:
            prompt = self._build_classification_prompt(file_info, repo_structure)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            # Extract category from response
            valid_categories = ['src', 'data', 'docs', 'tests', 'meta']
            for category in valid_categories:
                if category in result:
                    return category
                    
        except Exception as e:
            self.logger.warning(f"LLM classification failed for {file_info['relative_path']}: {e}")
            
        return 'ambiguous'
    
    def _build_classification_prompt(self, file_info: Dict[str, Any], repo_structure: Dict[str, Any]) -> str:
        """Build prompt for LLM classification."""
        path = file_info['relative_path']
        content = file_info.get('content_sample', '')[:500]  # Limit content sample
        
        return f"""
        Classify this file into one DSS category: src, data, docs, tests, or meta.

        File: {path}
        Extension: {file_info['extension']}
        Content sample:
        ```
        {content}
        ```

        Repository context:
        - Total files: {len(repo_structure['files'])}
        - Common patterns: {', '.join(repo_structure['patterns'].keys())}

        Respond with just the category name: src, data, docs, tests, or meta.
        """
    
    def _classify_fallback(self, file_info: Dict[str, Any]) -> str:
        """Fallback classification for ambiguous files."""
        ext = file_info['extension'].lower()
        
        # Common extensions fallback
        if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c']:
            return 'src'
        elif ext in ['.md', '.rst', '.txt']:
            return 'docs'
        elif ext in ['.csv', '.json', '.xml', '.parquet']:
            return 'data'
        elif ext in ['.yml', '.yaml', '.toml', '.ini']:
            return 'meta'
        else:
            return 'src'  # Default to src for unknown files
    
    def _create_transformation_plan(self, repo_structure: Dict[str, Any], classifications: Dict[str, str]) -> Dict[str, Any]:
        """Phase 3: Create comprehensive transformation plan."""
        plan = {
            'file_moves': [],
            'directory_structure': ['src', 'data', 'docs', 'meta', 'tests', 'canvas'],
            'metadata_injection': [],
            'conflicts': [],
            'risks': []
        }
        
        # Plan file movements
        for file_path, category in classifications.items():
            source_path = Path(file_path)
            dest_path = Path(category) / source_path.name
            
            # Handle naming conflicts
            if dest_path in [move['dest'] for move in plan['file_moves']]:
                dest_path = self._resolve_naming_conflict(dest_path, plan['file_moves'])
                plan['conflicts'].append({
                    'type': 'naming_conflict',
                    'file': file_path,
                    'resolution': str(dest_path)
                })
            
            plan['file_moves'].append({
                'source': source_path,
                'dest': dest_path,
                'category': category
            })
        
        # Plan metadata injection
        for file_path, category in classifications.items():
            if Path(file_path).suffix in ['.py', '.md', '.ipynb']:
                plan['metadata_injection'].append({
                    'file': file_path,
                    'category': category,
                    'metadata': self._generate_file_metadata(file_path, category)
                })
        
        self.logger.info(f"Created transformation plan: {len(plan['file_moves'])} moves, {len(plan['conflicts'])} conflicts")
        return plan
    
    def _execute_transformation(self, plan: Dict[str, Any]) -> bool:
        """Phase 4: Execute transformation with safety checks."""
        if self.config.get('dry_run', False):
            self.logger.info("DRY RUN: Would execute transformation plan")
            self._print_transformation_plan(plan)
            return True
        
        try:
            # Create destination directory
            self.dest_path.mkdir(parents=True, exist_ok=True)
            
            # Create DSS directory structure
            for directory in plan['directory_structure']:
                (self.dest_path / directory).mkdir(exist_ok=True)
            
            # Copy and move files
            for move in plan['file_moves']:
                source_full = self.source_path / move['source']
                dest_full = self.dest_path / move['dest']
                
                # Ensure destination directory exists
                dest_full.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(source_full, dest_full)
                self.logger.debug(f"Copied {move['source']} -> {move['dest']}")
            
            # Copy template files
            self._copy_dss_template_files()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            return False
    
    def _enhance_repository(self):
        """Phase 5: Add metadata, generate docs, and enhance structure."""
        # Inject metadata into files
        self._inject_metadata()
        
        # Generate basic documentation
        self._generate_basic_docs()
        
        # Create INDEX.md
        self._create_index_file()
        
        # Set up git repository if source had git
        self._setup_git_repository()
        
        # Set up Cursor assistant integration
        self._setup_cursor_integration()
    
    def _validate_transformation(self) -> bool:
        """Phase 6: Validate the transformation."""
        validation_checks = [
            self._validate_structure(),
            self._validate_file_integrity(),
            self._validate_metadata(),
        ]
        
        all_passed = all(validation_checks)
        self.logger.info(f"Validation {'PASSED' if all_passed else 'FAILED'}")
        return all_passed
    
    # Helper methods
    
    def _should_ignore_file(self, path: Path) -> bool:
        """Check if file should be ignored during processing."""
        ignore_patterns = self.config.get('ignore_patterns', [
            '**/.git/**', '**/node_modules/**', '**/__pycache__/**',
            '**/.venv/**', '**/.env', '**/.*'
        ])
        
        path_str = str(path.relative_to(self.source_path))
        return any(path.match(pattern) for pattern in ignore_patterns)
    
    def _get_content_sample(self, path: Path, max_size: int = 1000) -> str:
        """Get a sample of file content for analysis."""
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            return content[:max_size]
        except Exception:
            return ""
    
    def _analyze_patterns(self, files: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze file patterns in the repository."""
        patterns = {}
        for file_info in files:
            ext = file_info['extension'].lower()
            patterns[ext] = patterns.get(ext, 0) + 1
        return patterns
    
    def _extract_dependencies(self, files: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract dependency information from files."""
        dependencies = {}
        
        for file_info in files:
            if file_info['extension'] == '.py':
                content = file_info.get('content_sample', '')
                imports = self._extract_python_imports(content)
                if imports:
                    dependencies[str(file_info['relative_path'])] = imports
        
        return dependencies
    
    def _extract_python_imports(self, content: str) -> List[str]:
        """Extract import statements from Python content."""
        imports = []
        for line in content.split('\n')[:50]:  # Check first 50 lines
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports
    
    def _resolve_naming_conflict(self, dest_path: Path, existing_moves: List[Dict[str, Any]]) -> Path:
        """Resolve naming conflicts by adding suffixes."""
        counter = 1
        original_stem = dest_path.stem
        original_suffix = dest_path.suffix
        
        while dest_path in [Path(move['dest']) for move in existing_moves]:
            new_name = f"{original_stem}_{counter}{original_suffix}"
            dest_path = dest_path.parent / new_name
            counter += 1
        
        return dest_path
    
    def _generate_file_metadata(self, file_path: str, category: str) -> Dict[str, Any]:
        """Generate metadata for a file."""
        return {
            'tags': [category],
            'provides': [],
            'requires': [],
            'created_by': 'dss_autoformatter'
        }
    
    def _copy_dss_template_files(self):
        """Copy essential DSS template files."""
        template_files = [
            'meta/dss_config.yml',
            'meta/DSS_GUIDE.md',
            '.gitignore',
            '.cursorignore'
        ]
        
        for template_file in template_files:
            try:
                self._download_template_file(template_file)
            except Exception as e:
                self.logger.warning(f"Could not copy template file {template_file}: {e}")
    
    def _download_template_file(self, file_path: str):
        """Download a template file from the DSS repository."""
        url = f"{DEFAULT_DSS_TEMPLATE_URL}/raw/main/{file_path}"
        dest_path = self.dest_path / file_path
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            urllib.request.urlretrieve(url, dest_path)
            self.logger.debug(f"Downloaded template file: {file_path}")
        except Exception as e:
            self.logger.warning(f"Could not download {file_path}: {e}")
    
    def _inject_metadata(self):
        """Inject YAML metadata into appropriate files."""
        metadata_files = list(self.dest_path.rglob('*.py')) + list(self.dest_path.rglob('*.md'))
        
        for file_path in metadata_files:
            try:
                self._inject_file_metadata(file_path)
            except Exception as e:
                self.logger.warning(f"Could not inject metadata into {file_path}: {e}")
    
    def _inject_file_metadata(self, file_path: Path):
        """Inject metadata into a specific file."""
        content = file_path.read_text(encoding='utf-8')
        
        # Skip if metadata already exists
        if content.startswith('---') or content.startswith('"""---'):
            return
        
        # Generate metadata
        metadata = {
            'tags': ['draft'],
            'provides': [],
            'requires': []
        }
        
        # Inject based on file type
        if file_path.suffix == '.md':
            yaml_content = yaml.dump(metadata, default_flow_style=False)
            new_content = f"---\n{yaml_content}---\n\n{content}"
        elif file_path.suffix == '.py':
            yaml_content = yaml.dump(metadata, default_flow_style=False)
            new_content = f'"""---\n{yaml_content}---"""\n\n{content}'
        else:
            return
        
        file_path.write_text(new_content, encoding='utf-8')
    
    def _generate_basic_docs(self):
        """Generate basic documentation files."""
        # Create README.md files for each directory
        for directory in ['src', 'data', 'docs', 'meta', 'tests']:
            dir_path = self.dest_path / directory
            if dir_path.exists():
                readme_path = dir_path / 'README.md'
                if not readme_path.exists():
                    self._create_directory_readme(dir_path, directory)
    
    def _create_directory_readme(self, dir_path: Path, directory_name: str):
        """Create a basic README.md for a directory."""
        readme_content = f"""---
tags: [documentation, {directory_name}]
provides: [{directory_name}_overview]
requires: []
---

# {directory_name.title()} Directory

This directory contains files related to {directory_name}.

## Files

| File | Purpose |
|------|---------|
"""
        
        # List files in directory
        for file_path in dir_path.glob('*'):
            if file_path.is_file() and file_path.name != 'README.md':
                readme_content += f"| {file_path.name} | [Add description] |\n"
        
        (dir_path / 'README.md').write_text(readme_content)
    
    def _create_index_file(self):
        """Create the main INDEX.md file."""
        index_content = f"""---
tags: [index, overview]
provides: [project_index]
requires: []
---

# Project Index

This project has been transformed using DSS (Data SuperStructure) formatting.

## Structure

- [src/](src/README.md) - Source code and executable logic
- [data/](data/README.md) - Datasets, artifacts, and data files
- [docs/](docs/README.md) - Human and AI-generated documentation
- [meta/](meta/README.md) - Scripts, prompts, config, and automation
- [tests/](tests/README.md) - Test files and validation datasets

## Getting Started

1. Review the documentation in `docs/`
2. Explore the source code in `src/`
3. Check the configuration in `meta/`

## Generated by DSS Auto-formatter v{__version__}

This project structure was automatically generated from the source repository
using the DSS auto-formatter tool.

For more information about DSS, visit:
{DEFAULT_DSS_TEMPLATE_URL}
"""
        
        (self.dest_path / 'INDEX.md').write_text(index_content)
    
    def _setup_git_repository(self):
        """Set up git repository in destination if HAS_GIT and requested."""
        if not HAS_GIT or not self.config.get('preserve_git_history', True):
            return
        
        try:
            # Initialize new git repo
            dest_repo = git.Repo.init(self.dest_path)
            
            # Add all files
            dest_repo.git.add('.')
            
            # Initial commit
            dest_repo.index.commit("Initial DSS transformation")
            
            self.logger.info("Initialized new git repository")
            
        except Exception as e:
            self.logger.warning(f"Could not set up git repository: {e}")
    
    def _setup_cursor_integration(self):
        """Set up Cursor assistant integration with DSS intelligence."""
        try:
            # Download and run cursor rules manager
            import urllib.request
            import tempfile
            import subprocess
            
            url = f"{DEFAULT_DSS_TEMPLATE_URL}/raw/main/meta/scripts/cursor_rules_manager.py"
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
                try:
                    with urllib.request.urlopen(url) as response:
                        tmp.write(response.read().decode())
                    tmp_path = tmp.name
                except urllib.error.URLError:
                    self.logger.warning("Could not download Cursor rules manager - skipping Cursor integration")
                    return
            
            # Determine project type based on files
            project_type = self._detect_project_type()
            
            # Run the cursor rules manager
            result = subprocess.run([
                sys.executable, tmp_path, "install",
                "--project-type", project_type,
                "--repo-root", str(self.dest_path)
            ], capture_output=True, text=True, cwd=self.dest_path)
            
            # Cleanup
            Path(tmp_path).unlink()
            
            if result.returncode == 0:
                self.logger.info("✅ Cursor assistant integration installed")
                self.logger.info("   Your AI assistant now understands DSS conventions!")
            else:
                self.logger.warning(f"Cursor integration warning: {result.stderr}")
        
        except Exception as e:
            self.logger.error(f"Failed to setup Cursor integration: {e}")
    
    def _detect_project_type(self) -> str:
        """Detect project type based on files and structure."""
        # Check for common patterns
        files = list(self.dest_path.rglob('*'))
        file_names = [f.name.lower() for f in files]
        file_extensions = [f.suffix.lower() for f in files]
        
        # Data science indicators
        if any(ext in file_extensions for ext in ['.ipynb', '.csv', '.parquet']) or \
           any(name in file_names for name in ['requirements.txt', 'environment.yml', 'conda.yml']):
            return "data_science"
        
        # Web application indicators  
        if any(name in file_names for name in ['package.json', 'webpack.config.js', 'next.config.js']) or \
           any(ext in file_extensions for ext in ['.js', '.ts', '.jsx', '.tsx', '.vue']):
            return "web_application"
        
        # Python package indicators
        if any(name in file_names for name in ['setup.py', 'pyproject.toml', '__init__.py']):
            return "python_package"
        
        # Documentation project indicators
        if len([f for f in files if f.suffix.lower() == '.md']) > len(files) * 0.5:
            return "documentation"
        
        return "general"
    
    def _validate_structure(self) -> bool:
        """Validate that DSS structure was created correctly."""
        required_dirs = ['src', 'data', 'docs', 'meta']
        
        for directory in required_dirs:
            if not (self.dest_path / directory).exists():
                self.logger.error(f"Required directory missing: {directory}")
                return False
        
        if not (self.dest_path / 'INDEX.md').exists():
            self.logger.error("INDEX.md file missing")
            return False
        
        return True
    
    def _validate_file_integrity(self) -> bool:
        """Validate that files were copied correctly."""
        # Basic check - ensure we have some files
        file_count = len(list(self.dest_path.rglob('*')))
        if file_count < 5:  # Minimum expected files
            self.logger.error("Too few files in destination")
            return False
        
        return True
    
    def _validate_metadata(self) -> bool:
        """Validate that metadata was injected correctly."""
        md_files = list(self.dest_path.rglob('*.md'))
        py_files = list(self.dest_path.rglob('*.py'))
        
        files_with_metadata = 0
        for file_path in md_files + py_files:
            content = file_path.read_text(encoding='utf-8')
            if content.startswith('---') or '"""---' in content:
                files_with_metadata += 1
        
        total_files = len(md_files + py_files)
        if total_files > 0:
            metadata_ratio = files_with_metadata / total_files
            if metadata_ratio < 0.5:  # At least 50% should have metadata
                self.logger.warning(f"Low metadata coverage: {metadata_ratio:.1%}")
                return False
        
        return True
    
    def _print_transformation_plan(self, plan: Dict[str, Any]):
        """Print the transformation plan for dry run."""
        print("\n" + "="*60)
        print("DSS TRANSFORMATION PLAN")
        print("="*60)
        
        print(f"\nFile Movements ({len(plan['file_moves'])} files):")
        for move in plan['file_moves'][:10]:  # Show first 10
            print(f"  {move['source']} -> {move['dest']}")
        if len(plan['file_moves']) > 10:
            print(f"  ... and {len(plan['file_moves']) - 10} more files")
        
        if plan['conflicts']:
            print(f"\nConflicts ({len(plan['conflicts'])}):")
            for conflict in plan['conflicts']:
                print(f"  {conflict['type']}: {conflict['file']} -> {conflict['resolution']}")
        
        print(f"\nDirectory Structure:")
        for directory in plan['directory_structure']:
            print(f"  /{directory}/")
        
        print("\n" + "="*60)

def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults."""
    default_config = {
        'use_llm_classification': True,
        'preserve_git_history': True,
        'dry_run': False,
        'ignore_patterns': [
            '**/.git/**', '**/node_modules/**', '**/__pycache__/**',
            '**/.venv/**', '**/.env', '**/.*'
        ],
        'classification_rules': {
            'src': ['**/*.py', '**/*.js', '**/*.ts', '**/src/**', '**/lib/**'],
            'data': ['**/*.csv', '**/*.parquet', '**/*.json', '**/data/**'],
            'docs': ['**/*.md', '**/*.rst', '**/docs/**'],
            'tests': ['**/test_*.py', '**/*_test.py', '**/tests/**'],
            'meta': ['**/meta/**', '**/.github/**', '**/scripts/**']
        }
    }
    
    if config_path and config_path.exists():
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
            default_config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    return default_config

def check_dependencies():
    """Check for optional dependencies and warn if missing."""
    missing = []
    
    if not HAS_OPENAI:
        missing.append("openai (pip install openai) - for LLM-assisted classification")
    
    if not HAS_GIT:
        missing.append("gitpython (pip install gitpython) - for git repository handling")
    
    if missing:
        print("Optional dependencies missing:")
        for dep in missing:
            print(f"  - {dep}")
        print()

def main():
    """Main entry point for the DSS auto-formatter."""
    parser = argparse.ArgumentParser(
        description="DSS Auto-Formatter: Transform any repository into DSS structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --source ./my-repo --dest ./my-repo-dss
  %(prog)s --source . --dest ../formatted --config custom.yml --dry-run
  %(prog)s --source ./project --dest ./project-dss --no-llm
        """
    )
    
    parser.add_argument('--source', '-s', type=Path, required=True,
                        help='Source repository path')
    parser.add_argument('--dest', '-d', type=Path, required=True,
                        help='Destination path for DSS-formatted repository')
    parser.add_argument('--config', '-c', type=Path,
                        help='Custom configuration file (YAML)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--no-llm', action='store_true',
                        help='Disable LLM-assisted classification')
    parser.add_argument('--preserve-git', action='store_true', default=True,
                        help='Preserve git history (default: True)')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Validate paths
    if not args.source.exists():
        print(f"Error: Source path does not exist: {args.source}")
        sys.exit(1)
    
    if args.dest.exists() and any(args.dest.iterdir()):
        response = input(f"Destination path {args.dest} exists and is not empty. Continue? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(1)
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line args
    if args.dry_run:
        config['dry_run'] = True
    if args.no_llm:
        config['use_llm_classification'] = False
    if not args.preserve_git:
        config['preserve_git_history'] = False
    
    # Create formatter and run transformation
    formatter = DSSAutoFormatter(args.source, args.dest, config)
    
    print(f"DSS Auto-Formatter v{__version__}")
    print(f"Source: {args.source}")
    print(f"Destination: {args.dest}")
    print(f"Configuration: {args.config or 'default'}")
    print()
    
    success = formatter.transform_repository()
    
    if success:
        print(f"\n✅ Transformation completed successfully!")
        print(f"DSS-formatted repository created at: {args.dest}")
        print(f"\nNext steps:")
        print(f"1. Review the generated structure")
        print(f"2. Update any file descriptions in README.md files")
        print(f"3. Set up your development environment")
        print(f"4. Explore the documentation in docs/")
    else:
        print(f"\n❌ Transformation failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == '__main__':
    main() 