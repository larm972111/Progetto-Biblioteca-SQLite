from models import LibraryItem, ItemStatus
from extension import db

class ItemNotFoundError(Exception): pass

class LibraryManager:
        
    def add_item(self, new_item: LibraryItem):
        db.session.add(new_item)
        db.session.commit()
        
    def search_by_author(self, author: str) -> list[LibraryItem]:
        results = db.session.execute(db.select(LibraryItem).where(LibraryItem.author == author))
        return results.scalars().all()

    def remove_item(self, id_item: int) -> tuple[bool, str]:
        item = db.session.get(LibraryItem, id_item)
        if not item:
            return False, "Elemento non trovato nel catalogo."
        if item.status == ItemStatus.LOANED: 
            return False, "Impossibile eliminare: l'elemento è attualmente in prestito."
        try:
            db.session.delete(item)
            db.session.commit()
            return True, f"'{item.title}' è stato rimosso con successo."
        except Exception as e:
            db.session.rollback()
            return False, f"Errore interno durante l'eliminazione dal database. {e}"
        
    def lend_item(self, id_item: int) -> tuple[bool, str]:
        item = db.session.get(LibraryItem, id_item)
        if not item:
            return False, "Elemento non trovato nel catalogo."
        if item.status == ItemStatus.LOANED: 
            return False, "Elemento già in prestito."
        item.status = ItemStatus.LOANED
        db.session.commit()
        return True, f"'{item.title}' è stato prestato con successo."
    
    def return_item(self, id_item: int) -> tuple[bool, str]:
        item = db.session.get(LibraryItem, id_item)
        if not item:
            return False, "Elemento non trovato nel catalogo."
        if item.status != ItemStatus.LOANED:
            return False, f"il {item.item_type} {item.title} non si trova attualmente in prestito percio non puo essere restituito"
        item.status = ItemStatus.AVAILABLE
        db.session.commit()
        return True, f"'{item.title}' è stato restituito con successo."

