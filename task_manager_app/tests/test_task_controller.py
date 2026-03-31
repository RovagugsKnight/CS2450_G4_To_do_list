import pytest
from unittest.mock import MagicMock

from src.controller.task_controller import TaskController
from src.models.task_repository import TaskRepository


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
    controller.update_task(3, "New name", "New text", "2025-01-01")
    controller.repo.update_task.assert_called_once_with(3, "New name", "New text", "2025-01-01")