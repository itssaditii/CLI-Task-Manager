CLI Task Manager

A lightweight command-line task manager built with Python. It uses argparse subcommands to manage tasks and stores task data in a JSON file between runs.

Features
Add tasks with optional due dates.
List all tasks or filter by status.
Filter tasks due on a specific date or on/before a date.
Mark tasks as completed.
Delete tasks by ID.
Persist task data in JSON.
Validate due dates in YYYY-MM-DD format.
Run automated tests using pytest.
Requirements
Python 3.9 or newer
pip
pytest for running tests
Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/cli-task-manager.git
cd cli-task-manager


Create and activate a virtual environment (recommended).

Windows:

python -m venv .venv
.venv\Scripts\activate


macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate


Install the application in editable mode with testing dependencies:

python -m pip install -e ".[test]"

Usage
Add a task
tasker add "Finish Python project"
tasker add "Submit assignment" --due 2026-12-31

List tasks
tasker list

Filter by status
tasker list --status pending
tasker list --status completed

Filter by due date

Show tasks due on a particular date:

tasker list --due-on 2026-12-31


Show tasks due on or before a date:

tasker list --due-before 2026-12-31

Complete a task

Use the task ID shown by the list command:

tasker done 1

Delete a task
tasker delete 1

View help
tasker --help
tasker add --help
tasker list --help

Data Storage

By default, task data is stored at:

Windows: %USERPROFILE%\.task-manager\tasks.json
macOS/Linux: ~/.task-manager/tasks.json

Set the TASK_MANAGER_FILE environment variable to use a different data file. This is useful for testing or keeping separate task lists.

Running Tests

Run the test suite from the project root:

python -m pytest -v


The tests cover task creation, status filtering, due-date filtering, and deletion.

Project Structure
cli-task-manager/
├── task_manager/
│   ├── __init__.py
│   ├── cli.py
│   └── storage.py
├── tests/
│   └── test_task_manager.py
├── .gitignore
├── pyproject.toml
└── README.md

Design Decisions
argparse provides subcommands instead of an interactive menu.
Each task has an integer ID, title, status, and optional due date.
Tasks are stored in JSON for persistence between runs.
Due-date filters exclude tasks without a due date.
The TASK_MANAGER_FILE environment variable allows tests to use isolated temporary files.
The application has no runtime dependencies outside the Python standard library.
Future Improvements
Add task priorities and descriptions.
Support editing task titles and due dates.
Add overdue-task filtering.
Improve recovery and reporting for corrupted data files.
License

This project is available under the MIT License. Add a LICENSE file if you choose to distribute it under that license.

Author

Created as part of Task 04 — Capstone: CLI Task Manager.



Aditi Lodhi
