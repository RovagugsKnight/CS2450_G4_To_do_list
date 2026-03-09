import pathlib
from models.task_repository import TaskRepository
import sqlite3

# Ensure /data folder exists
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "tasks.db"

class SqliteRepo(TaskRepository):
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def execute(self, query, *args):
        result = self.cursor.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
                item_name TEXT,
                item TEXT,
                done INTEGER
            );
        """
        self.execute(query)

    def add_task(self,task_name:str, text:str):
        result = self.execute(
            "INSERT INTO todo VALUES (NULL, ?, ?, 0);",
            task_name, text
        )
        return result.lastrowid

    def delete_task(self, task_id):
        self.execute(
            "DELETE FROM todo WHERE item_id = ?;",
            task_id
        )

    def mark_done(self, task_id):
        self.execute(
            "UPDATE todo SET done = 1 WHERE item_id = ?;",
            task_id
        )

    def update_task(self, task_id, new_text):
        self.execute(
            "UPDATE todo SET item = ? WHERE item_id = ?;",
            new_text, task_id
        )

    def get_all_tasks(self):
        result = self.execute(
            "SELECT item_id, item_name, item, done FROM todo;"
        )
        return result.fetchall()

    def close(self):
        self.connection.close()