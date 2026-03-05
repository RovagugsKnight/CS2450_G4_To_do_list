from kivymd.app import MDApp
from kivy.core.window import Window
from controller.main_window import MainWindow

class TaskManagerApp(MDApp):
    title = "Task Manager App"


    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MainWindow()

if __name__ == "__main__":
    taskManager = TaskManagerApp()
    taskManager.run()
