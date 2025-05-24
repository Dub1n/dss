"""
llm_tasks.py ── DSS repo helper
================================
A command‑line utility that calls an LLM (OpenAI by default) to
materialise higher‑level documentation assets inside a DSS‑style project.

It can be executed locally **or** inside CI. Typical use‑cases:

* `docs`   – Create / update folder READMEs, module docs and INDEX.md
* `canvas` – Produce Obsidian Canvas JSON diagrams from a repo manifest
* `all`    – Run everything in one shot

Examples
--------

```bash
# Generate / refresh all docs for the current DSS repo
python meta/llm_tasks.py --mode docs

# Only regenerate items touched since the last commit
python meta/llm_tasks.py --mode docs --changed-only

# Build a high‑level architecture canvas as ./canvas/architecture.canvas
python meta/llm_tasks.py --mode canvas
```

Environment variables
---------------------

* **OPENAI_API_KEY**   – Standard OpenAI key (required)
* **DSS_LLM_MODEL**    – Defaults to `gpt-4o-mini`
* **DSS_LLM_MAX_TOKENS** – Defaults to `1024`
* **DSS_LLM_TEMPERATURE** – Defaults to `0.2`

Prompt files are read from `meta/prompts/*.md` (or *.txt). The file’s stem
becomes the task name (e.g. `folder_summary.md` → task `folder_summary`).

The script is intentionally minimal; feel free to extend it with Anthropic
or local models by swapping out the `_call_llm()` implementation.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence
from pathlib import Path, dotenv
dotenv.load_dotenv(Path(__file__).parent.parent / ".env")


try:
    import openai  # type: ignore
except ImportError as exc:
    raise SystemExit("openai package not found. Install via `pip install openai`.") from exc

# ---------------------------------------------------------------------------
# Config & constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent  # project root assuming meta/llm_tasks.py
PROMPT_DIR = ROOT / "meta" / "prompts"
CANVAS_DIR = ROOT / "canvas"
DEFAULT_MODEL = os.getenv("DSS_LLM_MODEL", "gpt-4o-mini")
MAX_TOKENS = int(os.getenv("DSS_LLM_MAX_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("DSS_LLM_TEMPERATURE", "0.2"))

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("llm_tasks")

# ---------------------------------------------------------------------------
# Helper dataclasses
# ---------------------------------------------------------------------------

@dataclass
class RepoItem:
    path: Path
    type: str  # "folder"|"file"

    @property
    def rel(self) -> Path:
        return self.path.relative_to(ROOT)


@dataclass
class Prompt:
    name: str
    template: str

# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------


def _load_prompts() -> Dict[str, Prompt]:
    """Load all prompt templates from PROMPT_DIR. Stem becomes the task name."""
    prompts: Dict[str, Prompt] = {}
    logger.debug("Loading prompts from %s", PROMPT_DIR)
    for p in PROMPT_DIR.glob("*.*"):
        if p.suffix not in {".md", ".txt"}:
            continue
        prompts[p.stem] = Prompt(name=p.stem, template=p.read_text(encoding="utf-8"))
    if not prompts:
        logger.error("No prompt files found in %s", PROMPT_DIR)
        raise SystemExit(1)
    return prompts


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _git_changed_files() -> Sequence[Path]:
    """Return a list of Paths that changed in the current branch compared to HEAD^."""
    try:
        res = subprocess.run(
            ["git", "diff", "--name-only", "HEAD^"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        logger.warning("Git diff failed; falling back to full run")
        return []  # means "everything"
    return [Path(line.strip()).resolve() for line in res.stdout.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# LLM call wrappers
# ---------------------------------------------------------------------------


def _call_llm_sync(prompt: str, *, model: str = DEFAULT_MODEL) -> str:
    """Synchronous convenience wrapper for OpenAI chat completions."""
    logger.debug("Calling OpenAI model=%s, %d chars prompt", model, len(prompt))
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message["content"].strip()


async def _call_llm(prompt: str, *, model: str = DEFAULT_MODEL) -> str:
    """Asynchronous version (preferred for bulk calls)."""
    logger.debug("[async] calling model=%s", model)
    resp = await openai.AsyncChatCompletion.acreate(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return resp.choices[0].message["content"].strip()


# ---------------------------------------------------------------------------
# Core generators
# ---------------------------------------------------------------------------


def _inventory_repo() -> List[RepoItem]:
    """Walk the repo and return interesting items (top‑level folders + files)."""
    items: List[RepoItem] = []
    for p in ROOT.iterdir():
        if p.name.startswith(".") or p.name in {"meta", "canvas", "__pycache__"}:
            continue
        if p.is_dir():
            items.append(RepoItem(path=p, type="folder"))
        elif p.is_file():
            items.append(RepoItem(path=p, type="file"))
    return items


async def _generate_folder_readme(folder: Path, prompt: Prompt) -> None:
    """Generate or update README.md inside *folder* using *prompt*."""
    manifest = "\n".join(f.name for f in folder.iterdir())
    final_prompt = prompt.template.format(folder=folder.name, manifest=manifest)
    readme_content = await _call_llm(final_prompt)
    readme_path = folder / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    logger.info("✓ %s", readme_path.relative_to(ROOT))


async def _generate_index_md(items: List[RepoItem], prompt: Prompt) -> None:
    manifest = json.dumps([str(i.rel) for i in items], indent=2)
    final_prompt = prompt.template.format(manifest=manifest)
    index_content = await _call_llm(final_prompt)
    (ROOT / "INDEX.md").write_text(index_content, encoding="utf-8")
    logger.info("✓ INDEX.md")


async def _generate_canvas(items: List[RepoItem], prompt: Prompt) -> None:
    CANVAS_DIR.mkdir(exist_ok=True)
    manifest = json.dumps([str(i.rel) for i in items])
    canvas_prompt = prompt.template.format(manifest=manifest)
    canvas_json = await _call_llm(canvas_prompt)
    (CANVAS_DIR / "architecture.canvas").write_text(canvas_json, encoding="utf-8")
    logger.info("✓ canvas/architecture.canvas")


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def generate_docs(*, changed_only: bool = False) -> None:
    """High‑level orchestrator for docs generation."""
    prompts = _load_prompts()
    items = _inventory_repo()

    if changed_only:
        changed = set(_git_changed_files())
        if changed:
            items = [i for i in items if any(i.path in c.parents or i.path == c for c in changed)]
            logger.info("Running in changed‑only mode (items=%d)", len(items))
        else:
            logger.info("No changed files detected; skipping generation.")
            return

    # Gather tasks (folder READMEs)
    tasks = []
    folder_prompt = prompts.get("folder_summary")
    if not folder_prompt:
        logger.error("Missing folder_summary prompt file in %s", PROMPT_DIR)
        return

    for it in items:
        if it.type == "folder":
            tasks.append(_generate_folder_readme(it.path, folder_prompt))

    # INDEX.md
    index_prompt = prompts.get("index") or prompts.get("index_md")
    if index_prompt:
        tasks.append(_generate_index_md(items, index_prompt))

    # Kick off concurrency gate
    asyncio.run(asyncio.gather(*tasks))


def generate_canvas(*, changed_only: bool = False) -> None:
    prompts = _load_prompts()
    canvas_prompt = prompts.get("canvas") or prompts.get("architecture_canvas")
    if not canvas_prompt:
        logger.error("No canvas prompt found in meta/prompts")
        return
    items = _inventory_repo()
    if changed_only:
        changed = set(_git_changed_files())
        if changed:
            items = [i for i in items if any(i.path in c.parents or i.path == c for c in changed)]
    asyncio.run(_generate_canvas(items, canvas_prompt))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate DSS docs and canvases using an LLM")
    p.add_argument("--mode", choices=["docs", "canvas", "all"], default="docs")
    p.add_argument("--changed-only", action="store_true", help="Only touch files changed since HEAD^")
    return p.parse_args(argv)


def main() -> None:
    args = _parse_args()
    logger.info("Starting llm_tasks.py mode=%s", args.mode)

    if args.mode in {"docs", "all"}:
        generate_docs(changed_only=args.changed_only)
    if args.mode in {"canvas", "all"}:
        generate_canvas(changed_only=args.changed_only)

    logger.info("Done.")


if __name__ == "__main__":
    main()
