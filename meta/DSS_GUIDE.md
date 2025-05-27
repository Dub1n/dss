---
description: 
globs: 
alwaysApply: true
---
# 🗂️  Data SuperStructure Guide

### Purpose

> **Goal:** make any dataset / codebase feel *native* to an LLM—minimal prompt tokens, zero duplicated effort, and crystal‑clear navigation for humans.
>
> **How:** store everything as plaintext (Markdown, code, JSON) plus light metadata so GitHub, Obsidian, Cursor **and** GPT all see the same structure.

#### Core benefits

| Need           | DSS Answer                                         |
| -------------- | -------------------------------------------------- |
| *Fast recall*  | Summaries + tags keep prompts short.               |
| *Modularity*   | Each concept lives in its own file—no giant blobs. |
| *Human UX*     | GitHub renders; Obsidian graphs; Cursor searches.  |
| *Self‑healing* | An LLM can update docs/links/canvas in one pass.   |

---

## Principles:
1. Modular files, minimal duplication.
2. YAML front‑matter for quick indexing.
3. Markdown links everywhere (GitHub‑ & Obsidian‑friendly).
4. `assistant.md` gives the bot deterministic steps.

Run `python meta/generate_docs.py` or your IDE's "sync‑DSS" command after coding sessions.


### Formatting a pre-existing repo
To format a repo in the DSS structure, run the folling commands:

python -m venv .venv && source .venv/bin/activate
pip install -r meta/requirements.txt
export OPENAI_API_KEY=sk-...
python meta/convert_to_dss.py --source ~/old_repo --dest ./dss_repo
cd ./dss_repo
python meta/llm_tasks.py --mode docs

# Canvas: DSS System Architecture

### 📁 Project Structure

- `src/`
  - Source code modules
  - Implements tooling and helpers for conversion, LLM tasks, etc.

- `docs/`
  - Human-facing documentation
  - Includes `DSS_OVERVIEW.md`, `README.md`, module docs, etc.

- `meta/`
  - Project metadata, config, and scripts
  - Contains:
    - `convert_to_dss.py`
    - `llm_tasks.py`
    - `dss_config.yml`
    - `prompts/` folder

- `canvas/`
  - Optional Obsidian-style canvas JSONs (if used)

- `.cursor/rules/`
  - Files loaded into every LLM prompt in Cursor
  - Contains:
    - `assistant.mdc`
    - `dss-overview.mdc`

- `tests/`
  - Test harness and validation scripts

### 🔄 Key Workflows

### ➤ 1. Convert arbitrary repo → DSS

**Script:** `convert_to_dss.py`

- Walks a source folder
- Sorts files into `src/`, `data/`, `docs/`, etc.
- Injects front-matter YAML (tags, provides/requires)
- Writes a manifest for downstream use

### ➤ 2. Generate documentation

**Script:** `llm_tasks.py`

- Summarizes code & folders via LLM
- Uses prompts from `meta/prompts/*.md`
- Outputs:
  - `docs/*_doc.md`
  - `README.md` in each folder
  - Project-wide `INDEX.md`
  - Optional canvas JSON

### ➤ 3. Update links / glossary

**Planned script:** `update_links.py`

- Cross-links mentioned files
- Refreshes `Glossary.md` based on tags and usage

### 🧠 Behavioral Conventions

- Tags are declared in YAML front-matter
- Every file and folder should be navigable via summaries
- Archive material is stored in `docs/🔒archive/` and excluded from LLM context
- All automation follows the rules in `meta/dss_config.yml`
- Canonical source of instruction lives in `meta/assistant.md`
- **Documentation Location:** The main project roadmap resides in `meta/roadmap.md`. Process-specific roadmaps should also be included and organized within `meta/roadmap.md`. `INDEX.md` is reserved for a fleshed-out file tree overview and should not contain roadmaps.
- **TODO Linking:** For tasks in `meta/TODO.md` that relate to a specific section of the detailed roadmap in `meta/roadmap.md`, add a reference `(@roadmap: [Section Name])` at the end of the TODO item line.

### 📌 Versioning Strategy

- Tags (e.g., `v1.0`, `v1.1`) are used to freeze major milestones
- Current state always lives in the working tree (HEAD)
- No snapshots or duplicates of old versions are stored in-tree

### 🧩 Integration with Cursor

- `.cursor/rules/assistant.mdc` — Cursor's persistent instruction set
- `.cursor/rules/dss-overview.mdc` — High-level system context
- Scripts and documentation ensure LLMs always operate within the current system view

## Referenced By

- [meta/scripts/sync_dss_mdc.py](mdc:meta/scripts/sync_dss_mdc.py) - Used as source file for generating .cursor/rules/dss-overview.mdc
- [.cursor/rules/dss-overview.mdc](mdc:.cursor/rules/dss-overview.mdc) - Generated from this file's content
- [meta/guidelines/backlink_conventions.md](mdc:meta/guidelines/backlink_conventions.md) - Referenced as part of backlink implementation examples
- [docs/automated_formatting](mdc:docs/automated_formatting) - Referenced in automation documentation

