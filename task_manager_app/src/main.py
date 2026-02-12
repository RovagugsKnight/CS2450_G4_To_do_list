from kivy.app import App
from kivy.core.window import Window
from views.main_window import MainWindow

class TaskManagerApp(App):
    title = "Task Manager App"

    def build(self):
        return MainWindow()
    
if __name__ == "__main__":
    taskManager = TaskManagerApp()
    taskManager.run()
