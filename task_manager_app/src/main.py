from kivymd.app import MDApp
from kivy.core.window import Window
from views.main_window import MainWindow
from models.sqllite_repository import SqliteRepo
from models.sqllite_category_list import SqliteCategories
from kivymd.uix.widget import Widget
import os


class TaskManagerApp(MDApp):
    title = "Task Manager App"

    def build(self) -> MainWindow:
        """build app data and start first window
        widget"""
        self.theme_cls.theme_style = "Dark"
        self.repo = SqliteRepo()
        self.catlist = SqliteCategories()

        print("------------------------------------------")
        print(f"DATABASE PATH IS: {os.path.abspath(self.catlist.db_path)}")
        print("------------------------------------------")
        
        return MainWindow(repo = self.repo, catlist= self.catlist)
    
    def on_stop(self) -> None:
        """close sql repository"""
        self.repo.close()
        self.catlist.close()

if __name__ == "__main__":
    taskManager = TaskManagerApp()
    taskManager.run()