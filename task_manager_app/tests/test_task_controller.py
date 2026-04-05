import pytest
from unittest.mock import MagicMock
import sqlite3

from src.controller.task_controller import TaskController
from src.models.task_repository import TaskRepository
from src.models.sqllite_repository import SqliteRepo
import src.models.sqllite_repository as _sq


@pytest.fixture
def controller():
    repo = MagicMock()
    controller = TaskController(repo=repo)
    return controller


def test_mark_done_calls_repo(controller):
    controller.mark_done(42)
    controller.repo.mark_done.assert_called_once_with(42)


def test_delete_task_calls_repo(controller):
    controller.delete_task(7)
    controller.repo.delete_task.assert_called_once_with(7)


def test_update_task_calls_repo(controller):
    controller.update_task(3, "New name", "New text", "01-01-2025", None)
    controller.repo.update_task.assert_called_once_with(3, "New name", "New text", "01-01-2025", None)

def test_add_task_rejects_empty_name(controller):
    result = controller.add_task(
        taskname="",
        text="optional",
        deadline=None,
        catid=None
    )
    assert not result.success
    assert result.error == "Name cannot be empty."

def test_add_task_rejects_long_text(controller):
    long_text = "x" * 200
    result = controller.add_task(
        taskname="Valid",
        text=long_text,
        deadline=None,
        catid=None
    )
    assert not result.success
    assert "too long" in result.error.lower()

def test_add_task_rejects_long_name(controller):
    long_name = "x" * 50
    result = controller.add_task(
        taskname=long_name,
        text="optional",
        deadline=None,
        catid=None
    )
    assert not result.success
    assert "20 char" in result.error

def test_update_task_rejects_empty_name(controller):
    result = controller.update_task(
        task_id=1,
        new_name="",
        new_text="optional",
        new_deadline=None,
        cat_id=None
    )
    assert not result.success

def test_update_task_rejects_long_text(controller):
    long_text = "x" * 200
    result = controller.update_task(
        task_id=1,
        new_name="Valid",
        new_text=long_text,
        new_deadline=None,
        cat_id=None
    )
    assert not result.success

def test_update_task_handles_exception(controller, monkeypatch):
    def boom(*args, **kwargs):
        raise Exception("DB error")

    monkeypatch.setattr(controller.repo, "update_task", boom)

    result = controller.update_task(
        task_id=1,
        new_name="Valid",
        new_text="optional",
        new_deadline=None,
        cat_id=None
    )

    assert not result.success
    assert "DB error" in result.error

@pytest.fixture
def real_controller(tmp_path):
    db_path = tmp_path / "test.db"

    # Create minimal category table to avoid foreign key constraint errors
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS category(
            category_id INTEGER PRIMARY KEY
        );
    """)
    conn.commit()
    conn.close()

    # Reset singleton and create repo with temp DB path
    SqliteRepo._instance = None
    repo = SqliteRepo(db_path=db_path)
    controller = TaskController(repo)

    yield controller

    # Clean up
    try:
        repo.close()
    except:
        pass



def test_integration_edit_and_delete(real_controller):
    # Create tasks directly in the repo
    t1_id = real_controller.repo.add_task("Task A", "Desc A", None, None)
    t2_id = real_controller.repo.add_task("Task B", "Desc B", None, None)

    tasks = real_controller.repo.get_all_tasks()
    assert len(tasks) == 2

    # 1. Edit first task through controller
    result = real_controller.update_task(
        t1_id,
        new_name="Task A Updated",
        new_text="Desc A Updated",
        new_deadline="2025-01-01",
        cat_id=None
    )
    assert result.success

    updated = real_controller.repo.get_all_tasks()
    t1 = next(row for row in updated if row[0] == t1_id)
    # columns: item_id, item_name, item, done, deadline, category_id
    assert t1[1] == "Task A Updated"
    assert t1[2] == "Desc A Updated"

    # 2. Delete second task through controller
    result = real_controller.delete_task(t2_id)
    assert result.success

    final_tasks = real_controller.repo.get_all_tasks()
    assert len(final_tasks) == 1
    assert final_tasks[0][0] == t1_id

def test_integration_add_and_mark_done(real_controller):
    # 1. Add a task through the controller
    result = real_controller.add_task(
        taskname="Test Task",
        text="Some description",
        deadline=None,
        catid=None
    )
    assert result.success

    task_id = result.return_val  # <-- correct field

    # 2. Verify it was added
    tasks = real_controller.repo.get_all_tasks()
    assert len(tasks) == 1

    row = tasks[0]
    # SQLite schema: (item_id, item_name, item, done, deadline, category_id)
    assert row[0] == task_id
    assert row[1] == "Test Task"
    assert row[2] == "Some description"
    assert row[3] == 0  # not done yet

    # 3. Mark the task done
    result = real_controller.mark_done(task_id)
    assert result.success

    # 4. Verify it is now marked done
    updated = real_controller.repo.get_all_tasks()
    row = updated[0]
    assert row[3] == 1  # done column should now be 1
