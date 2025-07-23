import sys
import os
import pytest
from pathlib import Path

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import INVALID_PARAMS
from mcp.shared.exceptions import McpError

# The module under test
from src.rules_injector_server import rules_injector

# ---------------------------------------------------------------------------
# Unit-level tests – call the tool function directly
# ---------------------------------------------------------------------------

def test_rules_injector_happy_path():
    """Injecting a valid rule should return a human-readable confirmation string."""
    result = rules_injector(
        rule_type="behavior",
        rule_content="Respond politely at all times.",
        context="Global",
        priority=4,
    )

    assert "Rule injected successfully" in result
    assert "behavior" in result
    assert "Respond politely" in result


def test_rules_injector_invalid_rule_type():
    """An unknown rule_type should raise an MCP INVALID_PARAMS error."""
    with pytest.raises(McpError) as exc_info:
        rules_injector(rule_type="unknown", rule_content="whatever", priority=3)

    err = exc_info.value.error
    assert err.code == INVALID_PARAMS
    assert "rule_type" in err.message


def test_rules_injector_invalid_priority():
    """A priority outside 1-5 should raise an MCP INVALID_PARAMS error."""
    with pytest.raises(McpError) as exc_info:
        rules_injector(rule_type="behavior", rule_content="text", priority=6)

    err = exc_info.value.error
    assert err.code == INVALID_PARAMS
    assert "priority" in err.message


# ---------------------------------------------------------------------------
# Integration test – spin up the stdio server and query tools/list
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_rules_injector_server_tools_list(tmp_path):
    """Ensure that the running server advertises the rules_injector tool."""

    # Use the same interpreter to start the server module via -m
    project_root = Path(__file__).resolve().parents[1]

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.rules_injector_server"],
        cwd=str(project_root),
    )

    # Integration test disabled by default – enable with env var to avoid hanging CI/developers
    if os.getenv("RUN_INTEGRATION_TESTS", "0") != "1":
        pytest.skip("Integration test skipped (set RUN_INTEGRATION_TESTS=1 to enable)")

    import anyio
    # Protect against hangs regardless of backend
    async with anyio.fail_after(15):
        async with stdio_client(server) as (read_stream, write_stream):
            # Create a ClientSession on top of the raw streams
            from mcp.client.session import ClientSession

            session = ClientSession(read_stream, write_stream)

            # Initialize protocol handshake
            init_result = await session.initialize()
            assert (
                init_result.capabilities.tools and init_result.capabilities.tools.listChanged is True
            )

            # Request the list of tools and ensure our tool is present
            tools_result = await session.list_tools()
            tool_names = {tool.name for tool in tools_result.tools}
            assert "rules_injector" in tool_names 