from app import app
from extension import db
from models import Book, Dvd, VideoResolution

def popola_database():
    print("⏳ Cancellazione vecchio database e creazione nuove tabelle...")
    db.drop_all()   
    db.create_all()
    
    print("📚 Creazione degli elementi di test...")
    
    libri = [
        Book(title="Il Signore degli Anelli", author="J.R.R. Tolkien", isbn="978-8845292613", pagnum=1200),
        Book(title="1984", author="George Orwell", isbn="978-8824773539", pagnum=328),
        Book(title="Il Nome della Rosa", author="Umberto Eco", isbn="978-8830104747", pagnum=620),
        Book(title="Dune", author="Frank Herbert", isbn="978-8834739600", pagnum=700)
    ]
    
    dvds = [
        Dvd(title="Inception", author="Christopher Nolan", duration=148, resolution=VideoResolution.FOUR_K),
        Dvd(title="Matrix", author="Lana & Lilly Wachowski", duration=136, resolution=VideoResolution.FHD),
        Dvd(title="Pulp Fiction", author="Quentin Tarantino", duration=154, resolution=VideoResolution.HD),
        Dvd(title="Interstellar", author="Christopher Nolan", duration=169, resolution=VideoResolution.FOUR_K)
    ]
    
    print("📥 Inserimento nel database in corso...")
    db.session.add_all(libri)
    db.session.add_all(dvds)
    
    db.session.commit()
    print("✅ Database popolato con successo!")

if __name__ == "__main__":
    with app.app_context():
        popola_database()