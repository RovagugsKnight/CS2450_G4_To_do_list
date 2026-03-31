import os
import tempfile
import pytest
from task_manager_app.src.models.task_repository import TaskRepository


@pytest.fixture
def repo():
    # Create a temporary file to act as the SQLite DB
    db_fd, db_path = tempfile.mkstemp()

    try:
        repo = TaskRepository(db_path=db_path)
        yield repo
    finally:
        os.close(db_fd)
        os.remove(db_path)


def test_set_deadline(repo):
    repo.set_deadline(1, "2025-04-01")
    deadline = repo.get_deadline(1)
    assert deadline == "2025-04-01"


def test_update_deadline(repo):
    repo.set_deadline(1, "2025-04-01")
    repo.update_deadline(1, "2025-04-02")
    deadline = repo.get_deadline(1)
    assert deadline == "2025-04-02"


def test_remove_deadline(repo):
    repo.set_deadline(1, "2025-04-01")
    repo.remove_deadline(1)
    deadline = repo.get_deadline(1)
    assert deadline is None


def test_get_overdue_tasks(repo):
    repo.set_deadline(1, "2000-01-01")   # overdue
    repo.set_deadline(2, "2050-01-01")   # not overdue

    overdue = repo.get_overdue_tasks()

    assert 1 in overdue
    assert 2 not in overdue