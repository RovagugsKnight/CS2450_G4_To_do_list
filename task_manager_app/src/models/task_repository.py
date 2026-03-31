from abc import ABC, abstractmethod

class TaskRepository(ABC):
    """Repository for tasks that can store, delete, modify, and grab task objects"""
        
    @abstractmethod
    def add_task(self, task_name: str, text: str):
        """Add task to repository"""
        pass
    
    @abstractmethod
    def delete_task(self, task_id: int):
        """delete task from repository"""
        pass

    @abstractmethod
    def mark_done(self, task_id: int):
        """mark task done in repository"""
        pass
    
    @abstractmethod
    def update_task(self, task_id: int, new_text: str):
        """update text in repository"""
        pass

    @abstractmethod
    def get_all_tasks(self):
        """grab all tasks from repository"""
        pass
