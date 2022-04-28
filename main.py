from faulthandler import dump_traceback_later
from flask import *
from flask_sqlalchemy import *
from flask_login import UserMixin, current_user, login_user, LoginManager, login_required, logout_user
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length


#######################################################
# CONFIGS
#######################################################

#initializing the webapp
app = Flask(__name__)

#setting secret key
app.config['SECRET_KEY']="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jrVSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjxx3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFaM4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.162.163.103/echos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    mail = db.Column(db.String(40), unique=True)
    cf = db.Column(db.String, primary_key=True)
    data_di_nascita = db.Column(db.Date)
    id_artista = db.Column(db.String(30))
    
    psw = db.Column(db.String(128))

    def __init__(self, nome, cognome, mail, cf, psw, data_di_nascita, id_artista):
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.cf = cf
        self.psw = generate_password_hash(psw, "sha256")
        self.data_di_nascita = data_di_nascita
        self.id_artista = id_artista

    def verify_password(self, psw):
        return check_password_hash(self.psw, psw)

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.nome)
        print(self.cognome)
        print(self.mail)
        print(self.cf)
        print(self.psw)
        print(self.data_di_nascita)
        print(self.id_artista)
        print("\n-------------------------\n")
    
    def get_id(self):
        return self.cf

#class that defines the login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    psw = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

#class that defines the register form
class RegisterForm(FlaskForm):
    nome = StringField("Nome*", validators=[DataRequired()])
    cognome = StringField("Cognome*", validators=[DataRequired()])
    cf = StringField("CF*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired()])
    psw = PasswordField("Password*", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'), Length(min=8)])
    psw2 = PasswordField("Confirm Password*", validators=[DataRequired(), Length(min=8)])
    data_di_nascita = DateField("Data di nascita")
    submit = SubmitField("Register")


class ModifyInfo(FlaskForm):
    nome = StringField("Nome")
    cognome = StringField("Cognome")
    cf = StringField("CF")
    email = StringField("Email")
    data_di_nascita = DateField("Data di nascita")
    submit = SubmitField("Change")

class ModifyPsw(FlaskForm):
    old_psw = PasswordField("Old Password", validators=[DataRequired()])
    psw = PasswordField("New password", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'), Length(min=8)])
    psw2 = PasswordField("Confirm new password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Change")

class ArtistForm(FlaskForm):
    nome_arte = StringField("Your stage name", validators=[DataRequired()])
    info = TextAreaField("Tell us what makes you special!", validators=(DataRequired(), Length(min=100)))
    submit = SubmitField("I'm ready!")

class Richieste_diventa_artistaForm(FlaskForm):
    nome_arte = StringField("nome_arte")
    motivazione = StringField("Motivazine")
    stato_richiesta = StringField("stato_richiesta")
    submit = SubmitField("I'm ready!")

class Richieste_diventa_artista(db.Model):
    __tablename__ = "richieste_diventa_artista"
    nome_arte = db.Column(db.String(40))
    id  = db.Column(db.Integer, primary_key=True)
    motivazione = db.Column(db.String(40))
    stato_richiesta = db.Column(db.String(20))
    id_utente = db.Column(db.String(20))
    

    def __init__(self, id, nome_arte, motivazione, stato_richiesta, id_utente):
        self.id = id
        self.nome_arte = nome_arte
        self.motivazione = motivazione
        self.stato_richiesta = stato_richiesta
        self.id_utente = id_utente


    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.id)
        print(self.nome_arte)
        print(self.motivazione)
        print(self.stato_richiesta)
        print(self.id_utente)
        print("\n-------------------------\n")
    
class Artista(db.Model):
    __tablename__ = "artisti"
    id_artista = db.Column(db.Integer, primary_key = True)
    nome_arte = db.Column(db.String)

    def __init__(self, id_artista, nome_arte):
        self.id_artista = id_artista
        self.nome_arte = nome_arte

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.id_artista)
        print(self.nome_arte)
        print("\n-------------------------\n")

class Artisti_album(db.Model):
    __tablename__ = "artisti_album"
    id_artista = db.Column(db.Integer, primary_key = True)
    id_album = db.Column(db.Integer, primary_key = True)
    
    def __init__(self, id_artista, id_album):
        self.id_album = id_album
        self.id_artista = id_artista

class Album(db.Model):
    __tablename__ = 'album'
    id_album = db.Column(db.Integer, primary_key = True)
    titolo = db.Column(db.String)
    anno = db.Column(db.Date)

    def __init__(self, id_album, titolo, anno):
        self.id_album = id_album
        self.titolo = titolo
        self.anno = anno

class Album_canzoni(db.Model):
    __tablename__ = 'album_canzoni'
    id_album = db.Column(db.Integer, primary_key = True)
    id_canzoni = db.Column(db.Integer, primary_key = True)

    def __intit__(self, id_album, id_canzoni):
        self.id_album = id_album
        self.id_canzoni = id_canzoni

class Canzoni(db.Model):
    __tablename__ = 'canzoni'
    id_canzone = db.Column(db.Integer, primary_key = True)
    titolo = db.Column(db.String)
    durata = db.Column(db.Integer)
    anno = db.Column(db.Date)
    id_genere_musicale = db.Column(db.Integer)
    file = db.Column(db.LargeBinary)

    def __intit__(self, id_canzone, titolo, durata, anno, id_genere_musicale, file):
        self.id_canzone = id_canzone
        self.titolo = titolo
        self.durata = durata
        self.anno = anno
        self.id_genere_musicale = id_genere_musicale
        self.file = file

class Generi_Musicali(db.Model):
    __tablename__ = 'generi_musicali'
    id_genere_musicale = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String)

    def __init__(self, id_genere_musicale, nome):
        self.id_genere_musicale = id_genere_musicale
        self.nome = nome      

class Playlist(db.Model):
    __tablename__  = 'playlist'
    id_playlist = db.Column(db.Integer, primary_key = True)
    titolo = db.Column(db.String)
    id_utente = db.Column(db.Integer)
    id_playlist_canzoni = db.Column(db.Integer)

    

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
    return render_template("profile.html", user=current_user.nome)

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
        user = User.query.filter_by(cf=form.cf.data).first()
        if user is None:
            user = User(nome=form.nome.data, cognome=form.cognome.data, mail=form.email.data, cf=form.cf.data, psw=form.psw.data, data_di_nascita=form.data_di_nascita.data, id_artista=None)
            user.debug()
            db.session.add(user)
            db.session.commit()
            print("User added correctly!")
            flash("User added correctly!")
            form.nome.data = ''
            form.cognome.data = ''
            form.email.data = ''
            form.cf.data = ''
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

@app.route('/profileinfo')
@login_required
def profileinfo():
    form = ModifyInfo()
    form2 = ModifyPsw()

    form.nome.data = current_user.nome
    form.cognome.data = current_user.cognome
    form.email.data = current_user.mail
    form.cf.data = current_user.cf
    form.data_di_nascita.data = current_user.data_di_nascita

    return render_template('profileinfo.html', form = form, form2 = form2)

@app.route('/artist')
@login_required
def artist():
    artist = False
    nome_arte = None 
    motivazione = None
    stato_richiesta = None
    richiesta_effettuata = False
    richieste_diventa_artista = Richieste_diventa_artista.query.filter_by(id_utente = current_user.cf).first()
    
    formArtista = ArtistForm()
    formRichieste_diventa_artista =  Richieste_diventa_artistaForm()

    # #TODO: rimuovere e nel caso fosse già un arista restituire il nome, altrimenti il nome_arte sarà null (vuoto)
    if current_user.id_artista != None:  
        # recuperare da database i dati dalla tabella richieste_diventa_artista
        artista=Artista.query.get(current_user.id_artista)
        artist=True
        richiesta_effettuata=True
        formArtista.nome_arte.data=artista.nome_arte
    elif richieste_diventa_artista != None :
        richiesta_effettuata = True
        formRichieste_diventa_artista.nome_arte.data = richieste_diventa_artista.nome_arte
        formRichieste_diventa_artista.motivazione.data  = richieste_diventa_artista.motivazione
        formRichieste_diventa_artista.stato_richiesta.data  = richieste_diventa_artista.stato_richiesta
    


    
        
    return render_template('artist.html', artist = artist, richiesta_effettuata=richiesta_effettuata, formArtista=formArtista,formRichieste_diventa_artista=formRichieste_diventa_artista)

#######################################################
# FUNCTIONS
#######################################################

@login_manager.user_loader
def load_user(cf):
    return User.query.get(cf)


if __name__ == "__main__":
    app.run(debug=True)