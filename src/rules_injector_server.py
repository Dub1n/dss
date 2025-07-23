"""DSS Rules Injector MCP Server (FastMCP version)
Context-aware DSS rule retrieval system for progressive agent guidance.

Provides tools for intelligent DSS rule loading based on task context.
Works over STDIO (the default transport expected by Cursor / Claude Desktop).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Annotated, Optional

# API imports
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolsCapability, ServerCapabilities, ToolListChangedNotification
import anyio
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import ErrorData, INVALID_PARAMS
from mcp.shared.exceptions import McpError

# Pydantic Field for parameter metadata
from pydantic import Field

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("dss_rules_injector")

# ---------------------------------------------------------------------------
# FastMCP server definition
# ---------------------------------------------------------------------------

# Properly typed tools capability so clients recognize listChanged
capabilities = ServerCapabilities(tools=ToolsCapability(listChanged=True))
# FastMCP instance with explicit capabilities
mcp = FastMCP("dss_rules_injector_server", capabilities=capabilities)

# Advertise that the tool list may change so clients request it immediately
mcp._mcp_server.notification_options.tools_changed = True  # type: ignore[attr-defined]

# Resolve project root (parent of src/ directory where this script lives)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# DSS Rules base path (relative to project root)
RULES_BASE_PATH = PROJECT_ROOT / ".cursor" / "rules"

# Default bootstrap trilogy for DSS initialization
DEFAULT_BOOTSTRAP_RULES = [
    "00-dss-core.mdc",
    "01-dss-behavior.mdc", 
    "workflows/00-workflow-selection.mdc"
]

# Context-based rule suggestions
CONTEXT_RULE_MAP = {
    "code": ["workflows/02-code-modification.mdc", "guidelines/11-documentation-standards.mdc"],
    "documentation": ["workflows/03-documentation-driven.mdc", "guidelines/07-folder-readme-policy.mdc"],
    "validation": ["guidelines/04-validation-rules.mdc", "guidelines/09-error-recovery.mdc"],
    "tasks": ["workflows/04-task-decomposition.mdc", "guidelines/05-tag-conventions.mdc"],
    "github": ["workflows/06-github-issues-integration.mdc", "guidelines/08-github-issue-labels.mdc"],
    "maintenance": ["guidelines/01-dss-maintenance.mdc", "guidelines/06-backlink-conventions.mdc"],
    "templates": ["guidelines/00-dss-templates.mdc", "guidelines/03-naming-conventions.mdc"]
}

RULES_SENT = False # Track if bootstrap rules have been sent

@mcp.tool(description="Retrieve DSS rule files with intelligent context-based suggestions for progressive agent guidance.")
def get_dss_rules(
    rule_files: Annotated[
        Optional[list[str]],
        Field(
            description="List of DSS rule files to retrieve. Omit, pass [], or null to load the default bootstrap trilogy.",
            json_schema_extra={
                "examples": [
                    {"rule_files": []},
                    {"rule_files": ["guidelines/04-validation-rules.mdc"]}
                ],
                "activation_triggers": [
                    "first user message",
                    "rules missing",
                    "agent bootstrap"
                ]
            },
        ),
    ] = None,
    context: Annotated[str, Field(description="Task context to suggest additional relevant rules: 'code', 'documentation', 'validation', 'tasks', 'github', 'maintenance', 'templates'")] = "",
    include_suggestions: Annotated[bool, Field(description="Whether to include context-based rule suggestions")] = True,
) -> str:
    """Retrieve DSS rule files with context-aware suggestions.

    Args:
        rule_files: Specific rule files to retrieve. Defaults to bootstrap trilogy.
        context: Task context for smart rule suggestions.
        include_suggestions: Whether to include additional context-based suggestions.

    Returns:
        Combined content of requested rule files plus suggestions.
    """
    
    # Treat None, "null", or empty list as request for defaults
    if not rule_files:
        rule_files = DEFAULT_BOOTSTRAP_RULES.copy()
        
    # Add context-based suggestions
    suggested_files = []
    if include_suggestions and context:
        context_lower = context.lower()
        for key, suggestions in CONTEXT_RULE_MAP.items():
            if key in context_lower:
                suggested_files.extend(suggestions)
                break
    
    all_files = rule_files + suggested_files
    
    # Read rule file contents
    rule_contents = []
    missing_files = []
    
    for rule_file in all_files:
        rule_path = RULES_BASE_PATH / rule_file
        try:
            if rule_path.exists():
                content = rule_path.read_text(encoding='utf-8')
                rule_contents.append(f"## File: {rule_file}\n\n{content}\n")
                logger.info(f"📖 Loaded rule file: {rule_file}")
            else:
                missing_files.append(rule_file)
                logger.warning(f"⚠️ Rule file not found: {rule_file}")
        except Exception as e:
            missing_files.append(f"{rule_file} (error: {e})")
            logger.error(f"❌ Error reading {rule_file}: {e}")
    
    # Build response
    response = "# DSS Rules Retrieved\n\n"
    
    if context:
        response += f"**Context**: {context}\n"
        if suggested_files:
            response += f"**Context-based suggestions included**: {', '.join(suggested_files)}\n"
        response += "\n"
    
    if rule_contents:
        response += "---\n\n"
        response += "\n---\n\n".join(rule_contents)
    
    if missing_files:
        response += f"\n\n## Missing Files\nThe following files could not be loaded:\n"
        for missing in missing_files:
            response += f"- {missing}\n"
    
    if not rule_contents:
        response += "No rule files could be loaded. Check that .cursor/rules directory exists."
    
    global RULES_SENT
    RULES_SENT = True  # mark that bootstrap rules have been provided
    return response

@mcp.tool(description="List all available DSS rule files organized by category for discovery and navigation.")
def list_available_rules(
    category: Annotated[str, Field(description="Rule category to list: 'workflows', 'guidelines', 'config', 'all'")] = "all",
    include_descriptions: Annotated[bool, Field(description="Whether to include file descriptions from frontmatter")] = True,
) -> str:
    """List available DSS rule files by category.

    Args:
        category: Which category of rules to list.
        include_descriptions: Whether to extract and show descriptions.

    Returns:
        Organized listing of available DSS rule files.
    """
    
    if not RULES_BASE_PATH.exists():
        return "❌ DSS rules directory (.cursor/rules) not found."
    
    def get_file_description(file_path: Path) -> str:
        """Extract description from file frontmatter."""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Look for description in YAML frontmatter
            in_frontmatter = False
            for line in lines:
                if line.strip() == '---':
                    if in_frontmatter:
                        break
                    in_frontmatter = True
                    continue
                
                if in_frontmatter and line.startswith('description:'):
                    return line.replace('description:', '').strip()
            
            # Fallback: look for first heading
            for line in lines:
                if line.startswith('# '):
                    return line.replace('# ', '').strip()
                    
        except Exception:
            pass
        return "No description available"
    
    categories_to_check = []
    if category == "all":
        categories_to_check = [".", "workflows", "guidelines", "config"]
    else:
        categories_to_check = [category]
    
    response = "# Available DSS Rules\n\n"
    
    for cat in categories_to_check:
        cat_path = RULES_BASE_PATH / cat if cat != "." else RULES_BASE_PATH
        
        if not cat_path.exists():
            continue
            
        # Get .mdc files in this category
        if cat == ".":
            files = [f for f in cat_path.glob("*.mdc") if not f.name.startswith('.')]
            cat_name = "Core Rules"
        else:
            files = list(cat_path.glob("*.mdc"))
            cat_name = cat.title()
        
        if files:
            response += f"## {cat_name}\n\n"
            
            for file_path in sorted(files):
                relative_path = file_path.relative_to(RULES_BASE_PATH)
                
                if include_descriptions:
                    desc = get_file_description(file_path)
                    response += f"- **{relative_path}** - {desc}\n"
                else:
                    response += f"- {relative_path}\n"
            
            response += "\n"
    
    # Add usage suggestions
    response += "## Usage Suggestions\n\n"
    response += "**Bootstrap**: Start with `get_dss_rules()` (default) to load core rules\n"
    response += "**Context-aware**: Use context parameter for smart suggestions:\n"
    for context_key, suggestions in CONTEXT_RULE_MAP.items():
        response += f"- `{context_key}` → {', '.join(suggestions[:2])}...\n"
    
    return response


async def _run() -> None:
    """Main async entry – launches reminder and MCP stdio server concurrently."""

    logger.info("🚀 Starting DSS Rules Injector (FastMCP / stdio)")

    async def _reminder() -> None:
        """Warn if bootstrap rules haven't been requested shortly after start."""
        await anyio.sleep(5)
        if not RULES_SENT:
            logger.warning(
                "⚠️  No get_dss_rules call detected within 5 seconds of server start. "
                "Agents should invoke get_dss_rules() to load bootstrap rules."
            )

    async def _run_mcp_server() -> None:
        """Run the FastMCP stdio server until EOF."""
        # DEBUG: list registered tools so we can verify the server is exposing them
        try:
            tool_names = list(mcp._mcp_server._tool_registry.keys())  # type: ignore[attr-defined]
            logger.debug("Registered tools at startup: %s", tool_names)
        except AttributeError:
            logger.debug("Could not access tool registry for debug logging.")

        init_opts = mcp._mcp_server.create_initialization_options(
            notification_options=NotificationOptions(tools_changed=True)
        )

        async with stdio_server() as (r, w):
            await mcp._mcp_server.run(r, w, init_opts)

    # Use a nursery so both tasks can run concurrently without TaskGroup state errors
    async with anyio.create_task_group() as tg:
        tg.start_soon(_reminder)
        tg.start_soon(_run_mcp_server)


def main() -> None:  # pragma: no cover
    anyio.run(_run)


# ---------------------------------------------------------------------------
# Entrypoint guard
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main() 