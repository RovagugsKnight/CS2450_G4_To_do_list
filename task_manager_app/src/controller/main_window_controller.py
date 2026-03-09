from models.task_repository import TaskRepository
from models.tasks import Task


class main_window_controller:
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
            done=bool(row[3])) 
            for row in rows]
        return tasks
    
    def add_task(self):
        """Adds task to task repository and signals for MainWindow view to show it"""
        pass
