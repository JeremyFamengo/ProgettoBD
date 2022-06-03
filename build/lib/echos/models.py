from sqlalchemy.ext.declarative import declarative_base
from flask import *
from flask_sqlalchemy import *
from sqlalchemy import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField,\
                    SelectField, FileField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length

#metadata
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "utenti"
    nome  = Column(String(20))
    cognome = Column(String(20))
    id = Column(Integer, unique=True, primary_key = True)
    username = Column(String(50), unique=True)
    mail = Column(String(40), unique=True)
    data_di_nascita = Column(Date)
    id_artista = Column(String(30))
    premium = Column(Boolean)

    psw = Column(String(128))

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
    psw = PasswordField("Password*", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'),
          Length(min=8)])
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
    psw = PasswordField("Nuova password", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match'),
          Length(min=8)])
    psw2 = PasswordField("Conferma nuova password", validators=[DataRequired(), Length(min=8)])
    submit2 = SubmitField("Cambia password")

class ArtistForm(FlaskForm):
    nome_arte = StringField("Your stage name", validators=[DataRequired()])
    motivazione = TextAreaField("Tell us what makes you special!", validators=(DataRequired(), Length(max = 128)))
    submit = SubmitField("I'm ready!")


class Richieste_diventa_artista(Base):
    __tablename__ = "richieste_diventa_artista"
    nome_arte = Column(String(40))
    motivazione = Column(String(128))
    stato_richiesta = Column(Integer)
    id_utente = Column(String(20), primary_key = True)


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

class Artista(Base):
    __tablename__ = "artisti"
    id_artista = Column(Integer, primary_key = True)
    nome_arte = Column(String)
    data_iscrizione = Column(Date)
    id_utente = Column(Integer)

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

class Album(Base):
    __tablename__ = 'album'
    id_album = Column(Integer, primary_key = True)
    id_artista = Column(Integer)
    singolo = Column(Boolean)
    scadenza = Column(Date)
    restricted = Column(Boolean)
    titolo = Column(String)
    anno = Column(Date)

    def __init__(self, id_artista, singolo, scadenza, restricted, titolo, anno):
        self.id_artista = id_artista
        self.singolo = singolo
        self.scadenza = scadenza
        self.restricted = restricted
        self.titolo = titolo
        self.anno = anno

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.id_artista)
        print(self.singolo)
        print(self.scadenza)
        print(self.restricted)
        print(self.titolo)
        print(self.anno)
        print("\n-------------------------\n")


class Canzoni(Base):
    __tablename__ = 'canzoni'
    id = Column(Integer, primary_key = True)
    id_artista = Column(Integer)
    riservato = Column(Boolean)
    data_inserimento = Column(Date)
    titolo = Column(String)
    scadenza = Column(Integer)
    data_uscita = Column(Date)
    id_genere = Column(Integer)
    file = Column(LargeBinary)
    extension = Column(String(10))
    durata = Column(Integer)
    n_riproduzioni = Column(Integer)

    def __init__(self, id_artista, titolo, scadenza, data_inserimento, data_uscita, id_genere, file,\
                 riservato, extension, durata, n_riproduzioni):
        self.id_artista = id_artista
        self.titolo = titolo
        self.scadenza = scadenza
        self.data_uscita = data_uscita
        self.data_inserimento = data_inserimento
        self.id_genere = id_genere
        self.file = file
        self.riservato = riservato
        self.extension = extension
        self.durata = durata
        self.n_riproduzioni=n_riproduzioni

class Generi_Musicali(Base):
    __tablename__ = 'generi_musicali'
    id_genere = Column(Integer, primary_key = True)
    nome = Column(String)
    descrizione = Column(String(255))

    def __init__(self, id_genere, nome, descrizione):
        self.id_genere = id_genere
        self.nome = nome
        self.descrizione = descrizione

class Playlist(Base):
    __tablename__  = 'playlist'
    id_playlist = Column(Integer, primary_key = True)
    titolo = Column(String)
    id_utente = Column(Integer)
    restricted = Column(Boolean)

    def __init__(self, titolo, id_utente, restricted):
        self.titolo = titolo
        self.id_utente = id_utente
        self.restricted = restricted

class Playlist_canzoni(Base):
    __tablename__  = 'playlist_canzoni'
    id_playlist = Column(Integer, primary_key = True)
    id_canzone = Column(Integer, primary_key = True)

    def __init__(self, id_playlist, id_canzone):
        self.id_playlist = id_playlist
        self.id_canzone = id_canzone

class  Album_canzoni(Base):
    __tablename__  = 'album_canzoni'
    id_album = Column(Integer, primary_key = True)
    id_canzone = Column(Integer, primary_key = True)

    def __init__(self, id_album, id_canzone):
        self.id_album = id_album
        self.id_canzone = id_canzone

# view playlist_canzoni_view
class Playlist_canzoni_view(Base):
    __tablename__  = 'playlist_canzoni_view'
    id_playlist = Column(Integer, primary_key=True)
    id_canzone = Column(Integer, primary_key=True)
    titolo_playlist = Column(String)
    titolo_canzone = Column(String)
    restricted = Column(Boolean)
    id_utente = Column(Integer)

class Utenti_ascolti(Base):
    __tablename__ = 'utenti_ascolti'
    id_utente = Column(Integer, primary_key=True)
    id_canzone = Column(Integer)
    n_ascolti = Column(Integer)

    def __init__(self, id_utente, id_canzone, n_ascolti):
        self.id_utente = id_utente
        self.id_canzone = id_canzone
        self.n_ascolti = n_ascolti

class Statistiche_utente_view(Base):
    __tablename__ = 'statistiche_utente_view'
    id_utente = Column(Integer, primary_key=True)
    id_canzone = Column(Integer, primary_key=True)
    id_artista = Column(Integer, primary_key=True)
    id_genere = Column(Integer, primary_key=True)
    n_ascolti = Column(Integer)
    nome_genere = Column(String)
    nome_arte = Column(String)
    titolo_canzone = Column(String)
# view n_riproduzioni_album_canzoni_view

class N_riproduzioni_album_canzoni_view(Base):
    __tablename__  = 'n_riproduzioni_album_canzoni_view'
    id_artista = Column(Integer, primary_key=True)
    id_album = Column(Integer, primary_key=True)
    id_canzone = Column(Integer, primary_key=True)
    titolo_album = Column(String)
    titolo_canzone = Column(String)
    n_riproduzioni = Column(Integer)

class Top_five_artists_view(Base):
    __tablename__ = 'top_five_artists_view'
    id_artista = Column(Integer, primary_key=True)
    fama = Column(Integer, primary_key=True)
    nome_arte = Column(String)

class Album_canzoni_view(Base):
    __tablename__ = 'album_canzoni_view'
    id_album = Column(Integer, primary_key=True)
    titolo_album = Column(String)
    titolo_canzone = Column(String)
    id_canzone = Column(Integer, primary_key=True)

class Canzoni_recenti_view(Base):
    __tablename__ = 'canzoni_recenti_view'
    titolo = Column(String)
    id = Column(Integer, primary_key=True)
    nome_genere = Column(String)
    data_inserimento = Column(Date)
    data_uscita = Column(Date)
    nome_arte = Column(String)

class Canzoni_popolari_view(Base):
    __tablename__ = 'canzoni_popolari_view'
    titolo = Column(String)
    id = Column(Integer, primary_key=True)
    nome_genere = Column(String)
    n_riproduzioni = Column(Integer)
    data_uscita = Column(Date)
    nome_arte = Column(String)

class Album_artisti_view(Base):
    __tablename__ = 'album_artisti_view'
    id_album = Column(Integer, primary_key=True)
    id_artista = Column(Integer)
    singolo = Column(Boolean)
    titolo = Column(String)
    vuoto = Column(Boolean)
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