from unittest.mock import MagicMock, patch
from main import TaskManagerApp


def test_app_initialization():
    app = TaskManagerApp()
    assert app.title == "Task Manager App"


def test_build_creates_main_window_with_repo_and_catlist():
    fake_repo = MagicMock()
    fake_catlist = MagicMock()
    fake_window = MagicMock()

    app = TaskManagerApp()
    app.theme_cls = MagicMock()

    with patch("main.SqliteRepo", return_value=fake_repo), \
         patch("main.SqliteCategories", return_value=fake_catlist), \
         patch("main.MainWindow", return_value=fake_window) as mock_window:

        result = app.build()

    assert result is fake_window
    mock_window.assert_called_once_with(repo=fake_repo, catlist=fake_catlist)