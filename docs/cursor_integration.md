---
tags: [cursor, integration, assistant, ai, automation]
provides: [cursor_dss_integration_guide]
requires: [meta/scripts/cursor_rules_manager.py, meta/scripts/dss_autoformat.py]
---

# Cursor Integration: Propagating DSS Assistant Intelligence

This guide explains how to bring DSS assistant intelligence to any repository opened in Cursor, enabling the AI assistant to understand DSS conventions and workflows automatically.

## 🎯 Overview

The DSS framework includes powerful tools to propagate intelligent AI assistant behavior to any codebase. Once integrated, your AI assistant will:

- ✅ Understand DSS folder structure and conventions
- ✅ Apply proper frontmatter to new files
- ✅ Use templates from `meta/templates/` automatically
- ✅ Follow DSS workflows and guidelines
- ✅ Maintain project-specific context and rules

## 🚀 Integration Options

### Option 1: Automatic Integration (Recommended)

The **DSS auto-formatter automatically installs Cursor rules** during transformation:

```bash
# Transform any repo with DSS + Cursor intelligence
curl -sSL https://raw.githubusercontent.com/Dub1n/dss/main/meta/scripts/install_dss_autoformatter.py | python3
```

**What happens automatically:**
1. ✅ Transforms repository to DSS structure  
2. ✅ **Installs `.cursor/rules/`** with full DSS intelligence
3. ✅ **Auto-detects project type** (data_science, web_application, python_package, etc.)
4. ✅ Creates project-specific context file
5. ✅ Sets up self-update mechanism

### Option 2: Manual Installation

For repositories already using DSS structure:

```bash
# Download and run cursor rules manager  
curl -sSL https://raw.githubusercontent.com/Dub1n/dss/main/meta/scripts/cursor_rules_manager.py | python3 - install --project-type data_science
```

### Option 3: Local Installation

If you have the DSS template repository locally:

```bash
# From within the DSS template repo
python meta/scripts/cursor_rules_manager.py install --project-type web_application --repo-root /path/to/target/repo
```

## 📁 What Gets Installed

### Minimal Footprint (~15KB total)

```
your-project/
├── .cursor/
│   └── rules/
│       ├── assistant.mdc           # Core DSS assistant logic
│       ├── dss-overview.mdc        # DSS framework overview  
│       ├── dss-guide.mdc           # DSS guidelines
│       ├── dss-config.mdc          # Configuration rules
│       ├── project_context.mdc     # Project-specific context
│       └── update_dss_rules.py     # Self-updater script
```

**Size comparison:**
- Full DSS repo: ~10MB+
- DSS-ified project with Cursor rules: **~15KB**

## 🎪 Dynamic Features

### 1. **Automatic Project Type Detection**

The system automatically detects your project type and applies appropriate context:

| Project Type | Detected By | Assistant Behavior |
|--------------|-------------|-------------------|
| `data_science` | `.ipynb`, `.csv`, `requirements.txt` | Prioritizes analysis notebooks, data files |
| `web_application` | `package.json`, `.js/.ts` files | Focuses on components, API routes |
| `python_package` | `setup.py`, `pyproject.toml` | Emphasizes module structure, testing |
| `documentation` | Majority `.md` files | Optimizes for content creation, linking |
| `general` | Fallback for mixed projects | Standard DSS conventions |

### 2. **Self-Updating Intelligence**

Keep your assistant intelligence current:

```bash
# Update DSS assistant rules from GitHub
python .cursor/rules/update_dss_rules.py
```

**What gets updated:**
- ✅ New assistant workflows → automatic propagation
- ✅ Updated guidelines → instant availability  
- ✅ Bug fixes → seamless updates
- ✅ New templates → immediate access

### 3. **Project-Specific Context**

Each repository gets custom context in `project_context.mdc`:

```markdown
## Project Configuration
- **Project Type**: data_science
- **Repository**: fraud-detection-ml
- **DSS Integration**: Active

## Custom Project Rules
- Follow DSS conventions with project-specific adaptations
- Prioritize Jupyter notebooks and data analysis workflows
- Use data science templates from meta/templates/
- Reference project documentation in INDEX.md
```

## 🔄 Team Collaboration

### Version Control the Intelligence

The `.cursor/rules/` files are normal files that can be version controlled:

```bash
# Add DSS assistant intelligence to your repo
git add .cursor/rules/
git commit -m "Add DSS assistant intelligence"
git push

# Team members automatically get the same intelligent assistant
git clone your-repo
# Assistant immediately understands DSS conventions!
```

### Team Benefits

- **Consistent behavior** across all team members
- **Shared templates** and conventions
- **Unified documentation** standards
- **Automatic onboarding** for new developers

## 🛠 Management Commands

### Check Compatibility

```bash
python meta/scripts/cursor_rules_manager.py check
```

**Output:**
```
DSS Compatibility: 100%
✅ has_dss_config
✅ has_index
✅ has_meta_dir
✅ has_docs_dir
```

### Force Update

```bash
python meta/scripts/cursor_rules_manager.py sync --force
```

### Install with Custom Project Type

```bash
python meta/scripts/cursor_rules_manager.py install --project-type python_package
```

## 📊 Usage Examples

### Example 1: Data Science Project

```bash
cd ml-fraud-detection
curl -sSL https://raw.githubusercontent.com/Dub1n/dss/main/meta/scripts/install_dss_autoformatter.py | python3

# Result: Assistant understands:
# - Jupyter notebook workflows
# - Data file organization
# - Analysis documentation patterns
# - ML model structure conventions
```

### Example 2: Web Application

```bash  
cd react-dashboard
python meta/scripts/cursor_rules_manager.py install --project-type web_application

# Result: Assistant understands:
# - Component file organization
# - API route structure  
# - Frontend/backend separation
# - Configuration management
```

### Example 3: Existing DSS Project

```bash
cd existing-dss-project
python .cursor/rules/update_dss_rules.py

# Result: Latest DSS intelligence without disrupting project
```

## 🔧 Advanced Configuration

### Custom Project Types

Create custom project configurations by extending the project type detection:

```python
# In your local cursor_rules_manager.py
def _detect_project_type(self) -> str:
    # Add custom detection logic
    if self.has_flutter_files():
        return "flutter_mobile"
    elif self.has_django_files():
        return "django_web"
    # ... continue with standard detection
```

### Custom Templates

Add project-specific templates to your `meta/templates/` directory:

```
meta/templates/
├── data_science/
│   ├── analysis_notebook.ipynb
│   └── data_processing.py
├── web_application/
│   ├── component.tsx
│   └── api_route.js
```

## ⚠️ Troubleshooting

### Assistant Not Following DSS Conventions

1. **Check installation:**
   ```bash
   ls .cursor/rules/
   # Should show: assistant.mdc, dss-overview.mdc, etc.
   ```

2. **Verify project context:**
   ```bash
   cat .cursor/rules/project_context.mdc
   ```

3. **Update rules:**
   ```bash
   python .cursor/rules/update_dss_rules.py
   ```

### Rules Not Updating

1. **Check internet connection** (rules download from GitHub)
2. **Verify GitHub repository access**
3. **Force update:**
   ```bash
   python meta/scripts/cursor_rules_manager.py sync --force
   ```

### Project Type Detection Issues

1. **Manually specify project type:**
   ```bash
   python meta/scripts/cursor_rules_manager.py install --project-type your_type
   ```

2. **Check file patterns** in your repository
3. **Add custom detection logic** if needed

## 🌟 Network Effect

By using DSS Cursor integration, you create a **network effect** where:

- ✅ **All your projects** have consistent AI assistant behavior
- ✅ **Team members** get the same intelligent experience
- ✅ **New repositories** automatically inherit DSS intelligence
- ✅ **Updates propagate** across your entire project ecosystem

This transforms your development workflow into a coherent, AI-enhanced experience that scales across all your work!

## 📚 Related Documentation

- [DSS Auto-formatter Usage Guide](mdc:docs/dss_autoformatter_usage.md)
- [Getting Started with DSS](mdc:docs/getting_started.md)
- [Assistant Workflows](mdc:meta/assistant_workflows/)
- [Template System](mdc:meta/templates/)
- [Frontmatter Validation](mdc:meta/scripts/readme_frontmatter.md) 