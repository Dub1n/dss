#!/usr/bin/env python3
"""
⚠️  WARNING: This script is in need of significant rework and is kept for reference only.
    It was written for an earlier version of DSS and does not match the current repo structure.
    DO NOT USE in production - significant updates required before it can be functional.
    
    For current DSS functionality, see the main documentation and newer scripts.

tags: [script, installer, dss, autoformatter]
provides: [dss_autoformatter_installer]
requires: [urllib, pathlib, subprocess]
---

DSS Auto-formatter Installer

This script downloads and sets up the DSS auto-formatter as a standalone tool.

Usage:
    python install_dss_autoformatter.py
    python install_dss_autoformatter.py --local-path /path/to/install
    python install_dss_autoformatter.py --help
"""

import argparse
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

DEFAULT_DSS_REPO = "https://github.com/yourusername/dss_template_repo"

def download_file(url: str, dest: Path) -> bool:
    """Download a file from URL to destination."""
    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def install_dss_autoformatter(install_path: Path = None) -> bool:
    """Install the DSS auto-formatter."""
    
    # Default installation path
    if install_path is None:
        install_path = Path.home() / ".local" / "bin"
    
    install_path = Path(install_path)
    install_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Installing DSS Auto-formatter to: {install_path}")
    
    # Download the main script
    script_url = f"{DEFAULT_DSS_REPO}/raw/main/meta/scripts/dss_autoformat.py"
    script_dest = install_path / "dss_autoformat.py"
    
    if not download_file(script_url, script_dest):
        return False
    
    # Make executable
    script_dest.chmod(0o755)
    
    # Download requirements
    requirements_url = f"{DEFAULT_DSS_REPO}/raw/main/meta/requirements_autoformatter.txt"
    requirements_dest = install_path / "requirements_autoformatter.txt"
    
    if not download_file(requirements_url, requirements_dest):
        print("Warning: Could not download requirements file")
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_dest)
        ], check=True)
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Warning: Some dependencies may not have installed correctly")
        print("You can install them manually with:")
        print(f"  pip install -r {requirements_dest}")
    
    # Create a convenient wrapper script
    wrapper_script = install_path / "dss-autoformat"
    wrapper_content = f"""#!/bin/bash
# DSS Auto-formatter wrapper script
python3 "{script_dest}" "$@"
"""
    
    wrapper_script.write_text(wrapper_content)
    wrapper_script.chmod(0o755)
    
    print(f"\n✅ DSS Auto-formatter installed successfully!")
    print(f"\nInstallation location: {install_path}")
    print(f"Main script: {script_dest}")
    print(f"Wrapper script: {wrapper_script}")
    
    # Check if install_path is in PATH
    path_env = os.environ.get("PATH", "")
    if str(install_path) not in path_env:
        print(f"\n⚠️  Add {install_path} to your PATH to use 'dss-autoformat' from anywhere:")
        print(f"   export PATH=\"{install_path}:$PATH\"")
        print(f"   # Add this line to your ~/.bashrc or ~/.zshrc")
    
    print(f"\nUsage examples:")
    print(f"  {wrapper_script} --source ./my-repo --dest ./my-repo-dss")
    print(f"  {wrapper_script} --source . --dest ../formatted --dry-run")
    print(f"  {wrapper_script} --help")
    
    return True

def main():
    """Main installer function."""
    parser = argparse.ArgumentParser(
        description="Install DSS Auto-formatter as a standalone tool"
    )
    
    parser.add_argument('--local-path', type=Path,
                        help='Custom installation path (default: ~/.local/bin)')
    parser.add_argument('--repo-url', default=DEFAULT_DSS_REPO,
                        help='DSS template repository URL')
    
    args = parser.parse_args()
    
    print("DSS Auto-formatter Installer")
    print("="*40)
    
    # Update global repo URL if provided
    global DEFAULT_DSS_REPO
    DEFAULT_DSS_REPO = args.repo_url
    
    success = install_dss_autoformatter(args.local_path)
    
    if not success:
        print("\n❌ Installation failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 