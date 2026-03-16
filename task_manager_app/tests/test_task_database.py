import unittest
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))
from models.sqllite_repository import SqliteRepo


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = SqliteRepo()
        self.db.execute("CREATE TABLE users(name TEXT)")
    def test_insert_data(self):
        self.db.execute("INSERT INTO users VALUES (?)", "Drew")
        result = self.db.execute("SELECT name FROM users").fetchone()
        self.assertEqual(result[0], "Drew")


if __name__ == "__main__":
    unittest.main()