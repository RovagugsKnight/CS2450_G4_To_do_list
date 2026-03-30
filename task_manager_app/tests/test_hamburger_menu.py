import unittest
from unittest.mock import MagicMock

from task_manager_app.src.views.main_window import MainWindow


class TestHamburgerMenu(unittest.TestCase):
    def setUp(self):
        self.fake_repo = MagicMock()
        self.window = MainWindow(self.fake_repo)

    def test_menu_items_present(self):
        labels = [item["text"] for item in self.window.menu.items]
        self.assertEqual(
            labels,
            ["Create Category", "Edit Category", "Remove Category"]
        )

    def test_menu_item_triggers_action(self):
        triggered = []
        self.window.menu_click = lambda text: triggered.append(text)

        for item in self.window.menu.items:
            item["on_release"]()

        self.assertEqual(
            triggered,
            ["Create Category", "Edit Category", "Remove Category"]
        )

    def test_hamburger_button_opens_menu(self):
        self.window.menu.open = MagicMock()
        self.window.hamburger_button.dispatch("on_release")
        self.window.menu.open.assert_called_once()
    
if __name__ == "__main__":
    unittest.main()