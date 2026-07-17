from flask import Flask, render_template
from models import Book, Dvd, User
from library import LibraryManager
from extension import db

app = Flask(__name__)
                             
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
mia_biblioteca = LibraryManager()

@app.route("/")
def home():
    books = db.session.scalars(db.select(Book)).all()
    dvds = db.session.scalars(db.select(Dvd)).all()
    return render_template("index.html", books = books, dvds = dvds)

@app.route("/info")
def info():
    return "<h2>Pagina Info</h2><p>Questa biblioteca è stata creata in Python e Flask!</p>"

@app.route("/test_users")
def test_users():
    users = db.session.scalars(db.select(User)).all()
    return render_template("test_users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)