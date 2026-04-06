import pytest
from unittest.mock import MagicMock, patch
from kivy.base import EventLoop
from kivy.uix.widget import Widget

from task_manager_app.src.views.main_window import MainWindow
from task_manager_app.src.models.task_repository import TaskRepository
from task_manager_app.src.models.category_list import CategoryList
from task_manager_app.src.models.category import Category


@pytest.fixture
def setup_window():
    """Creates a MainWindow with mocked controllers and initializes MDApp."""
    EventLoop.ensure_window()

    # Initialize dummy MDApp
    from kivymd.app import MDApp

    class TestApp(MDApp):
        def build(self):
            return Widget()

    if not MDApp.get_running_app():
        app = TestApp()
        app.root = Widget()

    repo = MagicMock(spec=TaskRepository)
    catlist = MagicMock(spec=CategoryList)

    window = MainWindow(repo, catlist)

    window.controller = MagicMock()
    window.task_controller = MagicMock()
    window.cat_controller = MagicMock()

    return window


# -----------------------------
# load_existing_tasks()
# -----------------------------
def test_load_existing_tasks(setup_window):
    window = setup_window

    task1 = MagicMock(task_id=1, task_name="A", text="t1", catid=None, done=False, deadline="")
    task2 = MagicMock(task_id=2, task_name="B", text="t2", catid=10, done=True, deadline="2025-01-01")

    window.controller.load_tasks.return_value = [task1, task2]

    fake_cat = Category(10, "School", "white")
    window.cat_controller.get_category.return_value.return_val = fake_cat

    # Mock TaskItem so no real widget is created - create NEW Widget instance each time
    with patch("task_manager_app.src.views.main_window.TaskItem") as MockTaskItem:
        MockTaskItem.side_effect = lambda *args, **kwargs: Widget()
        window.load_existing_tasks()

    # Assert TaskItem was created twice
    assert MockTaskItem.call_count == 2


# -----------------------------
# add_todo_item()
# -----------------------------
def test_add_todo_item_success(setup_window):
    window = setup_window

    result = MagicMock(success=True, return_val=99)
    window.controller.add_task.return_value = result

    cat = Category(5, "Work", "soft teal")

    with patch("task_manager_app.src.views.main_window.TaskItem") as MockTaskItem:
        MockTaskItem.return_value = Widget()
        window.add_todo_item("Task", "Desc", "2025-01-01", cat)

    window.controller.add_task.assert_called_once_with("Task", "Desc", "2025-01-01", 5)
    assert window.inputframe.ids.task_name.text == ""


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

    fake_selector = Widget()
    fake_selector.get_selected_category = MagicMock(return_value=Category(3, "Home", "light blue"))

    # Create button that captures the binding callback
    button = Widget()
    button.bind = MagicMock(side_effect=lambda **kwargs: None)

    # Mock dependencies to return Widget instances
    with patch("task_manager_app.src.views.main_window.CategorySelector", return_value=fake_selector):
        with patch("task_manager_app.src.views.main_window.YellowButton", return_value=button):
            with patch("task_manager_app.src.views.main_window.Popup"):
                with patch.object(window, "delete_cat_option") as delete_call:
                    window.delete_category()
                    
                    # Get the FIRST callback that was bound to the button (the decide_binding one)
                    assert button.bind.called
                    first_call_kwargs = button.bind.call_args_list[0][1]
                    if 'on_release' in first_call_kwargs:
                        first_call_kwargs['on_release'](button)
                    
                    delete_call.assert_called_once_with(3)


# -----------------------------
# delete_cat_option()
# -----------------------------
def test_delete_cat_option_success(setup_window):
    window = setup_window

    window.cat_controller.delete_category.return_value = True

    with patch.object(window.inputframe, "delete_category") as del_cat:
        with patch.object(window.scrollablelist, "disable_task_category") as disable:
            window.delete_cat_option(7)

            del_cat.assert_called_once_with(7)
            disable.assert_called_once_with(7)


def test_delete_cat_option_failure(setup_window):
    window = setup_window

    result = MagicMock(error="Nope")
    result.__bool__ = MagicMock(return_value=False)
    window.cat_controller.delete_category.return_value = result

    with patch.object(window, "show_popup") as popup:
        window.delete_cat_option(7)
        popup.assert_called_once_with("Nope")


# -----------------------------
# create_category()
# -----------------------------
def test_create_category_opens_popup(setup_window):
    window = setup_window

    with patch("task_manager_app.src.views.main_window.CategoryCreator") as creator:
        creator.return_value = Widget()

        with patch("task_manager_app.src.views.main_window.Popup"):
            window.create_category()

        creator.assert_called_once()


# -----------------------------
# add_cat_option()
# -----------------------------
def test_add_cat_option_success(setup_window):
    window = setup_window

    fake_cat = Category(1, "Work", "white")
    result = MagicMock(success=True, return_val=fake_cat)
    window.cat_controller.add_category.return_value = result

    with patch.object(window, "make_cat_widget") as mk:
        window.add_cat_option("Work", "white")
        mk.assert_called_once_with(fake_cat)


def test_add_cat_option_failure(setup_window):
    window = setup_window

    result = MagicMock(success=False, error="Duplicate")
    window.cat_controller.add_category.return_value = result

    with patch.object(window, "show_popup") as popup:
        window.add_cat_option("Work", "light blue")
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
