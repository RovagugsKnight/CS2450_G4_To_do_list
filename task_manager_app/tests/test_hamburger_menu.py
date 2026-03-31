import pytest
from unittest.mock import MagicMock
from task_manager_app.src.views.main_window import MainWindow


@pytest.fixture
def window():
    fake_repo = MagicMock()
    return MainWindow(fake_repo)


def test_menu_items_present(window):
    labels = [item["text"] for item in window.menu.items]
    assert labels == ["Create Category", "Edit Category", "Remove Category"]


def test_menu_item_triggers_action(window):
    triggered = []
    window.menu_click = lambda text: triggered.append(text)

    for item in window.menu.items:
        item["on_release"]()

    assert triggered == ["Create Category", "Edit Category", "Remove Category"]


def test_hamburger_button_opens_menu(window):
    window.menu.open = MagicMock()
    window.hamburger_button.dispatch("on_release")
    window.menu.open.assert_called_once()