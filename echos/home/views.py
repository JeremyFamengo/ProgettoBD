from flask import Blueprint, render_template
from echos import *
from echos.models import *
from flask_login import *
from echos.functions import *

home = Blueprint('home', __name__, template_folder="templates")

# Funzione dedicata alla pagina principale del sito
@home.route('/')
def home():
    artisti = Session_home.query(Top_five_artists_view).all()
    canzoni_recenti =  Session_home.query(Canzoni_recenti_view).all()
    canzoni_popolari =  Session_home.query(Canzoni_popolari_view).all()

    return render_template("index.html", artisti = artisti, canzoni = canzoni_recenti, popolari = canzoni_popolari)


# Funzione dedicata alla pagina di accesso al sito
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Session_user.query(User).filter(User.mail == form.email.data).first()
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

# Funzione dedicata onorevolmente alla pagina dei logo creatori
@app.route('/info')
def info():
    return render_template("info.html")

# Funzione dedicata al tasto cerca
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    resultQuery = getSearchTable()

    playlists = Session_user.query(Playlist).filter(Playlist.id_utente == current_user.id).all()
    count = len(resultQuery)

    if request.method == 'POST':
        id_playlist = request.form['id_playlist']
        id_canzone = request.form['id_canzone']
        addToPlaylist(id_playlist, id_canzone)

    return render_template("search.html", songs = resultQuery, count_canzoni = count, playlists = playlists)


# Funzione che richiama la pagina di errore 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

