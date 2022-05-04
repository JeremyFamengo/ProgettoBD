from faulthandler import dump_traceback_later
from typing_extensions import Self
from flask import *
from flask_sqlalchemy import *
from flask_login import UserMixin, current_user, login_user, LoginManager, login_required, logout_user
from psycopg2 import Date, IntegrityError
from sqlalchemy import PrimaryKeyConstraint
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import date


#######################################################
# CONFIGS
#######################################################

#initializing the webapp
app = Flask(__name__)

#setting secret key
app.config['SECRET_KEY']="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jrVSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjxx3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFaM4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.162.163.103/echos2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

#initializing database with flask-sqalchemy
db = SQLAlchemy(app)

#setting up native flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#######################################################
# CLASSES
#######################################################

#class that defines a user in the table of Utenti in the database
class User(db.Model, UserMixin):
    __tablename__ = "utenti"
    nome  = db.Column(db.String(20))
    cognome = db.Column(db.String(20))
    id = db.Column(db.Integer, unique=True, primary_key = True)
    username = db.Column(db.String(50), unique=True)
    mail = db.Column(db.String(40), unique=True)
    data_di_nascita = db.Column(db.Date)
    id_artista = db.Column(db.String(30))
    premium = db.Column(db.Boolean)
    ascoltate = db.Column(db.ARRAY(db.Integer))
    
    psw = db.Column(db.String(128))

    def __init__(self, nome, cognome, mail, psw, data_di_nascita, id_artista, premium, ascoltate, username):
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.psw = generate_password_hash(psw, "sha256")
        self.data_di_nascita = data_di_nascita
        self.id_artista = id_artista
        self.premium = premium
        self.ascoltate = ascoltate
        self.username = username

    def verify_password(self, psw):
        return check_password_hash(self.psw, psw)

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.nome)
        print(self.cognome)
        print(self.mail)
        print(self.id)
        print(self.psw)
        print(self.data_di_nascita)
        print(self.id_artista)
        print(self.premium)
        print(self.ascoltate)
        print(self.username)
        print("\n-------------------------\n")
    
    def get_id(self):
        return self.id

#class that defines the login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    psw = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

#class that defines the register form
class RegisterForm(FlaskForm):
    nome = StringField("Nome*", validators=[DataRequired()])
    cognome = StringField("Cognome*", validators=[DataRequired()])
    username = StringField("Username*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired()])
    psw = PasswordField("Password*", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'), Length(min=8)])
    psw2 = PasswordField("Conferma Password*", validators=[DataRequired(), Length(min=8)])
    data_di_nascita = DateField("Data di nascita")
    submit = SubmitField("Registrati")


class ModifyInfo(FlaskForm):
    nome = StringField("Nome")
    cognome = StringField("Cognome")
    email = StringField("Email")
    data_di_nascita = DateField("Data di nascita")
    submit1 = SubmitField("Applica modifiche")

class ModifyPsw(FlaskForm):
    old_psw = PasswordField("Vecchia Password", validators=[DataRequired()])
    psw = PasswordField("Nuova password", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'), Length(min=8)])
    psw2 = PasswordField("Conferma nuova password", validators=[DataRequired(), Length(min=8)])
    submit2 = SubmitField("Cambia password")

class ArtistForm(FlaskForm):
    nome_arte = StringField("Your stage name", validators=[DataRequired()])
    motivazione = TextAreaField("Tell us what makes you special!", validators=(DataRequired(), Length(max = 128)))
    submit = SubmitField("I'm ready!")

class Richieste_diventa_artista(db.Model):
    __tablename__ = "richieste_diventa_artista"
    nome_arte = db.Column(db.String(40))
    motivazione = db.Column(db.String(128))
    stato_richiesta = db.Column(db.Integer)
    id_utente = db.Column(db.String(20), primary_key = True)
    

    def __init__(self, nome_arte, motivazione, stato_richiesta, id_utente):
        self.nome_arte = nome_arte
        self.motivazione = motivazione
        self.stato_richiesta = stato_richiesta
        self.id_utente = id_utente


    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.nome_arte)
        print(self.motivazione)
        print(self.stato_richiesta)
        print(self.id_utente)
        print("\n-------------------------\n")
    
class Artista(db.Model):
    __tablename__ = "artisti"
    id_artista = db.Column(db.Integer, primary_key = True)
    nome_arte = db.Column(db.String)
    data_iscrizione = db.Column(db.Date)
    id_utente = db.Column(db.Integer)

    def __init__(self, nome_arte, data_iscrizione, id_utente):
        self.nome_arte = nome_arte
        self.data_iscrizione = data_iscrizione
        self.id_utente = id_utente


    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.id_artista)
        print(self.nome_arte)
        print(self.id_utente)
        print(self.data_iscrizione)
        print("\n-------------------------\n")


class Album(db.Model):
    __tablename__ = 'album'
    id_album = db.Column(db.Integer, primary_key = True)
    id_artista = db.Column(db.Integer)
    id_canzoni = db.Column(db.ARRAY(db.Integer))
    singolo = db.Column(db.Boolean)
    scadenza = db.Column(db.Date)
    restricted = db.Column(db.Boolean)
    titolo = db.Column(db.String)
    anno = db.Column(db.Date)

    def __init__(self, id_album, id_artista, id_canzoni, singolo, scadenza, restricted, titolo, anno):
        self.id_album = id_album
        self.id_artista = id_artista
        self.id_canzoni = id_canzoni
        self.singolo = singolo
        self.scadenza = scadenza
        self.restricted = restricted
        self.titolo = titolo
        self.anno = anno

class Canzoni(db.Model):
    __tablename__ = 'canzoni'
    id = db.Column(db.Integer, primary_key = True)
    id_artista = db.Column(db.Integer)
    riservato = db.Column(db.Boolean)
    data_inserimento = db.Column(db.Date)
    titolo = db.Column(db.String)
    durata = db.Column(db.Integer)
    anno = db.Column(db.Date)
    id_genere = db.Column(db.Integer)
    file = db.Column(db.LargeBinary)
    extension = db.Column(db.String(10))

    def __intit__(self, id_canzone, titolo, durata, anno, id_genere_musicale, file, extension):
        self.id_canzone = id_canzone
        self.titolo = titolo
        self.durata = durata
        self.anno = anno
        self.id_genere_musicale = id_genere_musicale
        self.file = file
        self.extension = extension

class Generi_Musicali(db.Model):
    __tablename__ = 'generi_musicali'
    id_genere = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String)
    descrizione = db.Column(db.String(255))

    def __init__(self, id_genere_musicale, nome, descrizione):
        self.id_genere_musicale = id_genere_musicale
        self.nome = nome      
        self.descrizione = descrizione

class Playlist(db.Model):
    __tablename__  = 'playlist'
    id_playlist = db.Column(db.Integer, primary_key = True)
    titolo = db.Column(db.String)
    id_utente = db.Column(db.Integer)
    id_canzoni = db.Column(db.Integer)
    restricted = db.Column(db.Boolean)

    def playlist(self, titolo, id_utente, id_canzoni, restricted):
        self.titolo = titolo
        self.id_utente = id_utente
        self.id_canzoni = id_canzoni
        self.restricted = restricted


    

#######################################################
# ROUTES
#######################################################

#home
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user:
            if user.verify_password(form.psw.data):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                print('Wrong password')
                flash('Wrong password')
        else:
            print('User does not exist')
            flash('User does not exist')
                
    return render_template("login.html", form=form)

#profile page
@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user.username)

#info page
@app.route('/info')
def info():
    
    return render_template("info.html")

#logout function as route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#register page and function
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user is None:
            user = User(nome=form.nome.data, cognome=form.cognome.data, mail=form.email.data, psw=form.psw.data, data_di_nascita=form.data_di_nascita.data, id_artista=None, premium=False, ascoltate=[], username = form.username.data)
            user.debug()
            db.session.add(user)
            db.session.commit()
            
            print("User added correctly!")
            flash("User added correctly!")

            form.nome.data = ''
            form.cognome.data = ''
            form.email.data = ''
            form.username.data = ''
            form.psw.data = ''
            form.data_di_nascita.data = ''
            
            return redirect(url_for('login'))

        else:
            print("User already registered!")
            flash("User already registered!")
            form.psw.data = ''
            form.psw2.data = ''

    return render_template("register.html", form = form)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/profileinfo', methods=['GET', 'POST'])
@login_required
def profileinfo():
    form = ModifyInfo()
    form2 = ModifyPsw()

    if form.submit1.data and form.validate():
        print("Modified info")
        user = User.query.filter_by(id = current_user.id).first()

        user.nome = form.nome.data
        user.cognome = form.cognome.data
        user.mail = form.email.data
        user.data_di_nascita = form.data_di_nascita.data

        db.session.commit()

        flash("Info updated correctly")

    
    if form2.submit2.data and form2.validate():    
        user = User.query.filter_by(id = current_user.id).first()

        if user.verify_password(form2.old_psw.data):
            user.psw = generate_password_hash(form2.psw.data)
            print("Modified password")
            db.session.commit()
            flash("Modified password")
        else:
            print("wrong old password")
            flash("Insert your current password correctly")

    form.nome.data = current_user.nome
    form.cognome.data = current_user.cognome
    form.email.data = current_user.mail
    form.data_di_nascita.data = current_user.data_di_nascita

    return render_template('profileinfo.html', form = form, form2 = form2)

@app.route('/artist', methods=['GET', 'POST'])
@login_required
def artist():
    form = ArtistForm()
    request_status = None
    nome_arte = None

    # controllo se esiste già una entry nella tabella artisti legata all'utente corrente e setto artist a True se vero, altrimenti a False
    artist = Artista.query.filter_by(id_artista = current_user.id_artista).first()
    if artist:
        nome_arte = artist.nome_arte
        artist = True
    else:
        artist = False


    # controllo se esiste già una richiesta a nome dell'utente, se esiste prendo il codice si stato, altrimenti setto il codice di stato a 0
    if not artist:
        request = Richieste_diventa_artista.query.filter_by(id_utente = current_user.id).first()
        if request:
            request_status = request.stato_richiesta
        else:
            request_status = 0

        if form.validate_on_submit():
            nome_arte = form.nome_arte.data
            motivazione = form.motivazione.data
            stato_richiesta = 1
            id_utente = current_user.id

            richiesta = Richieste_diventa_artista(nome_arte, motivazione, stato_richiesta, id_utente)
            richiesta.debug()
            db.session.add(richiesta)
            db.session.commit()

            form.nome_arte.data = ''
            form.motivazione.data = ''

            return redirect('profile')
    
    return render_template('artist.html', form = form, artist = artist, nome_arte = nome_arte, request_status = request_status)

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    # non so se è buona pratica gestire queta cosa con le eccezioni, da rivedere
    # si potrebbe fare con stesso nome dei pulsanti ma valore diverso TRUE per accept e FALSE per reject
    if request.method == 'POST':
        id = request.form['id_utente']
        nome_arte = request.form['nome_arte']
        print(id)
        print(nome_arte)
        
        accept = bool(request.form['accept'])
        print(accept)


        # TODO: controllare ridondanze in questa procedura
        if accept:
            req = Richieste_diventa_artista.query.filter_by(id_utente = id).first()
            req.stato_richiesta = 2
            artista = Artista(nome_arte, date.today(), id)
            db.session.add(artista)
            db.session.commit()

            user = User.query.filter_by(id = id).first()
            artista = Artista.query.filter_by(id_utente = user.id).first()
            user.id_artista = artista.id_artista

            db.session.commit()

        else:
            req = Richieste_diventa_artista.query.filter_by(id_utente = id).first()
            req.stato_richiesta = -1
            db.session.commit()

    requests = Richieste_diventa_artista.query.filter_by(stato_richiesta = '1').all()
    return render_template("admin.html", requests = requests)


@app.route('/artist/dashboard')
@login_required
def dashboard():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    user = Artista.query.filter_by(id_artista = current_user.id_artista).first().nome_arte

    return render_template("dashboard.html", user = user)

@app.route('/artist/uploadsong')
@login_required
def uploadsong():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    artista = Artista.query.filter_by(id_artista = current_user.id_artista).first()

    return render_template("uploadsong.html")

#######################################################   
# FUNCTIONS
#######################################################

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


if __name__ == "__main__":
    app.run(debug=True)