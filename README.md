---
tags: ["template", "dss", "framework"]
provides: [dss_template, project_structure]
requires: []
---

# DSS: Data SuperStructure

**DSS is an open protocol for building structured systems.** Help make every repository LLM-native and human-friendly.

---

## What Problem Does This Solve?

AI assistants are terrible at understanding most codebases. They give you generic suggestions, miss obvious context, and generally act like they've never seen your project before.

Meanwhile, as projects grow, even humans can't find anything. Documentation gets buried, code relationships become mysteries, and navigating your own project becomes a nightmare.

**DSS fixes both problems.** It's an open protocol that actually works with your existing tools:

- **AI assistants finally understand your codebase** and give useful help instead of irrelevant suggestions
- **Humans can actually find things** without digging through random folders  
- **Documentation doesn't go stale** because everything stays connected
- **Works with whatever you're already using** - GitHub, VS Code, Obsidian, Cursor, whatever

---

## How It Works

DSS is a protocol that is easy for you (and your assistants) to follow. It consists of a **folder structure + metadata protocol** that any tool can read:

```text
📁 your-project/
├── 📂 any/             ← Code
├── 📂 folders/         ← Documentation and guides  
├── 📂 that/            ← Image libraries
├── 📂 you/             ← Ideas
└── 📂 like/            ← To-do lists
```

Each file gets some **YAML frontmatter** (tags and relationships) that creates connections between everything, while folder READMEs sum up the important bits for quick reference. Both humans and AI can follow the breadcrumbs.

**The result:** Your project makes sense to everyone and everything, no matter at what stage they join.

---

## Quick Start

### Get DSS Intelligence in Cursor Right Now

Copy [this `.cursor/rules` folder](.cursor/rules) into your project's `.cursor/rules` directory.

That's it. Your AI assistant now understands DSS structure and will automatically organize files properly, add frontmatter, and maintain documentation links.

### Start a New DSS Project

1. [Use this template](https://github.com/yourusername/dss_template_repo/generate) to create a new repository
2. Clone it and start coding in the `src/` folder
3. Watch your AI assistant provide better assistance

---

## Learn More

### For Getting Started

- [Complete Setup Guide](docs/getting_started.md) - The full walkthrough
- [Troubleshooting](docs/troubleshooting.md) - When things break

### For Understanding DSS

- [DSS Guide](meta/DSS_GUIDE.md) - Core concepts and principles
- [Project Structure](docs/documentation_index.md) - How folders work

### For AI Integration

- [Cursor Setup](docs/cursor_integration.md) - AI assistant configuration
- [Auto-formatting](docs/automated_formatting.md) - Automatic transformation tools

---

## What Makes DSS Actually Useful

### **Open Protocol, Nothing Proprietary**

Uses standard stuff - Markdown, YAML, JSON. Works with any tool. No vendor lock-in, no special software required.

### **Built for Humans AND AI**

Something designed for both. Your IDE, GitHub, and Obsidian vault look good, AI assistants understand what's going on.

### **Enhances What You Already Use**

Doesn't replace your workflow - makes it work better. GitHub, VS Code, Obsidian, Cursor - they all just work better with DSS.

### **Actually Stays Organized**

Cross-references and metadata mean things stay connected as your project grows instead of becoming disorganized.

---

## Test Drive: DSS Benchmark

Want to see how this works? Try the benchmark:

```bash
# Copy benchmark to separate folder
cp -r benchmark/ ../dss-benchmark-test/
cd ../dss-benchmark-test/

# Open in your AI-enabled editor (like Cursor)
# Give your AI assistant this task: "Complete benchmark task 01-xs following RUN_BENCHMARK.md"
```

Watch your AI assistant handle realistic development tasks automatically with DSS-organized code.

---

## Contributing

1. Try DSS with your own projects
2. [Report issues](https://github.com/yourusername/dss_template_repo/issues) or share improvements
3. Help us make every codebase more navigable

Message for details

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

*DSS: An open protocol for projects that make sense.*

---
