import pytest
from unittest.mock import MagicMock, patch
from task_manager_app.src.views.main_window import MainWindow


class DummyButton:
    def __init__(self, *args, **kwargs):
        self._on_release = None

    def bind(self, **kwargs):
        self._on_release = kwargs.get("on_release")

    def dispatch(self, event_name):
        if event_name == "on_release" and self._on_release:
            self._on_release(self)


class DummyMenu:
    def __init__(self, caller=None, items=None, width_mult=None):
        self.caller = caller
        self.items = items or []
        self.width_mult = width_mult
        self.open = MagicMock()


def build_window():
    fake_repo = MagicMock()
    fake_catlist = MagicMock()

    fake_scrollable = MagicMock()
    fake_scrollable.todoitems = []

    with patch("task_manager_app.src.views.main_window.MDIconButton", DummyButton), \
         patch("task_manager_app.src.views.main_window.MDDropdownMenu", DummyMenu), \
         patch("task_manager_app.src.views.main_window.BoxLayout", return_value=MagicMock()), \
         patch("task_manager_app.src.views.main_window.Label", return_value=MagicMock()), \
         patch("task_manager_app.src.views.main_window.Widget", return_value=MagicMock()), \
         patch("task_manager_app.src.views.main_window.InputFrame", return_value=MagicMock()), \
         patch("task_manager_app.src.views.main_window.ScrollableList", return_value=fake_scrollable), \
         patch.object(MainWindow, "add_widget"), \
         patch.object(MainWindow, "load_existing_tasks"):

        return MainWindow(fake_repo, fake_catlist)


def test_menu_items_present():
    window = build_window()
    labels = [item["text"] for item in window.menu.items]
    assert labels == ["Create Category", "Remove Category"]


def test_menu_item_triggers_action():
    with patch.object(MainWindow, "create_category") as mock_create, \
         patch.object(MainWindow, "delete_category") as mock_delete:

        window = build_window()

        for item in window.menu.items:
            item["on_release"]()

        mock_create.assert_called_once()
        mock_delete.assert_called_once()


def test_hamburger_button_opens_menu():
    window = build_window()
    window.menu.open = MagicMock()

    window.hamburger_button.dispatch("on_release")

    window.menu.open.assert_called_once()