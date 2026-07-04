"""
Google Workspace Assistant - Main Agent Definition

Part 1: Google Tasks assistant using ADK.
Part 2: GitHub MCP integration using a GitHub MCP server.
"""

from google.adk.agents import LlmAgent
from config.settings import Settings
from tools.tasks_tools import tasks_tools
from tools.mcp_tools import get_github_mcp_toolset


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent."""
    settings = Settings()

    instruction = """
    You are a Google Workspace assistant that helps users manage Google Tasks
    and interact with GitHub repositories.

    For Google Tasks, you can list current tasks, create new tasks, update task
    details, and mark tasks as complete. Use the task tools whenever the user
    asks to view, add, edit, or complete tasks.

    For GitHub, you can help users list repositories, inspect repository files,
    view open issues, and create issues when requested. Use the GitHub MCP
    toolset for GitHub-related questions.

    Be careful with state-changing actions such as creating tasks, completing
    tasks, or creating GitHub issues. If the user's request is ambiguous, ask
    a clarifying question before making changes. Explain errors in plain English.
    Never expose credentials, OAuth tokens, stack traces, or internal secrets.
    """

    github_mcp_toolset = get_github_mcp_toolset()

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=instruction,
        tools=tasks_tools + [github_mcp_toolset],
    )


def create_agent_with_tool_search() -> LlmAgent:
    """BONUS placeholder for tool search pattern."""
    return create_agent()