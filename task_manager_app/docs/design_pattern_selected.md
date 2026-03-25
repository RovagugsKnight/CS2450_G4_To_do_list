Identify at least 3 design patterns that could address specific issues in your codebase or new features (e.g., handling varying behaviors, managing single instances, adapting interfaces).

For each, evaluate: What problem does it solve? Is it necessary, or would a basic implementation work? Avoid forcing patterns—document alternatives considered.

Draft initial implementations or pseudocode, ensuring compatibility with MVC (e.g., patterns in Controller or Model) and SOLID.
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
