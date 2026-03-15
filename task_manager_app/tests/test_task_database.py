import unittest
from src.models.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.execute("CREATE TABLE users(name TEXT)")
    def test_insert_data(self):
        self.db.execute("INSERT INTO users VALUES (?)", "Drew")
        result = self.db.execute("SELECT name FROM users").fetchone()
        self.assertEqual(result[0], "Drew")