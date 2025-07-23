"""Top-level table_formatter package.

Re-exports the canonical TableFormatter and related core modules for
convenient import::

    from table_formatter import TableFormatter

This shim avoids direct references to legacy implementations and ensures
all consumers use the unified implementation in ``table_formatter.core``.
"""

from importlib import import_module as _import_module

# Re-export core public symbols
_core = _import_module('table_formatter.core')
TableFormatter = _core.TableFormatter  # noqa: F401

# Optionally expose commonly used analysis/parsing helpers
TableParser = _core.TableParser  # noqa: F401
TableAnalyzer = _core.TableAnalyzer  # noqa: F401
TableDiagnostics = _core.TableDiagnostics  # noqa: F401
TableAnalysis = _core.TableAnalysis  # noqa: F401
ColumnAnalysis = _core.ColumnAnalysis  # noqa: F401
ContentType = _core.ContentType  # noqa: F401

__all__ = _core.__all__ + ['TableFormatter'] 