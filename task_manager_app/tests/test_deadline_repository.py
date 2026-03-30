import os
import tempfile
import unittest
from task_manager_app.src.models.task_repository import TaskRepository

class TestTaskRepositoryDeadlines(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.repo = TaskRepository(db_path=self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)

    def test_set_deadline(self):
        self.repo.set_deadline(1, "2025-04-01")
        deadline = self.repo.get_deadline(1)
        self.assertEqual(deadline, "2025-04-01")

    def test_update_deadline(self):
        self.repo.set_deadline(1, "2025-04-01")
        self.repo.update_deadline(1, "2025-04-02")
        deadline = self.repo.get_deadline(1)
        self.assertEqual(deadline, "2025-04-02")

    def test_remove_deadline(self):
        self.repo.set_deadline(1, "2025-04-01")
        self.repo.remove_deadline(1)
        deadline = self.repo.get_deadline(1)
        self.assertIsNone(deadline)

    def test_get_overdue_tasks(self):
        self.repo.set_deadline(1, "2000-01-01")
        self.repo.set_deadline(2, "2050-01-01")
        overdue = self.repo.get_overdue_tasks()
        self.assertIn(1, overdue)
        self.assertNotIn(2, overdue)

if __name__ == "__main__":
    unittest.main()
