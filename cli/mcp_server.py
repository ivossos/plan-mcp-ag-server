"""MCP Server - stdio transport for Claude Desktop integration."""

import asyncio
import json
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, Resource

from planning_agent.agent import (
    initialize_agent,
    close_agent,
    execute_tool,
    get_tool_definitions,
)

# Flag to track if agent is initialized
_initialized = False


async def ensure_initialized():
    """Ensure agent is initialized (lazy initialization)."""
    global _initialized
    if not _initialized:
        print("Initializing Planning agent...", file=sys.stderr)
        try:
            result = await initialize_agent()
            _initialized = True
            print(f"Planning agent initialized: {result}", file=sys.stderr)
        except Exception as e:
            error_msg = f"Failed to initialize Planning agent: {e}"
            print(error_msg, file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            # Don't set _initialized = True, so we can retry on next call
            raise RuntimeError(error_msg) from e


def create_mcp_server() -> Server:
    """Create and configure the MCP server."""
    server = Server(
        name="plan-mcp-ag-server",
        version="1.0.0"
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available Planning tools."""
        # Return tool definitions immediately without waiting for Planning connection
        definitions = get_tool_definitions()
        return [
            Tool(
                name=d["name"],
                description=d["description"],
                inputSchema=d["inputSchema"]
            )
            for d in definitions
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Execute a Planning tool."""
        # Initialize on first tool call
        await ensure_initialized()

        result = await execute_tool(name, arguments)
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        """List available prompts/instructions."""
        from planning_agent.agent import AGENT_INSTRUCTION
        return [
            Prompt(
                name="planning_agent_instructions",
                description="Instructions for the Oracle Planning agent",
                arguments=[]
            )
        ]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Get agent instructions/prompts."""
        from planning_agent.agent import AGENT_INSTRUCTION
        if name == "planning_agent_instructions":
            return [
                {
                    "role": "user",
                    "content": AGENT_INSTRUCTION
                }
            ]
        raise ValueError(f"Unknown prompt: {name}")

    @server.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources (offerings)."""
        # Planning agent doesn't expose resources, return empty list
        return []

    return server


async def run_server():
    """Run the MCP server with stdio transport."""
    # Create server immediately (don't initialize agent yet)
    server = create_mcp_server()
    print("MCP server created, waiting for connections...", file=sys.stderr)

    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    finally:
        if _initialized:
            await close_agent()


def main():
    """Entry point for MCP server."""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer stopped", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()









