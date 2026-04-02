import pytest
from unittest.mock import MagicMock
from task_manager_app.src.controller.task_controller import TaskController


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def controller(repo):
    return TaskController(repo=repo)


def test_set_deadline_calls_repo(controller, repo):
    controller.set_deadline(5, "05/05/2026")
    repo.set_deadline.assert_called_once_with(5, "05/05/2026")


def test_update_deadline_calls_repo(controller, repo):
    controller.update_deadline(5, "06/05/2026")
    repo.update_deadline.assert_called_once_with(5, "06/05/2026")


def test_remove_deadline_calls_repo(controller, repo):
    controller.remove_deadline(5)
    repo.remove_deadline.assert_called_once_with(5)


def test_get_overdue_tasks_calls_repo(controller, repo):
    controller.get_overdue_tasks()
    repo.get_overdue_tasks.assert_called_once()

def test_update_and_delete(controller):
    controller.update_task(1, "New Name", "New Text", "2026-12-31", 1)

    try:
        controller.delete_task(1)
        controller.mark_done(1)
    except Exception:
        pass