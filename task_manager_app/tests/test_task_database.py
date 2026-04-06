import pytest
import tempfile
import sqlite3
from pathlib import Path


@pytest.fixture
def db():
    """Create a temporary in-memory database for testing"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(name TEXT)")
    conn.commit()
    yield conn
    conn.close()


def test_insert_data(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users VALUES (?)", ("Drew",))
    db.commit()
    result = cursor.execute("SELECT name FROM users").fetchone()
    assert result[0] == "Drew"