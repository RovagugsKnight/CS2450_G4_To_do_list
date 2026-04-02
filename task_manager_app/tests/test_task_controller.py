import pytest
from unittest.mock import MagicMock

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

@pytest.fixture
def real_controller(tmp_path):
    # Create a real repository using a temp DB file
    db_path = tmp_path / "test.db"
    # ensure the concrete sqlite repo uses the temp DB
    _sq.DATABASE_PATH = db_path
    repo = SqliteRepo()
    return TaskController(repo)


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
    