---
tags: [implementation, specification, cursor, rules, distribution, integration]
provides: [cursor_rules_distribution_spec, implementation_details, acceptance_criteria]
requires: [dev/tasks/complete.md, dev/tasks/cursor_rules_migration_roadmap.md]
status: draft
priority: high
---

# Cursor Rules Distribution - Implementation Specification

## 1. Component Overview

The Cursor Rules Distribution system provides standardized methods for distributing, installing, and updating DSS rule files (.mdc) across projects, ensuring consistent AI assistant behavior while allowing for customization and version control.

### 1.1 Purpose

- Simplify distribution of DSS rules to new and existing projects
- Enable version control and tracking of rule updates
- Provide clear installation instructions for different environments
- Support customization while maintaining core rule integrity
- Facilitate easy updates when DSS rules are enhanced
- Ensure compatibility with Cursor's rule system

### 1.2 Core Functions

- Multiple distribution methods (direct copy, Git submodule, Git subtree)
- Automated update mechanisms
- Rule file validation and error checking
- User-friendly installation documentation
- Configuration preservation during updates
- Cross-platform compatibility

## 2. Technical Design

### 2.1 Architecture

```text
.cursor/rules/
├── 00-dss-core.mdc          # Core DSS concepts
├── 01-dss-behavior.mdc      # Assistant behavior
├── workflows/               # Workflow rule files
├── guidelines/              # Guidelines rule files
├── config/                  # Configuration and templates
│   └── structure-guide.mdc  # Structure and setup guide
└── README.md                # Installation and usage instructions

meta/scripts/
├── update_dss_rules.sh      # Shell script for updates
├── update_dss_rules.ps1     # PowerShell script for updates
├── validate_rules.py        # Validation utility
└── lib/
    ├── rule_updater.py      # Rule update utilities
    └── rule_validator.py    # Validation tools
```

### 2.2 Distribution Methods

#### Method 1: Direct Copy (Simplest)

Installation via curl or direct download:

```bash
# Unix/macOS
mkdir -p .cursor/rules
curl -L https://github.com/org/dss-repo/archive/main.tar.gz | tar xz --strip=2 -C .cursor/rules dss-repo-main/.cursor/rules

# Windows PowerShell
New-Item -ItemType Directory -Force -Path .cursor\rules
Invoke-WebRequest -Uri https://github.com/org/dss-repo/archive/main.zip -OutFile dss.zip
Expand-Archive -Path dss.zip -DestinationPath .cursor\rules -Force
Move-Item -Path .cursor\rules\dss-repo-main\.cursor\rules\* -Destination .cursor\rules\
Remove-Item -Path dss.zip, .cursor\rules\dss-repo-main -Recurse -Force
```

#### Method 2: Git Submodule (Trackable)

```bash
# Add submodule
git submodule add https://github.com/org/dss-repo.git .dss-repo

# Create symlinks or copy files
mkdir -p .cursor/rules
cp -r .dss-repo/.cursor/rules/* .cursor/rules/

# Update submodule
git submodule update --remote .dss-repo
cp -r .dss-repo/.cursor/rules/* .cursor/rules/
```

#### Method 3: Git Subtree (Integrated)

```bash
# Add subtree
git subtree add --prefix=.cursor/rules/dss https://github.com/org/dss-repo.git main --squash

# Update subtree
git subtree pull --prefix=.cursor/rules/dss https://github.com/org/dss-repo.git main --squash
```

### 2.3 Update Script Implementation

```bash
#!/bin/bash
# update_dss_rules.sh - Update DSS rules in .cursor/rules directory

set -e

# Configuration
DSS_REPO="https://github.com/org/dss-repo"
RULES_DIR=".cursor/rules"
BACKUP_DIR=".cursor/rules_backup_$(date +%Y%m%d%H%M%S)"
TEMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo "DSS Rules Update Tool"
echo "====================="

# Backup existing rules
if [ -d "$RULES_DIR" ]; then
    echo "Backing up existing rules to $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
    cp -r "$RULES_DIR"/* "$BACKUP_DIR"/
fi

# Download latest rules
echo "Downloading latest DSS rules..."
git clone --depth 1 "$DSS_REPO" "$TEMP_DIR"

# Copy rules to destination
echo "Installing rules to $RULES_DIR"
mkdir -p "$RULES_DIR"

# Copy core rules
cp "$TEMP_DIR/.cursor/rules/00-dss-core.mdc" "$RULES_DIR"/
cp "$TEMP_DIR/.cursor/rules/01-dss-behavior.mdc" "$RULES_DIR"/

# Copy workflow rules
mkdir -p "$RULES_DIR/workflows"
cp "$TEMP_DIR/.cursor/rules/workflows/"*.mdc "$RULES_DIR/workflows"/

# Copy guideline rules
mkdir -p "$RULES_DIR/guidelines"
cp "$TEMP_DIR/.cursor/rules/guidelines/"*.mdc "$RULES_DIR/guidelines"/

# Copy config
mkdir -p "$RULES_DIR/config"
cp -r "$TEMP_DIR/.cursor/rules/config/"* "$RULES_DIR/config"/

# Copy README
cp "$TEMP_DIR/.cursor/rules/README.md" "$RULES_DIR"/

# Restore customizations
if [ -d "$BACKUP_DIR/custom" ]; then
    echo "Restoring custom rules"
    cp -r "$BACKUP_DIR/custom" "$RULES_DIR"/
fi

echo "DSS rules updated successfully!"
echo ""
echo "IMPORTANT: You must manually configure each .mdc file in Cursor settings:"
echo "1. Open Cursor Settings (Ctrl/Cmd + ,)"
echo "2. Navigate to 'Rules' in the left sidebar"
echo "3. For each .mdc file, click '+ Always include in prompts'"
echo ""
echo "See $RULES_DIR/README.md for detailed instructions"
```

### 2.4 Rule Validation

```python
def validate_rules(rules_dir):
    """
    Validate DSS rule files in the specified directory.
    
    Args:
        rules_dir: Path to rules directory
        
    Returns:
        Dictionary with validation results
    """
    results = {
        'valid': [],
        'invalid': [],
        'missing': [],
        'warnings': []
    }
    
    # Check for required core files
    required_files = [
        '00-dss-core.mdc',
        '01-dss-behavior.mdc',
        'workflows/00-workflow-selection.mdc'
    ]
    
    for file in required_files:
        file_path = os.path.join(rules_dir, file)
        if not os.path.exists(file_path):
            results['missing'].append(file)
    
    # Validate .mdc file format and content
    for root, dirs, files in os.walk(rules_dir):
        for file in files:
            if file.endswith('.mdc'):
                file_path = os.path.join(root, file)
                
                # Check file naming convention
                if not re.match(r'^\d+-[a-z0-9-]+\.mdc$', file) and file != 'structure-guide.mdc':
                    results['warnings'].append(f"{file}: File naming doesn't follow convention (should be ##-kebab-case.mdc)")
                
                # Validate frontmatter
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for cursor-specific frontmatter
                    cursor_frontmatter = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if not cursor_frontmatter:
                        results['warnings'].append(f"{file}: Missing Cursor frontmatter section")
                    else:
                        try:
                            frontmatter_data = yaml.safe_load(cursor_frontmatter.group(1))
                            if 'description' not in frontmatter_data:
                                results['warnings'].append(f"{file}: Missing 'description' in Cursor frontmatter")
                        except yaml.YAMLError:
                            results['invalid'].append(f"{file}: Invalid YAML in Cursor frontmatter")
                    
                    # Check for DSS frontmatter
                    dss_frontmatter = re.search(r'^---\s*\n.*?\n---\s*\n---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if not dss_frontmatter:
                        results['warnings'].append(f"{file}: Missing DSS frontmatter section")
                    else:
                        try:
                            frontmatter_data = yaml.safe_load(dss_frontmatter.group(1))
                            if 'tags' not in frontmatter_data:
                                results['warnings'].append(f"{file}: Missing 'tags' in DSS frontmatter")
                            if 'provides' not in frontmatter_data:
                                results['warnings'].append(f"{file}: Missing 'provides' in DSS frontmatter")
                            if 'requires' not in frontmatter_data:
                                results['warnings'].append(f"{file}: Missing 'requires' in DSS frontmatter")
                        except yaml.YAMLError:
                            results['invalid'].append(f"{file}: Invalid YAML in DSS frontmatter")
                    
                    # If no errors found, mark as valid
                    if file_path not in results['invalid'] and file not in results['warnings']:
                        results['valid'].append(file)
                        
                except Exception as e:
                    results['invalid'].append(f"{file}: {str(e)}")
    
    return results
```

## 3. Implementation Plan

### 3.1 Phase 1: Documentation (Week 1)

- Create comprehensive README.md with installation instructions
- Document manual Cursor configuration steps
- Create troubleshooting guide
- Prepare example installation commands

### 3.2 Phase 2: Distribution Scripts (Week 1-2)

- Implement update_dss_rules.sh for Unix/macOS
- Implement update_dss_rules.ps1 for Windows
- Create validation scripts
- Develop error handling and recovery mechanisms

### 3.3 Phase 3: Testing (Week 2)

- Test on Windows, macOS, and Linux
- Test all distribution methods
- Test customization preservation
- Test various edge cases and error scenarios

### 3.4 Phase 4: Integration (Week 2-3)

- Create GitHub Actions workflow for distribution
- Implement versioning system
- Develop migration guidance
- Build compatibility checks

## 4. Acceptance Criteria

### 4.1 Functional Requirements

- [ ] **Multiple Distribution Methods**: Successfully implements direct copy, Git submodule, and Git subtree methods
- [ ] **Update Mechanism**: Reliable update scripts for all platforms
- [ ] **Rule Validation**: Effective validation of rule file integrity
- [ ] **Customization Support**: Preserves user customizations during updates
- [ ] **Documentation**: Clear installation and usage instructions
- [ ] **Cross-platform**: Works on Windows, macOS, and Linux

### 4.2 Technical Requirements

- [ ] **Error Handling**: Graceful handling of network issues, permissions, and file conflicts
- [ ] **Performance**: Fast installation and update process (under 30 seconds)
- [ ] **Modularity**: Separation of concerns between distribution, validation, and customization
- [ ] **Compatibility**: Works with different Git providers and environments
- [ ] **Security**: Safe handling of files and repositories

### 4.3 User Experience Requirements

- [ ] **Intuitive Commands**: Clear and concise commands for installation and updates
- [ ] **Helpful Output**: Informative progress messages and error reporting
- [ ] **Minimal Dependencies**: Few external dependencies required
- [ ] **Reversibility**: Easy rollback if issues occur
- [ ] **Customization Path**: Clear guidance on how to customize rules

## 5. Integration Points

### 5.1 Integration with GitHub Releases

```yaml
name: Release DSS Rules

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Create distribution package
        run: |
          mkdir -p dist/dss-rules
          cp -r .cursor/rules/* dist/dss-rules/
          cd dist
          zip -r dss-rules.zip dss-rules
          tar -czf dss-rules.tar.gz dss-rules
      
      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: DSS Rules ${{ github.ref }}
          draft: false
          prerelease: false
      
      - name: Upload Zip
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./dist/dss-rules.zip
          asset_name: dss-rules.zip
          asset_content_type: application/zip
      
      - name: Upload Tarball
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./dist/dss-rules.tar.gz
          asset_name: dss-rules.tar.gz
          asset_content_type: application/gzip
```

### 5.2 Integration with NPM Scripts

```json
{
  "scripts": {
    "update-dss": "bash .dss-repo/meta/scripts/update_dss_rules.sh",
    "validate-dss": "python .dss-repo/meta/scripts/validate_rules.py"
  }
}
```

### 5.3 Migration Path for Bootstrap Users

```bash
#!/bin/bash
# migrate_from_bootstrap.sh - Migrate from bootstrap to rule-based approach

# Check if bootstrap script exists
if [ ! -f "dss_bootstrap.py" ]; then
    echo "No bootstrap script found."
    exit 1
fi

# Backup bootstrap script
echo "Backing up bootstrap script..."
cp dss_bootstrap.py dss_bootstrap.py.backup

# Install new rules
echo "Installing DSS rules..."
mkdir -p .cursor/rules
curl -L https://github.com/org/dss-repo/archive/main.tar.gz | tar xz --strip=2 -C .cursor/rules dss-repo-main/.cursor/rules

# Create migration note
cat > MIGRATION_NOTE.md << EOL
# DSS Migration Note

This project has been migrated from the bootstrap approach to the rule-based approach.

## Changes Made

- Installed DSS rules in .cursor/rules/
- Backed up original dss_bootstrap.py to dss_bootstrap.py.backup

## Required Manual Steps

1. Open Cursor Settings (Ctrl/Cmd + ,)
2. Navigate to "Rules" in the left sidebar
3. For each .mdc file in .cursor/rules/, click "+ Always include in prompts"

## Verification

Run the following command to verify the installation:
\`\`\`
python .cursor/rules/meta/scripts/validate_rules.py
\`\`\`

See .cursor/rules/README.md for more information.
EOL

echo "Migration complete! See MIGRATION_NOTE.md for next steps."
```

## 6. Performance Considerations

- **Efficient Downloads**: Use shallow clones and sparse checkouts when possible
- **Incremental Updates**: Only update changed files when updating
- **Parallel Processing**: Use parallel downloads for faster installation
- **Compression**: Use appropriate compression for distribution packages
- **Caching**: Implement caching for validation and rule processing

## 7. Risk Mitigation

|  Risk                                  |  Impact  |  Likelihood  |  Mitigation                                              |
| -------------------------------------- | -------- | ------------ | -------------------------------------------------------- |
|  Network failures during installation  |  High    |  Medium      |  Atomic operations; rollback capabilities                |
|  File permission issues                |  Medium  |  High        |  Clear error messages; privilege escalation when needed  |
|  Git version compatibility             |  Medium  |  Medium      |  Version checking; fallback mechanisms                   |
|  Cursor configuration confusion        |  High    |  High        |  Clear documentation; validation tools                   |
|  Customization conflicts               |  Medium  |  Medium      |  Separate custom rules directory; merge strategies       |

## 8. Future Enhancements

- **Automated Cursor Configuration**: Investigate ways to automate Cursor rule configuration
- **Change Detection**: Detect and highlight changes between rule versions
- **Rule Marketplace**: Community-contributed rule extensions
- **VSCode Integration**: Support for VSCode extension-based distribution
- **Rule Plugins**: Modular rule extension system

## 9. Development Estimates

|  Task                              |  Effort (days)  |  Dependencies           |
| ---------------------------------- | --------------- | ----------------------- |
|  Documentation creation            |  2              |  None                   |
|  Shell script implementation       |  2              |  Documentation          |
|  PowerShell script implementation  |  2              |  Documentation          |
|  Validation tool development       |  1              |  None                   |
|  Cross-platform testing            |  3              |  All scripts            |
|  GitHub Actions integration        |  1              |  Distribution packages  |
|  Migration guide                   |  1              |  All previous tasks     |

**Total Estimated Time**: 1-2 weeks (1 developer)

## 10. Implementation Assistant Prompts

The following prompts can be used to guide an AI assistant through implementing this specification using the DSS Code Modification workflow:

0.
    > _**Documentation Phase**_

1. **Develop Distribution Concept Documentation**:
   "Create the core documentation for the Cursor Rules Distribution System in `docs/tools/cursor_rules_distribution.md`. Include the concept, benefits, system architecture, and user journey as described in sections 1-3 of the specification."

2. **Create Rule Migration Guide**:
   "Develop a comprehensive migration guide in `docs/tools/rule_migration.md` that explains how to convert existing rules to the new modular structure, including file naming, content organization, and dependency management."

3. **Document Installation Process**:
   "Create detailed installation documentation in `docs/tools/cursor_rules_install.md` with platform-specific instructions for Windows, macOS, and Linux. Include prerequisites, installation steps, verification, and troubleshooting sections."

4. **Design Rule Description Format**:
   "Create the specification for rule description formats in `docs/tools/rule_descriptions.md`, explaining the format shown in section 2.3 with examples of effective descriptions for different rule types."

    > _**Shell Script Implementation Phase**_

5. **Create Shell Script Structure**:
   "Implement the basic structure of the shell script installer (`install_dss_rules.sh`) following section 4.1 of the specification. Include platform detection, prerequisites checking, and the overall workflow."

6. **Implement Repository Cloning Logic**:
   "Add the repository cloning functionality to the shell script that handles various source locations (GitHub, local path, etc.) with proper error handling and cleanup in case of failures."

7. **Implement Rule File Processing**:
   "Implement the rule file processing logic in the shell script that extracts rules from the source, validates them, and prepares them for installation in the Cursor configuration."

8. **Implement Cursor Configuration Detection**:
   "Add the Cursor configuration detection functionality to the shell script that finds the Cursor settings directory on different platforms and validates that it exists and is writable."

9. **Implement Rules Installation**:
   "Implement the actual rules installation functionality in the shell script that correctly places the rule files in the Cursor configuration directory and updates any necessary metadata."

10. **Add Validation and Verification Steps**:
    "Implement validation and verification steps in the shell script that confirm the rules were installed correctly and are accessible to Cursor."

    > _**PowerShell Implementation Phase**_

11. **Create PowerShell Script Structure**:
    "Implement the basic structure of the PowerShell script installer (`Install-DssRules.ps1`) following section 4.2 of the specification. Include platform verification, prerequisites checking, and the overall workflow."

12. **Implement Repository Cloning in PowerShell**:
    "Add the repository cloning functionality to the PowerShell script that handles various source locations (GitHub, local path, etc.) with proper error handling and cleanup in case of failures."

13. **Implement Rule File Processing in PowerShell**:
    "Implement the rule file processing logic in the PowerShell script that extracts rules from the source, validates them, and prepares them for installation in the Cursor configuration."

14. **Implement Cursor Configuration Detection in PowerShell**:
    "Add the Cursor configuration detection functionality to the PowerShell script that finds the Cursor settings directory on Windows and validates that it exists and is writable."

15. **Implement Rules Installation in PowerShell**:
    "Implement the actual rules installation functionality in the PowerShell script that correctly places the rule files in the Cursor configuration directory and updates any necessary metadata."

16. **Add Validation and Verification Steps in PowerShell**:
    "Implement validation and verification steps in the PowerShell script that confirm the rules were installed correctly and are accessible to Cursor."

    > _**Validation Tool Implementation Phase**_

17. **Create Rule Validation Tool Structure**:
    "Implement the basic structure of the rule validation tool (`validate_dss_rules.py`) following section 4.3 of the specification. Include command-line interface, configuration loading, and the overall workflow."

18. **Implement Rule Content Validation**:
    "Add functionality to the validation tool to check rule content for correctness, including frontmatter format, required fields, and valid MDC links."

19. **Implement Rule Structure Validation**:
    "Implement the validation of rule structure, checking for correct organization, file naming conventions, and dependency relationships between rules."

20. **Implement Cursor Configuration Validation**:
    "Add functionality to the validation tool to verify the Cursor configuration is correctly set up for the DSS rules, including checking for rule inclusion settings."

21. **Implement Validation Reporting**:
    "Implement comprehensive reporting functionality in the validation tool that produces clear, actionable feedback about validation results, including errors, warnings, and recommendations."

    > _**Integration and Testing Phase**_

22. **Create GitHub Actions Workflow**:
    "Implement the GitHub Actions workflow described in section 5.1 that provides one-click installation of DSS rules from the GitHub repository."

23. **Implement Cross-platform Testing Framework**:
    "Create a testing framework that can verify the installation scripts work correctly across Windows, macOS, and Linux environments, including containers for automated testing."

24. **Create Test Scenarios**:
    "Develop comprehensive test scenarios that cover various installation conditions, rule configurations, and potential error cases."

25. **Implement Test Execution**:
    "Create the test execution scripts that run the tests in various environments and report the results in a consistent format."

    > _**Final Documentation and Quality Assurance Phase**_

26. **Create Example Usage Documentation**:
    "Create detailed example usage documentation in `docs/examples/cursor_rules_installation.md` with real-world scenarios for installing and managing DSS rules in Cursor."

27. **Create Troubleshooting Guide**:
    "Develop a comprehensive troubleshooting guide in `docs/tools/cursor_rules_troubleshooting.md` that addresses common issues, error messages, and their solutions."

28. **Review Security Implementation**:
    "Review all scripts for security considerations, including proper handling of user input, secure network connections, and file permission management."

29. **Performance Optimization**:
    "Optimize the performance of the installation scripts by reducing unnecessary operations, implementing caching, and minimizing network requests."

30. **Final Integration Testing**:
    "Perform final integration testing of the entire system, including installation, validation, and usage with actual Cursor instances across all supported platforms."

When implementing each part, follow the Code Modification workflow from the DSS guidelines, which includes:

1. Analyze the current state and the specification
2. Check for existing templates or patterns
3. Implement the changes with proper testing
4. Update documentation
5. Validate dependencies and cross-references
