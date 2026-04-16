Our project achieved **83% test coverage**, exceeding the milestone requirement of ~70%.
This reflects strong testing of core logic, controllers, and database interactions.

Below is the screenshot of the coverage summary
<img width="579" height="666" alt="Screenshot 2026-04-06 120639" src="https://github.com/user-attachments/assets/8cbec280-ea22-48e0-9d30-069b603afe41" />

## Coverage Summary (Text Version)

## Coverage Summary (Text Version)

| File | Stmts | Miss | Cover |
|------|-------|-------|--------|
| controller/category_controller.py | 37 | 3 | 92% |
| controller/main_window_controller.py | 14 | 2 | 86% |
| controller/result.py | 6 | 0 | 100% |
| controller/task_controller.py | 59 | 7 | 88% |
| main.py | 20 | 4 | 80% |
| models/category.py | 13 | 2 | 85% |
| models/category_list.py | 15 | 4 | 73% |
| models/sqllite_category_list.py | 41 | 0 | 100% |
| models/sqllite_repository.py | 57 | 1 | 98% |
| models/task_repository.py | 31 | 10 | 68% |
| models/tasks.py | 8 | 6 | 25% |
| views/buttons.py | 20 | 2 | 90% |
| views/category_button.py | 27 | 10 | 63% |
| views/category_creator.py | 26 | 13 | 50% |
| views/category_selector.py | 45 | 13 | 71% |
| views/color_button.py | 20 | 9 | 55% |
| views/color_selector.py | 21 | 10 | 52% |
| views/colors.py | 6 | 1 | 83% |
| views/grid_layout.py | 8 | 0 | 100% |
| views/inputs.py | 57 | 30 | 47% |
| views/main_window.py | 128 | 7 | 95% |
| views/scrollable_list.py | 25 | 12 | 52% |
| views/spacer.py | 6 | 0 | 100% |
| views/task_widget.py | 100 | 74 | 26% |
| tests/conftest.py | 39 | 16 | 59% |
| tests/test_category_controller.py | 73 | 0 | 100% |
| tests/test_category_database.py | 87 | 3 | 97% |
| tests/test_deadline_controller.py | 30 | 1 | 97% |
| tests/test_deadline_repository.py | 41 | 0 | 100% |
| tests/test_hamburger_menu.py | 40 | 0 | 100% |
| tests/test_main_window.py | 119 | 1 | 99% |
| tests/test_task_controller.py | 96 | 2 | 98% |
| tests/test_task_database.py | 18 | 0 | 100% |
| tests/test_task_main.py | 15 | 0 | 100% |
| tests/test_task_repository.py | 56 | 0 | 100% |
| **TOTAL** | **1404** | **243** | **83%** |

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
