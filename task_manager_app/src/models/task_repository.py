import sqlite3
import pathlib

# Ensure /data folder exists relative to the project root
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database file path
DATABASE_PATH = DATA_DIR / "tasks.db"

class TaskRepository:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
                item TEXT,
                done INTEGER
            );
        """
        self._run_query(query)

    def _run_query(self, query, *query_args):
        result = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return result

    def add_task(self, text):
        result = self._run_query(
            "INSERT INTO todo VALUES (NULL, ?, 0);",
            text
        )
        return result.lastrowid

    def delete_task(self, task_id):
        self._run_query(
            "DELETE FROM todo WHERE item_id = ?;",
            task_id
        )

    def mark_done(self, task_id):
        self._run_query(
            "UPDATE todo SET done = 1 WHERE item_id = ?;",
            task_id
        )

    def get_all_tasks(self):
        result = self._run_query(
            "SELECT item_id, item, done FROM todo;"
        )
        return result.fetchall()
    
    def update_task(self, task_id, new_text):
        self._run_query(
            "UPDATE todo SET item = ? WHERE item_id = ?;",
            new_text, task_id
        )

    def close(self):
        self.db.close()