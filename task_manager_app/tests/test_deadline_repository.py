import os
import tempfile
import pytest
from task_manager_app.src.models.sqllite_repository import SqliteRepo


@pytest.fixture
def repo():
    SqliteRepo._instance = None
    # Create a temporary file to act as the SQLite DB
    db_fd, db_path = tempfile.mkstemp()

    try:
        repo = SqliteRepo(db_path=db_path) 
        repo.execute("CREATE TABLE category (category_id INTEGER PRIMARY KEY);")
        
        yield repo
    finally:
        repo.close() 
        os.close(db_fd)
        os.remove(db_path)


def test_set_deadline(repo):
    repo.add_task("Task 1", "Description", "") 
    
    repo.set_deadline(1, "2026-04-30")
    deadline = repo.get_deadline(1)
    assert deadline == "2026-04-30"


def test_update_deadline(repo):
    repo.add_task("Task 1", "Description", "")
    
    repo.set_deadline(1, "2026-04-30")
    repo.update_deadline(1, "2026-05-05")
    deadline = repo.get_deadline(1)
    assert deadline == "2026-05-05"


def test_remove_deadline(repo):
    repo.add_task("Task 1", "Description", "")
    
    repo.set_deadline(1, "2026-05-05")
    repo.remove_deadline(1)
    deadline = repo.get_deadline(1)
    assert deadline is None


def test_get_overdue_tasks(repo):
    # Seed two tasks for IDs 1 and 2
    repo.add_task("Overdue Task", "Desc", "") # ID 1
    repo.add_task("Future Task", "Desc", "")  # ID 2
    
    # Use YYYY-MM-DD for reliable SQL comparisons
    repo.set_deadline(1, "2020-01-01")    
    repo.set_deadline(2, "2050-01-01")   

    overdue_rows = repo.get_overdue_tasks()
    
    # Extract IDs from the list of tuples returned by SQLite
    overdue_ids = [row[0] for row in overdue_rows]

    assert 1 in overdue_ids
    assert 2 not in overdue_ids