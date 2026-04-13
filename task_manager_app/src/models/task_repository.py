from abc import ABC, abstractmethod
from typing import Any


class TaskRepository(ABC):
    """Abstract base class for task storage backends."""

    @abstractmethod
    def add_task(self, task_name: str, text: str, deadline: str, cat_id: int | None = None) -> int:
        """Add a task to the repository and return its id."""
        pass

    @abstractmethod
    def update_task(
        self,
        task_id: int,
        new_name: str,
        new_text: str,
        new_deadline: str,
        cat_id: int | None = None,
    ) -> None:
        """Update task fields in the repository."""
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> None:
        pass

    @abstractmethod
    def mark_done(self, task_id: int) -> None:
        pass

    # NOTE: no abstract load_tasks here – we leave it to the concrete repo

    @abstractmethod
    def set_deadline(self, task_id: int, date: str) -> None:
        """Set a deadline for a specific task."""
        pass

    @abstractmethod
    def get_deadline(self, task_id: int) -> Any:
        """Retrieve the deadline for a specific task."""
        pass

    @abstractmethod
    def update_deadline(self, task_id: int, date: str) -> None:
        pass

    @abstractmethod
    def remove_deadline(self, task_id: int) -> None:
        pass

    @abstractmethod
    def get_overdue_tasks(self):
        pass
    
    @abstractmethod
    def reassign_tasks_from_category(self, cat_id: int) -> None:
        """Reassign all tasks belonging to a deleted category."""
        pass