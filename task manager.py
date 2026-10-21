import argparse
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path.home() / ".cli_task_manager.json"


def load_tasks():
    """Load tasks from JSON storage."""
    if not DATA_FILE.exists():
        return []

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and all(
            isinstance(task, dict)
            and {"id", "title", "due", "done"} <= task.keys()
            and isinstance(task["id"], int)
            and isinstance(task["title"], str)
            and isinstance(task["due"], str)
            and isinstance(task["done"], bool)
            for task in data
        ):
            return data
    except (json.JSONDecodeError, OSError):
        pass

    return []


def save_tasks(tasks):
    """Save tasks to JSON storage."""
    DATA_FILE.write_text(
        json.dumps(tasks, indent=2),
        encoding="utf-8"
    )


def validate_due_date(value):
    """Validate YYYY-MM-DD dates."""
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def add_task(title, due=None):
    """Create and save a task."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")

    if due and not validate_due_date(due):
        raise ValueError("Due date must use YYYY-MM-DD format.")

    tasks = load_tasks()
    task_id = max((task["id"] for task in tasks), default=0) + 1

    task = {
        "id": task_id,
        "title": title,
        "due": due or "",
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks(status="all", due=None):
    """Filter tasks by status and/or due date."""
    if due and not validate_due_date(due):
        raise ValueError("Due date must use YYYY-MM-DD format.")

    tasks = load_tasks()

    if status == "pending":
        tasks = [task for task in tasks if not task["done"]]
    elif status == "done":
        tasks = [task for task in tasks if task["done"]]

    if due:
        tasks = [task for task in tasks if task["due"] == due]

    return tasks


def complete_task(task_id):
    """Mark a task as complete."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return task

    raise ValueError(f"Task ID {task_id} was not found.")


def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    remaining = [task for task in tasks if task["id"] != task_id]

    if len(remaining) == len(tasks):
        raise ValueError(f"Task ID {task_id} was not found.")

    save_tasks(remaining)


def build_parser():
    """Configure the command-line interface."""
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="A simple command-line task manager."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--status",
        choices=["all", "pending", "done"],
        default="all"
    )
    list_parser.add_argument("--due", help="Filter by due date (YYYY-MM-DD)")

    done_parser = subparsers.add_parser("done", help="Complete a task")
    done_parser.add_argument("id", type=int, help="Task ID")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            task = add_task(args.title, args.due)
            print(f"Added task #{task['id']}: {task['title']}")

        elif args.command == "list":
            tasks = list_tasks(args.status, args.due)

            if not tasks:
                print("No tasks found.")
            else:
                for task in tasks:
                    status = "Done" if task["done"] else "Pending"
                    due = task["due"] or "No due date"
                    print(
                        f"#{task['id']} [{status}] "
                        f"{task['title']} (Due: {due})"
                    )

        elif args.command == "done":
            task = complete_task(args.id)
            print(f"Completed task #{task['id']}: {task['title']}")

        elif args.command == "delete":
            delete_task(args.id)
            print(f"Deleted task #{args.id}.")

    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()