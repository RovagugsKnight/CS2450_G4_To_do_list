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
    controller.set_deadline(5, "2025-04-01")
    repo.set_deadline.assert_called_once_with(5, "2025-04-01")


def test_update_deadline_calls_repo(controller, repo):
    controller.update_deadline(5, "2025-04-02")
    repo.update_deadline.assert_called_once_with(5, "2025-04-02")


def test_remove_deadline_calls_repo(controller, repo):
    controller.remove_deadline(5)
    repo.remove_deadline.assert_called_once_with(5)


def test_get_overdue_tasks_calls_repo(controller, repo):
    controller.get_overdue_tasks()
    repo.get_overdue_tasks.assert_called_once()