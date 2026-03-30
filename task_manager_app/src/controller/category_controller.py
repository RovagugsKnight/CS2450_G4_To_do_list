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
        try:
            new_cat = Category(None, name, color)
            ret_cat = self.catlist.add_category(new_cat)
            return Result(True, return_val= ret_cat )
        except ValueError as e:
            return Result(False, error = str(e))
    
    def delete_category(self, id: int) -> Result:
        """Delete category from db with given id"""
        try:
            self.catlist.delete_category(id)
            return Result(True)
        except ValueError as e:
            return Result(False, error = str(e))
    
    def edit_category(self, id: int, name: str, color: str) -> Result:
        """Edit Category from db with given id"""
        try:
            new_cat = Category(id, name, color)
            self.catlist.edit_category(new_cat)
            return Result(True)
        except ValueError as e:
            return Result(False, error = str(e))
    
    def get_category(self, id: int) -> Result:
        """grab category with given id"""
        try:
            result = self.catlist.grab_category(id)
            category = result[0]
            ret_cat = Category(id, category[1], category[2])
            return Result(True, return_val= ret_cat)
        except ValueError as e:
            return Result(False, error = str(e))