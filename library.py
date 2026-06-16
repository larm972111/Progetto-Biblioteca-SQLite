from models import LibraryItem

class ItemNotFoundError(Exception): pass

class LibraryManager:
    def __init__(self):
        self.catalog = []
        
    def __str__(self):
        result = "Library Catalog: \n"
        for item in self.catalog:
            result += f"{item.title} of {item.author}\n"
        return result
        
        
    def add_item(self, new_item: LibraryItem):
        for item in self.catalog:
            if new_item.item_id == item.item_id:
                raise ValueError(f"Error Duplicate id: {item.item_id}")        
        self.catalog.append(new_item)
        
    def search_by_author(self, author: str) -> [LibraryItem]:
        matches = []
        for item in self.catalog:
            if author == item.author:
                matches.append(item)
        return matches 
        
    def remove_item(self, id_item: str):
        for item in self.catalog:
            if id_item == item.item_id:
                self.catalog.remove(item)
                return
        raise ItemNotFoundError(f"{id_item} not found in catalog")   
        
    def lend_item(self, item_id: str):
        for item in self.catalog:
            if item_id == item.item_id:
                item.borrow_item()
                return
        raise ItemNotFoundError(f"Item id {item_id} not found")
        