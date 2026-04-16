from unittest.mock import MagicMock, patch

from main import TaskManagerApp


def test_app_initialization():
    app = TaskManagerApp()
    assert app.title == "Task Manager App"


def test_build_wires_repo_and_catlist_into_main_window():
    """``build`` loads KV, injects backends into ``main_window``, and returns the root."""
    fake_repo = MagicMock()
    fake_catlist = MagicMock()
    fake_catlist.load_categories = MagicMock(
        return_value=[
            (1, "Todo", "teal"),
            (2, "Done", "gray"),
        ]
    )

    fake_main = MagicMock()
    fake_root = MagicMock()
    fake_root.ids.main_window = fake_main

    def load_file(path: str):
        if path == "views/app.kv":
            return fake_root
        return MagicMock()

    app = TaskManagerApp()
    app.theme_cls = MagicMock()

    with patch("main.SqliteRepo", return_value=fake_repo), \
         patch("main.SqliteCategories", return_value=fake_catlist), \
         patch("main.Builder.load_file", side_effect=load_file), \
         patch("main.load_theme_style", return_value="Light"):

        result = app.build()

    assert result is fake_root
    assert fake_main.repo is fake_repo
    assert fake_main.catlist is fake_catlist
