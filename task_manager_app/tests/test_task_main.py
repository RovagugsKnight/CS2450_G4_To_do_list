import pytest
from main import TaskManagerApp


def test_app_initialization():
    app = TaskManagerApp()
    assert app.title == "Task Manager App"