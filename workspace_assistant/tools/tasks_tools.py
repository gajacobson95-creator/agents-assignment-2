"""
Option B: Tasks Manager Tools

Google Tasks tools for listing, creating, completing, and updating tasks.
Each tool returns a dictionary with a status field so the agent can explain
success or failure clearly to the user.
"""

from typing import Optional, Dict, Any
from tools.auth import get_tasks_service


def _format_due_date(due: Optional[str]) -> Optional[str]:
    """Convert a YYYY-MM-DD date into the RFC3339-style date Google Tasks expects."""
    if not due:
        return None

    due = due.strip()
    if "T" in due:
        return due

    return f"{due}T00:00:00.000Z"


def list_tasks(max_results: int = 10, show_completed: bool = False) -> Dict[str, Any]:
    """
    List tasks from the user's default Google Tasks list.

    Args:
        max_results: Maximum number of tasks to return.
        show_completed: Whether completed tasks should be included.

    Returns:
        A dictionary containing status and a list of tasks or an error message.
    """
    try:
        service = get_tasks_service()
        result = service.tasks().list(
            tasklist="@default",
            maxResults=max_results,
            showCompleted=show_completed,
            showHidden=show_completed,
        ).execute()

        tasks = result.get("items", [])
        simplified_tasks = [
            {
                "id": task.get("id"),
                "title": task.get("title"),
                "status": task.get("status"),
                "due": task.get("due"),
                "notes": task.get("notes"),
            }
            for task in tasks
        ]

        return {
            "status": "success",
            "count": len(simplified_tasks),
            "tasks": simplified_tasks,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"Could not list tasks: {error}",
        }


def create_task(title: str, notes: Optional[str] = None, due: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new task in the user's default Google Tasks list.

    Args:
        title: Title of the task to create.
        notes: Optional notes or details for the task.
        due: Optional due date in YYYY-MM-DD format.

    Returns:
        A dictionary containing status and the created task or an error message.
    """
    try:
        if not title or not title.strip():
            return {
                "status": "error",
                "message": "Task title cannot be empty.",
            }

        task_body = {"title": title.strip()}

        if notes:
            task_body["notes"] = notes.strip()

        formatted_due = _format_due_date(due)
        if formatted_due:
            task_body["due"] = formatted_due

        service = get_tasks_service()
        created_task = service.tasks().insert(
            tasklist="@default",
            body=task_body,
        ).execute()

        return {
            "status": "success",
            "message": f"Created task: {created_task.get('title')}",
            "task": created_task,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"Could not create task: {error}",
        }


def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Mark an existing Google Task as complete.

    Args:
        task_id: The Google Tasks ID of the task to complete.

    Returns:
        A dictionary containing status and the completed task or an error message.
    """
    try:
        if not task_id or not task_id.strip():
            return {
                "status": "error",
                "message": "Task ID is required to complete a task.",
            }

        service = get_tasks_service()
        completed_task = service.tasks().patch(
            tasklist="@default",
            task=task_id.strip(),
            body={"status": "completed"},
        ).execute()

        return {
            "status": "success",
            "message": f"Completed task: {completed_task.get('title')}",
            "task": completed_task,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"Could not complete task: {error}",
        }


def update_task(task_id: str, title: Optional[str] = None, notes: Optional[str] = None, due: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing Google Task's title, notes, or due date.

    Args:
        task_id: The Google Tasks ID of the task to update.
        title: Optional new title for the task.
        notes: Optional new notes for the task.
        due: Optional new due date in YYYY-MM-DD format.

    Returns:
        A dictionary containing status and the updated task or an error message.
    """
    try:
        if not task_id or not task_id.strip():
            return {
                "status": "error",
                "message": "Task ID is required to update a task.",
            }

        update_body = {}

        if title:
            update_body["title"] = title.strip()

        if notes:
            update_body["notes"] = notes.strip()

        formatted_due = _format_due_date(due)
        if formatted_due:
            update_body["due"] = formatted_due

        if not update_body:
            return {
                "status": "error",
                "message": "Provide at least one field to update: title, notes, or due.",
            }

        service = get_tasks_service()
        updated_task = service.tasks().patch(
            tasklist="@default",
            task=task_id.strip(),
            body=update_body,
        ).execute()

        return {
            "status": "success",
            "message": f"Updated task: {updated_task.get('title')}",
            "task": updated_task,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": f"Could not update task: {error}",
        }


tasks_tools = [
    list_tasks,
    create_task,
    complete_task,
    update_task,
]
