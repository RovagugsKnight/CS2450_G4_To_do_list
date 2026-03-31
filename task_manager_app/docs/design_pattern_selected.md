# Design Patterns
## Pattern 1:
### Factory Pattern

#### Overview
The Factory Pattern centralizes and standardizes the creation of objects. Instead of constructing objects directly throughout the codebase, a factory is responsible for producing them with consistent defaults, validation, and configuration.

#### Why It’s Useful
- Ensures all created objects follow the same rules and structure  
- Prevents duplicated initialization logic across the system  
- Makes it easier to update object creation in one place  
- Supports future extensibility (e.g., different task types or creation rules)

#### Core Pieces
- **Factory**: a dedicated component that creates objects  
- **Product**: the object being created (e.g., a Task)  
- **Client**: requests objects from the factory instead of instantiating them directly

#### Fit for This Project
The Factory Pattern ensures all tasks are created with consistent defaults (timestamps, status, priority, IDs) and validated fields. It also prepares the system for future variations of tasks without requiring changes across the entire codebase. 
### Example usage based on our code
Right now, our `Task` model stores `task_id`, `task_name`, `text`, `done`, and `deadline`. A Factory would give us one clean place to build valid `Task` objects before they are saved in the repository.

```python
from models.tasks import Task

class TaskFactory:
    """Centralizes task creation so every Task is built the same way."""

    @staticmethod
    def create_task(task_id: int, task_name: str, text: str, deadline: str = "") -> Task:
        task_name = task_name.strip()
        text = text.strip()
        deadline = deadline.strip() if deadline else ""

        if not task_name:
            raise ValueError("Name cannot be empty.")
        if not text:
            raise ValueError("Task cannot be empty.")
        if len(task_name) > 20:
            raise ValueError("Name should be 20 char or less.")
        if len(text) > 150:
            raise ValueError("Task is too long. Maximum length is 150 characters.")

        return Task(
            task_id=task_id,
            task_name=task_name,
            text=text,
            done=False,
            deadline=deadline
        )
```

Example of how it could fit into the repository layer:

```python
class SQLiteTaskRepository(TaskRepository):
    def add_task(self, task_id: int, task_name: str, text: str, deadline: str = ""):
        task = TaskFactory.create_task(task_id, task_name, text, deadline)

        # Save the created task to the database
        # INSERT INTO tasks (task_id, task_name, text, done, deadline)
        # VALUES (task.task_id, task.task_name, task.text, task.done, task.deadline)
```

This is a good fit because task creation rules are currently scattered between controllers and repositories. With a factory, the creation logic becomes reusable, easier to maintain, and easier to extend later if we add different task types.

## Pattern 2:
### Command Pattern

#### Overview
The Command Pattern separates the object that requests an action from the object that performs it. Each action is wrapped in a command object with a single `execute()` method.

#### Why It’s Useful
- Reduces coupling between UI/controllers and business logic  
- Makes actions easy to log, queue, undo, or schedule  
- Treats actions as data that can be stored or passed around  

#### Core Pieces
- **Command**: interface with `execute()`
- **Concrete Command**: holds the receiver and any needed parameters
- **Receiver**: performs the actual work
- **Invoker**: triggers the command
- **Client**: wires everything together

#### Fit for This Project
Each task operation (create, update, delete, complete) can be represented as a command. This enables undo/redo, history tracking, automation, and future scheduling features.
### Example usage based on our code
Our current `TaskController` already has action-based methods like `mark_done`, `delete_task`, and `update_task`. That makes it a natural place to apply the Command Pattern by turning each action into its own command object.

```python
from abc import ABC, abstractmethod
from controller.result import Result
from models.task_repository import TaskRepository

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class MarkDoneCommand(Command):
    def __init__(self, repo: TaskRepository, task_id: int):
        self.repo = repo
        self.task_id = task_id

    def execute(self):
        self.repo.mark_done(self.task_id)


class DeleteTaskCommand(Command):
    def __init__(self, repo: TaskRepository, task_id: int):
        self.repo = repo
        self.task_id = task_id

    def execute(self):
        self.repo.delete_task(self.task_id)


class UpdateTaskCommand(Command):
    def __init__(self, repo: TaskRepository, task_id: int, new_name: str, new_text: str, new_deadline: str):
        self.repo = repo
        self.task_id = task_id
        self.new_name = new_name
        self.new_text = new_text
        self.new_deadline = new_deadline

    def execute(self):
        if not self.new_text:
            raise ValueError("Task cannot be empty.")
        if not self.new_name:
            raise ValueError("Name cannot be empty.")
        if len(self.new_text) > 150:
            raise ValueError("Task is too long. Maximum length is 150 characters.")
        if len(self.new_name) > 20:
            raise ValueError("Name should be 20 char or less.")

        deadline = self.new_deadline.strip() if self.new_deadline else ""
        self.repo.update_task(self.task_id, self.new_name, self.new_text, deadline)
```

Then the controller can become the invoker:

```python
class TaskController:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def run_command(self, command: Command) -> Result:
        try:
            command.execute()
            return Result(True)
        except Exception as e:
            return Result(False, str(e))

    def mark_done(self, task_id: int):
        return self.run_command(MarkDoneCommand(self.repo, task_id))

    def delete_task(self, task_id: int):
        return self.run_command(DeleteTaskCommand(self.repo, task_id))

    def update_task(self, task_id: int, new_name: str, new_text: str, new_deadline: str):
        return self.run_command(UpdateTaskCommand(self.repo, task_id, new_name, new_text, new_deadline))
```

This improves the design because each task action becomes its own object. That makes the system easier to extend later with features like undo/redo, action history, macro actions, or scheduled commands.


## Pattern 3:  
### Observer Pattern

#### Overview  
The Observer pattern defines a one‑to‑many relationship between objects so that when the Subject (your data model) changes, all registered Observers (your UI components) are automatically notified. In a Python + Kivy application, this pattern keeps the View updated whenever the Model changes, without requiring manual refresh calls throughout the codebase.

#### Why It’s Useful  
The pattern ensures the UI always reflects the latest task data, removes scattered refresh logic, and keeps the Model independent of the View. It allows multiple UI components—such as task lists, counters, and filter widgets—to react to the same data changes. This fits naturally with MVC and Kivy’s event‑driven architecture, improving scalability and maintainability as the app grows.

#### Core Pieces
- **Subject (Observable)**: Holds changing data (e.g., TaskRepository). Manages observers and notifies them on updates. 
- **Observer**: Any UI element that needs to react to changes (e.g., TaskListScreen, StatsWidget). 
- **Notification Mechanism**: The Subject calls a notify method after any mutation to broadcast updates. 

#### **Fit for This Project**  
The Task Manager app frequently updates task data through operations like adding, editing, deleting, and completing tasks. Currently, the UI must be manually refreshed after each operation, which is brittle and easy to forget. Using the Observer pattern, the TaskRepository becomes the Subject, and Kivy screens or widgets become Observers. Whenever the repository changes, all observers automatically update their UI. This provides clean separation of concerns and a scalable update flow that aligns with MVC and Kivy’s architecture.
### Example usage based on our code
# --- Observer Interface ---
class Observer:
    def update(self):
        raise NotImplementedError


# --- Subject Interface ---
class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()


# --- Subject Implementation: TaskRepository ---
class TaskRepository(Subject):
    def __init__(self):
        super().__init__()
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.notify_observers()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.notify_observers()

    def toggle_complete(self, task):
        task.completed = not task.completed
        self.notify_observers()


# --- Observer Implementation: Kivy View ---
from kivy.uix.boxlayout import BoxLayout

class TaskListView(BoxLayout, Observer):
    def __init__(self, repository: TaskRepository, **kwargs):
        super().__init__(**kwargs)
        self.repository = repository
        self.repository.add_observer(self)

    def update(self):
        self.refresh_ui()

    def refresh_ui(self):
        self.clear_widgets()
        for task in self.repository.tasks:
            self.add_widget(TaskRow(task))
