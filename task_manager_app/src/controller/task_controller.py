from models.task_repository import TaskRepository
from models.tasks import Task
from controller.result import Result

class TaskController:
    """Accepts signals from task widget, updates 
    task info in repository, and signals back to task
    widget to update view"""
    def __init__(self, repo:TaskRepository):
        self.repo = repo

    def mark_done(self, task_id:int):
        """Mark task done in repository"""
        try:
            self.repo.mark_done(task_id)
            return Result(True)
        except Exception as e:
            return Result(False, e)
    
    def delete_task(self, task_id:int):
        """Deletes task from repository."""
        try:
            self.repo.delete_task(task_id)
            return Result(True)
        except Exception as e:
            return Result(False, e)
    
    def update_task(self, task_id:int, new_name:str, new_text:str, new_deadline:str, cat_id:int) -> Result:
        """check description length, update task name and description in repository, 
        and signals task view to change"""
        try:
            if not new_text:
                return Result(False, "Task cannot be empty.")
            if not new_name:
                return Result(False, "Name cannot be empty.")

            if len(new_text) > 150:
                return Result(False, "Task is too long. Maximum length is 150 characters.")
            if len(new_name) > 20:
                return Result(False, "Name should be 20 char or less.")
            
            if new_deadline:
                new_deadline = new_deadline.strip()
       
            self.repo.update_task(task_id, new_name, new_text, new_deadline, cat_id)
            return Result(True)
        
        except Exception as e:
            return Result(False, str(e))