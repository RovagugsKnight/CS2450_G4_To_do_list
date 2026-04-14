import pathlib
from typing import Any
from models.task_repository import TaskRepository
import sqlite3

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DEFAULT_DATABASE_PATH = DATA_DIR / "task_manager.db"

class SqliteRepo(TaskRepository):
    """sqlite3 implementation of task repository"""
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SqliteRepo, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path=None):
        if not hasattr(self, '_initialized'):
            self.db_path = db_path if db_path else DEFAULT_DATABASE_PATH
            
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.connection.execute('PRAGMA foreign_keys = ON') 
            self.create_table()
            self._initialized = True
    
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        """Execute sql query on db"""
        result = self.connection.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self) -> None:
        """Creates task repository db table"""
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                item TEXT,
                done INTEGER,
                deadline TEXT,
                category_id INTEGER,
                FOREIGN KEY(category_id) REFERENCES category(category_id)
                ON DELETE SET NULL
            );
        """
        self.execute(query)

    def add_task(self, task_name:str, text:str, deadline:str, cat_id: int | None = None) -> int:
        """adds task to database and returns task id"""
        result = self.execute(
            "INSERT INTO todo (item_name, item, done, deadline, category_id) VALUES (?, ?, 0, ?, ?);",
            task_name, text, deadline, cat_id
        )
        return result.lastrowid

    def delete_task(self, task_id:int) -> None:
        self.execute("DELETE FROM todo WHERE item_id = ?;", task_id)

    def mark_done(self, task_id) -> None:
        self.execute("UPDATE todo SET done = 1 WHERE item_id = ?;", task_id)
    
    def mark_undone(self, task_id: int) -> None:
        self.execute("UPDATE todo SET done = 0 WHERE item_id = ?;", task_id)

    def update_task(self, task_id:int, new_name:str, new_text:str, new_deadline:str, cat_id:int) -> None:
        """updates task info for task with task id"""
        self.execute(
            "UPDATE todo SET item = ?, item_name = ?, deadline = ?, category_id = ? WHERE item_id = ?;",
            new_text, new_name, new_deadline, cat_id, task_id
        )

    def get_all_tasks(self):
        result = self.execute("SELECT * FROM todo;")
        return result.fetchall()

    def set_deadline(self, task_id: int, date: str) -> None:
        self.execute("UPDATE todo SET deadline = ? WHERE item_id = ?;", date, task_id)

    def update_deadline(self, task_id: int, date: str) -> None:
        self.execute("UPDATE todo SET deadline = ? WHERE item_id = ?;", date, task_id)

    def remove_deadline(self, task_id: int) -> None:
        self.execute("UPDATE todo SET deadline = NULL WHERE item_id = ?;", task_id)

    def get_deadline(self, task_id: int):
        """Returns the deadline for a specific task"""
        result = self.execute("SELECT deadline FROM todo WHERE item_id = ?;", task_id)
        row = result.fetchone()
        if row:
            return row[0]
        return None

    def get_overdue_tasks(self):
        """Returns all tasks where the deadline is in the past and they are not done."""
        result = self.execute(
            "SELECT * FROM todo WHERE deadline < date('now', 'localtime') AND deadline IS NOT NULL AND deadline != '' AND done = 0;"
        )
        return result.fetchall()
    
    def reassign_tasks_from_category(self, cat_id: int) -> None:
        self.execute(
        "UPDATE todo SET category_id = NULL WHERE category_id = ?;",
        cat_id
        )

    def close(self) -> None:
        self.connection.close()