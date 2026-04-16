# Code Smell Fix Log

## 2026-04-15

### Fixed

- Replaced broad exception swallowing in dashboard/task list date parsing with explicit helper parsing in:
  - `task_manager_app/src/views/main_window/dashboard_view.py`
  - `task_manager_app/src/views/main_window/kanban_view.py`
- Reduced Kanban rendering complexity by pre-grouping tasks once per refresh instead of scanning all tasks per category in:
  - `task_manager_app/src/views/main_window/kanban_view.py`
- Removed duplicated `TaskItem` class from dialog module and reused the canonical widget class from:
  - `task_manager_app/src/views/task_widget.py`
  - updated imports/usages in `task_manager_app/src/views/main_window/task_dialogs.py`
- Centralized repeated UI refresh calls into `MainWindow.refresh_ui()` to reduce duplication and drift risk:
  - `task_manager_app/src/views/main_window/main_window.py`
  - `task_manager_app/src/views/main_window/task_dialogs.py`
  - `task_manager_app/src/views/task_widget.py`
- Normalized task color assignment to use RGBA tuple consistently for `TaskItem.color`:
  - `task_manager_app/src/views/task_widget.py`
  - `task_manager_app/src/views/main_window/task_dialogs.py`
- Removed `None` category fallback at the view level by defaulting missing category display/state to `Todo` and enforcing `Todo` on edit-save when no category is selected:
  - `task_manager_app/src/views/task_widget.py`
  - `task_manager_app/src/views/main_window/task_dialogs.py`
- Fixed backend overdue-date smell by evaluating overdue tasks using the app's `MM/DD/YYYY` deadline format (instead of SQL lexical date compare):
  - `task_manager_app/src/models/sqllite_repository.py`
- Updated backend category deletion reassignment to move tasks into `Todo` instead of `NULL`:
  - `task_manager_app/src/models/sqllite_repository.py`
- Updated sqlite execute helpers to commit only for write queries (not `SELECT`), improving transaction hygiene:
  - `task_manager_app/src/models/sqllite_repository.py`
  - `task_manager_app/src/models/sqllite_category_list.py`
- Standardized controller error payloads to always return string messages in `Result` and removed unused controller imports:
  - `task_manager_app/src/controller/task_controller.py`
  - `task_manager_app/src/controller/main_window_controller.py`

### Remaining Smells / Follow-up Candidates

- `MainWindow` still has many responsibilities (menu construction, popup orchestration, category edit/delete flow, nav submenu anchor). Consider moving category flow and/or hamburger/cascade menu wiring into a dedicated UI helper or coordinator.
- `menu_view.py`, `submenu_view.py`, and related `MainWindow` menu code duplicate **dark/light menu colors** (`menu_text`, `menu_bg`) and identical **`MDDropdownMenu`** kwargs (`width_mult=4`, `radius`, `elevation`). Extract a small `nav_menu_styles()` / `build_dropdown_menu(...)` helper.
- **Cascade positioning** uses unexplained **magic numbers** (`0.94`, `dp(73)`, `dp(24)`, `dp(240)` fallback width, anchor size). Name these as module constants with a one-line comment (e.g. tied to default `dp(48)` row height + separators).
- **`dismiss_all_menus`** uses bare `except Exception: pass` around `dismiss()`, which can hide real bugs. Prefer checking `callable(getattr(menu, "dismiss", None))` or catching a narrower Kivy exception type where safe.
- **`load_existing_tasks()`** still catches broad `Exception`; narrow once repository errors are standardized.
- **`TaskController`** still catches broad `Exception` in several methods; prefer `sqlite3.Error` (and domain types) once wired through the repository.
- **`task_manager_app/tests/test_hamburger_menu.py`** appears **stale** (expects `Create Category` / `Remove Category` flat items and patches old symbols). Update or remove so CI reflects the current nav + cascade structure.
- **`SqliteRepo` singleton** (`__new__` pattern) complicates **test isolation**; tests may share one DB instance unless carefully reset.
- **`DeadlineSelector`** contains multiple broad `except Exception` blocks; tighten or document why each must be broad.
- **Double `Clock.schedule_once(..., 0)`** in cascade flow (`submenu_view` + `_reopen_nav_menu_if_dismissed`) is **timing-sensitive** and hard to unit test; acceptable for KivyMD, but a short comment in code near the schedulers would help future readers.

---

## 2026-04-15 (full pass after menu / cascade changes)

### Summary

Recent nav submenu work is functionally fine but adds **UI complexity** and **duplication** in the menu modules. Backend patterns are largely unchanged: broad `except` in controllers and some views remain the main structural smell.

### Strengths (unchanged or improved)

- **Clear layering** in many places: view functions delegate to `MainWindow`, controllers validate + `Result`, repository handles SQL.
- **`CategoryController.add_category`** narrows exceptions to `ValueError` (good contrast with `TaskController`).
- **`Result`** usage is consistent enough for UI error display; commit-on-non-SELECT in sqlite helpers is clean.

### Priority follow-ups (suggested order)

1. **Deduplicate** nav menu styling and `MDDropdownMenu` constructor args between `menu_view.py`, `submenu_view.py`, and any shared theme tuples in `MainWindow`.
2. **Constants + comment** for cascade anchor math in `nav_submenu_anchor_caller` / `_nav_submenu_anchor_fallback_xy`.
3. **Repair or delete** `test_hamburger_menu.py` so automated tests match the real menu.
4. **Narrow exceptions** in `TaskController` and `load_existing_tasks` when you introduce typed repository errors or `sqlite3.Error`.
5. **Optional:** extract a `NavMenuController` (or plain module) owning `build_nav_menu`, submenu openers, anchor widget, and `dismiss_all_menus` to shrink `MainWindow`.

---

## 2026-04-15 (smell cleanup pass)

### Fixed

- Centralized nav dropdown styling and ``MDDropdownMenu`` construction in `task_manager_app/src/views/main_window/nav_menu_helpers.py` (theme tuples, shared kwargs, cascade layout constants with comments). `menu_view.py` and `submenu_view.py` use `make_nav_dropdown` / `nav_menu_item_style`.
- Replaced magic numbers in `MainWindow` cascade anchoring with imports from `nav_menu_helpers`.
- `dismiss_all_menus` now calls ``dismiss()`` only when callable (no silent bare ``except``).
- Narrowed ``except`` clauses: `load_existing_tasks` (sqlite + row/shape issues), `dashboard_view.update_dashboard`, `TaskController` repo calls (`sqlite3.Error`), `deadline_selector` bind/format paths (typed exceptions); left user-callback errors in `_on_save` as logged ``Exception`` by design.
- Added `SqliteRepo.reset_singleton_for_tests()`; tests use it instead of assigning ``_instance = None`` by hand.
- Rewrote `tests/test_hamburger_menu.py` to assert current nav labels and handlers (patches ``make_nav_dropdown`` to avoid requiring a running Kivy window).

### Remaining (optional)

- `MainWindow` could still shrink further by extracting nav anchor + menu dismissal into a small coordinator class.
- `DeadlineSelector.open()` outer ``except Exception`` (after MDDatePicker init) left broad where any KivyMD failure should surface in logs; can narrow further per deployed KivyMD version.
