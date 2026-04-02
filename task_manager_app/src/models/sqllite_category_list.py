import sqlite3
import pathlib
from typing import Any
from models.category_list import CategoryList
from models.category import Category

# Ensure /data folder exists
DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "task_manager.db"

class SqliteCategories(CategoryList):
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.create_table()
    
    def execute(self, query:str, *args:Any) -> sqlite3.Cursor:
        """Execute and commit sql query on db"""
        result = self.cursor.execute(query, args)
        self.connection.commit()
        return result

    def create_table(self) -> None:
        """Creates category db table"""
        query = """
            CREATE TABLE IF NOT EXISTS category(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT,
                color TEXT
            );
        """
        self.execute(query)
        
    def load_categories(self) -> tuple[Any]:
        """ returns all categories from db"""
        result = self.execute(
            "SELECT category_id, category_name, color FROM category;"
        )
        return result.fetchall()
    
    def add_category(self, category: Category) -> int:
        """add a category to db"""
        result = self.execute(
            "INSERT INTO category VALUES (NULL, ?, ? );",
            category.name, category.color
        )
        id = result.lastrowid
        return Category(id, category.name, category.color)
    
    def delete_category(self, cat_id: int) -> None:
        """delete a category from db"""
        self.execute(
            "DELETE FROM category WHERE category_id = ?",
            cat_id
        )
    
    def edit_category(self, category: Category) -> None:
        """edit a category from db"""
        self.execute(
            "Update category SET category_name = ?, color = ? WHERE category_id = ?",
            category.name, category.color, category.id
        )
    
    def grab_category(self, id:int) -> tuple[Any]:
        """return category with given id"""
        result = self.execute(
            "SELECT * FROM category WHERE category_id = ?",
            id
        )
        return result.fetchall()

    def close(self) -> None:
        """close connection to db"""
        self.connection.close()