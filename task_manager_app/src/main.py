from kivymd.app import MDApp
from kivy.lang import Builder

from models.sqllite_repository import SqliteRepo
from models.sqllite_category_list import SqliteCategories

from views.main_window.main_window import MainWindow
from controller.main_window_controller import MainWindowController
from controller.task_controller import TaskController
from controller.category_controller import CategoryController


class TaskManagerApp(MDApp):
    title = "Task Manager App"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Backend
        self.repo = SqliteRepo()
        self.catlist = SqliteCategories()

        # Load dialog KV FIRST
        Builder.load_file("views/dialogs.kv")

        # Load task widget KV before main KV
        Builder.load_file("views/task_widget.kv")

        # Load main KV
        root = Builder.load_file("views/app.kv")

        # Inject backend
        main_window = root.ids.main_window
        main_window.repo = self.repo
        main_window.catlist = self.catlist

        # Controllers
        main_window.controller = MainWindowController(main_window.repo)
        main_window.task_controller = TaskController(main_window.repo)
        main_window.cat_controller = CategoryController(main_window.catlist)
        main_window.load_existing_tasks()
        main_window.update_dashboard()

        return root

    def on_stop(self):
        self.repo.close()
        self.catlist.close()


if __name__ == "__main__":
    TaskManagerApp().run()
