from models.tasks import Task

class TaskFactory:
    """Factory class responsible for creating all Task objects"""

    @staticmethod
    def create_task(task_id, task_name, text, catid, done, deadline, task_type="Standard"):
        """
        Creates and returns a Task.
        """
        
        if task_type == "Standard":
            return Task(
                task_id=task_id, 
                task_name=task_name, 
                text=text,
                catid=catid,
                done=done, 
                deadline=deadline
            )
        
        else:
            return Task(
                task_id=task_id, task_name=task_name, text=text,
                catid=catid, done=done, deadline=deadline
            )