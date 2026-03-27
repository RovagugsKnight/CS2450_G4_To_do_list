from abc import ABC, abstractmethod
from models.category import Category

class CategoryList(ABC):

    @abstractmethod
    def load_categories(self):
        pass
    
    @abstractmethod
    def grab_categories(self):
        pass

    @abstractmethod
    def add_category(self, category: Category):
        pass
    
    @abstractmethod
    def delete_category(self, category_id: int):
        pass
    
    @abstractmethod
    def edit_category(self, category: Category):
        pass
