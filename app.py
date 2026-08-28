import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from models import Book, Dvd, User
from library import LibraryManager
from extension import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
                             
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

db.init_app(app)

with app.app_context():
    db.create_all()
    
mia_biblioteca = LibraryManager()

@app.route("/")
def home():
    books = db.session.scalars(db.select(Book)).all()
    dvds = db.session.scalars(db.select(Dvd)).all()
    return render_template("index.html", books = books, dvds = dvds)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_inserito = request.form.get('username')
        email_inserita = request.form.get('email')

        nuovo_utente = User(
            name=username_inserito,
            email=email_inserita
        )

        try:
            db.session.add(nuovo_utente)
            db.session.commit()
            flash('Registrazione completata con successo!', 'success')
            return redirect(url_for('home'))

        except IntegrityError:
            db.session.rollback() 
            flash('Questa email è già registrata. Prova a fare il login o usane un\'altra.', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route("/users")
def list_users():
    users = db.session.scalars(db.select(User)).all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)