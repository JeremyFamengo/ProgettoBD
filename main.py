from crypt import methods
from enum import unique
import mailbox
from tty import CFLAG
from flask import *
import os
from datetime import timedelta
from flask_sqlalchemy import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#######################################################
# CONFIGS
#######################################################

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.162.163.103/echos"
app.config['SECRET_KEY']="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jrVSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjxx3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFaM4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"
app.permanent_session_lifetime = timedelta(minutes=10)


#######################################################
# CLASSES
#######################################################

class User(db.Model, UserMixin):
    __tablename__ = "utenti"
    nome  = db.Column(db.String(20))
    cognome = db.Column(db.String(20))
    mail = db.Column(db.String(40), unique=True)
    cf = db.Column(db.String, primary_key=True)
    psw = db.Column(db.String(50))
    data_di_nascita = db.Column(db.Date)
    id_artista = db.Column(db.String(30))

    def __init__(self, nome, cognome, mail, cf, psw, data_di_nascita, id_artista):
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.cf = cf
        self.psw = psw
        self.data_di_nascita = data_di_nascita
        self.id_artista = id_artista


#######################################################
# ROUTES
#######################################################

#home
@app.route('/')
def home():
    return render_template("index.html")

#profile page
@app.route('/profile')
def profile():
    if 'user' in session:
        session.permanent = True
        user = session['user']
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('login'))

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['psw']
        if user != '' and password != '':
            session['user'] = user
            session['password'] = password
            return redirect(url_for('profile'))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

#info page
@app.route('/info')
def info():
    return render_template("info.html")

#logout function as route
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('login'))

#register page and function
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        mail = request.form['mail']
        cf = request.form['cf']
        psw = request.form['psw']
        data_di_nascita = request.form['data_di_nascita']
        id_artista = None
        
        user = User(nome, cognome, mail, cf, psw, data_di_nascita, id_artista)
        db.session.add(user)
        db.session.commit()

    return render_template("register.html")


#######################################################
# FUNCTIONS
#######################################################

if __name__ == "__main__":
    app.run(debug=True)