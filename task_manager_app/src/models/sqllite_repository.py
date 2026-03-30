import pathlib
from typing import Any
from models.task_repository import TaskRepository
import sqlite3


DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "task_manager.db"

class SqliteRepo(TaskRepository):
    """sqlite3 implementation of task repository"""
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.connection.execute('PRAGMA foreign_keys = ON') #enable foreign keys
        self.fk_status = self.connection.execute('PRAGMA foreign_keys').fetchall() #check foreign key activation
        self.fk_errors = self.connection.execute('PRAGMA foreign_key_check').fetchall() #See foreign key errors
        self.create_table()
    
    def execute(self, query:str, *args:Any) -> sqlite3.Cursor:
        """Execute sql query on db"""
        result = self.cursor.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self) -> None:
        """Creates task repository db table"""
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
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
        """deletes task with task id"""
        self.execute(
            "DELETE FROM todo WHERE item_id = ?;",
            task_id
        )

    def mark_done(self, task_id) -> None:
        """sets done to true for task with task id"""
        self.execute(
            "UPDATE todo SET done = 1 WHERE item_id = ?;",
            task_id
        )

    def update_task(self, task_id:int, new_name:str, new_text:str, new_deadline:str, cat_id:int) -> None:
        """updates task info for task with task id"""
        self.execute(
            "UPDATE todo SET item = ?, item_name = ?, deadline = ?, category_id = ? WHERE item_id = ?;",
            new_text, new_name, new_deadline, cat_id, task_id
        )

    def get_all_tasks(self) -> list[tuple[int, str, str, int, int, str]]:
        """ returns all tasks from db"""
        result = self.execute(
            "SELECT item_id, item_name, item, done, deadline, category_id FROM todo;"
        )
        return result.fetchall()

    def close(self) -> None:
        """close connection to db"""
        self.connection.close()