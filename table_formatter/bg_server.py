"""---
 tags: [code, table_formatter, python_server]
 provides: [background_python_bridge]
 requires: [core.table_parser, core.table_analyzer, core.table_formatter]
 status: active
 priority: high
---

Background server that keeps a Python formatter process alive and processes
line-delimited JSON requests from the VS Code extension. Each request must be a
single JSON object on one line:

    {"table": "markdown table text", "options": {<formatter options>}}

The server responds with a single JSON line:

    {"ok": true, "result": "formatted table"}
    {"ok": false, "error": "message"}

This avoids the process-spawn overhead for every formatting command.
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any, Dict

from core.table_parser import TableParser
from core.table_analyzer import TableAnalyzer
from core.table_formatter import TableFormatter, FormatConfig


parser = TableParser()
analyzer = TableAnalyzer()


def build_config(opts: Dict[str, Any]) -> FormatConfig:
    """Convert a JSON options dict into a FormatConfig instance."""
    return FormatConfig(
        max_width=opts.get("max_width", 80),
        min_padding=opts.get("min_padding", 1),
        padding=opts.get("min_padding", 1),
        preserve_code_blocks=opts.get("preserve_code_blocks", True),
        wrap_text=opts.get("wrap_text", True),
    )


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            table_text: str = req.get("table", "")
            options: Dict[str, Any] = req.get("options", {})

            fmt = TableFormatter(build_config(options))
            parsed_table, diagnostics = parser.parse_table(table_text)
            analysis = analyzer.analyze_table(parsed_table, diagnostics)
            formatted = fmt.format_table(parsed_table, diagnostics, analysis)

            sys.stdout.write(json.dumps({"ok": True, "result": formatted}) + "\n")
            sys.stdout.flush()
        except Exception as exc:
            # Include traceback for easier debugging on the TS side when needed
            sys.stdout.write(json.dumps({"ok": False, "error": str(exc)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main() 