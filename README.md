---
tags: ["template", "dss", "framework"]
provides: [dss_template, project_structure]
requires: []
---

# DSS Template Repository

**A structured, LLM-optimized project framework for seamless human+AI collaboration.**

[![Use this template](https://img.shields.io/badge/Use%20this-Template-green?style=flat-square)](https://github.com/yourusername/dss_template_repo/generate)
[![DSS Auto-formatter](https://img.shields.io/badge/DSS-Auto--formatter-blue?style=flat-square)](#auto-formatter)

---

## 🧭 What is DSS?

Data SuperStructure (DSS) is a structured, LLM-compatible project framework designed to:

* **Enable transparent, documented evolution** of code, data, and ideas
* **Support human+AI collaboration** through consistent structure and metadata  
* **Use automation and LLMs** to generate and maintain clean, living documentation
* **Make any codebase feel native to LLMs** with minimal prompt tokens and crystal-clear navigation

---

## 🚀 Quick Start

### Option 1: Voice Command (Instant!) 🎙️

**drop the [bootstrapper](github.com/Dub1n/dss/blob/main/meta/scripts/dss_bootstrap.py) into any repository in Cursor and say:**
- **"Format this repo"** 
- **"Apply DSS formatting"**
- **"Transform to DSS structure"**

The AI assistant will guide you through instant transformation with full intelligence integration!

### Option 2: One-File Bootstrap

```bash
# Download and run the bootstrap
curl -sSL https://raw.githubusercontent.com/yourusername/dss_template_repo/main/meta/scripts/dss_bootstrap.py -o dss_bootstrap.py
python dss_bootstrap.py
```

**Result:** 2-minute transformation with Cursor AI intelligence!

### Option 3: Use as GitHub Template

1. Click the **"Use this template"** button above or [create a new repository from this template](https://github.com/yourusername/dss_template_repo/generate)
2. Clone your new repository
3. Run the initialization script:
   ```bash
   cd your-new-repo
   python meta/scripts/init_dss_project.py --name "Your Project" --description "Your description"
   ```

### Option 4: Advanced Auto-formatter

Transform any existing repository with full control:

```bash
# Download the full auto-formatter
curl -sSL https://raw.githubusercontent.com/yourusername/dss_template_repo/main/meta/scripts/install_dss_autoformatter.py | python3

# Format your repository
dss-autoformat --source /path/to/your/repo --dest /path/to/dss/repo
```

### Option 5: Manual Setup

```bash
# Clone this template
git clone https://github.com/yourusername/dss_template_repo.git my_project
cd my_project

# Set up environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r meta/requirements.txt

# Configure your project
python meta/scripts/setup_project.py
```

---

## 📁 Project Structure

```text
/src/         → Source code and executable logic
/data/        → Datasets, artifacts, and data files  
/docs/        → Human and AI-generated documentation
/canvas/      → Obsidian Canvas JSON diagrams (optional)
/meta/        → Scripts, prompts, config, and automation
/tests/       → Test files and validation datasets
```

### Key Features

* **YAML front-matter** on all files for rich metadata and LLM context
* **Automated documentation generation** via LLM integration
* **Token-efficient prompts** through structured summaries and cross-references
* **Git-friendly structure** that renders beautifully on GitHub
* **Obsidian-compatible** for visual knowledge management

---

## 🤖 Auto-Formatter

The DSS auto-formatter intelligently transforms any repository into DSS structure while preserving functionality and git history.

### Features

* **Multi-phase processing**: Discovery → Classification → Planning → Execution → Enhancement → Validation
* **LLM-assisted classification** for ambiguous files
* **Cursor AI assistant integration** with project-specific context and DSS intelligence
* **Safe transformation** with automatic rollback on failure
* **Dependency analysis** and import updating
* **Metadata injection** with intelligent tag generation
* **Risk assessment** and conflict resolution

### Usage

```bash
# Basic transformation
dss-autoformat --source ./my-repo --dest ./my-repo-dss

# Advanced options
dss-autoformat \
  --source ./my-repo \
  --dest ./my-repo-dss \
  --config custom_dss_config.yml \
  --llm-assist \
  --preserve-git-history \
  --dry-run
```

For comprehensive documentation, see [Automated Formatting Guide](docs/automated_formatting.md).

---

## 📖 Documentation

### Getting Started
- [DSS Bootstrap Guide](docs/dss_bootstrap_guide.md) - **⚡ Instant transformation with voice commands**
- [Getting Started Guide](docs/getting_started.md) - Complete setup and usage guide
- [DSS Overview](meta/DSS_GUIDE.md) - Core concepts and principles
- [Configuration](meta/dss_config.yml) - Customization options

### Advanced Usage  
- [LLM Task Automation](meta/llm_tasks.py) - Generate docs and maintain structure
- [Naming Conventions](meta/guidelines/naming_conventions.md) - File and folder naming standards
- [Template System](meta/templates/README.md) - Standardized file templates

### Integration
- [Cursor Integration Guide](docs/cursor_integration.md) - Complete Cursor AI assistant setup and propagation
- [Cursor IDE Setup](.cursor/rules/assistant.mdc) - AI assistant configuration files
- [VS Code Integration](meta/integrations/vscode.md) - Editor plugins and workflows
- [CI/CD Integration](meta/integrations/github_actions.yml) - Automated workflows

---

## 🛠 Requirements

- **Python 3.8+**
- **Git** 
- **OpenAI API key** (for LLM-powered automation)
- [Optional] **Node.js** (for markdown table formatting)

---

## 🤝 Contributing

1. Use this template to create your own DSS project
2. Share improvements back via pull requests
3. Report issues or suggest enhancements
4. Help improve the auto-formatter based on real-world usage

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Related Projects

- [DSS Auto-formatter](https://github.com/yourusername/dss-autoformatter) - Standalone formatting tool
- [DSS Examples](https://github.com/yourusername/dss-examples) - Example projects using DSS
- [DSS Plugins](https://github.com/yourusername/dss-plugins) - Community extensions

---

> **DSS is a structured system for building structured systems.** Help us make every codebase LLM-native and human-friendly.

# DSS GPT Bridge Service

A FastAPI service that connects Custom ChatGPT with DSS-formatted GitHub repositories, providing intelligent repository analysis and interaction capabilities.

## Features

- **GitHub Integration**: Seamless access to repository structure and files
- **DSS Intelligence**: Deep understanding of DSS metadata and conventions  
- **Search Capabilities**: Content and metadata-aware search across repositories
- **Safety Features**: Validation and safety checks for repository modifications
- **Multi-Repository Support**: Work with multiple DSS projects from one interface

## Architecture

The bridge service acts as an intermediary between Custom GPT Actions and GitHub's API, translating conversational requests into appropriate repository operations while maintaining DSS conventions.

## Development Status

🚧 **In Development** - This project is being actively developed as part of the DSS ecosystem.

See the [task breakdown](meta/tasks/custom_gpt_dss_integration.md) for detailed development progress.
