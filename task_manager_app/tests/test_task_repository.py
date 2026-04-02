import tempfile
from pathlib import Path

import pytest

# Use the concrete sqlite repo implementation and point its DATABASE_PATH to
# a temp file so each test runs against an isolated DB.
from task_manager_app.src.models import sqllite_repository as _sq
from task_manager_app.src.models.sqllite_repository import SqliteRepo


@pytest.fixture
def repo():
    tmp = tempfile.TemporaryDirectory()
    db_path = Path(tmp.name) / "test_tasks.db"

    # override module-level DATABASE_PATH used by SqliteRepo
    _sq.DATABASE_PATH = db_path

    repo = SqliteRepo()
    yield repo
    try:
        repo.close()
    finally:
        tmp.cleanup()


def test_add_task_returns_new_id_and_persists(repo):
    task_id = repo.add_task("Buy milk", "Buy milk", "")
    assert isinstance(task_id, int)

    rows = repo.get_all_tasks()
    assert len(rows) == 1
    assert rows[0][0] == task_id
    assert rows[0][1] == "Buy milk"
    # columns: item_id, item_name, item, done, deadline
    assert rows[0][3] == 0


def test_delete_task_removes_row(repo):
    task_id = repo.add_task("Delete me", "Delete me", "")
    repo.delete_task(task_id)

    rows = repo.get_all_tasks()
    assert rows == []


def test_mark_done_sets_done_to_1(repo):
    task_id = repo.add_task("Do homework", "Do homework", "")
    repo.mark_done(task_id)

    rows = repo.get_all_tasks()
    assert rows[0][0] == task_id
    assert rows[0][3] == 1


def test_update_task_changes_text(repo):
    task_id = repo.add_task("Old text", "Old text", "")
    repo.update_task(task_id, "New name", "New text", "")

    rows = repo.get_all_tasks()
    assert rows[0][0] == task_id
    # item_name should be updated to the new name, item should be the new text
    assert rows[0][1] == "New name"
    assert rows[0][2] == "New text"


def test_table_exists_on_init(repo):
    task_id = repo.add_task("Table check", "Table check", "")
    assert task_id is not None


def test_multiple_tasks(repo):
    id1 = repo.add_task("Task A", "Task A", "")
    id2 = repo.add_task("Task B", "Task B", "")

    rows = repo.get_all_tasks()
    assert len(rows) == 2
    ids = {rows[0][0], rows[1][0]}
    assert ids == {id1, id2}