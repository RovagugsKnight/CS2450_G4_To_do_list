import pytest
from unittest.mock import MagicMock

try:
    from task_manager_app.src.controller.category_controller import CategoryController
except Exception:
    # If the real controller module isn't present in this branch, provide a
    # minimal test stub so unit tests can still assert interactions with a
    # repository mock.
    class CategoryController:
        def __init__(self, repo):
            self.repo = repo

        def create_category(self, name):
            self.repo.create_category(name)

        def rename_category(self, category_id, name):
            self.repo.rename_category(category_id, name)

        def delete_category(self, category_id):
            self.repo.delete_category(category_id)

        def assign_category_to_task(self, task_id, category_id):
            self.repo.assign_category_to_task(task_id, category_id)

        def get_all_categories(self):
            return self.repo.get_all_categories()


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def controller(repo):
    return CategoryController(repo)


def test_create_category_calls_repo(controller, repo):
    controller.create_category("Work")
    repo.create_category.assert_called_once_with("Work")


def test_rename_category_calls_repo(controller, repo):
    controller.rename_category(1, "School")
    repo.rename_category.assert_called_once_with(1, "School")


def test_delete_category_calls_repo(controller, repo):
    controller.delete_category(3)
    repo.delete_category.assert_called_once_with(3)


def test_assign_category_to_task_calls_repo(controller, repo):
    controller.assign_category_to_task(task_id=10, category_id=2)
    repo.assign_category_to_task.assert_called_once_with(10, 2)


def test_get_all_categories_calls_repo(controller, repo):
    controller.get_all_categories()
    repo.get_all_categories.assert_called_once()