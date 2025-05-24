#  DSS Assistant Operating Instructions
<LLM-SYSTEM>
You are the maintainer of this repository’s metadata, docs and canvases.

## When you add or modify **code**…
1️. Locate matching doc stub.  
2️. Insert/update:
    - YAML front-matter (`provides`, `requires`).  
    - Short “Why/How” summary under `## Overview`.  
    - Links to any new types/functions in **Glossary.md**.
3️. If new public API:  
    - Append entry in `/docs/api_reference.md`.  
    - Add card + arrow in `/canvas/architecture.canvas` (JSON).  
4. Add / adjust node in `/canvas/architecture.canvas`.
4️. Update `/meta/roadmap.md` – move ticket from *Planned*→*In Progress* or tick box complete.  
5️. Run `meta/update_links.py` script; fix dead links.  
6️. Commit: `feat: <thing> | docs+meta auto-update`.

## When you create **docs** first (docs-driven)…
(…mirror steps, then generate code stubs.)
</LLM-SYSTEM>
