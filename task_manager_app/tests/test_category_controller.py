import unittest
from unittest.mock import MagicMock
from task_manager_app.src.controller.category_controller import CategoryController

class TestCategoryController(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.controller = CategoryController(self.repo)

    def test_create_category_calls_repo(self):
        self.controller.create_category("Work")
        self.repo.create_category.assert_called_once_with("Work")

    def test_rename_category_calls_repo(self):
        self.controller.rename_category(1, "School")
        self.repo.rename_category.assert_called_once_with(1, "School")

    def test_delete_category_calls_repo(self):
        self.controller.delete_category(3)
        self.repo.delete_category.assert_called_once_with(3)

    def test_assign_category_to_task_calls_repo(self):
        self.controller.assign_category_to_task(task_id=10, category_id=2)
        self.repo.assign_category_to_task.assert_called_once_with(10, 2)

    def test_get_all_categories_calls_repo(self):
        self.controller.get_all_categories()
        self.repo.get_all_categories.assert_called_once()

if __name__ == "__main__":
    unittest.main()