---
module: "meta"
status: draft
tags: [meta]
provides: []
requires: []
---
# Meta Info
## Overview
Contains the documentation on how the DSS system is implemented and maintained, along with a folder for file maintenance scripts and file templates. 
## Files 
| file          | purpose           |
|---------------|-------------------|
|README.md      |Folder Overview    |
|roadmap.md     |                   |
|DSS_GUIDE.md   |                   |
|scipts         |scripts folder     |
|templates      |templates folder   |

## File Specifics

### requirements.txt
Role: Declaration of the libraries your code needs. Think of it as the “shopping list.”
Typical contents: Only direct dependencies, usually with loose or caret pins:
    openai>=1.30
    PyYAML>=6
Who/what reads it: Humans (“what does this project use?”) & new contributors (pip install -r … to create their first venv).

openai – the LLM API wrapper used in llm_tasks.py
PyYAML – parsing dss_config.yml
aiofiles – async file reads/writes for faster batch processing
rich – coloured CLI logging/spinners (both scripts)
tqdm – progress bars when walking large repos
pathspec – advanced glob/ignore matching that mirrors .gitignore rules

### requirements.lock:
Role: Snapshot of every package (direct and transitive) and the exact versions that worked on your machine on this day.
Typical contents: Dozens of fully-pinned lines, e.g.:
    openai==1.30.1
    urllib3==2.2.1
Who/what reads it: CI / production deploys that must be bit-for-bit reproducible: pip install -r meta/requirements.lock.

