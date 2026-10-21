import json
import pytest
import task_manager as tm


@pytest.fixture
def task_file(tmp_path, monkeypatch):
    """Use a temporary JSON file for each test."""
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(tm, "DATA_FILE", path)
    return path


def test_add_task(task_file):
    task = tm.add_task("Study Python", "2026-10-25")

    assert task["id"] == 1
    assert task["title"] == "Study Python"
    assert task["done"] is False
    assert len(tm.load_tasks()) == 1


def test_filter_pending_and_done(task_file):
    first = tm.add_task("Finish assignment")
    tm.add_task("Read notes")
    tm.complete_task(first["id"])

    assert len(tm.list_tasks(status="pending")) == 1
    assert len(tm.list_tasks(status="done")) == 1


def test_filter_by_due_date(task_file):
    tm.add_task("Task A", "2026-10-25")
    tm.add_task("Task B", "2026-10-26")

    result = tm.list_tasks(due="2026-10-25")

    assert len(result) == 1
    assert result[0]["title"] == "Task A"


def test_delete_task(task_file):
    task = tm.add_task("Temporary task")

    tm.delete_task(task["id"])

    assert tm.load_tasks() == []


def test_invalid_due_date(task_file):
    with pytest.raises(ValueError):
        tm.add_task("Invalid date task", "25-10-2026")


def test_broken_json_starts_empty(task_file):
    task_file.write_text("{broken json", encoding="utf-8")

    assert tm.load_tasks() == []