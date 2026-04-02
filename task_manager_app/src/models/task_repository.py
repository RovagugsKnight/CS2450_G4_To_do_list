from abc import ABC, abstractmethod

class TaskRepository(ABC):
    """Repository for tasks that can store, delete, modify, and grab task objects"""
    
    def __init__(self, db_path=None):
        """Allows an optional database path for testing purposes"""
        self.db_path = db_path

    @abstractmethod
    def add_task(self, task_name: str, text: str):
        pass
    
    @abstractmethod
    def delete_task(self, task_id: int):
        pass

    @abstractmethod
    def mark_done(self, task_id: int):
        pass
    
    @abstractmethod
    def update_task(self, task_id: int, new_name: str, new_text: str, new_deadline: str, cat_id: int):
        """Update task details"""
        pass

    @abstractmethod
    def get_all_tasks(self):
        pass


    @abstractmethod
    def set_deadline(self, task_id: int, date: str):
        """Set a deadline for a specific task"""
        pass

    @abstractmethod
    def get_deadline(self, task_id: int):
        """Retrieve the deadline for a specific task"""
        pass

    @abstractmethod
    def remove_deadline(self, task_id: int):
        """Remove a deadline from a task"""
        pass

    @abstractmethod
    def get_overdue_tasks(self):
        """Retrieve all tasks where the deadline has passed"""
        pass