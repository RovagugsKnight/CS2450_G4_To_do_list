"""
Nav menu content: verify ``build_nav_menu`` wires the expected items and MDDropdownMenu.
"""
from unittest.mock import MagicMock, patch

import pytest

from views.main_window.menu_view import build_nav_menu


@pytest.fixture
def menu_self():
    """Minimal ``MainWindow`` stand-in with handlers referenced by menu items."""
    m = MagicMock()
    m.open_view_submenu = MagicMock()
    m.open_manage_categories_submenu = MagicMock()
    m.toggle_theme = MagicMock()
    return m


def test_build_nav_menu_contains_expected_entries(menu_self):
    captured = {}

    class CaptureMenu:
        def __init__(self, caller, items, *, submenu=False, **kwargs):
            captured["caller"] = caller
            captured["items"] = items
            captured["submenu"] = submenu
            captured.update(kwargs)

    app = MagicMock()
    app.theme_cls.theme_style = "Light"
    app.root = MagicMock()
    app.root.ids.nav_button = MagicMock()

    with patch("views.main_window.menu_view.App.get_running_app", return_value=app), \
         patch("views.main_window.menu_view.make_nav_dropdown", CaptureMenu):
        build_nav_menu(menu_self)

    items = captured["items"]
    labels = [i["text"] for i in items if isinstance(i, dict) and "text" in i]
    assert "Switch View  >" in labels
    assert "Manage Categories  >" in labels
    assert any(t in ("Dark Mode", "Light Mode") for t in labels)


def test_nav_menu_item_callbacks_invoke_handlers(menu_self):
    built = {}

    class CaptureMenu:
        def __init__(self, caller, items, *, submenu=False, **kwargs):
            built["kwargs"] = {
                "caller": caller,
                "items": items,
                "submenu": submenu,
                **kwargs,
            }

    app = MagicMock()
    app.theme_cls.theme_style = "Dark"
    app.root = MagicMock()
    app.root.ids.nav_button = MagicMock()

    with patch("views.main_window.menu_view.App.get_running_app", return_value=app), \
         patch("views.main_window.menu_view.make_nav_dropdown", CaptureMenu):
        build_nav_menu(menu_self)

    for item in built["kwargs"]["items"]:
        if not isinstance(item, dict) or "on_release" not in item:
            continue
        if item["text"] == "Switch View  >":
            item["on_release"]()
            menu_self.open_view_submenu.assert_called()
        elif item["text"] == "Manage Categories  >":
            item["on_release"]()
            menu_self.open_manage_categories_submenu.assert_called()
        elif item["text"] in ("Dark Mode", "Light Mode"):
            item["on_release"]()
            menu_self.toggle_theme.assert_called()
