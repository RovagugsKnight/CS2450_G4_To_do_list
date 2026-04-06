import pytest
from unittest.mock import MagicMock, patch
from kivy.base import EventLoop

from views.main_window import MainWindow
from models.task_repository import TaskRepository
from models.category_list import CategoryList
from models.category import Category


@pytest.fixture
def setup_window():
    """Creates a MainWindow with mocked controllers and repo."""
    EventLoop.ensure_window()

    repo = MagicMock(spec=TaskRepository)
    catlist = MagicMock(spec=CategoryList)

    window = MainWindow(repo, catlist)

    # Patch controllers so we can control behavior
    window.controller = MagicMock()
    window.task_controller = MagicMock()
    window.cat_controller = MagicMock()

    return window


# -----------------------------
# load_existing_tasks()
# -----------------------------
def test_load_existing_tasks(setup_window):
    window = setup_window

    # Fake tasks returned by controller
    task1 = MagicMock(task_id=1, task_name="A", text="t1", catid=None, done=False, deadline=None)
    task2 = MagicMock(task_id=2, task_name="B", text="t2", catid=10, done=True, deadline="2025-01-01")

    window.controller.load_tasks.return_value = [task1, task2]

    # Fake category lookup
    fake_cat = Category(10, "School", "#FF0000")
    window.cat_controller.get_category.return_value.return_val = fake_cat

    window.load_existing_tasks()

    assert len(window.todoitems.children) == 2
    window.controller.load_tasks.assert_called_once()
    window.cat_controller.get_category.assert_called_once_with(10)


# -----------------------------
# add_todo_item()
# -----------------------------
def test_add_todo_item_success(setup_window):
    window = setup_window

    # Fake successful result
    result = MagicMock(success=True, return_val=99)
    window.controller.add_task.return_value = result

    cat = Category(5, "Work", "#00FF00")

    window.add_todo_item("Task", "Desc", "2025-01-01", cat)

    window.controller.add_task.assert_called_once_with("Task", "Desc", "2025-01-01", 5)
    assert window.inputframe.ids.task_name.text == ""
    assert window.inputframe.ids.description.text == ""
    assert window.inputframe.ids.deadline.text == ""


def test_add_todo_item_failure(setup_window):
    window = setup_window

    result = MagicMock(success=False, error="Bad input")
    window.controller.add_task.return_value = result

    with patch.object(window, "show_popup") as popup:
        window.add_todo_item("X", "Y", "Z", None)
        popup.assert_called_once_with("Bad input")


# -----------------------------
# delete_category()
# -----------------------------
def test_delete_category_triggers_delete(setup_window):
    window = setup_window

    fake_selector = MagicMock()
    fake_selector.get_selected_category.return_value = Category(3, "Home", "#123456")

    with patch("views.main_window.CategorySelector", return_value=fake_selector):
        with patch.object(window, "delete_cat_option") as delete_call:
            window.delete_category()
            # The popup is created; actual delete happens on button press
            fake_selector.get_selected_category.assert_called()


# -----------------------------
# delete_cat_option()
# -----------------------------
def test_delete_cat_option_success(setup_window):
    window = setup_window

    window.cat_controller.delete_category.return_value = True

    with patch.object(window, "delete_cat_widget") as del_widget:
        with patch.object(window.scrollablelist, "disable_task_category") as disable:
            window.delete_cat_option(7)

            del_widget.assert_called_once_with(7)
            disable.assert_called_once_with(7)


def test_delete_cat_option_failure(setup_window):
    window = setup_window

    result = MagicMock(success=False, error="Nope")
    window.cat_controller.delete_category.return_value = result

    with patch.object(window, "show_popup") as popup:
        window.delete_cat_option(7)
        popup.assert_called_once_with("Nope")


# -----------------------------
# create_category()
# -----------------------------
def test_create_category_opens_popup(setup_window):
    window = setup_window

    with patch("views.main_window.CategoryCreator") as creator:
        creator.return_value = MagicMock()
        window.create_category()
        creator.assert_called_once()


# -----------------------------
# add_cat_option()
# -----------------------------
def test_add_cat_option_success(setup_window):
    window = setup_window

    fake_cat = Category(1, "Work", "#ABCDEF")
    result = MagicMock(success=True, return_val=fake_cat)
    window.cat_controller.add_category.return_value = result

    with patch.object(window, "make_cat_widget") as mk:
        window.add_cat_option("Work", "#ABCDEF")
        mk.assert_called_once_with(fake_cat)


def test_add_cat_option_failure(setup_window):
    window = setup_window

    result = MagicMock(success=False, error="Duplicate")
    window.cat_controller.add_category.return_value = result

    with patch.object(window, "show_popup") as popup:
        window.add_cat_option("Work", "#ABCDEF")
        popup.assert_called_once_with("Duplicate")


# -----------------------------
# remove_task_widget()
# -----------------------------
def test_remove_task_widget(setup_window):
    window = setup_window

    with patch.object(window.scrollablelist, "remove_item") as rm:
        window.remove_task_widget(42)
        rm.assert_called_once_with(42)


# -----------------------------
# menu_click()
# -----------------------------
def test_menu_click(setup_window, capsys):
    window = setup_window

    with patch.object(window.menu, "dismiss") as dis:
        window.menu_click("Create Category")

        dis.assert_called_once()
        captured = capsys.readouterr()
        assert "Hamburger Menu Clicked: Create Category" in captured.out
