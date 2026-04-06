from models.category import Category
from models.category_list import CategoryList
from controller.result import Result
class CategoryController:

    def __init__(self, catlist: CategoryList):
        self.catlist = catlist

    def load_categories(self) -> list[Category]:
        """Create all category objects from category data return in list"""
        categories = []
        for row in self.catlist.load_categories():
            categories.append(Category(
                row[0],
                row[1],
                row[2]
            ))
        return categories
    
    def add_category(self, name: str, color: str) -> Result:
        """Validate and add category to db. Signal back to view with Result."""
        # type validation
        if not isinstance(name, str):
            raise TypeError("name has to be a str")
        if not isinstance(color, str):
            raise TypeError("color has to be a str")
        # try adding category
        try:
            new_cat = Category(None, name, color)
            ret_cat = self.catlist.add_category(new_cat)
            return Result(True, return_val= ret_cat )
        # return error message on failure
        except ValueError as e:
            return Result(False, error = str(e))
    
    def delete_category(self, id: int) -> Result:
        """Delete category from db with given id"""
        if id <= 0:
            raise ValueError("cat_id must be a positive integer")
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        self.catlist.delete_category(id)
        return Result(True)
    
    def get_category(self, id: int) -> Result:
        """grab category with given id"""
        if id <= 0:
            raise ValueError("cat_id must be a positive integer")
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        category = self.catlist.grab_category(id)
        ret_cat = Category(id, category[1], category[2])
        return Result(True, return_val= ret_cat)

