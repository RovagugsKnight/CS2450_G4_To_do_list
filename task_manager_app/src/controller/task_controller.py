from models.task_repository import TaskRepository
from models.tasks import Task


class TaskController:
    def __init__(self):
        self.repo = TaskRepository()

    def load_tasks(self):
        rows = self.repo.get_all_tasks()
        return [Task(task_id=row[0], task_name=row[1], text=row[2], done=bool(row[3])) for row in rows]

    def add_task(self,task_name, text):
        return self.repo.add_task(task_name, text)

    def delete_task(self, task_id):
        self.repo.delete_task(task_id)

    def mark_done(self, task_id):
        self.repo.mark_done(task_id)
    
    def update_task(self, task_id, new_text):
        self.repo.update_task(task_id, new_text)