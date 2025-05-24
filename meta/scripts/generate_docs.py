"""Stub: generate docs from code — fill with your favourite LLM calls."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
(DOCS/"auto_placeholder.md").write_text("# Auto docs placeholder\n")
print("Docs refreshed (placeholder).")
