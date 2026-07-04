"""
Part 2: GitHub MCP Integration

Configure McpToolset to connect to the GitHub MCP server.
"""

import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()


def get_github_mcp_toolset() -> McpToolset:
    """
    Create a GitHub MCP toolset using the GitHub MCP server.

    Returns:
        McpToolset configured with the user's GitHub personal access token.
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN is not set in .env")

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params)
    )


mcp_tools = [
    get_github_mcp_toolset,
]