## Grade: 100 / 100

**Assignment:** Google Workspace Assistant + GitHub MCP (ADK)  
**Attempt:** 1 of 2  ·  **Graded:** 2026-07-11  ·  Commit `e1b1c59`

> **Note: provided files were modified.** These instructor-provided files (not meant to be changed) differ from the originals: `workspace_assistant/main.py`. No automatic deduction was applied. If this was a necessary setup fix, no action is needed.

### Score breakdown
| Criterion | Max | Earned | Notes |
|-----------|-----|--------|-------|
| tool_design | 18 | 18 | Four tools (list_tasks, create_task, complete_task, update_task) implemented as plain functions with clear action-verb names, complete Args/Returns docstrings, and typed parameters (e.g. tasks_tools.py:70, :154); all collected into the tasks_tools list at tasks_tools.py:212. Exceeds the 3-tool minimum. Option B chosen; calendar_tools.py left as stub and ignored per instructions. (`workspace_assistant/tools/tasks_tools.py:212`) |
| agent_instructions | 14 | 13 | System instruction is clear and scoped: separates Tasks vs GitHub duties, guides tool selection ('Use the task tools whenever...', 'Use the GitHub MCP toolset...'), and enforces safe behavior (be careful with state-changing actions, ask a clarifying question when ambiguous, never expose credentials). Minor: guidance is somewhat generic and does not spell out per-tool confirmation flows. (`workspace_assistant/agent.py:19`) |
| error_handling | 14 | 14 | Every tool wraps its API call in try/except and returns a user-friendly {status, message} dict on failure (tasks_tools.py:63, :110, :147, :205). Also validates edge cases before calling the API: empty title (tasks_tools.py:83), missing task_id (tasks_tools.py:128, :168), and no-op updates (tasks_tools.py:186). Exemplary. (`workspace_assistant/tools/tasks_tools.py:63`) |
| functionality | 14 | 14 | Statically correct Google Tasks API usage via get_tasks_service(): list_tasks -> tasks().list (tasks_tools.py:38), create_task -> tasks().insert with title/notes/due body (tasks_tools.py:99), complete_task -> tasks().patch status=completed (tasks_tools.py:135), update_task -> tasks().patch (tasks_tools.py:193). Due date normalized to RFC3339 via _format_due_date (tasks_tools.py:13). Operations match intended behavior. (`workspace_assistant/tools/tasks_tools.py:37`) |
| code_quality | 10 | 10 | Readable, well-organized, consistently documented code; a private helper (_format_due_date) reduces duplication. Tools wired into an LlmAgent via create_agent() (agent.py:39-44) with tools=tasks_tools + [github_mcp_toolset]. (`workspace_assistant/agent.py:39`) |
| mcp_configured | 10 | 10 | McpToolset configured correctly for the GitHub MCP server: StdioServerParameters runs npx @modelcontextprotocol/server-github with the token in env (mcp_tools.py:65-69), wrapped in StdioConnectionParams and passed to McpToolset (mcp_tools.py:125-127). Attached to the agent via tools=tasks_tools + [github_mcp_toolset] (agent.py:43). (`workspace_assistant/tools/mcp_tools.py:125`) |
| github_queries | 15 | 13 | GitHub queries are routed through the unfiltered McpToolset, which exposes the server's repo/issue/PR tools to the agent (get_github_mcp_toolset, mcp_tools.py:116; attached agent.py:43), and the instruction directs GitHub requests to that toolset (agent.py:27-29). Reflection reports the MCP server successfully read the repository README (reflection_template.md:33). Wiring is correct; no explicit per-query tooling beyond the MCP passthrough. (`workspace_assistant/agent.py:43`) |
| mcp_error_handling | 5 | 4 | Missing GitHub token is detected with an explicit, clear message ('GITHUB_PERSONAL_ACCESS_TOKEN is not set in .env', mcp_tools.py:62-63) and the instruction tells the agent to explain errors in plain English and never leak tokens (agent.py:33-34). Partial: it raises a ValueError rather than returning a friendly {status, message} dict, and connection/runtime MCP failures are not caught. (`workspace_assistant/tools/mcp_tools.py:62`) |
| _bonus_ | +25 | +23 | |
| Integrity deduction | — | 0 | Provided files MODIFIED — flagged, no deduction (workspace_assistant/main.py) |
| **Total** | **100** | **100** | |

### What went well
- Robust, consistent error handling: every Tasks tool combines input validation with try/except and returns a structured {status, message} dict (tasks_tools.py:63, :83, :128, :186).
- Statically correct Google Tasks API usage across all four operations via get_tasks_service(), including RFC3339 due-date normalization (tasks_tools.py:13, :99, :135, :193).
- Clear, safety-aware agent instruction that scopes Tasks vs GitHub duties, guides tool selection, and forbids leaking credentials (agent.py:19-35).
- Both bonus paths attempted with a thoughtful compatibility shim: search_github_tools plus a defer_loading=True config that gracefully falls back to tool_filter on older ADK (mcp_tools.py:72-150).

### What to improve (actionable)
- Return MCP/token failures as a friendly {status, message} dict instead of raising ValueError, and catch MCP connection/runtime errors so GitHub failures degrade as gracefully as the Tasks tools (mcp_tools.py:62).
- Add a concrete token/context comparison (before vs after tool search) to the reflection to fully earn the tool-search bonus (reflection_template.md:61).
- Clean up the reflection: the 'Bonus: Tool Search Pattern' section is duplicated (reflection_template.md:55 and :69) and 'Key Learnings' is left empty (reflection_template.md:65).
- Consider exposing explicit per-query GitHub confirmation for state-changing MCP actions (e.g. create_issue) mirroring the care taken with Tasks writes.

### Automated checks
- ✅ All required files implemented
- ⚠️ Provided files MODIFIED — flagged, no deduction (workspace_assistant/main.py)
- ✅ 0/0 output artifacts committed
- ✅ Reflection 867 words

### Resubmission
You may resubmit **once**. Push fixes to this repo, then notify the instructor; we'll re-grade as **Attempt 2 (final)**. This is attempt 1 of 2.

---
*Graded automatically with Claude Code against the course rubric. Questions → contact the instructor.*


---
<sub>🔎 **Autograder record** — attempt 1 of 2 · graded at commit `e1b1c59` · delivered 2026-07-11T18:01:16Z. Commits pushed to `main` after this timestamp are treated as a resubmission.</sub>
