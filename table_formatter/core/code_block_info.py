from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeBlockInfo:
    """Information about a code block in a cell."""
    start: int
    end: int
    content: str
    language: Optional[str]
    is_fenced: bool
    indent_level: int = 0
    parent_block: Optional['CodeBlockInfo'] = None 