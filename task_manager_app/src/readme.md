# Task Manager App (Kivy + MVC)

A task management application built with Python and Kivy, structured using the MVC architecture for clarity, maintainability, and group collaboration. This project is inspired by the PythonGuis Kivy tutorial but expanded with custom UI components and a clean, scalable file layout.

## Features

- Add and display tasks
- Scrollable task list
- Custom-styled buttons and inputs
- Organized MVC architecture
- Easy to extend (categories, priorities, due dates, etc.)
- Edit Tasks and Save to `tasks.db`

## Project Structure

project/
│
├── main.py
│
├── models/
│   ├── database.py
│   ├── task.py
│   └── task_repository.py
│
├── controllers/
│   └── task_controller.py
│
├── views/
│   ├── main_window.py
│   ├── task_widget.py
│   ├── scrollable_list.py
│   ├── inputs.py
│   ├── base_buttons.py
│   ├── buttons.py
│   └── colors.py
│
└── data/
    └── tasks.db

## Dependencies

- Python 3.12
- Kivy (latest stable)
- KivyMD
- Virtual environment recommended
- pytest

Create Venv:

- Windows: py -3.12 -m venv venv (or py -3.12 -m venv venv.nosync to prevent onedrive syncing)
- Mac: python3.12 -m venv venv

Activate venv:

- Windows: venv\Scripts\activate.bat or venv.nosync\Scripts\activate.bat
- Mac: source venv/bin/activate

Open a new terminal and you should see (venv)

Install Kivy:

pip install kivy

Install KivyMD:

pip install kivymd2

Run the application:

python main.py

Install pytest:

pip install pytest

Run the tests:

cd task_manager_app/tests
pytest -v

## Contributors

- Nathan
- Forrest
- Andy
- Drew


- This project follows the MVC pattern for maintainability.
- UI components are separated into individual files for clean OOP structure.
- The database file (`tasks.db`) is created automatically on first run.
- Future improvements may include:
  - Overdue task highlighting
  - Categories or tags
  - Animations and transitions
  - Persistent settings
