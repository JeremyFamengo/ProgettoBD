from flask import *
from flask_sqlalchemy import *
from flask_login import UserMixin, current_user, login_user, LoginManager, login_required, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField, FileField, IntegerField
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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.177.180.60/echos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

#setting upload folder
app.config['UPLOAD_FOLDER'] = "/tmp/"

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

    def __init__(self, id_artista, id_canzoni, singolo, scadenza, restricted, titolo, anno):
        self.id_artista = id_artista
        self.id_canzoni = id_canzoni
        self.singolo = singolo
        self.scadenza = scadenza
        self.restricted = restricted
        self.titolo = titolo
        self.anno = anno

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.id_artista)
        print(self.id_canzoni)
        print(self.singolo)
        print(self.scadenza)
        print(self.restricted)
        print(self.titolo)
        print(self.anno)
        print("\n-------------------------\n")

class Canzoni(db.Model):
    __tablename__ = 'canzoni'
    id = db.Column(db.Integer, primary_key = True)
    id_artista = db.Column(db.Integer)
    riservato = db.Column(db.Boolean)
    data_inserimento = db.Column(db.Date)
    titolo = db.Column(db.String)
    scadenza = db.Column(db.Integer)
    data_uscita = db.Column(db.Date)
    id_genere = db.Column(db.Integer)
    file = db.Column(db.LargeBinary)
    extension = db.Column(db.String(10))
    durata = db.Column(db.Integer)

    def __intit__(self, id_artista, titolo, scadenza, data_uscita, id_genere_musicale, file, riservato, extension, durata):
        self.id_artista = id_artista
        self.titolo = titolo
        self.scadenza = scadenza
        self.data_uscita = data_uscita
        self.id_genere_musicale = id_genere_musicale
        self.file = file
        self.riservato = riservato
        self.extension = extension
        self.durata = durata

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

class UploadForm(FlaskForm):
    titolo = StringField("Titolo", validators=[DataRequired()])
    genere = SelectField("Genere", validators=[DataRequired()])
    data_uscita = DateField("Data di uscita", validators=[DataRequired()])
    file = FileField("Canzone")
    riservato = SelectField("Riservato", choices=[(0, "No"), (1, "Sì")], validators=[DataRequired()])
    album = SelectField("Album", validators=[DataRequired()])
    scadenza = DateField("Scadenza")
    submit = SubmitField("Carica")

class CreateAlbumForm(FlaskForm):
    titolo = StringField("Titolo", validators=[DataRequired()])
    singolo = SelectField("Singolo", choices=[(0, "No"), (1, "Sì")])
    scadenza = DateField("Scadenza (opzionale)")
    restricted = SelectField("Riservato", choices=[(0, "No"), (1, "Sì")])
    anno = DateField("Anno di uscita", validators=[DataRequired()])
    submit = SubmitField("Crea")

class CreaPlaylistForm(FlaskForm):
    restricted = SelectField("Privacy", choices=[(0, "Pubblica"), (1, "Personale")], validators=[DataRequired()])
    titolo = StringField("Nome", validators=[DataRequired()])
    submit = SubmitField("Crea")
    

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
    artist = current_user.id_artista
    if artist:
        return redirect("/artist/dashboard")
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

    user = Artista.query.filter_by(id_artista = current_user.id_artista).first()
    songs = Canzoni.query.filter_by(id_artista = current_user.id_artista)
    albums = Album.query.filter_by(id_artista = user.id_artista).all()
    length = len(albums)

    return render_template("dashboard.html", user=user.nome_arte, albums=albums, songs=songs, length = length)

@app.route('/artist/uploadsong')
@login_required
def uploadsong():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    form = UploadForm()

    artista = Artista.query.filter_by(id_artista = current_user.id_artista).first()
    generi = Generi_Musicali.query.all()
    albums = Album.query.filter_by(id_artista = artista.id_artista).all()

    choices = []
    for album in albums:
        if album.singolo and len(album.id_canzoni) != 0:
            tmp = (album.id_album,album.titolo)
            choices.append(tmp)

    form.album.choices = choices

    choices = []
    for genere in generi:
        tmp = (genere.id_genere,genere.nome)
        choices.append(tmp)

    form.genere.choices = choices

    return render_template("uploadsong.html", form=form)

@app.route('/artist/creaalbum', methods=['GET', 'POST'])
@login_required
def creaalbum():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    artista = Artista.query.filter_by(id_artista = current_user.id_artista).first()

    form = CreateAlbumForm()


    if form.is_submitted():
        titolo = form.titolo.data
        anno = form.anno.data
        singolo = bool(form.singolo.data)
        restricted = bool(form.restricted.data)
        scadenza = form.scadenza.data

        album = Album(artista.id_artista, [], singolo, scadenza, restricted, titolo, anno)

        album.debug()

        db.session.add(album)
        db.session.commit()

        form.titolo.data = ''
        form.scadenza.data = ''
        form.anno.data = ''
        form.singolo.data = ''
        form.restricted.data = ''

        flash("Album aggiunto correttamente")

    return render_template("creaalbum.html", form=form)
    

@app.route('/168AN4df15/uploader', methods=['GET', 'POST'])
@login_required
def uploader():
      
    form = UploadForm()

    if form.is_submitted():
        f = request.files['file']
        titolo = form.titolo.data
        data_uscita = form.data_uscita.data
        riservato = bool(form.riservato.data)
        album_id = int(form.album.data)
        scadenza = form.scadenza.data
        genere=form.genere.data
        id_artista = current_user.id_artista
        data = f.stream.read()
        durata = 180

        
        canzone = Canzoni(id_artista=id_artista, titolo=titolo, scadenza=scadenza, data_uscita=data_uscita, id_genere=genere, file=data, riservato=riservato, extension='mp3', durata=durata)

        db.session.add(canzone)

        id_canzone = Canzoni.query.filter_by(id_artista = current_user.id_artista, data_uscita = data_uscita).first().id

        query = """UPDATE album SET id_canzoni = id_canzoni || '{" """ + str(id_canzone) + """ "}' WHERE id_album = """ + str(album_id)
        db.session.execute(query)
        db.session.commit()
        
        flash("file uploaded successfully")

    return redirect('/artist/uploadsong')

@app.route('/player')
@login_required
def player():

    id = request.args.get('id')
    canzone = Canzoni.query.filter_by(id = id).first()
    artista = Artista.query.filter_by(id_artista = canzone.id_artista).first().nome_arte
    genere = Generi_Musicali.query.filter_by(id_genere = canzone.id_genere).first()
    descrizione = genere.descrizione
    genere = genere.nome

    riservato = canzone.riservato
    if riservato and current_user.premium:
        riservato = False
    
    
    return render_template("player.html", canzone=canzone, artista=artista, riservato=riservato, genere=genere, descrizione=descrizione)


@app.route('/creaplaylist', methods=['GET', 'POST'])
@login_required
def creaplaylist():
    form = CreaPlaylistForm()

    if form.validate_on_submit():
        titolo = form.titolo.data
        restricted = bool(form.restricted.data)
        id_utente = current_user.id
        id_canzoni = []

        playlist = Playlist(titolo = titolo, id_utente = id_utente, id_canzoni = id_canzoni, restricted = restricted)
        print(playlist)

        db.session.add(playlist)
        db.session.commit()

        flash("Playlist creata correttamente")

    return render_template("creaplaylist.html", form = form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#######################################################   
# FUNCTIONS
#######################################################

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


if __name__ == "__main__":
    app.run(debug=True) 