from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from models.sqllite_repository import SqliteRepo
from models.sqllite_category_list import SqliteCategories

from views.main_window import MainWindow   # same file, same class name


class TaskManagerApp(MDApp):
    title = "Task Manager App"

    def build(self):
        # Theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Backend
        self.repo = SqliteRepo()
        self.catlist = SqliteCategories()

        # Screen Manager
        sm = MDScreenManager()
        sm.add_widget(MainWindow(name="main", repo=self.repo, catlist=self.catlist))

        return sm

    def on_stop(self):
        self.repo.close()
        self.catlist.close()


if __name__ == "__main__":
    TaskManagerApp().run()
