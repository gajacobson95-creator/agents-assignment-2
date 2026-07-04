# Assignment 2 Reflection

**Name:** Gabe Jacobson  
**Option:** B - Tasks  
**Date:** July 4, 2026

---

## Tool Design Decisions

### Tools Implemented
1. **list_tasks**: Retrieves tasks from the user's Google Tasks list, with options to control the number of results and whether completed tasks are included.
2. **create_task**: Creates a new Google Task with a title, optional notes, and an optional due date.
3. **complete_task**: Marks an existing task as completed using its task ID.
4. **update_task**: Updates an existing task's title, notes, or due date.

### Why These Tools?
I chose the Tasks option because task management is a practical workspace use case for an assistant. These tools cover the core task workflow: viewing what needs to be done, creating new tasks, updating task details, and marking tasks complete. Together, they allow the agent to act like a lightweight productivity assistant rather than just answering questions.

### Description Strategy
I wrote the tool names and docstrings with direct action verbs so the model could clearly match user intent to the right tool. For example, "list," "create," "complete," and "update" map closely to common user requests. I also used clear parameter names like `task_id`, `title`, `notes`, and `due` so the expected inputs would be easy for both the model and a developer to understand.

---

## Challenges Encountered

### Challenge 1: InMemoryRunner Session Setup
- **Problem:** When testing the assistant through `python main.py --interactive`, the agent failed with a `SessionNotFoundError`. The runner was trying to use a session ID before a session had been created.
- **Solution:** I updated `main.py` so the `InMemoryRunner` creates a session with `create_session_sync()` before calling `runner.run(...)`. After that change, the CLI test moved past the session error.

### Challenge 2: Model and MCP Authentication Issues
- **Problem:** The Gemini model produced a `429 RESOURCE_EXHAUSTED` quota error during testing. After switching providers, the GitHub MCP test also initially failed because the `.env` file still had a placeholder GitHub token.
- **Solution:** I switched the agent to use OpenAI through ADK's LiteLLM support and added `litellm` to the requirements. I also replaced the placeholder GitHub token with a real personal access token stored only in `.env`. After that, the token authenticated successfully and the GitHub MCP server was able to read the repository README.

---

## Error Handling Approach

Each task tool uses a `try/except` block and returns a structured dictionary instead of letting raw exceptions crash the assistant. Successful responses include a status and relevant data, while failures return an error status and a clear message. This makes the tools more predictable for the LLM and gives the user a cleaner response when something goes wrong.

I anticipated errors such as missing required inputs, invalid task IDs, Google API failures, and authentication/configuration problems. The goal was to make the tools fail safely and explain the issue without exposing sensitive details.

---

## Ideas for Improvement

If I had more time, I would add or change:

1. Add OAuth-based live testing for Google Tasks so the assistant can be tested against a real Google account end to end.
2. Add date parsing so users can say things like "tomorrow" or "next Friday" instead of needing ISO-style due dates.
3. Improve the CLI to use the async ADK runner methods directly instead of relying on deprecated synchronous behavior.

---

## Key Learnings

This assignment helped me understand that building an AI agent is different from writing a normal script. The tool functions need to be clear enough for both Python and the language model. Good function names, docstrings, type hints, and structured return values make it much easier for the agent to decide what to do.

I also learned that a lot of agent development is integration work. The Python code can be correct, but the system still depends on environment variables, API keys, model provider limits, OAuth, Node.js, MCP servers, and GitHub permissions. Debugging required separating code errors from configuration errors.

The biggest takeaway was that tests are necessary but not enough by themselves. The automated tests confirmed the tool and MCP setup, but the real CLI smoke test exposed session setup, model quota, and token issues. Running both automated tests and realistic prompts gave me more confidence that the assistant was actually wired together correctly.
