import pathlib
from typing import Any
from models.task_repository import TaskRepository
import sqlite3
from datetime import datetime

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DEFAULT_DATABASE_PATH = DATA_DIR / "task_manager.db"

class SqliteRepo(TaskRepository):
    """sqlite3 implementation of task repository"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path else DEFAULT_DATABASE_PATH
        
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.connection.execute('PRAGMA foreign_keys = ON') 
        self.create_table()
    
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        """Execute sql query on db"""
        result = self.connection.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self) -> None:
        """Creates category and todo tables"""
        # Create the Category table 
        category_query = """
            CREATE TABLE IF NOT EXISTS category(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT
            );
        """
        self.execute(category_query)

        todo_query = """
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
        self.execute(todo_query)



    def set_deadline(self, task_id: int, date: str):
        """Sets or updates the deadline for a specific task"""
        self.execute("UPDATE todo SET deadline = ? WHERE item_id = ?;", date, task_id)

    def update_deadline(self, task_id: int, date: str):
        """Uses the set_deadline logic to update an existing deadline"""
        self.set_deadline(task_id, date)
        
    def get_deadline(self, task_id: int) -> str | None:
        """Retrieves the deadline string for a specific task"""
        cursor = self.execute("SELECT deadline FROM todo WHERE item_id = ?;", task_id)
        row = cursor.fetchone()
        return row[0] if row else None

    def remove_deadline(self, task_id: int):
        """Removes the deadline (sets to NULL)"""
        self.execute("UPDATE todo SET deadline = NULL WHERE item_id = ?;", task_id)

    def get_overdue_tasks(self) -> list:
        """Returns tasks where the deadline is in the past and not done"""
        today = datetime.now().strftime("%Y-%m-%d")
        result = self.execute(
            "SELECT * FROM todo WHERE deadline < ? AND done = 0 AND deadline IS NOT NULL;", 
            today
        )
        return result.fetchall()


    def add_task(self, task_name:str, text:str, deadline:str = None, cat_id: int | None = None) -> int:
        result = self.execute(
            "INSERT INTO todo (item_name, item, done, deadline, category_id) VALUES (?, ?, 0, ?, ?);",
            task_name, text, deadline, cat_id
        )
        return result.lastrowid

    def delete_task(self, task_id:int) -> None:
        self.execute("DELETE FROM todo WHERE item_id = ?;", task_id)

    def mark_done(self, task_id) -> None:
        self.execute("UPDATE todo SET done = 1 WHERE item_id = ?;", task_id)

    def update_task(self, task_id:int, new_name:str, new_text:str, new_deadline:str, cat_id:int) -> None:
        self.execute(
            "UPDATE todo SET item = ?, item_name = ?, deadline = ?, category_id = ? WHERE item_id = ?;",
            new_text, new_name, new_deadline, cat_id, task_id
        )

    def get_all_tasks(self):
        result = self.execute("SELECT * FROM todo;")
        return result.fetchall()

    def close(self) -> None:
        self.connection.close()