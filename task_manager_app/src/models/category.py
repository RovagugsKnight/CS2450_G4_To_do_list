from dataclasses import dataclass

@dataclass
class Category:
    def __init__(self,id: int | None, name: str, color: str):
        self.id = id
        self.name = name
        self.color = color
    
    def __post_init__(self):
        #validate input
        if not self.name:
            raise ValueError("Category name required")
        if not self.color:
            raise ValueError("Category color required")
        if len(self.name) > 20:
            raise ValueError("Keep Category name 20 char or less")
        

