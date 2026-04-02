from models.task_repository import TaskRepository
from models.tasks import Task
from controller.result import Result
from controller.category_controller import CategoryController

class MainWindowController:
    """controller class to link main window view to data"""
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def load_tasks(self) -> list[Task]:
        """Loads tasks from task repository and sends them to MainWindow view"""
        rows = self.repo.get_all_tasks()
        tasks = [Task(
            task_id=row[0], 
            task_name=row[1], 
            text=row[2],
            catid= row[5],
            done=bool(row[3]), 
            deadline=row[4]
        ) for row in rows]
        return tasks
    

    
