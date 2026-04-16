"""Unit tests for ``MainWindow`` orchestration (no full Kivy app run)."""
from unittest.mock import MagicMock, patch

import pytest
import sqlite3

from models.category import Category
from controller.result import Result
from views.main_window.main_window import MainWindow


def test_load_existing_tasks_populates_from_controller():
    window = MainWindow.__new__(MainWindow)
    window.controller = MagicMock()
    window.controller.load_tasks.return_value = []
    with patch("views.main_window.main_window.populate_task_lists") as pop:
        MainWindow.load_existing_tasks(window)
    window.controller.load_tasks.assert_called_once()
    pop.assert_called_once_with(window, [])


def test_load_existing_tasks_show_error_on_db_failure():
    window = MainWindow.__new__(MainWindow)
    window.controller = MagicMock()
    window.controller.load_tasks.side_effect = sqlite3.OperationalError("no such table")
    with patch.object(MainWindow, "show_error") as err:
        MainWindow.load_existing_tasks(window)
    err.assert_called_once()


def test_delete_category_skips_system_categories():
    window = MainWindow.__new__(MainWindow)
    window.task_controller = MagicMock()
    window.cat_controller = MagicMock()
    window.refresh_ui = MagicMock()

    MainWindow.delete_category(window, Category(1, "Todo", "teal"))
    window.task_controller.reassign_tasks_from_category.assert_not_called()

    MainWindow.delete_category(window, Category(2, "Done", "gray"))
    window.task_controller.reassign_tasks_from_category.assert_not_called()


def test_delete_category_deletes_user_category():
    window = MainWindow.__new__(MainWindow)
    window.task_controller = MagicMock()
    window.cat_controller = MagicMock()
    window.cat_controller.delete_category.return_value = Result(True)
    window.refresh_ui = MagicMock()

    cat = Category(9, "Work", "blue")
    MainWindow.delete_category(window, cat)

    window.task_controller.reassign_tasks_from_category.assert_called_once_with(9)
    window.cat_controller.delete_category.assert_called_once_with(9)
    window.refresh_ui.assert_called_once_with(
        reload_categories=True,
        refresh_category_popup=True,
    )
