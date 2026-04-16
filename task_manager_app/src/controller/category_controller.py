from models.category import Category
from models.category_list import CategoryList
from controller.result import Result

DEFAULT_CATEGORY_NAME = "Todo"
DONE_CATEGORY_NAME = "Done"
DEFAULT_CATEGORY_COLOR = "teal"
DONE_CATEGORY_COLOR = "gray"


class CategoryController:

    def __init__(self, catlist: CategoryList):
        self.catlist = catlist
        self._ensure_system_categories()

    """
    SYSTEM CATEGORY SETUP
    """

    def _ensure_system_categories(self):
        """Ensure Todo and Done categories exist in the DB."""
        existing = {row[1].lower(): row for row in self.catlist.load_categories()}

        if DEFAULT_CATEGORY_NAME.lower() not in existing:
            self.catlist.add_category(
                Category(None, DEFAULT_CATEGORY_NAME, DEFAULT_CATEGORY_COLOR)
            )

        if DONE_CATEGORY_NAME.lower() not in existing:
            self.catlist.add_category(
                Category(None, DONE_CATEGORY_NAME, DONE_CATEGORY_COLOR)
            )

    def _is_system_category(self, name: str) -> bool:
        return name.lower() in (DEFAULT_CATEGORY_NAME.lower(), DONE_CATEGORY_NAME.lower())

    """
    LOAD
    """

    def load_categories(self) -> list[Category]:
        """Create all category objects from category data returned in list."""
        categories = []
        for row in self.catlist.load_categories():
            cat = Category(
                row[0],
                row[1],
                row[2],
            )
            cat.is_system = self._is_system_category(cat.name)
            categories.append(cat)
        return categories

    """
    ADD
    """

    def add_category(self, name: str, color: str) -> Result:
        """Validate and add category to db. Signal back to view with Result."""
        if not isinstance(name, str):
            raise TypeError("name has to be a str")
        if not isinstance(color, str):
            raise TypeError("color has to be a str")

        if self._is_system_category(name):
            return Result(False, error="Cannot create system category names.")

        try:
            new_cat = Category(None, name, color)
            ret_cat = self.catlist.add_category(new_cat)
            return Result(True, return_val=ret_cat)
        except ValueError as e:
            return Result(False, error=str(e))

    """
    DELETE
    """

    def delete_category(self, id: int) -> Result:
        """Delete category from db with given id."""
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        if id <= 0:
            raise ValueError("cat_id must be a positive integer")

        cat = self.get_category(id).return_val
        if self._is_system_category(cat.name):
            return Result(False, error="Cannot delete system categories.")

        self.catlist.delete_category(id)
        return Result(True)

    """
    GET
    """

    def get_category(self, id: int) -> Result:
        """Grab category with given id."""
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        if id <= 0:
            raise ValueError("cat_id must be a positive integer")

        category = self.catlist.grab_category(id)
        ret_cat = Category(id, category[1], category[2])
        ret_cat.is_system = self._is_system_category(ret_cat.name)
        return Result(True, return_val=ret_cat)

    """
    UPDATE
    """

    def update_category(self, id: int, new_name: str, new_color: str) -> Result:
        """Update category name or color."""
        cat = self.get_category(id).return_val

        if cat.is_system and new_name != cat.name:
            return Result(False, error="Cannot rename system categories.")

        try:
            updated = self.catlist.update_category(id, new_name, new_color)
            return Result(True, return_val=updated)
        except ValueError as e:
            return Result(False, error=str(e))

    def move_category_up(self, id: int) -> Result:
        try:
            self.catlist.move_category_up(id)
            return Result(True)
        except ValueError as e:
            return Result(False, error=str(e))

    def move_category_down(self, id: int) -> Result:
        try:
            self.catlist.move_category_down(id)
            return Result(True)
        except ValueError as e:
            return Result(False, error=str(e))
