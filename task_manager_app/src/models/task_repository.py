import pathlib
from .database import Database

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database file path
DATABASE_PATH = DATA_DIR / "tasks.db"


class TaskRepository:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = Database(db_path)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
                item TEXT,
                done INTEGER
            );
        """
        self.db.execute(query)

    def add_task(self, text):
        result = self.db.execute(
            "INSERT INTO todo VALUES (NULL, ?, 0);",
            text
        )
        return result.lastrowid

    def delete_task(self, task_id):
        self.db.execute(
            "DELETE FROM todo WHERE item_id = ?;",
            task_id
        )

    def mark_done(self, task_id):
        self.db.execute(
            "UPDATE todo SET done = 1 WHERE item_id = ?;",
            task_id
        )

    def get_all_tasks(self):
        result = self.db.execute(
            "SELECT item_id, item, done FROM todo;"
        )
        return result.fetchall()

    def update_task(self, task_id, new_text):
        self.db.execute(
            "UPDATE todo SET item = ? WHERE item_id = ?;",
            new_text, task_id
        )

    def close(self):
        self.db.close()