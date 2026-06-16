from app import app
from extensions import db
from models import Book, Dvd

def popola_database():
    print("⏳ Cancellazione vecchio database e creazione nuove tabelle...")
    db.drop_all()   # Cancello tutto così non ho problemi di ID duplicati se lo lancio più volte
    db.create_all() # Ricreo le tabelle pulite
    
    print("📚 Creazione degli elementi di test...")
    
    libri = [
        Book(item_id="B01", title="Il Signore degli Anelli", author="J.R.R. Tolkien", isbn="978-8845292613"),
        Book(item_id="B02", title="1984", author="George Orwell", isbn="978-8824773539"),
        Book(item_id="B03", title="Il Nome della Rosa", author="Umberto Eco", isbn="978-8830104747"),
        Book(item_id="B04", title="Dune", author="Frank Herbert", isbn="978-8834739600")
    ]
    
    dvds = [
        Dvd(item_id="D01", title="Inception", author="Christopher Nolan", duration=148),
        Dvd(item_id="D02", title="Matrix", author="Lana & Lilly Wachowski", duration=136),
        Dvd(item_id="D03", title="Pulp Fiction", author="Quentin Tarantino", duration=154),
        Dvd(item_id="D04", title="Interstellar", author="Christopher Nolan", duration=169)
    ]
    
    print("📥 Inserimento nel database in corso...")
    # Aggiungo tutte le istanze alla sessione di SQLAlchemy
    db.session.add_all(libri)
    db.session.add_all(dvds)
    
    # Sparo i dati fisicamente nel file .db con il commit
    db.session.commit()
    print("✅ Database popolato con successo!")

if __name__ == "__main__":
    # Cruciale: Bisogna dire a Python di usare il "contesto" dell'app Flask,
    # altrimenti SQLAlchemy non sa a quale file .db collegarsi.
    with app.app_context():
        popola_database()