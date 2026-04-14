import sqlite3
import pathlib
from typing import Any
from models.category_list import CategoryList
from models.category import Category

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "task_manager.db"


class SqliteCategories(CategoryList):
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.create_table()
    
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        result = self.cursor.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS category(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT,
                color TEXT
            );
        """
        self.execute(query)
        
    def load_categories(self) -> tuple[Any]:
        result = self.execute(
            "SELECT * FROM category;"
        )
        return result.fetchall()
    
    def add_category(self, category: Category) -> int:
        result = self.execute(
            "INSERT INTO category VALUES (NULL, ?, ?);",
            category.name, category.color
        )
        id = result.lastrowid
        category.id = id
        return category
    
    def delete_category(self, cat_id: int) -> None:
        result = self.execute(
            "DELETE FROM category WHERE category_id = ?",
            cat_id
        )
        if result.rowcount == 0:
            raise ValueError("Category not in DataBase")
    
    def grab_category(self, id: int) -> tuple[Any]:
        result = self.execute(
            "SELECT * FROM category WHERE category_id = ?",
            id
        )
        row = result.fetchone()
        if row is None:
            raise ValueError("Category not in DataBase")
        return row

    def update_category(self, cat_id: int, new_name: str, new_color: str) -> Category:
        result = self.execute(
            "UPDATE category SET category_name = ?, color = ? WHERE category_id = ?;",
            new_name, new_color, cat_id
        )

        if result.rowcount == 0:
            raise ValueError("Category not in DataBase")

        return Category(id=cat_id, name=new_name, color=new_color)

    def close(self) -> None:
        self.connection.close()
