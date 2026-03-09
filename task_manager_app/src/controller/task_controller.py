from models.prev_task_repo import PrevTaskRepository
from models.tasks import Task


class TaskController:
    def __init__(self):
        self.repo = PrevTaskRepository()

    def mark_done(self, task_id):
        self.repo.mark_done(task_id)
    
    def update_task(self, task_id, new_text):
        self.repo.update_task(task_id, new_text)