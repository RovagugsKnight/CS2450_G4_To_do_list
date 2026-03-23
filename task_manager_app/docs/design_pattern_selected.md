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
### 


### Example usage based on our code

