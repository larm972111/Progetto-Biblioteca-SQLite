import os
from flask import Flask, render_template
from models import Book, Dvd, User
from library import LibraryManager
from extension import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_url = os.getenv("DATABASE_URL")
                             
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
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

@app.route("/users")
def list_users():
    users = db.session.scalars(db.select(User)).all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)