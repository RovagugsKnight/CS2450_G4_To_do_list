import unittest
from unittest.mock import MagicMock
from task_manager_app.src.controller.task_controller import TaskController

class TestTaskControllerDeadlines(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.controller = TaskController(repo=self.repo)

    def test_set_deadline(self):
        self.controller.set_deadline(5, "2025-04-01")
        self.repo.set_deadline.assert_called_once_with(5, "2025-04-01")

    def test_update_deadline(self):
        self.controller.update_deadline(5, "2025-04-02")
        self.repo.update_deadline.assert_called_once_with(5, "2025-04-02")

    def test_remove_deadline(self):
        self.controller.remove_deadline(5)
        self.repo.remove_deadline.assert_called_once_with(5)

    def test_get_overdue_tasks(self):
        self.controller.get_overdue_tasks()
        self.repo.get_overdue_tasks.assert_called_once()

if __name__ == "__main__":
    unittest.main()
