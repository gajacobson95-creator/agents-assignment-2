"""
Part 2: GitHub MCP Integration

Configure McpToolset to connect to the GitHub MCP server.
"""

import inspect
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()


GITHUB_TOOL_CATALOG = [
    {
        "name": "get_file_contents",
        "description": "Read the contents of a file from a GitHub repository.",
        "keywords": ["file", "readme", "contents", "repository", "code"],
    },
    {
        "name": "search_repositories",
        "description": "Search for GitHub repositories by keyword or owner.",
        "keywords": ["repository", "repo", "search", "owner"],
    },
    {
        "name": "list_issues",
        "description": "List issues for a GitHub repository.",
        "keywords": ["issues", "bugs", "tickets", "open"],
    },
    {
        "name": "get_issue",
        "description": "Get details for a specific GitHub issue.",
        "keywords": ["issue", "details", "ticket"],
    },
    {
        "name": "create_issue",
        "description": "Create a new issue in a GitHub repository.",
        "keywords": ["create", "issue", "bug", "ticket"],
    },
    {
        "name": "list_pull_requests",
        "description": "List pull requests for a GitHub repository.",
        "keywords": ["pull request", "pr", "review", "merge"],
    },
    {
        "name": "get_pull_request",
        "description": "Get details for a specific GitHub pull request.",
        "keywords": ["pull request", "pr", "details"],
    },
]


def _github_server_params() -> StdioServerParameters:
    """Create stdio server parameters for the GitHub MCP server."""
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN is not set in .env")

    return StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )


def _mcp_toolset_supports_defer_loading() -> bool:
    """Return whether the installed ADK McpToolset supports defer_loading."""
    return "defer_loading" in str(inspect.signature(McpToolset))


def search_github_tools(query: str) -> Dict[str, Any]:
    """Search for available GitHub MCP tools by keyword.

    Args:
        query: Search term such as "issues", "repository", "file", or "pull request".

    Returns:
        A dictionary containing matching GitHub tool names and descriptions.
    """
    try:
        normalized_query = query.lower().strip()
        matches: List[Dict[str, str]] = []

        for item in GITHUB_TOOL_CATALOG:
            searchable_text = " ".join(
                [item["name"], item["description"], " ".join(item["keywords"])]
            ).lower()

            if not normalized_query or normalized_query in searchable_text:
                matches.append(
                    {
                        "name": item["name"],
                        "description": item["description"],
                    }
                )

        return {
            "status": "success",
            "query": query,
            "matches": matches,
            "count": len(matches),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unable to search GitHub tools: {str(e)}",
        }


def get_github_mcp_toolset() -> McpToolset:
    """
    Create a GitHub MCP toolset using the GitHub MCP server.

    Returns:
        McpToolset configured with the user's GitHub personal access token.
    """
    server_params = _github_server_params()

    return McpToolset(
        connection_params=StdioConnectionParams(server_params=server_params)
    )


def get_github_mcp_toolset_deferred() -> McpToolset:
    """
    Create a GitHub MCP toolset for the bonus tool-search pattern.

    The assignment bonus asks for defer_loading=True. The installed ADK version
    may not expose that constructor argument, so this function uses it when
    available and falls back to tool_filter for compatibility.
    """
    server_params = _github_server_params()
    connection_params = StdioConnectionParams(server_params=server_params)

    if _mcp_toolset_supports_defer_loading():
        return McpToolset(
            connection_params=connection_params,
            defer_loading=True,
        )

    return McpToolset(
        connection_params=connection_params,
        tool_filter=["get_file_contents", "search_repositories"],
    )


mcp_tools = [
    get_github_mcp_toolset,
]
