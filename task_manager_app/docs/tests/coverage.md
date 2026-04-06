Our project achieved **83% test coverage**, exceeding the milestone requirement of ~70%.
This reflects strong testing of core logic, controllers, and database interactions.

Below is the screenshot of the coverage summary
<img width="579" height="666" alt="Screenshot 2026-04-06 120639" src="https://github.com/user-attachments/assets/8cbec280-ea22-48e0-9d30-069b603afe41" />

## Coverage Summary (Text Version)

| File | Coverage | Notes |
|------|----------|--------|
| `category_controller.py` | 92% | Well-tested logic, only minor branches untested |
| `sqllite_category_list.py` | 100% | Fully covered due to deterministic behavior |
| `sqllite_repository.py` | 98% | Only one error-handling branch untested |
| `main_window.py` | 95% | High coverage despite UI mocking |
| **Total** | **83%** | Above milestone target |

---

## Well‑Tested Areas

### **1. Controllers**
The controllers (`category_controller.py`, `task_controller.py`) are heavily tested because they contain pure logic and interact with mocked repositories. These modules are deterministic and easy to isolate, resulting in high coverage.

### **2. Database Models**
Both SQLite-backed model classes (`sqllite_repository.py`, `sqllite_category_list.py`) reached near‑complete coverage. Their behavior is predictable and does not depend on UI components, making them ideal for unit testing.

### **3. MainWindow Logic**
Even though the UI is mocked, the underlying logic in `main_window.py`—such as task creation, category deletion, and controller interactions—is thoroughly tested. This ensures the core behavior of the app is validated without relying on Kivy’s rendering engine.

---

## Areas Needing Improvement

### **1. UI Components (Views)**
Files under `views/` such as:

- `task_widget.py`
- `inputs.py`
- `scrollable_list.py`
- `category_creator.py`
- `category_selector.py`

are **not directly tested**.  
This is intentional: Kivy widgets are difficult to instantiate in a headless test environment, and attempting to do so caused instability. We resolved this by **mocking all UI components**, which stabilizes the suite but prevents these files from contributing to coverage.

### **2. Popup and Layout Logic**
Popup creation, widget layout, and KivyMD menu behavior are mocked out. These areas would require full integration tests with a running event loop, which are outside the scope of this milestone.

---

## Key Findings From the Testing Process

1. **Mocking the UI was essential for stability.**  
   Directly instantiating Kivy/KivyMD widgets caused crashes, event‑loop issues, and nondeterministic behavior. Mocking these components allowed us to test logic without relying on the rendering engine.

2. **Logic-heavy modules naturally achieve high coverage.**  
   Controllers and database layers reached 90–100% coverage because they are deterministic and easy to isolate.

3. **Coverage depends on where pytest is run.**  
   Running tests inside `/tests` produced artificially low coverage (only test files). Running from the project root produced the correct 83%.

4. **UI code does not appear in coverage due to mocking.**  
   This is expected for Kivy applications and does not indicate missing logic tests.

---

## How to Reproduce the Coverage Report

From the project root (`task_manager_app/`):

```bash
pytest --cov=task_manager_app/src --cov-report=html
