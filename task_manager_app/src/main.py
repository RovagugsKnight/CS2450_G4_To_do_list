from kivymd.app import MDApp
from kivy.core.window import Window
from views.main_window import MainWindow
from models.sqllite_repository import SqliteRepo

class TaskManagerApp(MDApp):
    title = "Task Manager App"

    def build(self) -> None:
        """build app data and start first window
        widget"""
        self.theme_cls.theme_style = "Dark"
        self.repo = SqliteRepo()
        return MainWindow(repo = self.repo)
    
    def on_stop(self) -> None:
        """close sql repository"""
        self.repo.close()

if __name__ == "__main__":
    taskManager = TaskManagerApp()
    taskManager.run()
