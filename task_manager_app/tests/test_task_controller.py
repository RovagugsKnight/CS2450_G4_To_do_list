import unittest
import tempfile
from pathlib import Path

from src.controller.task_controller import TaskController
from src.models.task_repository import TaskRepository


class TestTaskController(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test_tasks.db"

        self.controller = TaskController()
        # swap the real repo for one that uses our temp db
        self.controller.repo = TaskRepository(db_path=self.db_path)

    def tearDown(self):
        self.controller.repo.close()
        self.tmp.cleanup()

    def test_load_tasks_returns_task_objects(self):
        task_id = self.controller.add_task("Test load")
        tasks = self.controller.load_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_id, task_id)
        self.assertEqual(tasks[0].text, "Test load")
        self.assertEqual(tasks[0].done, False)

    def test_update_task_changes_text_in_db(self):
        task_id = self.controller.add_task("Old")
        self.controller.update_task(task_id, "New")

        tasks = self.controller.load_tasks()
        self.assertEqual(tasks[0].text, "New")

    def test_mark_done_sets_done_true(self):
        task_id = self.controller.add_task("Done me")
        self.controller.mark_done(task_id)

        tasks = self.controller.load_tasks()
        self.assertEqual(tasks[0].done, True)

    def test_delete_task_removes_task(self):
        task_id = self.controller.add_task("Delete me")
        self.controller.delete_task(task_id)

        tasks = self.controller.load_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
