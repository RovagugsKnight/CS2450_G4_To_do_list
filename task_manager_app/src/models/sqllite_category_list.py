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
        self._enforce_system_positions()
    
    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        result = self.cursor.execute(query, args)
        if not query.lstrip().upper().startswith("SELECT"):
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
        self._ensure_next_pointer_column()

    def _ensure_next_pointer_column(self) -> None:
        cols = self.execute("PRAGMA table_info(category);").fetchall()
        col_names = {row[1] for row in cols}
        if "next_category_id" not in col_names:
            self.execute("ALTER TABLE category ADD COLUMN next_category_id INTEGER;")

    def _rows_for_ordering(self) -> list[tuple[int, str, int | None]]:
        return self.execute(
            "SELECT category_id, category_name, next_category_id FROM category;"
        ).fetchall()

    def _ordered_ids(self) -> list[int]:
        rows = self._rows_for_ordering()
        if not rows:
            return []

        ids = [row[0] for row in rows]
        next_by_id = {row[0]: row[2] for row in rows}
        inbound = {row[2] for row in rows if row[2] is not None}

        heads = [cid for cid in ids if cid not in inbound]
        start = heads[0] if heads else ids[0]

        ordered = []
        seen = set()
        cur = start
        while cur is not None and cur not in seen and cur in next_by_id:
            ordered.append(cur)
            seen.add(cur)
            cur = next_by_id[cur]

        # Recover from broken/cyclic pointer states.
        if len(ordered) < len(ids):
            for cid in sorted(ids):
                if cid not in seen:
                    ordered.append(cid)
                    seen.add(cid)
        return ordered

    def _write_order(self, ordered_ids: list[int]) -> None:
        for idx, cid in enumerate(ordered_ids):
            next_id = ordered_ids[idx + 1] if idx + 1 < len(ordered_ids) else None
            self.execute(
                "UPDATE category SET next_category_id = ? WHERE category_id = ?;",
                next_id,
                cid,
            )

    def _enforce_system_positions(self) -> None:
        rows = self.execute(
            "SELECT category_id, category_name FROM category;"
        ).fetchall()
        if not rows:
            return

        name_by_id = {row[0]: row[1].lower() for row in rows}
        todo_id = next((cid for cid, name in name_by_id.items() if name == "todo"), None)
        done_id = next((cid for cid, name in name_by_id.items() if name == "done"), None)

        ordered = self._ordered_ids()
        ordered = [cid for cid in ordered if cid in name_by_id]

        if todo_id in ordered:
            ordered.remove(todo_id)
            ordered.insert(0, todo_id)
        if done_id in ordered:
            ordered.remove(done_id)
            ordered.append(done_id)
        self._write_order(ordered)
        
    def load_categories(self) -> tuple[Any]:
        rows = self.execute(
            "SELECT category_id, category_name, color, next_category_id FROM category;"
        ).fetchall()
        if not rows:
            return []

        color_by_id = {row[0]: row[2] for row in rows}
        name_by_id = {row[0]: row[1] for row in rows}
        ordered_ids = self._ordered_ids()
        return [(cid, name_by_id[cid], color_by_id[cid]) for cid in ordered_ids]
    
    def add_category(self, category: Category) -> int:
        result = self.execute(
            "INSERT INTO category (category_name, color, next_category_id) VALUES (?, ?, NULL);",
            category.name,
            category.color,
        )
        id = result.lastrowid
        category.id = id
        self._enforce_system_positions()
        return category
    
    def delete_category(self, cat_id: int) -> None:
        ordered = self._ordered_ids()
        result = self.execute(
            "DELETE FROM category WHERE category_id = ?",
            cat_id
        )
        if result.rowcount == 0:
            raise ValueError("Category not in DataBase")
        if cat_id in ordered:
            ordered.remove(cat_id)
            self._write_order(ordered)
            self._enforce_system_positions()
    
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

    def move_category_up(self, category_id: int) -> None:
        ordered = self._ordered_ids()
        rows = self.execute("SELECT category_id, category_name FROM category;").fetchall()
        name_by_id = {row[0]: row[1].lower() for row in rows}
        todo_id = next((cid for cid, n in name_by_id.items() if n == "todo"), None)
        done_id = next((cid for cid, n in name_by_id.items() if n == "done"), None)

        if category_id in (todo_id, done_id):
            return
        if category_id not in ordered:
            raise ValueError("Category not in DataBase")

        idx = ordered.index(category_id)
        if idx <= 1:  # keep Todo fixed at the front
            return
        ordered[idx - 1], ordered[idx] = ordered[idx], ordered[idx - 1]
        self._write_order(ordered)
        self._enforce_system_positions()

    def move_category_down(self, category_id: int) -> None:
        ordered = self._ordered_ids()
        rows = self.execute("SELECT category_id, category_name FROM category;").fetchall()
        name_by_id = {row[0]: row[1].lower() for row in rows}
        todo_id = next((cid for cid, n in name_by_id.items() if n == "todo"), None)
        done_id = next((cid for cid, n in name_by_id.items() if n == "done"), None)

        if category_id in (todo_id, done_id):
            return
        if category_id not in ordered:
            raise ValueError("Category not in DataBase")

        idx = ordered.index(category_id)
        done_idx = ordered.index(done_id) if done_id in ordered else len(ordered) - 1
        if idx >= done_idx - 1:  # keep Done fixed at the end
            return
        ordered[idx + 1], ordered[idx] = ordered[idx], ordered[idx + 1]
        self._write_order(ordered)
        self._enforce_system_positions()

    def close(self) -> None:
        self.connection.close()
