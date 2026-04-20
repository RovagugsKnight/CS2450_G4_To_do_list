import pytest
import sqlite3
from unittest.mock import MagicMock

from controller.task_controller import TaskController


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def controller(repo):
    return TaskController(repo=repo)


def test_set_deadline_calls_repo(controller, repo):
    result = controller.set_deadline(5, "05/05/2026")
    repo.set_deadline.assert_called_once_with(5, "05/05/2026")
    assert result.success


def test_set_deadline_returns_error_on_sqlite(controller, repo):
    repo.set_deadline.side_effect = sqlite3.OperationalError("locked")
    result = controller.set_deadline(5, "05/05/2026")
    assert not result.success
    assert "locked" in result.error


def test_update_deadline_calls_repo(controller, repo):
    result = controller.update_deadline(5, "06/05/2026")
    repo.update_deadline.assert_called_once_with(5, "06/05/2026")
    assert result.success


def test_remove_deadline_calls_repo(controller, repo):
    result = controller.remove_deadline(5)
    repo.remove_deadline.assert_called_once_with(5)
    assert result.success


def test_get_overdue_tasks_calls_repo(controller, repo):
    controller.get_overdue_tasks()
    repo.get_overdue_tasks.assert_called_once()
