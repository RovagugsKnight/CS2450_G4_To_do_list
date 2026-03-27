from models.task_repository import TaskRepository
from models.tasks import Task
from controller.result import Result

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
            done=bool(row[3])) 
            for row in rows]
        return tasks
    
    def add_task(self, taskname: str, text: str, catid: int) -> Result:
        """Checks and adds task to task repository. Signals for MainWindow view to show it."""
        text = text.strip()
        # Empty check
        if not text:
            return Result(False, "Task cannot be empty.")
        if not taskname:
            return Result(False, "Name cannot be empty.")

        # Length check
        if len(text) > 150:
            return Result(False, "Task is too long. Maximum length is 150 characters.")
        
        if len(taskname) > 20:
            return Result(False, "Name should be 20 char or less.")

        task_id = self.repo.add_task(taskname, text, catid)
        return Result(True, return_val = task_id)
    

    
