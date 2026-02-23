import unittest
import tempfile
from pathlib import Path

from task_manager_app.src.models.task_repository import TaskRepository


class TestTaskRepository(unittest.TestCase):
    def setUp(self):
        # make a temporary sqlite db file for each test
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "test_tasks.db"
        self.repo = TaskRepository(db_path=self.db_path)

    def tearDown(self):
        self.repo.close()
        self.tmp.cleanup()

    def test_add_task_returns_new_id_and_persists(self):
        task_id = self.repo.add_task("Buy milk")
        self.assertIsInstance(task_id, int)

        rows = self.repo.get_all_tasks()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], task_id)      # item_id
        self.assertEqual(rows[0][1], "Buy milk")   # item
        self.assertEqual(rows[0][2], 0)            # done

    def test_delete_task_removes_row(self):
        task_id = self.repo.add_task("Delete me")
        self.repo.delete_task(task_id)

        rows = self.repo.get_all_tasks()
        self.assertEqual(rows, [])

    def test_mark_done_sets_done_to_1(self):
        task_id = self.repo.add_task("Do homework")
        self.repo.mark_done(task_id)

        rows = self.repo.get_all_tasks()
        self.assertEqual(rows[0][0], task_id)
        self.assertEqual(rows[0][2], 1)

    def test_update_task_changes_text(self):
        task_id = self.repo.add_task("Old text")
        self.repo.update_task(task_id, "New text")

        rows = self.repo.get_all_tasks()
        self.assertEqual(rows[0][0], task_id)
        self.assertEqual(rows[0][1], "New text")

    def test_table_exists_on_init(self):
        # If create_table didn't run, simple insert would fail.
        task_id = self.repo.add_task("Table check")
        self.assertIsNotNone(task_id)

    def test_multiple_tasks(self):
        id1 = self.repo.add_task("Task A")
        id2 = self.repo.add_task("Task B")

        rows = self.repo.get_all_tasks()
        self.assertEqual(len(rows), 2)
        ids = {rows[0][0], rows[1][0]}
        self.assertEqual(ids, {id1, id2})


if __name__ == "__main__":
    unittest.main()
