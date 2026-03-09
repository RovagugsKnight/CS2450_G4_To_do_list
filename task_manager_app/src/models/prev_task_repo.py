import pathlib
from models.database import Database

# Ensure /data folder exists
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "tasks.db"


class PrevTaskRepository:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = Database(db_path)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS todo(
                item_id INTEGER PRIMARY KEY,
                item_name TEXT,
                item TEXT,
                done INTEGER
            );
        """
        self.db.execute(query)

    def add_task(self,task_name:str, text:str):
        result = self.db.execute(
            "INSERT INTO todo VALUES (NULL, ?, ?, 0);",
            task_name, text
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

    def update_task(self, task_id, new_text):
        self.db.execute(
            "UPDATE todo SET item = ? WHERE item_id = ?;",
            new_text, task_id
        )

    def get_all_tasks(self):
        result = self.db.execute(
            "SELECT item_id, item_name, item, done FROM todo;"
        )
        return result.fetchall()

    def close(self):
        self.db.close()