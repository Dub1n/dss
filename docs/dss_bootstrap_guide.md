---
tags: [bootstrap, quick_start, voice_commands, transformation]
provides: [bootstrap_guide, instant_dss_setup]
requires: [meta/scripts/dss_bootstrap.py]
---

# DSS Bootstrap: One-File Repository Transformation

The DSS Bootstrap system enables **instant transformation** of any repository with a single file and voice commands in Cursor.

## 🚀 Quick Start

### Option 1: Voice Commands in Cursor (Instant)

1. **Open any repository in Cursor**
2. **Say: "Format this repo"** or **"Apply DSS formatting"**
3. **Follow the provided instructions** - the AI will guide you through the process
4. **Done!** Your repository is now DSS-structured with full AI intelligence

### Option 2: Download & Run Bootstrap

```bash
# Download the bootstrap file
curl -sSL https://raw.githubusercontent.com/Dub1n/dss/main/meta/scripts/dss_bootstrap.py -o dss_bootstrap.py

# Transform your repository  
python dss_bootstrap.py
```

### Option 3: Drop File & Run

1. **Download** `dss_bootstrap.py` to any repository root
2. **Run:** `python dss_bootstrap.py`
3. **Follow the prompts** for transformation options

## 🎯 What Happens Automatically

The bootstrap process:

1. **📥 Downloads** the latest DSS auto-formatter from GitHub
2. **🔍 Analyzes** your project to detect type (data_science, web_application, etc.)
3. **⚡ Transforms** repository to DSS structure with intelligent file organization
4. **🧠 Installs** Cursor AI intelligence with project-specific context
5. **🎪 Sets up** voice commands for ongoing DSS operations
6. **✅ Preserves** your original repository (creates `-dss` version)

## 🗣️ Voice Commands Available

After bootstrap installation, you can use these voice commands in Cursor:

### Repository Management
- **"Format this repo"** - Transform to DSS structure
- **"Apply DSS formatting"** - Alternative transformation command
- **"Show DSS structure"** - Explain current organization

### File Creation
- **"Create analysis notebook"** - New Jupyter notebook with DSS frontmatter
- **"Add Python module"** - New .py file in src/ with proper structure
- **"Create documentation"** - New markdown file with DSS metadata
- **"Add test file"** - New test file in tests/ directory

### Project Management
- **"Update project index"** - Refresh INDEX.md with current structure
- **"Generate documentation"** - Create comprehensive project docs
- **"Create project overview"** - Generate high-level documentation

## 🛠️ Command Line Options

```bash
# Basic transformation (creates new -dss directory)
python dss_bootstrap.py

# Transform in place (CAUTION: backup first!)
python dss_bootstrap.py --in-place

# Preview changes without making them
python dss_bootstrap.py --dry-run

# Transform specific directory
python dss_bootstrap.py --repo-path /path/to/repo

# Show help
python dss_bootstrap.py --help
```

## 🎪 Project Type Detection

The bootstrap automatically detects your project type for optimal configuration:

| **Project Type** | **Detected By** | **Optimizations** |
|------------------|------------------|-------------------|
| **Data Science** | `.ipynb`, `.csv`, `requirements.txt` | Jupyter workflows, data organization |
| **Web Application** | `package.json`, `.js/.ts` files | Component structure, API routes |
| **Python Package** | `setup.py`, `pyproject.toml` | Module organization, testing |
| **Documentation** | Majority `.md` files | Content creation, cross-linking |
| **General** | Mixed/unknown files | Standard DSS conventions |

## 📁 What Gets Created

After bootstrap transformation:

```
your-repo-dss/                    # New DSS-structured repository
├── src/                          # Your source code (organized)
├── data/                         # Data files and datasets
├── docs/                         # Documentation
├── meta/                         # Configuration and scripts
├── tests/                        # Test files
├── .cursor/
│   └── rules/                    # AI intelligence files (~15KB)
│       ├── assistant.mdc         # Core DSS logic
│       ├── dss-overview.mdc      # Framework overview
│       ├── dss-guide.mdc         # Guidelines  
│       ├── project_context.mdc   # Project-specific context
│       ├── dss_bootstrap_commands.mdc  # Voice commands
│       └── dss_quick_reference.mdc     # Quick reference
└── INDEX.md                      # Project overview
```

**Original repository remains untouched!**

## ✨ AI Assistant Enhancement

After bootstrap, your AI assistant becomes **DSS-intelligent** and automatically:

- ✅ **Understands** DSS folder structure and conventions
- ✅ **Applies** proper frontmatter to all new files  
- ✅ **Uses** templates from `meta/templates/` when creating files
- ✅ **Follows** project-specific patterns and requirements
- ✅ **Cross-references** files using DSS linking conventions
- ✅ **Maintains** project metadata and documentation
- ✅ **Suggests** improvements for DSS compliance

## 🔄 Team Usage

### Share Bootstrap Intelligence

```bash
# After transformation, commit the Cursor rules
cd your-repo-dss
git add .cursor/rules/
git commit -m "Add DSS AI intelligence"
git push

# Team members get the same intelligent assistant
git clone your-repo-dss
# AI immediately understands DSS conventions!
```

### Update Intelligence

Keep your assistant current with latest DSS improvements:

```bash
# Update DSS rules from GitHub  
python .cursor/rules/update_dss_rules.py
```

## 🆚 Comparison: Bootstrap vs Manual

| **Method** | **Time** | **Complexity** | **AI Integration** | **Updates** |
|------------|----------|----------------|-------------------|-------------|
| **DSS Bootstrap** | ~2 minutes | Single command | ✅ Automatic | ✅ Self-updating |
| **Manual Setup** | ~30+ minutes | Multiple steps | ❌ Manual config | ❌ Manual updates |
| **GitHub Template** | ~10 minutes | Repository creation | ⚠️ Partial | ❌ Manual updates |

## 🎯 Use Cases

### For Individual Developers
- **Instant DSS adoption** for any existing project
- **Voice-controlled** file creation and project management
- **Consistent structure** across all repositories
- **AI-enhanced** development workflow

### For Teams
- **Standardized** project structure across team
- **Shared AI intelligence** with consistent behavior
- **Easy onboarding** for new team members
- **Automated compliance** with project conventions

### For Organizations
- **Scalable** DSS adoption across multiple projects
- **Consistent documentation** and structure standards
- **Reduced setup time** for new projects
- **AI-assisted** development at organizational scale

## ⚠️ Important Notes

1. **Backup First**: Always commit or backup your repository before transformation
2. **Internet Required**: Bootstrap downloads files from GitHub
3. **Python 3.8+**: Required for running the bootstrap script
4. **Cursor IDE**: Voice commands work best with Cursor editor
5. **Preservation**: Original repository is never modified (unless using `--in-place`)

## 🆘 Troubleshooting

### Bootstrap Fails to Download
```bash
# Check internet connection and GitHub access
curl -sSL https://raw.githubusercontent.com/Dub1n/dss/main/meta/scripts/dss_bootstrap.py
```

### Voice Commands Not Working
1. Ensure `.cursor/rules/` directory was created
2. Restart Cursor after transformation
3. Try text commands first, then voice commands

### Project Type Detection Issues
```bash
# Manually specify project type
python dss_bootstrap.py --help
# Look for project-type options in auto-formatter
```

## 🌟 Success Story

> *"I dropped `dss_bootstrap.py` into my messy research repository, said 'Format this repo' in Cursor, and 2 minutes later had a beautifully organized DSS project with an AI assistant that understood my data science workflow. Game changer!"*

---

**🎯 The DSS Bootstrap makes adopting structured, AI-enhanced development as simple as saying "Format this repo" - no configuration, no complexity, just instant intelligent organization.**

## 📚 Related Documentation

- [Cursor Integration Guide](cursor_integration.md) - Complete Cursor setup details
- [DSS Auto-formatter Usage](dss_autoformatter_usage.md) - Advanced auto-formatter options  
- [Getting Started with DSS](getting_started.md) - Full DSS framework guide
- [Voice Commands Reference](.cursor/rules/dss_voice_commands.mdc) - Complete voice command list 