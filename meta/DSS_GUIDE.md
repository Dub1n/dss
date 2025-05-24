# 🗂️  Data SuperStructure Guide

## Principles:
1. Modular files, minimal duplication.
2. YAML front‑matter for quick indexing.
3. Markdown links everywhere (GitHub‑ & Obsidian‑friendly).
4. `assistant.md` gives the bot deterministic steps.

Run `python meta/generate_docs.py` or your IDE’s “sync‑DSS” command after coding sessions.


## Formatting a pre-existing repo
To format a repo in the DSS structure, run the folling commands:

python -m venv .venv && source .venv/bin/activate
pip install -r meta/requirements.txt
export OPENAI_API_KEY=sk-...
python meta/convert_to_dss.py --source ~/old_repo --dest ./dss_repo
cd ./dss_repo
python meta/llm_tasks.py --mode docs

## Requirements
openai – the LLM API wrapper used in llm_tasks.py
PyYAML – parsing dss_config.yml
aiofiles – async file reads/writes for faster batch processing
rich – coloured CLI logging/spinners (both scripts)
tqdm – progress bars when walking large repos
pathspec – advanced glob/ignore matching that mirrors .gitignore rules

## TODO
TODO: explain when and how to use the python scripts
TODO: find an appropriate doc to add instructions for what to do when encountering certain keywords such as TODO or FILL (should they be !TODO and !FILL?)
TODO: create a super-repo for managing and developing DSS that contains this repo in its src as a template (perhaps template ver1?) and git it



## [Pre-commit hooks, Version pinning, Smoke test]

# 0️⃣  activate your virtual-env first
pip install pre-commit pytest

# 1️⃣  Quick pre-commit protection
echo "repos:\n  - repo: https://github.com/psf/black\n    rev: 24.3.0\n    hooks:\n      - id: black" > .pre-commit-config.yaml
pre-commit install   # one time only

# 2️⃣  Lock exact versions
pip freeze > meta/requirements.lock

# 3️⃣  Add the smoke test file shown above under tests/
pytest                # run locally

git add .pre-commit-config.yaml meta/requirements.lock tests/
git commit -m "Add basic safety nets"
