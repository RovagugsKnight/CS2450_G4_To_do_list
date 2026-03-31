import pytest
from models.sqllite_repository import SqliteRepo


@pytest.fixture
def db():
    repo = SqliteRepo()
    repo.execute("CREATE TABLE users(name TEXT)")
    return repo


def test_insert_data(db):
    db.execute("INSERT INTO users VALUES (?)", "Drew")
    result = db.execute("SELECT name FROM users").fetchone()
    assert result[0] == "Drew"